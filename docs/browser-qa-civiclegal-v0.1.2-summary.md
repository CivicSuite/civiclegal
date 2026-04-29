# CivicLegal v0.1.2 Browser QA

- Date: 2026-04-29
- Scope: updated `docs/index.html` landing page plus live `/civiclegal` public page after the shared `civiccore.search` access-helper rollout.
- Desktop docs screenshot: `docs/browser-qa-civiclegal-v0.1.2-docs-desktop.png`
- Mobile docs screenshot: `docs/browser-qa-civiclegal-v0.1.2-docs-mobile.png`
- Desktop public-page screenshot: `docs/browser-qa-civiclegal-v0.1.2-public-desktop.png`
- Mobile public-page screenshot: `docs/browser-qa-civiclegal-v0.1.2-public-mobile.png`
- Visible checks: version `0.1.2`, dependency copy updated to the published `civiccore` v0.11.0 release wheel, shared-access-helper copy present, no stale `0.3.0` dependency claims on current-facing pages.
- Console/result note: no page-level console issues surfaced during the docs/public-page browser pass; headless Edge emitted unrelated internal renderer task-provider stderr outside the page context.
