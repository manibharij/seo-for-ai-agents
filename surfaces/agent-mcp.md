---
surface: agent-mcp
title: Agents and machine-readable interfaces
verification: strong
verification_methods: [api_response, response_headers, feed, served_html]
claimable_outcome: measured_availability
weighting: [access, identity, substance, demand, distribution]
---

# Agents and machine-readable interfaces

## What this surface is

The surface where the consumer is a program rather than a person: an agent calling an API,
reading a feed, querying an MCP server, or fetching a structured document because a user
asked it to do something on their behalf.

It is the odd one out in this model, in two ways that matter.

**It is fully deterministic.** If an agent can call your endpoint and read your data, it
does not have to guess what you offer. There is no ranking, no synthesis, no sampling. It
either works or it does not, and you can test it exactly. After five other surfaces where
the honest answer is "we can only sample", that is worth something.

**Almost nobody is doing it.** Which cuts both ways: there is no established playbook and
no proven return, and equally no competition. This is the surface where demand is
arriving rather than the one where it has arrived, and that should be said plainly to
anyone deciding whether to invest.

## What decides whether an agent can use you

1. **Access.** Genuinely and overwhelmingly first, because this surface is Access almost
   all the way down. Can the agent reach it, authenticate if needed, parse it, and trust
   its shape? Specifically: does it return structured data rather than HTML that happens
   to contain data; does it declare its content type honestly; is it stable enough to
   build against; does it rate-limit politely rather than blocking outright.
2. **Identity.** The agent has to know whose data this is and be able to attribute it.
   A machine-readable interface with no clear owner is one an agent cannot responsibly act
   on. The same entity consistency that matters everywhere else, expressed in the payload.
3. **Substance.** The data has to be true, current and complete enough to act on. Stale
   prices and availability are worse here than anywhere else in this model, because the
   agent will not notice and may transact.
4. **Demand.** Observed as "what are agents actually asking for", which for most
   businesses today is a short list: availability, pricing, specifications, locations,
   hours, catalogue.
5. **Distribution.** Being listed in whatever registries and directories agents discover
   through, which is early and unsettled.

## What this looks like in practice

In rough order of cost and of how established each is:

- **Clean structured data on the page**, which is the version everyone already has. Honest
  JSON-LD is machine-readable by definition, and an agent reading your product page gets
  the price from it. This is free and you should already be doing it.
- **Feeds**: product, availability, pricing, locations, events. Already standard in
  commerce, already consumed, and already the thing that must agree with the page.
- **A documented public API**, where one exists for other reasons. The SEO-adjacent work
  is making it discoverable and documented rather than building it.
- **An MCP server** exposing the queries an agent would actually want. The newest, the
  least proven, and the most interesting. Treat it as a bet, sized accordingly.
- **`llms.txt` and similar**, which belong here rather than under assistants, and remain
  optional and low-certainty. Google says it does not need them. Some tools fetch them.
  Cheap to add, not a substitute for anything.

## How to verify

Properly, for once, and this is the pleasure of this surface:

- **Call it.** Make the request an agent would make, and assert on the response: status,
  content type, schema shape, the specific fields, the values.
- **Compare against the page.** The API, the feed and the visible page must agree. A
  mismatch is a finding here exactly as it is in commerce feed parity.
- **Check it from outside your network**, without your cookies, without your IP allowlist,
  the way an agent will arrive.
- **Put it in CI.** This is the one surface in the model where a contract test is
  possible, so a regression can fail a build rather than being discovered later.

## What is unknowable here

- Whether agent traffic will become commercially significant for your sector, and when.
- Which protocols and registries will matter in two years.
- Who is calling, often, and why. Agent traffic is poorly identified in most analytics.

## What may never be claimed

Do not claim traffic, revenue or competitive advantage from this surface, because for most
businesses it is not measurable yet and may not materialise. **Availability** is the
claimable outcome: your data is reachable, correct and parseable by a program, verified by
calling it.

Do not sell an MCP server as an SEO deliverable with an expected return. Sell it, if at
all, as cheap optionality on a surface that is deterministic and uncontested.

## Honest note on effort

For nearly every business the right amount of work here today is: get the structured data
and the feeds honest and in parity with the page, which you need anyway, and stop. That
covers the realistic agent demand of the next year for a fraction of the cost of building
an interface.

Build the dedicated interface when there is a specific agent use case someone actually
wants, or when a competitor's absence from it is a genuine opening. "Agents are coming" is
a reason to keep your data clean, not a reason to ship an MCP server.
