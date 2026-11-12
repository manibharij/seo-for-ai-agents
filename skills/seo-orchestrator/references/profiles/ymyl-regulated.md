# Profile: YMYL and regulated

Use for anything where being wrong costs someone real harm: health and medical, legal, finance
and insurance, safety, pharmaceuticals, gambling, childcare, immigration. A **modifier** you
combine with the base profile (a clinic is `local-business` + `ymyl-regulated`; a fintech
marketing site is `saas-marketing` + `ymyl-regulated`).

This is the only profile where **Identity is a gate rather than a weighting**. Everywhere else
a weak entity costs you visibility. Here, unsupported authorship on consequential advice is a
reason the page should not be published at all, and the agent's refusals get stricter rather
than its checklist getting longer.

It is also the profile where this method's core discipline earns its keep. "Only `established`
facts may be published" is a sensible rule on a shop. On a page telling someone what to do
about a symptom, it is the whole job.

## How the five systems shift

- **Demand** (observed). Read it, then **filter it**. High-volume demand you cannot answer
  responsibly is demand to decline, and saying so is the finding. A query asking for a
  diagnosis, a legal opinion on specific facts, or a return forecast is one no page should
  answer directly, however much traffic it carries.
- **Identity** (built). **The gate.** Named authors with real, verifiable, relevant
  qualifications; a reviewer where the sector expects one, with their credentials shown; a
  regulator registration number where one exists (GMC, SRA, FCA and their equivalents); a
  visible corrections and editorial policy; clear ownership and funding. Every one of these is
  an `established` fact with a source, or it does not appear. There is no placeholder author
  here, ever.
- **Substance** (built). Accuracy first, completeness second, and every consequential claim
  attributed to a citable source. The honest hedge is part of the substance, not a weakness:
  "this depends on your circumstances, here is what changes the answer, see a professional for
  your case" is the correct content, and a page that gives a confident universal answer where
  one does not exist is wrong even if it ranks.
- **Access** (built). The Visibility Ladder, in dependency order, as everywhere.
  1. **Reach.** Standard checks.
  2. **Read.** Author, credentials, review date and last-updated date visible in the served
     HTML, not only in a database or a tooltip.
  3. **Understand.** `Person` with real `sameAs` to genuine professional profiles, `Organization`
     with real registration details, `MedicalWebPage` or the appropriate specific type where it
     applies, `datePublished` and `dateModified` that are true. Never `Review` or
     `AggregateRating` on a treatment, a practitioner or a financial product unless the reviews
     are real and the sector permits publishing them.
  4. **Connect.** Clear paths to the regulated disclosures, the complaints procedure and the
     professional-advice route, because a reader who needs to escalate should not have to search.
- **Distribution** (earned, advisory). Recognition by professional bodies, registers,
  regulators and reputable sector publications counts for more here than general links, and it
  is less fakeable. The usual boundary applies, with a sharper edge: never pursue a link or
  mention that implies an endorsement or accreditation the business does not hold.

**On assistant surfaces.** Assistants answer consequential questions constantly, and they weight
authorship and source trust heavily when they do. That means the Identity work is also the
eligibility work, and it means the stakes of being quoted are higher: a confident wrong sentence
on your page can be repeated as fact without the hedge that surrounded it. Write every
consequential claim so that it is still true when lifted out of context. Eligibility remains the
only claim. See `surfaces/` and `seo-surface-assistants`.

## Type-specific checks

- **Author and reviewer provenance.** For every page giving consequential guidance: who wrote
  it, what qualifies them, who reviewed it, when. All four, all verifiable, all visible.
- **Claim constraints from the context pack.** `.seo/context.md` carries what this business may
  and may not assert, including the regulator's restrictions. Every claim on a page is checked
  against it, and anything outside it is a finding, not a rewrite.
- **Regulated disclosures present and findable.** Registration numbers, risk warnings, terms,
  complaints routes, cooling-off rights. Varies by sector and jurisdiction; the business
  confirms which apply, and their absence is `needs-human` rather than something to draft.
- **No implied guarantees.** Outcomes, recoveries, returns, success rates and cure claims are
  the highest-risk sentences on the site. Flag each one; remove what cannot be sourced.
- **Testimonials and case studies** only where real, permitted by the regulator (some prohibit
  them outright for certain sectors), and with consent recorded.
- **Staleness is a safety issue, not just an SEO one.** A page citing superseded guidance,
  repealed legislation or an old rate is actively harmful. Set `stale_after` tightly on these
  facts and flag them aggressively.
- **Jurisdiction stated.** Legal, financial and medical guidance is jurisdiction-bound. A page
  that does not say where it applies is wrong for most readers.

## The honest boundary (state this first)

Three things, said before the work starts:

- **The agent does not write consequential advice.** It assesses, structures, checks claims
  against established facts, and briefs a qualified human. Where a page needs a clinician, a
  solicitor or an authorised adviser to write or sign it, that is an escalation, permanently.
- **It cannot verify a credential.** It can check that one is claimed, formatted correctly and
  linked to a register. Confirming the person holds it needs a human with access to the
  register, and it is `needs-human`.
- **Compliance is not SEO.** This profile improves honesty and the visible trust signals search
  engines weigh. It is not a regulatory review, and nothing in it substitutes for the business's
  own compliance process or legal advice.

## Common failures

- Anonymous or pseudonymous bylines on consequential pages, or a generic "Editorial Team".
- A plausible-looking author with no verifiable existence, which is the single worst failure
  available on this profile.
- `MedicalWebPage` or professional schema asserting a reviewer who never reviewed it.
- Confident universal answers to questions whose honest answer is "it depends, and here is what
  on".
- Outcome and return claims with no source, inherited from old marketing copy.
- Pages citing guidance, rates or legislation that has since changed.
- No jurisdiction stated anywhere.
- Fabricated reviews or success rates, in copy or in markup.

## Priority tilt

Weight **Identity** first and treat it as a gate: no publishable consequential page without
verifiable authorship. Then **Substance** for accuracy, attribution and honest hedging. Access
is routine here and goes in its usual order. Expect a higher proportion of `needs-human`
findings than on any other profile, and present that as the correct outcome rather than as the
audit falling short.
