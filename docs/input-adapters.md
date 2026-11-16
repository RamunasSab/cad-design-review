# External input-adapter contract

No parser is bundled. STEP, DXF, PDF and image extraction remain host-specific. The JSON Schema in references/review_input.schema.json defines an optional integration envelope, not a replacement for the existing per-tool CLI inputs.

An adapter must retain source identifier, revision, original units, tool/version, extraction method and verification state. Represent unknown facts as absent/null, not zero. Separate semantic/vector extraction, OCR and measured geometry. A file hash identifies bytes, not engineering correctness. Preserve units until conversion is explicit. Raster pixels and a drawing view scale alone do not prove a numerical CAD measurement.

Use payloads.drawing_data for check_drawing_data.py's existing normalized input, payloads.dfm for check_dfm.py, and payloads.stackup for stackup.py. Extract the relevant payload before invoking the utility. The utilities do not accept/validate the envelope directly. Each payload retains its existing schema; validate it with the consumer as applicable.

Adapters must not treat one fused STEP body as two identifiable snap-fit parts or assume a final engaged position reveals peak deflection. A proposed parser is implemented only when tested with actual files and a suitable CAD/PDF/DXF tool. No automatic adapter selection is provided.
