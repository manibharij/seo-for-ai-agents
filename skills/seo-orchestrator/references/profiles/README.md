# Site-type profiles

Read the profile that matches the site. A profile doesn't replace the Visibility Model, it **tunes** it: which of the five systems and which issues matter most for this kind of site, and the type-specific checks to add. The orchestrator detects (or asks) the site type in Step 0 and pulls the relevant profile.

| Profile | Use when the site is… |
|---|---|
| [content-blog.md](content-blog.md) | A blog, magazine, or content/affiliate site |
| [news-publisher.md](news-publisher.md) | A news site or publisher (recency, Top Stories, `NewsArticle`) |
| [ecommerce.md](ecommerce.md) | A shop selling products (Shopify, WooCommerce, custom) |
| [local-business.md](local-business.md) | A business serving a place (shop, clinic, tradesperson, restaurant) |
| [saas-marketing.md](saas-marketing.md) | A SaaS/product marketing site or app landing pages |
| [documentation.md](documentation.md) | Developer/product docs, knowledge bases, help centres |
| [international.md](international.md) | Any site targeting multiple countries/languages (combine with another profile) |

A site can match more than one (for example an international e-commerce site applies `ecommerce.md` plus `international.md`). Profiles tune emphasis and add checks; they never drop a system, and they never let you work above a broken rung of Access. Infer the type from the site's content and structure; when genuinely ambiguous, pick the most likely and proceed rather than asking.

These are deliberately horizontal *modalities*, not narrow sector playbooks: they shift how each system applies, they don't fork the method.
