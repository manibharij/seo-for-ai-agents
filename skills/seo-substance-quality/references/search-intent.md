# Search intent: working out what the page has to be

Read this to decide what a page should actually do, before judging whether it does it well. An
intent mismatch is the most common ranking failure on a technically sound site, and it is also
the one most often misdiagnosed as a content-quality problem: the page is not thin, it is
answering a different question.

**Infer the intent yourself.** Never ask the user "what keyword is this page for". Work it out
from the page's content, its position in the site, its internal links, its URL, and above all
from what the live results for the query look like. Then say what you inferred, so a human can
correct you cheaply.

---

## Read the intent off the SERP, not off a tool

A keyword tool will label a query "informational" or "commercial". That label is a guess from a
model. The live results are Google's actual answer to the question "what does this query mean",
derived from billions of interactions, and it is free to look at.

So the primary method is: search the query, and read the shape of the page.

| What the results look like | What Google thinks the query means | What your page has to be |
|---|---|---|
| Long articles, guides, "how to" | Informational. Someone wants to understand | A genuinely useful explanation |
| Listicles, "best X", comparison tables | Commercial investigation. Someone is choosing | An honest comparison, not a product page |
| Product and category pages, prices, shopping results | Transactional. Someone is buying | A page they can buy from, with price in the HTML |
| One brand's own pages, sitelinks | Navigational. Someone wants a specific site | Your own brand page, if it is yours |
| A mix of article and product results | Genuinely split intent. See below | A deliberate choice, documented |
| A local pack, a map | Local intent, even without a place name in the query | A location or service-area page, and `google-maps` work |
| Video results carried into the web results | Video demand exists here | Consider a video, or at least a transcript page |
| A generated answer at the top | The question has a factual answer | Something extractable. See `seo-surface-assistants` |

Two further signals in the same place, both cheap and both routinely ignored:

- **The "People also ask" box** tells you the sub-questions a complete answer covers. It is the
  closest thing to a free content brief.
- **The result shape changing over time** is the clearest evidence of an intent shift. If a
  query that used to return guides now returns product pages, your guide did not get worse. The
  query moved. That is a different finding with a different fix.

  To observe it rather than remember it, snapshot the **type** of every SERP element for the
  keyword and diff it month on month. Where the environment has DataForSEO, workflow 3 in
  [`seo-orchestrator/references/data/dataforseo.md`](../../seo-orchestrator/references/data/dataforseo.md)
  does exactly this, and distinguishes an intent shift from ordinary decay with evidence
  instead of a hunch.

---

## The four mismatch patterns

These are distinct problems with distinct fixes, and they get lumped together as "the content
is not good enough". Tell them apart before recommending anything.

### 1. Wrong page type for the intent

The classic. A thin product page ranking for an informational query, or a 3,000-word essay where
somebody wanted a price and a delivery date.

**How it looks in data:** impressions but almost no clicks, or clicks with immediate return to
the SERP.

**Fix:** change what the page *is*, or point the query at a different page. Adding words does
not fix a type mismatch, and this is the single most common wasted content investment.

### 2. Right type, wrong stage

The page addresses the topic at the wrong point in the buyer's journey: a solution-aware page
competing for a problem-aware query. Someone who does not yet know that software like yours
exists will not search for your category.

**How it looks in data:** ranking, some traffic, no conversions, and the pages above you are
pitched earlier or later than yours.

**Fix:** usually a new page at the right stage rather than a rewrite of this one, which is doing
its own job properly.

### 3. One page, two intents

A page trying to be both the guide and the product page. It serves neither fully, and it is very
common on small sites where one page carries everything.

**How it looks:** ranking mid-table for two different query clusters and winning neither, with
the SERP for each cluster dominated by pages that do only one thing.

**Fix:** split, deliberately, with each page linking to the other. Decide which keeps the URL,
because that is a redirect decision. Where traffic is already arriving at the existing URL,
treat it as a protected page and get approval.

### 4. The intent moved

The page is unchanged, still correct, still good, and the SERP has changed shape around it.

**How it looks:** a gradual decline with no technical cause and no competitor obviously
outdoing you, and a result page that now contains a different *kind* of result than it used to.

**Fix:** a judgement, not an edit. Either change the page to match the new intent, accept the
loss and target the demand elsewhere, or build a new page of the right type. Say which, and say
that the old page did not fail.

---

## Intent and the audience's actual words

Matching intent is not the same as matching phrasing, and both matter.

Take the vocabulary from `.seo/context.md`'s audience section, which the Identity Steward
established from real sources, rather than from a keyword tool's suggestions. Customers and
practitioners frequently use different words for the same thing, and a page written in the
practitioner's vocabulary can match the intent perfectly and still miss every query.

Where the two differ, the page uses the customer's words in the title, headings and opening,
and may use the practitioner's terms in the body where precision requires it.

What this never licenses: repeating the phrase to signal relevance. If a sentence exists because
of a keyword rather than because of a reader, it is off-intent padding and it gets removed.

---

## Recording an intent finding

A useful intent finding names four things, and a vague one names none:

1. **The intent the page currently serves**, as evidenced by its content.
2. **The intent it should serve**, as evidenced by the live results for the query.
3. **Which mismatch pattern** of the four it is, because that determines the fix.
4. **The evidence**: the SERP shape, and the Search Console impressions-to-clicks pattern where
   data exists.

Confidence is `established` where the SERP was actually checked and recorded, and `inferred`
where the intent was reasoned from the page and the site alone. Both are legitimate. Labelling
them differently is what keeps the report honest.
