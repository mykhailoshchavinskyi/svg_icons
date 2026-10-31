# Plane Watch reference artwork adaptations

Upstream: https://github.com/plane-watch/pw-silhouettes

Pinned revision: `338826d35d1e30cca0464713001de5f2723a3aee`

Copyright (c) 2026 Plane Watch Contributors.
Licence: Creative Commons Attribution–NonCommercial–ShareAlike 4.0 International.
https://creativecommons.org/licenses/by-nc-sa/4.0/

These 23 adaptations are for **noncommercial use only**, with attribution and
share-alike requirements. The user explicitly approved inclusion of this licence.
Keep this notice and per-file attribution with copies. These terms apply to
the listed adaptations, not unrelated artwork in the repository.

Models are enumerated in `tools/adapt_planewatch.py`; exact source SVG links,
selected animation frame, attribution and changes are recorded in
`references.json` and in each adapted SVG's metadata.

The saved `silhouettes/` files are sanitized copies of upstream vector artwork:
all embedded images, hidden "Reference Artwork" layers, editor metadata and
non-vector content have been removed. The upstream licence does not grant
rights to embedded reference images; none are included here. The retained
vector paths, transforms and drawing order are unchanged.

Adaptation changes: unified grey fill/outline, fitted viewBox, accessible labels
and provenance metadata. Rotor/propeller animation uses one static frame.
These are community SVG references, not certified manufacturer drawings.

Source selection checks:

- R44 uses its actual `R44-3.svg` vector, not `B06-1.svg` incorrectly referenced
  by the upstream R44 airframe JSON.
- B429 is not adapted: its manifest points to a B412 silhouette.
- E295 is not adapted: its manifest aliases E290.
- The Plane Watch F16 snapshot is included only for comparison, not used as an
  adaptation; the active F-16 now uses the AircraftShapesSVG reference.
