# DEPLOY — vintage-press-cafe (Granby CT)

- GitHub: https://github.com/gnaritas/vintage-press-cafe (public, no secrets)
- Railway: workspace "Ramon Leon's Projects", project 5be9a2cb-4597-48ed-9368-e8fb587aa71b (co-host shell 'honeyspell-cafe' project lineage — account project cap hit 11-23; teardown = GraphQL serviceDelete ONLY, never project delete), service 070acc83-c47a-44b3-a79e-c9bd01c39a8c
- Preview host: https://vintage-press-cafe-demo.up.railway.app (noindex meta on every page incl. 404/thanks + X-Robots-Tag; canonical/og:url/sitemap pinned to the -demo host)
- Env: BREVO_API_KEY (xkeysib token from ~/.hermes/secrets/brevo_smtp_key.txt line 2 from "xkeysib" onward, set via `railway variable set BREVO_API_KEY --stdin`, sha-prefix verified cffe2fd40342)
- Stack: static 10-page build via build_pages.py (single source) + server.js (static serve + /contact Brevo HTTP API relay htmlContent/textContent + /open pixel + /healthz + utm CLICK log) + make_og.py (1200x630 og.png) + sweep.py (headless Chrome CDP, viewports 1280x900 + 390x844)
- Deploy: `railway up -d -y -s vintage-press-cafe -e production` from this dir (PATH needs /Users/rleon/.hermes/installs/cc9fa85aa0727d13/node_modules/.bin)
- Acceptance evidence 2026-11-25: _verify.py PASS (0 fails); 15-asset sha parity live==disk; contact form 303 + MAILSENT proven in deployment logs (test tokens VPC-SWEEPTEST + VPC-FINALTEST delivered into lane mailbox via Gmail All Mail search); OPEN pixel + utm CLICK logged server-side; render sweep 20/20 DOM gates CLEAN (post visit-mapwrap mobile fix, fixed height 320px/auto aspect <640px); OpenRouter gemini battery 20 shots → 20 nitpick claims adjudicated FALSE by 4 native-res vision crops (precedent: finders-records/honey-bistro hallucination class); montages renders/montage-{desktop,mobile}-{A,B}.jpg
- Built: 2026-11-25. Facts on site ONLY from Patch/CT Bites/FB Intro (hours 7a-2p daily per Patch; former print shop per CT Bites; no published owner name -> none on site).
