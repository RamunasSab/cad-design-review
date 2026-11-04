#!/usr/bin/env python3
"""Validate normalized CAD/drawing metadata and cross-file consistency.

This is not a STEP/DXF/PDF parser. A CAD/PDF/DXF extraction tool must provide JSON
conforming to the --example schema. All dimensions are in mm unless stated otherwise.

Usage:
  python check_drawing_data.py input.json
  python check_drawing_data.py input.json --json
  python check_drawing_data.py --example > sample.json
"""
import argparse
import json
import math
import sys
from pathlib import Path

SEVERITY_ORDER = {"NONCONFORMANCE": 0, "RISK": 1, "NEEDS_CLARIFICATION": 2, "INFO": 3}


def add(out, severity, code, location, message, evidence="", recommendation=""):
    out.append({"severity": severity, "code": code, "location": location,
                "message": message, "evidence": evidence, "recommendation": recommendation})


def close(a, b, tol=0.01):
    return abs(float(a) - float(b)) <= tol


def check(data):
    out = []
    files = data.get("files", {})
    supported = ("step", "pdf", "dxf")
    present = [k for k in supported if isinstance(files.get(k), dict)]
    if not present:
        add(out, "NEEDS_CLARIFICATION", "PKG-000", "package", "No recognizable STEP, PDF, or DXF data was found.", recommendation="Provide at least one of these formats or normalized JSON from a parser.")
    else:
        # PDF and DXF are normally exports of the same SolidWorks drawing, not
        # three independent mandatory inputs. Report only what is unavailable.
        if "step" not in present:
            add(out, "INFO", "PKG-001", "scope", "No STEP file supplied: 2D drawing/DXF analysis is possible, but 3D geometry and full 3D DFM cannot be verified.", recommendation="A STEP file is required only to check 3D geometry, wall thicknesses, volumes, or model-to-drawing consistency.")
        if "pdf" not in present and "dxf" in present:
            dxf_drawing = files["dxf"].get("drawing", {})
            has_dims = bool(dxf_drawing.get("dimensions_present") or dxf_drawing.get("dimension_count"))
            has_notes = bool(dxf_drawing.get("notes_present") or dxf_drawing.get("text_count"))
            if not (has_dims and has_notes):
                add(out, "INFO", "PKG-002", "DXF drawing content", "DXF supplied without a PDF. Check whether dimensions, tolerances, notes, and the title block were retained in the exported DXF.", recommendation="Provide a PDF only if this drawing information is missing from the DXF or cannot be read.")
        if "dxf" not in present and "pdf" in present:
            add(out, "INFO", "PKG-003", "2D contour scope", "No DXF supplied: the PDF can be used to review drawing requirements, but precise 2D contour/flat-pattern geometry checks may be limited.", recommendation="A DXF file is needed only when digital checks of contours, cutting geometry, or flat patterns are required.")
        if "pdf" in present and "dxf" in present:
            add(out, "INFO", "PKG-004", "PDF/DXF relationship", "PDF and DXF are treated as exports of the same SolidWorks drawing; they are complementary 2D sources, not three mandatory independent documents.")

    # Metadata consistency
    metas = {k: files[k].get("metadata", {}) for k in present}
    for field, label in (("part_number", "part number"), ("revision", "revision")):
        vals = {str(m[field]).strip() for m in metas.values() if m.get(field) not in (None, "")}
        missing = [k for k in present if metas[k].get(field) in (None, "")]
        if len(vals) > 1:
            add(out, "NONCONFORMANCE", "PKG-010", field, f"Files {label} do not match: {', '.join(sorted(vals))}.", recommendation="Align the document number/revision or confirm that the difference is intentional.")
        if missing:
            add(out, "NEEDS_CLARIFICATION", "PKG-011", field, f"{label} missing from files: {', '.join(missing)}.")

    # STEP integrity and units
    step = files.get("step", {})
    if step:
        st = step.get("geometry", {})
        if st.get("unit") not in ("mm", "millimeter", "millimetre"):
            add(out, "NEEDS_CLARIFICATION", "STEP-001", "STEP units", f"STEP units are missing or are not mm: {st.get('unit')}.", recommendation="Confirm the units before comparing dimensions.")
        if st.get("solid_count") == 0:
            add(out, "NONCONFORMANCE", "STEP-002", "STEP geometry", "No solid bodies were found in the STEP file.")
        if st.get("invalid_solid_count", 0) > 0:
            add(out, "NONCONFORMANCE", "STEP-003", "STEP geometry", f"Invalid solid bodies: {st['invalid_solid_count']}.")
        if st.get("open_shell_count", 0) > 0:
            add(out, "RISK", "STEP-004", "STEP geometry", f"Open shells: {st['open_shell_count']}.")
        if st.get("self_intersection_count", 0) > 0:
            add(out, "NONCONFORMANCE", "STEP-005", "STEP geometry", f"Self-intersections: {st['self_intersection_count']}.")
        if st.get("pmi_present") and st.get("pmi_validation") not in ("valid", "not_checked"):
            add(out, "NEEDS_CLARIFICATION", "STEP-006", "STEP PMI", "PMI is present, but its semantic/associative validation has not been confirmed.")

    # PDF drawing quality
    pdf = files.get("pdf", {})
    if pdf:
        d = pdf.get("drawing", {})
        if d.get("ocr_confidence") is not None and float(d["ocr_confidence"]) < 0.90:
            add(out, "NEEDS_CLARIFICATION", "PDF-001", "PDF OCR", f"OCR confidence is only {d['ocr_confidence']}; dimension and note text must be verified by a person.")
        for field, label in (("general_tolerance", "general-tolerance reference"), ("projection", "projection method"), ("material", "material")):
            if not d.get(field):
                add(out, "NEEDS_CLARIFICATION", "PDF-002", label, f"Not specified on the drawing: {label}.")
        if d.get("dimension_conflicts"):
            for item in d["dimension_conflicts"]:
                add(out, "NONCONFORMANCE", "PDF-003", item.get("location", "drawing"), item.get("message", "Conflicting dimensions."))
        if d.get("duplicate_dimensions"):
            add(out, "RISK", "PDF-004", "drawing dimensions", f"Potentially duplicated dimensions: {len(d['duplicate_dimensions'])}.")

    # DXF integrity
    dxf = files.get("dxf", {})
    if dxf:
        g = dxf.get("geometry", {})
        unit = g.get("unit")
        if unit not in ("mm", "millimeter", "millimetre"):
            add(out, "NEEDS_CLARIFICATION", "DXF-001", "DXF units", f"DXF units are missing or are not mm: {unit}.")
        if g.get("open_contour_count", 0) > 0:
            add(out, "NONCONFORMANCE", "DXF-002", "DXF contour", f"Open contours: {g['open_contour_count']}.", recommendation="Close the cutting contours and separate construction geometry.")
        if g.get("self_intersection_count", 0) > 0:
            add(out, "NONCONFORMANCE", "DXF-003", "DXF contour", f"Contour self-intersections: {g['self_intersection_count']}.")
        if g.get("duplicate_entity_count", 0) > 0:
            add(out, "RISK", "DXF-004", "DXF entities", f"Duplicate geometry entities: {g['duplicate_entity_count']}.")
        if g.get("zero_length_entity_count", 0) > 0:
            add(out, "RISK", "DXF-005", "DXF entities", f"Zero-length entities: {g['zero_length_entity_count']}.")
        if g.get("unassigned_layer_entity_count", 0) > 0:
            add(out, "NEEDS_CLARIFICATION", "DXF-006", "DXF layers", f"Entities are on unapproved layers: {g['unassigned_layer_entity_count']}.")
        if g.get("scale_factor") is not None and not close(g["scale_factor"], 1.0, 1e-6):
            add(out, "NONCONFORMANCE", "DXF-007", "DXF scale", f"DXF scale factor {g['scale_factor']}, expected 1:1.")

    # Cross-file geometry checks
    if "step" in files and "dxf" in files:
        a = files["step"].get("geometry", {}).get("bbox_mm")
        b = files["dxf"].get("geometry", {}).get("bbox_mm")
        if a and b:
            # DXF flat-pattern bounds can differ from formed 3D bounds. Compare only if declared comparable.
            if files["dxf"].get("geometry", {}).get("represents") == "formed_projection":
                diffs = [abs(float(x)-float(y)) for x,y in zip(a,b)]
                if max(diffs) > float(data.get("comparison_tolerance_mm", 0.1)):
                    add(out, "RISK", "XREF-001", "STEP vs DXF bounding box", f"Bounding-box difference X/Y/Z: {diffs} mm.", recommendation="Check units, scale, orientation, and whether the DXF represents the same geometry state.")
            elif files["dxf"].get("geometry", {}).get("represents") == "flat_pattern":
                add(out, "INFO", "XREF-002", "STEP vs DXF", "The DXF is marked as a flat pattern; do not compare its bounding box directly with the formed STEP model.", recommendation="Compare the DXF with the STEP flat pattern, not with the formed model envelope.")

    out.sort(key=lambda x: (SEVERITY_ORDER[x["severity"]], x["code"]))
    counts = {s: sum(x["severity"] == s for x in out) for s in SEVERITY_ORDER}
    if all(k in present for k in ("step", "pdf", "dxf")):
        auto_scope = "EXTENDED_REVIEW"
    elif "step" in present and ("pdf" in present or "dxf" in present):
        auto_scope = "3D_AND_DRAWING_REVIEW" if "pdf" in present else "3D_AND_DXF_REVIEW"
    elif "step" in present:
        auto_scope = "3D_MODEL_REVIEW"
    elif "pdf" in present and "dxf" in present:
        auto_scope = "DRAWING_EXPORT_REVIEW"
    elif "pdf" in present:
        auto_scope = "DRAWING_REVIEW"
    elif "dxf" in present:
        auto_scope = "DXF_REVIEW"
    else:
        auto_scope = "NO_RECOGNIZED_INPUT"
    return {"part": data.get("part", "?"), "scope": auto_scope, "provided_files": present,
            "findings": out, "counts": counts,
            "status": "BLOCK" if counts["NONCONFORMANCE"] else ("REVIEW" if counts["RISK"] or counts["NEEDS_CLARIFICATION"] else "PASS")}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--example", action="store_true")
    a = ap.parse_args()
    if a.example:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False)); return 0
    if not a.input:
        ap.error("provide a JSON file or use --example")
    data = json.loads(Path(a.input).read_text(encoding="utf-8"))
    result = check(data)
    if a.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['part']} | scope={result['scope']} | status={result['status']}")
        print("| Code | Status | Location | Finding | Recommendation |\n|---|---|---|---|---|")
        for f in result["findings"]:
            print(f"| {f['code']} | {f['severity']} | {f['location']} | {f['message']} | {f['recommendation']} |")
        print("\nSummary: " + ", ".join(f"{k}: {v}" for k,v in result['counts'].items()))
    return 0


EXAMPLE = {"part": "BRK-001", "scope": "FULL", "comparison_tolerance_mm": 0.1, "files": {
  "step": {"metadata": {"part_number": "BRK-001", "revision": "B"}, "geometry": {"unit": "mm", "solid_count": 1, "invalid_solid_count": 0, "open_shell_count": 0, "self_intersection_count": 0, "pmi_present": False, "bbox_mm": [100, 50, 2]}},
  "pdf": {"metadata": {"part_number": "BRK-001", "revision": "B"}, "drawing": {"ocr_confidence": 0.98, "general_tolerance": "ISO 2768-mK", "projection": "first_angle", "material": "S235JR", "dimension_conflicts": [], "duplicate_dimensions": []}},
  "dxf": {"metadata": {"part_number": "BRK-001", "revision": "B"}, "drawing": {"dimensions_present": True, "notes_present": True}, "geometry": {"unit": "mm", "represents": "formed_projection", "scale_factor": 1.0, "open_contour_count": 0, "self_intersection_count": 0, "duplicate_entity_count": 0, "zero_length_entity_count": 0, "unassigned_layer_entity_count": 0, "bbox_mm": [100, 50, 2]}}
}}

if __name__ == "__main__":
    raise SystemExit(main())
