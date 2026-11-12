# Profile: portfolio and personal brand

Use for a small site that represents one person or a very small studio: a developer or designer
portfolio, a consultant or freelancer site, an author or speaker page, a founder's personal
site, a small agency of two or three people.

This is the most common shape of site built by the people this pack is written for, and it is
the one most badly served by general SEO advice, which assumes a content programme, a team and a
budget that do not exist. A five-page site does not need a topic cluster strategy. It needs to
be reachable, to say clearly what this person does and for whom, and to resolve as an entity.

The scope is genuinely small, and saying so is part of the value. The honest finding on most of
these sites is that an afternoon of work covers nearly everything available, and the rest is
Distribution that cannot be rushed.

## How the five systems shift

- **Demand** (observed). Usually tiny and heavily branded: the person's name, the name plus a
  skill, and a small number of service or specialism queries. Reading it honestly often shows
  that the realistic traffic is people who already know the name, plus a narrow niche. That
  changes the whole plan, and it is better known at the start.
- **Identity** (built). **The whole profile, essentially.** The site exists to establish who one
  person is. One consistent name spelled identically everywhere, `Person` schema with real
  `sameAs` to the profiles that genuinely exist (GitHub, LinkedIn, the relevant platform for the
  field), a clear statement of what they do and for whom, and real proof: named clients where
  permitted, actual work, genuine credentials. This is also what makes the person resolvable to
  an assistant asked "who is X".
- **Substance** (built). Depth comes from specificity, not volume. A page that says precisely
  what this person does, for which kind of client, with what approach and what it costs, beats
  twenty generic blog posts. Case studies with real detail are the highest-value content type
  here and the most commonly missing.
- **Access** (built). The Visibility Ladder, and the one place where these sites fail hard.
  1. **Reach.** The classic failure, because portfolios are exactly the sites built as
     client-rendered SPAs by developers showing off. A beautiful animated portfolio serving
     crawlers an empty root div is the single most common finding on this profile. Verify on the
     served HTML.
  2. **Read.** A real title and description per page, a clear `h1`, the work described in text
     and not only in images, and page weight kept sane despite a heavy visual design.
  3. **Understand.** `Person` and, where it applies, `Organization`, with honest `sameAs`.
     `CreativeWork` on portfolio pieces where useful. Modest and accurate beats extensive.
  4. **Connect.** Trivial at this size and still worth getting right: every page linked, clean
     URLs, one canonical each, no orphaned case study reachable only from a carousel.
- **Distribution** (earned, advisory). For an individual this is reputation: talks, open-source
  work, writing published elsewhere, podcast appearances, client referrals, a real presence in
  the professional community. Entirely earned, slow, and the main driver of whether anyone
  searches the name at all. Advisory only.

**On assistant surfaces.** Being named when somebody asks an assistant for "a freelance X who
does Y" is plausible for a specialist with a resolvable identity and a clear specialism, and it
rests almost entirely on Identity plus third-party presence. Generic positioning makes it
impossible, because there is nothing specific to match. Eligibility only. See `surfaces/` and
`seo-surface-assistants`.

## Type-specific checks

- **Does the served HTML say what you do?** Fetch the homepage without JavaScript. If it is
  empty, or if it contains only a name and a hero animation, the site does not communicate
  anything to a machine. Start here.
- **Is the work described in text?** Portfolio pieces presented purely as images have no
  content. Each needs a real description: the problem, the approach, the outcome, the stack or
  the medium.
- **One name, spelled one way.** Across the site, the schema, and every linked profile. A
  surprising number of personal sites use two variants.
- **`sameAs` to profiles that exist and are current.** A dead link to an abandoned platform is
  worse than no link.
- **Contactable.** A real, working contact route in the HTML, not only behind a JavaScript form
  that fails silently.
- **Specialism stated, not implied.** "Developer" matches nothing anyone searches. "Rails
  developer for marketplaces" is a position. This is the highest-value copy change available on
  most of these sites.
- **Client names and logos only where permitted.** Check before publishing; NDAs are common in
  this modality and an agent must not assume.
- **A blog that exists but has two posts from 2023.** Either commit to it or remove it. A visibly
  abandoned blog is a trust signal in the wrong direction.

## The honest boundary (say this early)

- **The scope here really is small.** On a five-page site there is no content strategy worth
  building. The work is Access, clear positioning, honest Identity, and then nothing, and
  recommending a twelve-month content plan to a freelancer is overselling.
- **Most of the traffic will be branded.** People who heard the name look it up. That is normal,
  it is valuable, and it means the job is mostly to be findable and convincing rather than to
  compete for category terms.
- **Competing for broad category terms is usually not realistic.** "Web designer" belongs to
  directories and agencies with authority. A niche, specific position is both more winnable and
  more commercially useful.
- **No fabricated proof.** No invented clients, testimonials, case studies, awards or
  qualifications. On a personal site these are claims about a real named individual, which makes
  inventing them worse rather than more tempting.

## Common failures

- A client-rendered portfolio serving crawlers nothing.
- Work shown only as images, with no text anywhere.
- Positioning so generic it matches no query: "creative problem solver", "passionate about
  technology".
- No `Person` schema, or `sameAs` pointing at profiles that no longer exist.
- Two spellings of the same name across the site and the schema.
- An abandoned blog visible in the navigation.
- Testimonials with no attributable source.
- Beautiful design, 8MB homepage, three-second first paint.

## Priority tilt

Weight **Access** first, because the rendering failure is both the most common and the most
total: nothing else matters until the served HTML says something. Then **Identity** (one name,
real profiles, stated specialism) and **Substance** (describe the work in words). Then stop, and
tell the owner honestly that Distribution is the rest of the job and it is earned by doing
visible work in public over time.
