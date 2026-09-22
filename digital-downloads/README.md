# The Front-of-House Series (DigitalByHileen)

Six printable digital-download guides for restaurant and hospitality workers, plus a combined bundle.

| File | Guide |
|---|---|
| `pdf/01-…` | How to Increase Your Tips and Income |
| `pdf/02-…` | Preventing Burnout in the Restaurant Industry |
| `pdf/03-…` | How to Document Mistreatment in the Workplace from Management |
| `pdf/04-…` | Essential Skills Every Front-of-House Worker Needs |
| `pdf/05-…` | Restaurant Communication and Workplace Conflict |
| `pdf/06-…` | Dealing with Being Outcasted and Treated Differently by Management |
| `pdf/00-…` | The Restaurant Worker's Survival Bundle (all six) |

- `content/`: guide text in a simple markup (see the top of `build.py`). Edit these to change the guides.
- `pdf/`: finished, ready-to-sell PDFs.
- `images/`: cover images for product listings.
- `SHOPIFY-LISTINGS.md`: product titles, descriptions, tags, and suggested prices.

## Rebuilding

```sh
pip install reportlab pypdf pymupdf
python3 build.py                      # all guides + bundle
python3 -c "import pymupdf,glob;[pymupdf.open(f)[0].get_pixmap(dpi=150).save('images/'+f[4:-4]+'-cover.png') for f in glob.glob('pdf/*.pdf')]"   # refresh cover images
```

Fonts (Liberation Sans, DejaVu Serif) are bundled in `fonts/` under their open licenses.
