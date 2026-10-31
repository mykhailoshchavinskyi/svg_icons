# tar1090 SVG reference adaptations

Upstream: https://github.com/wiedehopf/tar1090

Pinned revision: `5d59b1ba2c5e30eb23f1161940367b7767f10ad5`

Source: `html/markers.js` (preserved here, with original contributor comments).
Licence: GPL version 2 or later; upstream licence and notices are in `LICENSE`.
Upstream notices credit Matthias Wirth and FlightAware dump1090. The A320/B737
family refinements are credited to pimlie. Preserve these notices with copies.

Only the 39 explicitly selected model shapes in `tools/adapt_references.py`
are adapted into `reference-artwork/` and the corresponding root SVGs.
Their original geometry is retained. Changes: palette, SVG wrapper, accessibility
labels and provenance/licence metadata. These adaptations remain under
GPL-2.0-or-later. This notice does not relicense the unrelated original SVGs or
the other independently drawn artwork in this repository.

`selected-shapes.json` is a data-only extraction of the selected `viewBox` and
`path` values. No downloaded JavaScript is executed. Other upstream shapes,
including the separately CC BY 4.0 C-130 by Peter Lowden, are not adapted here;
their original credits remain in the preserved source file.

These are community-created SVG reference images, not official manufacturer
orthographic drawings. Technical rendering and visual agreement with these
references do not prove exact real-aircraft dimensions or configuration.
