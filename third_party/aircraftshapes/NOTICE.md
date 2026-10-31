# AircraftShapesSVG reference adaptations

Source: https://github.com/RexKramer1/AircraftShapesSVG

Pinned revision: `0743718760c42a5e91801adc053b5b828a434a5e`

Author credited in source metadata and tutorial: RexKramer1.
Project: AircraftShapesSVG / BelugaProject, with acknowledgement of amnesica,
tar1090, FlightAware dump1090 and their contributors in upstream README.

The selected source SVGs explicitly identify **GNU General Public License v3.0**
in their metadata. The GPL version 3 text is preserved in `LICENSE`. These
22 adaptations are distributed under GPL-3.0-only; this notice does not relicense
unrelated artwork. Preserve these notices and source data when distributing them.

`selected.json` records exact source paths, source titles, fitted framing and
accent group identifiers. Saved vector-only source SVGs are in `silhouettes/`.
Embedded raster images, hidden reference layers, editor metadata and other
non-vector content are excluded from these saved copies and from adaptations.

Changes: existing unfilled outline paths filled with #505a64 to form silhouettes;
accent paths retain unfilled geometry in the same grey; viewBox fitted to artwork;
accessible labels and licence/provenance metadata added. Coordinates, transforms
and drawing order are retained. `tools/adapt_aircraftshapes.py` reproduces outputs.

Variant checks:

- C130 source is specifically C-130J-30; catalogue title and length reflect that.
- MIRA source explicitly names Mirage IIIE, not Mirage 2000.
- F18S explicitly names F/A-18E Super Hornet.
- AT45 is ATR 42-500; B712 is Boeing 717-200; T204 is Tu-204-100.
- CL2T is a shared CL-215T / CL-415 family reference; it does not establish every
  detail specific to a CL-415 variant.
- KC-135E source is intentionally not adapted for current KC-135R aircraft.

These are community-authored top-view SVG references, not certified engineering
drawings. Per-model attribution and source links are also in `references.json`
and each generated SVG's metadata.
