# Drawing Data Schema

`check_drawing_data.py` validates normalized metadata extracted from STEP, PDF, and DXF files. It is not a file parser. A separate extraction adapter must populate the JSON structure.

## Top-level fields
- `part`: part number or identifier.
- `scope`: `FULL`, `3D_ONLY`, `DRAWING_ONLY`, `DXF_ONLY`, or `PARTIAL`.
- `comparison_tolerance_mm`: tolerance used for cross-file envelope comparisons.
- `files.step.metadata`, `files.pdf.metadata`, `files.dxf.metadata`: part number and revision where available.

## STEP geometry
Provide units, solid count, invalid-solid count, open-shell count, self-intersection count, PMI presence/validation status, and bounding box in millimetres.

## PDF drawing data
Provide OCR confidence (0–1), general tolerance reference, projection method, material, dimension conflicts, and duplicate dimensions.

## DXF geometry
Provide units, representation (`formed_projection` or `flat_pattern`), scale factor, open-contour count, self-intersection count, duplicate-entity count, zero-length-entity count, unassigned-layer-entity count, and bounding box in millimetres.

## Integration principles
1. Preserve source filename, SHA-256, revision, and extraction-tool version in metadata.
2. Normalize geometry to millimetres before calculations.
3. A DXF flat pattern must not be compared directly with the envelope of a formed STEP model.
4. Missing or unverified data must remain missing; do not fabricate values.
