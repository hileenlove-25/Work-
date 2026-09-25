# Hileenlove website

Standalone storefront for Hileenlove's digital downloads and print-on-demand goods. No marketplace storefront is required: this is plain HTML/CSS/JS in this folder, hosted for free on GitHub Pages.

## 1. Turn on GitHub Pages

1. On GitHub, open **Settings → Pages** for this repository.
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Branch: pick the branch this was merged into (e.g. `main`) — Folder: **/docs**.
4. Save. GitHub will publish at `https://<your-username>.github.io/<repo>/` within a minute or two.

## 2. Connect hileenlove.com

A `CNAME` file with `hileenlove.com` is already in this folder, so once Pages is on:

1. Still in **Settings → Pages**, under **Custom domain**, enter `hileenlove.com` and save.
2. At your domain registrar (wherever you bought/will buy hileenlove.com), add these DNS records:
   - **A records** for the root domain (`hileenlove.com`) pointing to GitHub's Pages IPs:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - **CNAME record** for `www` pointing to `<your-username>.github.io`
3. Wait for DNS to propagate (can take a few minutes to a few hours), then back in Settings → Pages check **Enforce HTTPS**.

If you don't own hileenlove.com yet, buy it from any registrar (Namecheap, Google Domains successor Squarespace Domains, Cloudflare, GoDaddy, etc.) — then do the DNS steps above.

## 3. Connect checkout and fulfillment

The catalog is ready for direct product links, but each `checkoutUrl` starts as `"#"` until you connect your own checkout and fulfillment accounts. To start actually selling:

1. For digital downloads, create a payment link that delivers the matching PDF after payment.
2. For print-on-demand goods, create the tee and tote with your chosen printer and connect their product or checkout links.
3. Open `assets/products.js` and replace each product's `checkoutUrl: "#"` with the real link. The page itself remains the customer-facing Hileenlove shop.
4. Commit and push — the live site updates automatically next time Pages rebuilds.

## Editing content

- **Products, prices, descriptions, checkout links:** `assets/products.js`
- **Page copy (hero, about, FAQ):** `index.html`
- **Colors, fonts, layout:** `assets/styles.css` (brand colors are defined once at the top as CSS variables)
- **Cover images:** `assets/images/` (currently copied from `../digital-downloads/images/`)

## Preview locally

```sh
cd docs
python3 -m http.server 8000
# open http://localhost:8000
```
