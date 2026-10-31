# Model-specific SVG references by Peter Lowden

Source repository: https://github.com/alkissack/Dump1090-OpenLayers3-html

Pinned revision: `88e6ea19bdd11cb4196ce6a30304282776a50d89`

Source file: `public_html/plMarkers.js`, preserved here with original credits.
The file credits Peter Lowden (FlyingPete), build 6, 13 April 2017.
Repository GPL version 2 licence is preserved in `LICENSE`; these 14 adaptations
are distributed under GPL-2.0-only. This does not relicense unrelated artwork.

Adapted models: A300-600, A310, A318, A330-300, A340-600, ATR 72,
Boeing 727-200, 747-400, 757-200, 767-300, 777-300ER, 787-9,
Cessna 172 and EC135 / H135.

Each reference was rendered and inspected before adaptation. Geometry, transforms
and model-specific silhouettes are retained. Changes: unified grey fill/outline,
fitted framing, accessible labels and provenance metadata. This is an adaptation
of community SVG artwork, not tracing of a manufacturer drawing.

The upstream B789 SVG was missing a closing quote after its path's final `z`.
The extraction repairs that XML delimiter only, without changing coordinates;
both the original upstream file and the repair record are retained.

`selected-shapes.json` contains safely extracted SVGs and fitted bounding boxes.
Downloaded JavaScript is never executed. `tools/adapt_references.py` reproduces
the adapted artwork; exact source links and per-file attribution are recorded
in `references.json` and SVG metadata. Preserve licence and attribution notices
when distributing these files.
