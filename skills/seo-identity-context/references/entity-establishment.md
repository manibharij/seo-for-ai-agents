# Entity establishment: the half of Identity that is not on your site

Read this when an engine cannot work out who a business is, when a knowledge panel is wrong
or absent, or when assistant surfaces name competitors and not you despite good pages.

`model/systems.md` says Identity "decides whether an assistant can name you at all, because
an engine that cannot resolve who you are has nothing to recommend". Most of this pack's
Identity work is on-site: consistent naming, `Organization` and `Person` markup, `sameAs`,
NAP. That is the half you control. This file is the other half, which is **where the engine
actually forms its understanding**, and it is mostly not on your domain.

## What an entity is, in the only sense that matters here

Not your website. A thing the engine believes exists, distinct from similarly named things,
with properties it has corroborated from more than one source.

The practical test is disambiguation: search the business name and see whether the engine
returns one coherent thing, several confused things, or something else entirely. A company
sharing a name with a band, a town or a bigger company in another sector has an entity
problem that no amount of on-page schema will solve by itself.

## The three jobs, in order

### 1. Be internally consistent first
Nothing off-site can resolve what the site itself contradicts. Before anything here:

- One canonical name, spelled identically on every page, in the schema, and in the footer.
  Not "Acme Ltd", "Acme Limited" and "ACME" across three templates.
- One `Organization` with a stable `@id`, referenced rather than repeated, so the publisher
  of an article *is* the business *is* the entity in the footer.
- `sameAs` pointing only at profiles that genuinely exist, are current, and are actually
  yours. A dead link to an abandoned platform is a corroboration failure.
- Real people with `Person` entities that resolve to profiles a human could check.

This is the `seo-access-understand` and `seo-identity-context` work, and it is the
precondition for everything below.

### 2. Be corroborated in the places engines already trust
An engine builds confidence from independent agreement. The job is therefore not to assert
more loudly on your own site, but to be consistently described elsewhere:

- **The obvious profiles for the sector**, complete and matching: Companies House or the
  equivalent register, LinkedIn, the relevant trade body, the app store listing, the package
  registry, GitHub, Crunchbase. Which ones matter varies enormously by sector, and the right
  set is the one your actual peers appear in.
- **Press and industry coverage** that names the business the same way. This is
  Distribution work and it is earned (`seo-distribution-authority`).
- **Public knowledge bases**, below.

Every one of these is a place the name, the description and the key facts must agree. A
business describing itself three different ways across five profiles is giving the engine
three candidate entities.

### 3. Public knowledge bases, carefully
Wikidata and Wikipedia are open, structured, widely consumed, and **governed by their own
communities with their own rules**. They are not marketing channels and treating them as one
goes badly.

The hard rules, which this pack applies regardless of what a client wants:

- **Notability is theirs to judge, not yours.** Most small businesses do not qualify for a
  Wikipedia article, and creating one for a business that does not meet the criteria wastes
  everyone's time and damages the relationship with those communities.
- **Editing an entry about yourself is a conflict of interest**, and both projects have
  explicit expectations about disclosure. The agent does not create or edit entries on a
  customer's behalf. That is a permanently human task, done openly, by someone who has read
  the community's rules.
- **Never fabricate sourcing to meet a notability bar.** This is the same refusal as
  inventing an author, in a context where it is more likely to be noticed and more damaging
  when it is.

What the agent *can* do: check whether an entry exists, whether its facts match reality,
and report a factual error with its evidence so a human can raise it properly.

## Knowledge panels

A knowledge panel is the engine's view of the entity, assembled from sources it trusts. It
is not a profile you fill in.

- **You cannot create one on demand.** Panels appear when the engine is confident enough
  about an entity, and no markup, submission or payment produces one.
- **Google offers a verification route for entity owners**, which allows suggesting changes
  to an existing panel rather than authoring it. Check the current process before describing
  it to a client: this mechanism has changed more than once.
- **A wrong panel is a real finding** and often traces to a stale or contradictory source
  that is still being corroborated. Finding the source of the wrong fact is the work; the
  panel is the symptom.

Do not promise a knowledge panel. Do not quote a timeline for one. The claim available is
that the entity is consistent, corroborated and resolvable, which is the precondition.

## Why this matters more than it used to

On a classic web result, a weak entity costs you some trust signals. On an assistant surface
it is the gate: `surfaces/chatgpt.md` puts Identity first in the weighting, above Substance
and well above Access, precisely because a synthesiser must resolve who you are before it
can consider recommending you.

So the work in this file is the highest-leverage thing available for the `ai-visible` job,
and it is almost always the thing that job actually needs rather than the answer formatting
people arrive asking about.

## Diagnosing an entity problem

Observable, cheap, and worth doing before any of the above:

1. **Search the exact business name.** Is the result coherent? Is there a panel? Does it
   describe the right thing?
2. **Search the name plus the sector.** Does disambiguation improve it? If so, the entity is
   weak rather than absent.
3. **Ask two assistants who the business is**, recorded as a dated sample. A confident wrong
   answer and a refusal are different problems: the first means a competing entity is being
   resolved, the second means none is.
4. **Collect every public description** across profiles and registers, and diff them. The
   contradictions are the finding, and they are usually surprising.
5. **Check `sameAs`** actually resolves, everywhere it appears.

Record each as a finding with the evidence quoted. Anything requiring a credential, a
verification or a relationship is `needs-human`, which here is most of the remedy and should
be said plainly rather than buried.
