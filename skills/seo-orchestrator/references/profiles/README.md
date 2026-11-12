# Site-type profiles

Read the profile that matches the site. A profile doesn't replace the Visibility Model, it **tunes** it: which of the five systems and which issues matter most for this kind of site, and the type-specific checks to add. The orchestrator detects (or asks) the site type in Step 0 and pulls the relevant profile.

### Base profiles

| Profile | Use when the site is… | Leading system |
|---|---|---|
| [content-blog.md](content-blog.md) | A blog, magazine, or content site | Substance |
| [news-publisher.md](news-publisher.md) | A news site or publisher (recency, Top Stories, `NewsArticle`) | Access + Identity |
| [ecommerce.md](ecommerce.md) | A shop selling products (Shopify, WooCommerce, custom) | Access |
| [local-business.md](local-business.md) | A business serving a place (shop, clinic, tradesperson, restaurant) | Identity |
| [saas-marketing.md](saas-marketing.md) | A SaaS/product marketing site or app landing pages | Access, then Substance |
| [documentation.md](documentation.md) | Developer/product docs, knowledge bases, help centres | Access, then Substance |
| [marketplace-directory.md](marketplace-directory.md) | Content supplied by other people: marketplaces, job boards, property portals, directories, listings | Access |
| [affiliate-comparison.md](affiliate-comparison.md) | Reviewing or comparing things you don't sell: "best X", versus pages, buyer's guides, referral-monetised content | Identity + Substance |
| [portfolio-personal-brand.md](portfolio-personal-brand.md) | One person or a very small studio: portfolio, consultant, freelancer, founder, author | Identity |

### Modifiers, combined with a base profile

| Profile | Use when… | What it changes |
|---|---|---|
| [international.md](international.md) | The site targets multiple countries or languages | Access (hreflang, canonicals, URL strategy) becomes critical |
| [ymyl-regulated.md](ymyl-regulated.md) | Being wrong causes real harm: health, legal, finance, safety, gambling, childcare | Identity stops being a weighting and becomes a **gate** |

A site can match more than one, and most real sites do: an international shop applies
`ecommerce.md` plus `international.md`; a private clinic applies `local-business.md` plus
`ymyl-regulated.md`; a SaaS with docs applies `saas-marketing.md` plus `documentation.md`; a
financial comparison site applies `affiliate-comparison.md` plus `ymyl-regulated.md`, which is
the strictest combination here.

Profiles tune emphasis and add checks; they never drop a system, and they never let you work
above a broken rung of Access. Infer the type from the site's content and structure; when
genuinely ambiguous, pick the most likely and proceed rather than asking.

These are deliberately horizontal *modalities*, not narrow sector playbooks: they shift how each
system applies, they don't fork the method. That is why there is no `healthcare.md` or
`legal.md`. What those sectors share is that a wrong answer harms somebody, which is a modality,
and it is `ymyl-regulated.md`. A dentist's site is `local-business` plus `ymyl-regulated`, and
that composition carries more than a sector playbook would.

**If no profile fits**, run the five systems unmodified rather than forcing the nearest one. A
missing profile costs you some tuning; the wrong profile costs you the wrong priority order.
