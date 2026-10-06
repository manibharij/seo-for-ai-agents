#!/usr/bin/env python3
"""Freshness check for the seo-for-ai-agents pack.

Scans skills/, install/ and the root *.md files for:
  1. "verified YYYY-MM" stamps older than N months (default 3);
  2. http(s) URLs, checked with a polite HEAD request (falling back to GET),
     reporting non-2xx responses and redirects with their targets.

Prints a Markdown report. Exits 0 unless --strict is passed, in which case it
exits 1 when there are stale stamps, broken links or unreachable URLs.
Redirects and "blocked, check manually" results never fail the run.

Standard library only. Usage:
  python scripts/check-freshness.py                 # dates and links
  python scripts/check-freshness.py --offline       # dates only
  python scripts/check-freshness.py --months 6 --strict --output report.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

USER_AGENT = (
    "seo-for-ai-agents-freshness/1.0 "
    "(+https://github.com/manibharij/seo-for-ai-agents; link check, monthly)"
)
SCAN_DIRS = ("skills", "install")
SCAN_EXTS = {".md", ".txt", ".json", ".yml", ".yaml"}

STAMP_RE = re.compile(r"\bverified\s+(\d{4})-(\d{2})\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>\"'`)\]|]+")
TRAILING = ".,;:!?*_'\""

# Hosts that are placeholders in examples, not sources to check.
PLACEHOLDER_HOSTS = {
    "example.com", "example.org", "example.net", "localhost", "127.0.0.1",
    "0.0.0.0", "yoursite.com", "your-site.com", "yourdomain.com", "domain.com",
    "staging.example.com", "preview.example.com",
}
PLACEHOLDER_MARKERS = ("{", "}", "$", "<", ">", "...", "…", "your-", "YOUR_", "API_KEY", "METHOD_NAME")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
FENCE_RE = re.compile(r"^\s*(```|~~~)")

# Hosts known to refuse automated clients (bot protection). Any non-2xx or
# connection failure from these is reported as "blocked, check manually".
BOT_BLOCKING_HOSTS = (
    "openai.com", "help.openai.com", "platform.openai.com", "chatgpt.com",
    "perplexity.ai", "x.com", "twitter.com", "linkedin.com", "reddit.com",
    "medium.com", "g2.com", "trustpilot.com", "glassdoor.com", "quora.com",
    "facebook.com", "instagram.com", "tiktok.com",
)
BLOCKED_STATUSES = {401, 403, 429, 451, 999}


@dataclass
class Stamp:
    path: str
    line: int
    year: int
    month: int
    text: str


@dataclass
class LinkResult:
    url: str
    status: int | None = None
    kind: str = "ok"  # ok | redirect | minor-redirect | broken | blocked | error
    target: str | None = None
    detail: str = ""
    method: str = "HEAD"
    where: list[tuple[str, int]] = field(default_factory=list)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


_OPENER = urllib.request.build_opener(_NoRedirect())


def iter_files(root: Path):
    for name in sorted(root.glob("*.md")):
        yield name
    for d in SCAN_DIRS:
        base = root / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.suffix.lower() in SCAN_EXTS:
                yield p


def clean_url(raw: str) -> str:
    url = raw
    while url and url[-1] in TRAILING:
        url = url[:-1]
    # Keep balanced parentheses, e.g. Wikipedia-style URLs.
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1]
    return url


def is_checkable(url: str) -> bool:
    if any(m in url for m in PLACEHOLDER_MARKERS):
        return False
    try:
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
    except ValueError:
        return False
    if not host or "." not in host:
        return False
    if host in PLACEHOLDER_HOSTS or host.endswith((".example.com", ".example", ".test", ".localhost", ".invalid")):
        return False
    return True


def scan(root: Path, include_code: bool = False):
    stamps: list[Stamp] = []
    urls: dict[str, list[tuple[str, int]]] = {}
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        in_fence = False
        markdown = path.suffix.lower() == ".md"
        for n, line in enumerate(text.splitlines(), start=1):
            for m in STAMP_RE.finditer(line):
                stamps.append(Stamp(rel, n, int(m.group(1)), int(m.group(2)), line.strip()))
            if markdown and FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            # URLs in code (fenced blocks, inline code) are examples, API
            # endpoints or XML namespaces, not sources. Skip them unless asked.
            if markdown and not include_code:
                if in_fence:
                    continue
                line = INLINE_CODE_RE.sub(" ", line)
            for m in URL_RE.finditer(line):
                url = clean_url(m.group(0))
                if is_checkable(url):
                    urls.setdefault(url, []).append((rel, n))
    return stamps, urls


def months_between(year: int, month: int, today: dt.date) -> int:
    return (today.year - year) * 12 + (today.month - month)


def host_of(url: str) -> str:
    return (urllib.parse.urlsplit(url).hostname or "").lower()


def is_bot_blocking_host(host: str) -> bool:
    return any(host == h or host.endswith("." + h) for h in BOT_BLOCKING_HOSTS)


_host_locks: dict[str, threading.Lock] = {}
_host_locks_guard = threading.Lock()


def _host_lock(host: str) -> threading.Lock:
    with _host_locks_guard:
        return _host_locks.setdefault(host, threading.Lock())


def _request(url: str, method: str, timeout: float):
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    })
    try:
        with _OPENER.open(req, timeout=timeout) as resp:
            if method == "GET":
                resp.read(1024)
            return resp.status, resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.headers


def is_minor_redirect(url: str, target: str) -> bool:
    """A trailing-slash change or an http to https upgrade on the same host and path."""
    a, b = urllib.parse.urlsplit(url), urllib.parse.urlsplit(target)
    same_host = a.netloc.lower() == b.netloc.lower()
    same_path = a.path.rstrip("/") == b.path.rstrip("/") and a.query == b.query
    return same_host and same_path


def check_url(url: str, timeout: float, delay: float) -> LinkResult:
    res = LinkResult(url)
    host = host_of(url)
    # One request at a time per host, with a short pause, to stay polite.
    with _host_lock(host):
        try:
            status, headers = _request(url, "HEAD", timeout)
            if status >= 400 or status in (300,):
                res.method = "GET"
                time.sleep(delay)
                status, headers = _request(url, "GET", timeout)
        except Exception as e:  # noqa: BLE001
            try:
                res.method = "GET"
                time.sleep(delay)
                status, headers = _request(url, "GET", timeout)
            except Exception as e2:  # noqa: BLE001
                res.kind = "blocked" if is_bot_blocking_host(host) else "error"
                res.detail = f"{type(e2).__name__}: {e2}"[:160]
                time.sleep(delay)
                return res
        finally:
            time.sleep(delay)

    res.status = status
    if 200 <= status < 300:
        res.kind = "ok"
    elif 300 <= status < 400:
        res.kind = "redirect"
        loc = headers.get("Location") if headers else None
        res.target = urllib.parse.urljoin(url, loc) if loc else "(no Location header)"
        if is_minor_redirect(url, res.target):
            res.kind = "minor-redirect"
    elif status in BLOCKED_STATUSES or is_bot_blocking_host(host):
        res.kind = "blocked"
    else:
        res.kind = "broken"
    return res


def check_links(urls: dict[str, list[tuple[str, int]]], workers: int, timeout: float, delay: float):
    results: list[LinkResult] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(check_url, u, timeout, delay): u for u in urls}
        for fut, u in futures.items():
            r = fut.result()
            r.where = urls[u]
            results.append(r)
    return results


def fmt_where(where: list[tuple[str, int]], limit: int = 3) -> str:
    shown = ", ".join(f"`{p}:{n}`" for p, n in where[:limit])
    if len(where) > limit:
        shown += f" and {len(where) - limit} more"
    return shown


def build_report(stamps, stale, link_results, args, today) -> str:
    out: list[str] = []
    out.append("# Freshness check")
    out.append("")
    out.append(f"Run on {today.isoformat()}. Stamps older than {args.months} months count as stale.")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(f"- \"verified YYYY-MM\" stamps found: {len(stamps)}")
    out.append(f"- Stale stamps: {len(stale)}")
    if link_results is None:
        out.append("- Links: not checked (`--offline`)")
    else:
        counts: dict[str, int] = {}
        for r in link_results:
            counts[r.kind] = counts.get(r.kind, 0) + 1
        out.append(f"- Unique URLs checked: {len(link_results)}")
        for kind, label in (("ok", "OK (2xx)"), ("redirect", "Redirects (update the link)"),
                            ("minor-redirect", "Minor redirects (trailing slash or https)"), ("broken", "Broken (4xx/5xx)"),
                            ("error", "Unreachable (timeout, DNS, TLS)"), ("blocked", "Blocked, check manually")):
            out.append(f"- {label}: {counts.get(kind, 0)}")
    out.append("")

    out.append("## Stale stamps")
    out.append("")
    if not stale:
        out.append("None.")
    else:
        out.append("| File | Line | Stamp | Age (months) |")
        out.append("|---|---|---|---|")
        for s, age in sorted(stale, key=lambda x: (-x[1], x[0].path, x[0].line)):
            out.append(f"| `{s.path}` | {s.line} | {s.year}-{s.month:02d} | {age} |")
    out.append("")

    if link_results is not None:
        def section(title, kind, cols, row):
            items = sorted((r for r in link_results if r.kind == kind), key=lambda r: r.url)
            out.append(f"## {title}")
            out.append("")
            if not items:
                out.append("None.")
            else:
                out.append("| " + " | ".join(cols) + " |")
                out.append("|" + "---|" * len(cols))
                for r in items:
                    out.append("| " + " | ".join(row(r)) + " |")
            out.append("")

        section("Broken links", "broken", ["URL", "Status", "Found in"],
                lambda r: [r.url, str(r.status), fmt_where(r.where)])
        section("Unreachable", "error", ["URL", "Error", "Found in"],
                lambda r: [r.url, r.detail.replace("|", "/"), fmt_where(r.where)])
        section("Redirects", "redirect", ["URL", "Status", "Target", "Found in"],
                lambda r: [r.url, str(r.status), r.target or "", fmt_where(r.where)])
        section("Minor redirects", "minor-redirect", ["URL", "Status", "Target", "Found in"],
                lambda r: [r.url, str(r.status), r.target or "", fmt_where(r.where)])
        section("Blocked, check manually", "blocked", ["URL", "Status", "Found in"],
                lambda r: [r.url, str(r.status) if r.status else r.detail.split(":")[0], fmt_where(r.where)])

    out.append("Re-verify each item against its primary source, then update the fact and its "
               "\"verified YYYY-MM\" stamp. See `skills/seo-automations/references/freshness.md`.")
    return "\n".join(out) + "\n"


def parse_args(argv):
    p = argparse.ArgumentParser(description="Check 'verified YYYY-MM' stamps and source URLs in the pack.")
    p.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="repo root (default: parent of scripts/)")
    p.add_argument("--months", type=int, default=3, help="flag stamps older than this many months (default 3)")
    p.add_argument("--offline", action="store_true", help="check dates only, no network")
    p.add_argument("--strict", action="store_true", help="exit 1 on stale stamps, broken or unreachable links")
    p.add_argument("--include-code", action="store_true", help="also check URLs inside code blocks and inline code")
    p.add_argument("--as-of", help="treat this YYYY-MM as the current month (for testing)")
    p.add_argument("--workers", type=int, default=6, help="maximum concurrent requests (default 6, capped at 10)")
    p.add_argument("--timeout", type=float, default=15.0, help="per-request timeout in seconds (default 15)")
    p.add_argument("--delay", type=float, default=0.5, help="pause between requests to the same host (default 0.5s)")
    p.add_argument("--output", help="also write the report to this file")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    if args.as_of:
        y, m = (int(x) for x in args.as_of.split("-"))
        today = dt.date(y, m, 1)
    else:
        today = dt.date.today()

    stamps, urls = scan(root, args.include_code)
    stale = [(s, age) for s in stamps if (age := months_between(s.year, s.month, today)) > args.months]

    link_results = None
    if not args.offline:
        link_results = check_links(urls, max(1, min(args.workers, 10)), args.timeout, args.delay)

    report = build_report(stamps, stale, link_results, args, today)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    sys.stdout.write(report)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")

    failing = len(stale)
    if link_results is not None:
        failing += sum(1 for r in link_results if r.kind in ("broken", "error"))
    return 1 if (args.strict and failing) else 0


if __name__ == "__main__":
    sys.exit(main())
