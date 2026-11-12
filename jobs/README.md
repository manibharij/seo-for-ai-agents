# Jobs

A **job** is the situation someone actually arrives with. It is the front door to the
method, because nobody turns up asking for "the Access system": they turn up saying the
site dropped, or they are about to launch, or they want ChatGPT to mention them.

A job does three things:

1. **Scopes the model.** It says which of the five systems matter here and in what order,
   so the work does not start in the most comfortable place.
2. **Activates roles.** It names which roles do the work and who reports.
3. **Sets the default autonomy** for the situation, which is the part most people get
   backwards. See below.

The nine jobs are the `job` enum in
[`contracts/work-item.schema.json`](../contracts/work-item.schema.json), so a work item
always knows which situation it belongs to.

## The nine jobs

| Job | They arrive saying | Leading system | Default autonomy |
|---|---|---|---|
| [`new-site`](new-site.md) | "I have an idea and I am about to build it" | Demand | 4 |
| [`launch`](launch.md) | "We are going live this week" | Access | 3 |
| [`rescue`](rescue.md) | "Something is wrong and I do not know why" | Operations, then Access | 2 |
| [`grow`](grow.md) | "It works, I want more of it" | Demand, Substance, Distribution | 2 |
| [`migrate`](migrate.md) | "The URLs are changing" | Access | 2 |
| [`scale`](scale.md) | "I need a lot of pages" | Substance (as a gate) | 2 |
| [`ai-visible`](ai-visible.md) | "I want AI assistants to recommend me" | Identity | 2 |
| [`client-audit`](client-audit.md) | "I need to audit a site I do not control" | All five, briefly, then the constraint | 1 |
| [`maintain`](maintain.md) | "Keep it from breaking" | Operations | 4 |

## Why autonomy is not a measure of difficulty

Autonomy tracks **what is at risk**, not how hard the work is.

`new-site` and `maintain` sit at rung 4 from opposite directions. A new site has nothing
to break: no rankings, no traffic, no directive that might be load-bearing. Maintenance is
narrow and repetitive, re-running known checks against known expectations, so it cannot
surprise anyone.

`migrate` and `grow` sit at rung 2 although they are the jobs an expert would find most
interesting, because both can destroy something that already earns. `client-audit` sits at
rung 1 because there is no mandate to change anything at all.

The rungs themselves are defined in `contracts/work-item.schema.json`: 1 observe,
2 recommend, 3 propose, 4 execute within fences, 5 operate. A customer can widen a fence
themselves with an `always_allow_rule`, and the work item records that they did, rather
than the platform assuming it.

## Jobs combine and hand over

They are not exclusive, and a real engagement moves between them:

- A relaunch is `migrate` **then** `launch`, in that order. Treating it as only a launch
  is how sites lose everything they had earned.
- A rescue that clears every system and finds nothing broken was never a rescue. The
  market moved, and it is a `grow` job.
- A `client-audit` that turns into an engagement becomes `rescue`, `grow` or `maintain`
  depending on what the audit found.
- Every job ends in `maintain`, or it quietly loses what it won.

## Writing a new job

Match the shape of the existing files: frontmatter declaring `job`, `title`, `situation`,
`roles`, `data`, `guardrails`, `default_autonomy`, `stop_when` and `done_when`; then the
order of work with the workflows each step calls; then **what this job must never do**;
then the output.

Two sections earn their place in every one of them. State the most common way the job
goes wrong, because that is usually the whole value of having written it down. And state
what the honest negative answer looks like, so the agent can return it.
