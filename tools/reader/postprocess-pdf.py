#!/usr/bin/env python3
"""Post-process and QA-gate the Quantum Computing Handbook A4 PDF (V4).

Supports --probe-pages (Pass 1 -> Pass 2 TOC page-number loop), chunked mode
(--chunks-manifest / manifest["chunks"]), and legacy monolithic mode (--body):
1. --probe-pages scans ordered body chunk PDFs and emits exact 1-based printed
   body page numbers for every Named Destination so build-pdf.mjs can render
   the two-column TOC with right-aligned page numbers and dot leaders.
2. Merges cover.pdf + chunk-00-toc.pdf + body chunks via native MuPDF insert_pdf,
   sets /PageLabels (Cover / i, ii / 1..N) with 0 offset between PDF labels,
   printed TOC numbers, and running footers, and suppresses running headers and
   footers on cover, TOC, and part divider pages.
3. Converts all TOC and cross-chunk sentinel links (https://qch.local/#<anchor>)
   into exact internal PDF GoTo link annotations and writes 3-level Unicode
   bookmarks (including frontmatter sections).
4. Removes any partial /StructTreeRoot or /MarkInfo when untagged (noting native
   MathML 3 EPUB 3 as the preferred accessible edition), runs doc.subset_fonts(),
   normalizes Kangxi /ToUnicode CMaps, performs two-stage leaf + Image/SMask
   stream deduplication, and saves with garbage=4, deflate, clean=True, and
   use_objstms=True.
5. Runs automated publishing QA gates (reporting totalPages, fileSizeMiB,
   embeddedFonts, tocPageNumberCoverage, /PageLabels, and 0-offset alignment).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import sys
import tempfile
import time
import unicodedata
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import fitz  # PyMuPDF
from pypdf import PdfReader, PdfWriter
from pypdf.generic import BooleanObject


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TMP = Path("/tmp/qch-pdf-build")
DEFAULT_COVER = DEFAULT_TMP / "cover.pdf"
DEFAULT_BODY = DEFAULT_TMP / "body.pdf"
DEFAULT_MANIFEST = DEFAULT_TMP / "outline-manifest.json"
DEFAULT_OUTPUT = REPO_ROOT / "dist" / "quantum-computing-handbook.pdf"
DEFAULT_REPORT = REPO_ROOT / "work" / "research" / "pdf-build-report.json"
DEFAULT_PREVIEW_DIR = REPO_ROOT / "work" / "rendered"

BOOK_TITLE = "量子计算手册：从直觉、数学与物理到容错、传感与模拟边界"
BOOK_HEADER_LEFT = "量子计算手册｜从直觉到研究入口"
BOOK_AUTHOR = "量子计算手册编写组"
BOOK_SUBJECT = "系统量子计算与量子力学教材（A4 高保真印刷精排本；无障碍屏幕朗读请优先使用配套原生 MathML 3 EPUB 3 版本）"
BOOK_KEYWORDS = "量子计算, 量子力学, 量子算法, 量子纠错, 表面码, 量子传感, 稳定子模拟, 离线出版, KaTeX, EPUB3无障碍配套"

DEFAULT_CROSS_LINK_PREFIX = "https://qch.local/#"

# Running header/footer palette matching tools/reader/pdf.css (@page margin: 17.5mm 15mm)
HEADER_RULE_COLOR = (0xD7 / 255.0, 0xD1 / 255.0, 0xC5 / 255.0)  # #D7D1C5
HEADER_TEXT_COLOR = (0x53 / 255.0, 0x66 / 255.0, 0x60 / 255.0)  # #536660
MARGIN_X_PT = 15.0 * 72.0 / 25.4  # 15 mm = 42.520 pt

KANGXI_RADICAL_RE = re.compile(r"[\u2e80-\u2eff\u2f00-\u2fdf]")
UNRENDERED_TEX_RE = re.compile(
    r"\\(?:frac|dfrac|tfrac|begin|end|ket|bra|braket|rangle|langle|otimes|"
    r"operatorname|mathbb|mathcal|mathrm|mathbf|sqrt|sum|prod|int)(?![A-Za-z])"
)

# Canonical Unicode CJK Unified Ideograph mapping for CJK Radicals Supplement (U+2E80..U+2EF3)
# per Unicode Consortium CJKRadicals.txt. All U+2F00..U+2FDF Kangxi Radicals normalize via NFKC.
CJK_RADICAL_SUPPLEMENT_MAP: dict[int, int] = {
    0x2E81: 0x5382, 0x2E82: 0x4E5B, 0x2E83: 0x4E5A, 0x2E84: 0x4E59, 0x2E85: 0x4EBB,
    0x2E86: 0x5182, 0x2E87: 0x51E0, 0x2E88: 0x5200, 0x2E89: 0x5202, 0x2E8A: 0x535C,
    0x2E8B: 0x353E, 0x2E8C: 0x5C0F, 0x2E8D: 0x5C0F, 0x2E8E: 0x5C22, 0x2E8F: 0x5C23,
    0x2E90: 0x5C22, 0x2E91: 0x5C23, 0x2E92: 0x5DF3, 0x2E93: 0x5E7A, 0x2E94: 0x5F51,
    0x2E95: 0x5F50, 0x2E96: 0x5FC4, 0x2E97: 0x5FC3, 0x2E98: 0x624C, 0x2E99: 0x6535,
    0x2E9B: 0x65E1, 0x2E9C: 0x65E5, 0x2E9D: 0x6708, 0x2E9E: 0x6B79, 0x2E9F: 0x6BCD,
    0x2EA0: 0x6C11, 0x2EA1: 0x6C35, 0x2EA2: 0x6C3A, 0x2EA3: 0x706C, 0x2EA4: 0x722B,
    0x2EA5: 0x722B, 0x2EA6: 0x4E2C, 0x2EA7: 0x725B, 0x2EA8: 0x72AD, 0x2EA9: 0x738B,
    0x2EAA: 0x758B, 0x2EAB: 0x76EE, 0x2EAC: 0x793A, 0x2EAD: 0x793B, 0x2EAE: 0x7AF9,
    0x2EAF: 0x7CF8, 0x2EB0: 0x7E9F, 0x2EB1: 0x7F53, 0x2EB2: 0x7F52, 0x2EB3: 0x7F51,
    0x2EB4: 0x7F51, 0x2EB5: 0x7F51, 0x2EB6: 0x7F8A, 0x2EB7: 0x7F8A, 0x2EB8: 0x7F8B,
    0x2EB9: 0x8002, 0x2EBA: 0x8080, 0x2EBB: 0x807F, 0x2EBC: 0x8089, 0x2EBD: 0x81FC,
    0x2EBE: 0x8279, 0x2EBF: 0x8279, 0x2EC0: 0x8279, 0x2EC1: 0x864E, 0x2EC2: 0x8864,
    0x2EC3: 0x897F, 0x2EC4: 0x897E, 0x2EC5: 0x89C1, 0x2EC6: 0x89D2, 0x2EC7: 0x89D2,
    0x2EC8: 0x8BA0, 0x2EC9: 0x8D1D, 0x2ECA: 0x8DB3, 0x2ECB: 0x8F66, 0x2ECC: 0x8FB6,
    0x2ECD: 0x8FB6, 0x2ECE: 0x8FB6, 0x2ECF: 0x9091, 0x2ED0: 0x9485, 0x2ED1: 0x9577,
    0x2ED2: 0x9578, 0x2ED3: 0x957F, 0x2ED4: 0x95E8, 0x2ED5: 0x961C, 0x2ED6: 0x961D,
    0x2ED7: 0x96E8, 0x2ED8: 0x9752, 0x2ED9: 0x97E6, 0x2EDA: 0x9875, 0x2EDB: 0x98CE,
    0x2EDC: 0x98DE, 0x2EDD: 0x98DF, 0x2EDE: 0x98E0, 0x2EDF: 0x98DF, 0x2EE0: 0x9963,
    0x2EE1: 0x9996, 0x2EE2: 0x9A6C, 0x2EE3: 0x9AA8, 0x2EE4: 0x9B3C, 0x2EE5: 0x9C7C,
    0x2EE6: 0x9E1F, 0x2EE7: 0x5364, 0x2EE8: 0x9EA6, 0x2EE9: 0x9EC4, 0x2EEA: 0x9EFE,
    0x2EEB: 0x6589, 0x2EEC: 0x9F50, 0x2EED: 0x9F7F, 0x2EEE: 0x9F99, 0x2EEF: 0x9F9F,
    0x2EF0: 0x9F99, 0x2EF1: 0x9F9C, 0x2EF2: 0x4E80, 0x2EF3: 0x9F9F,
}


def canonicalize_radical_cp(cp: int) -> int:
    """Map Kangxi Radical (U+2F00..U+2FDF) or CJK Radical Supplement (U+2E80..U+2EFF) to canonical CJK."""
    if 0x2F00 <= cp <= 0x2FDF:
        norm = unicodedata.normalize("NFKC", chr(cp))
        if len(norm) == 1:
            return ord(norm)
    if cp in CJK_RADICAL_SUPPLEMENT_MAP:
        return CJK_RADICAL_SUPPLEMENT_MAP[cp]
    return cp


def normalize_kangxi_tounicode_cmaps(doc: fitz.Document) -> dict:
    """Fix macOS CoreText/Skia Kangxi radical U+2E80..U+2FDF glitches in PDF /ToUnicode CMaps.

    SVG figures embedded by Chrome on macOS inherit CoreText's CMap mapping for shared
    Kangxi glyphs (e.g. 子 -> U+2F26, 一 -> U+2F00, 门 -> U+2ED4). Normalizing ONLY the
    /ToUnicode CMap tables preserves 100% bit-identical vector outlines while restoring
    canonical Unicode CJK Unified Ideographs for copy/paste, search, and accessibility.
    """
    bfchar_block_re = re.compile(r"(\d+\s+beginbfchar\b)([\s\S]*?)(\bendbfchar\b)")
    bfchar_pair_re = re.compile(r"(<[0-9A-Fa-f]+>\s*<)([0-9A-Fa-f]{4})(>)")
    bfrange_block_re = re.compile(r"(\d+\s+beginbfrange\b)([\s\S]*?)(\bendbfrange\b)")
    bfrange_line_re = re.compile(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]{4})>")
    bfrange_arr_re = re.compile(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[([^\]]+)\]")

    cmaps_scanned = 0
    cmaps_fixed = 0
    glyphs_fixed = 0

    for x in range(1, doc.xref_length()):
        if not doc.xref_is_stream(x):
            continue
        raw = doc.xref_stream(x)
        if not raw or b"begincmap" not in raw:
            continue
        cmaps_scanned += 1
        text = raw.decode("latin1", errors="ignore")
        if not any(tag in text for tag in ("<2E", "<2e", "<2F", "<2f")):
            # Fast-path check: also catch bfranges spanning into 2E80..2FDF
            if "beginbfrange" not in text:
                continue

        local_fixes = 0

        def fix_bfchar_block(bm: re.Match) -> str:
            nonlocal local_fixes
            def fix_pair(pm: re.Match) -> str:
                nonlocal local_fixes
                cp = int(pm.group(2), 16)
                new_cp = canonicalize_radical_cp(cp)
                if new_cp != cp:
                    local_fixes += 1
                    return f"{pm.group(1)}{new_cp:04X}{pm.group(3)}"
                return pm.group(0)
            return bm.group(1) + bfchar_pair_re.sub(fix_pair, bm.group(2)) + bm.group(3)

        new_text = bfchar_block_re.sub(fix_bfchar_block, text)

        if "beginbfrange" in new_text:
            def fix_bfrange_block(bm: re.Match) -> str:
                nonlocal local_fixes
                body = bm.group(2)
                # First normalize any array-style bfrange entries: <s1> <s2> [<u1> <u2> ...]
                def fix_arr(am: re.Match) -> str:
                    nonlocal local_fixes
                    def fix_u(um: re.Match) -> str:
                        nonlocal local_fixes
                        cp = int(um.group(1), 16)
                        new_cp = canonicalize_radical_cp(cp)
                        if new_cp != cp:
                            local_fixes += 1
                            return f"<{new_cp:04X}>"
                        return um.group(0)
                    return f"<{am.group(1)}> <{am.group(2)}> [" + re.sub(r"<([0-9A-Fa-f]{4})>", fix_u, am.group(3)) + "]"
                body = bfrange_arr_re.sub(fix_arr, body)

                # Expand linear bfranges <s1> <s2> <dst> ONLY if the destination range overlaps 0x2E80..0x2FDF
                def fix_lin(lm: re.Match) -> str:
                    nonlocal local_fixes
                    s1 = int(lm.group(1), 16)
                    s2 = int(lm.group(2), 16)
                    dst0 = int(lm.group(3), 16)
                    span = s2 - s1
                    if span < 0 or span > 512:
                        return lm.group(0)
                    dst1 = dst0 + span
                    if dst1 < 0x2E80 or dst0 > 0x2FDF:
                        return lm.group(0)
                    arr = []
                    for offset in range(span + 1):
                        cp = dst0 + offset
                        new_cp = canonicalize_radical_cp(cp)
                        if new_cp != cp:
                            local_fixes += 1
                        arr.append(f"<{new_cp:04X}>")
                    return f"<{lm.group(1)}> <{lm.group(2)}> [{' '.join(arr)}]"
                body = bfrange_line_re.sub(fix_lin, body)
                return bm.group(1) + body + bm.group(3)

            new_text = bfrange_block_re.sub(fix_bfrange_block, new_text)

        if local_fixes > 0:
            doc.update_stream(x, new_text.encode("latin1"))
            cmaps_fixed += 1
            glyphs_fixed += local_fixes

    return {
        "cmapsScanned": cmaps_scanned,
        "cmapsFixed": cmaps_fixed,
        "glyphsNormalized": glyphs_fixed,
    }


def clean_outline_title(raw: str) -> str:
    """Ensure bookmark titles are crisp single-line Unicode with no HTML/TeX noise."""
    text = re.sub(r"<[^>]+>", "", raw or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_for_match(text: str) -> str:
    """Normalize text for resilient heading-to-page fallback matching."""
    cleaned = re.sub(r"[\s\u00a0\u200b\u200c\u200d·•|｜:：—–\-_.,，。！？()（）\[\]【】]", "", text or "")
    return cleaned.lower()


def extract_chunk_named_dests(
    c_doc: fitz.Document,
    page_offset_0: int,
    dest_map: dict[str, dict],
) -> int:
    """Extract all Named Destinations from an open chunk Document, shifted by page_offset_0."""
    n_pages = len(c_doc)
    named = c_doc.resolve_names()
    for key, val in named.items():
        if not isinstance(val, dict) or not isinstance(val.get("page"), int) or val["page"] < 0:
            continue
        local_p0 = val["page"]
        if local_p0 >= n_pages:
            continue
        y_top: float | None = None
        if isinstance(val.get("to"), (tuple, list)) and len(val["to"]) >= 2:
            page_h = float(c_doc[local_p0].rect.height)
            raw_y = float(val["to"][1])
            y_top = max(0.0, min(page_h - 12.0, page_h - raw_y))
        entry = {
            "page": page_offset_0 + local_p0,
            "y_top": y_top,
            "to": val.get("to"),
        }
        norm_key = key[1:] if key.startswith("/") else key
        dest_map[norm_key] = entry
        dest_map["/" + norm_key] = entry
        decoded = urllib.parse.unquote(norm_key)
        if decoded != norm_key:
            dest_map[decoded] = entry
    return n_pages


def probe_body_chunk_pages(probe_json_path: Path) -> dict:
    """Scan ordered body chunk PDFs and return 1-based printed body page numbers per anchor."""
    payload = json.loads(probe_json_path.read_text(encoding="utf-8"))
    chunk_paths = [Path(p) for p in payload.get("chunks", [])]
    dest_map: dict[str, dict] = {}
    running_pages = 0
    chunk_page_counts: list[dict] = []

    for c_path in chunk_paths:
        c_doc = fitz.open(str(c_path))
        try:
            n_pages = extract_chunk_named_dests(c_doc, running_pages, dest_map)
        finally:
            c_doc.close()
        chunk_page_counts.append({"file": c_path.name, "startBodyPage1": running_pages + 1, "pages": n_pages})
        running_pages += n_pages

    page_numbers: dict[str, int] = {}
    for key, val in dest_map.items():
        if key.startswith("/"):
            continue
        p0 = val.get("page")
        if isinstance(p0, int) and p0 >= 0:
            page_numbers[key] = p0 + 1

    return {
        "totalBodyPages": running_pages,
        "chunks": chunk_page_counts,
        "pageNumbers": page_numbers,
    }


def merge_cover_and_chunks_fitz(
    cover_path: Path,
    chunk_paths: list[Path],
) -> tuple[fitz.Document, dict, dict[str, dict]]:
    """Merge cover.pdf + ordered chunk PDFs via MuPDF insert_pdf."""
    if not chunk_paths:
        raise RuntimeError("No body/chunk PDFs provided for merge")

    cover_doc = fitz.open(str(cover_path))
    cover_pages = len(cover_doc)
    if cover_pages < 1:
        cover_doc.close()
        raise RuntimeError(f"Cover PDF has no pages: {cover_path}")

    for c_path in chunk_paths:
        if not c_path.exists():
            cover_doc.close()
            raise RuntimeError(f"Missing chunk PDF: {c_path}")

    global_dest_map: dict[str, dict] = {}
    chunk_offsets: list[dict] = []
    running_body_pages = 0

    # Start from chunk 0 (keeps its /StructTreeRoot & /MarkInfo /Marked true),
    # insert cover at index 0, then append remaining chunks in exact reading order.
    doc = fitz.open(str(chunk_paths[0]))
    n0 = extract_chunk_named_dests(doc, cover_pages, global_dest_map)
    if n0 < 1:
        doc.close()
        cover_doc.close()
        raise RuntimeError(f"Chunk PDF has no pages: {chunk_paths[0]}")
    chunk_offsets.append({
        "file": chunk_paths[0].name,
        "startPage1": cover_pages + 1,
        "pages": n0,
    })
    running_body_pages += n0

    doc.insert_pdf(cover_doc, start_at=0)
    cover_doc.close()

    for c_path in chunk_paths[1:]:
        page_offset_0 = cover_pages + running_body_pages
        c_doc = fitz.open(str(c_path))
        n_pages = extract_chunk_named_dests(c_doc, page_offset_0, global_dest_map)
        if n_pages < 1:
            c_doc.close()
            doc.close()
            raise RuntimeError(f"Chunk PDF has no pages: {c_path}")
        doc.insert_pdf(c_doc)
        c_doc.close()
        chunk_offsets.append({
            "file": c_path.name,
            "startPage1": page_offset_0 + 1,
            "pages": n_pages,
        })
        running_body_pages += n_pages

    merge_info = {
        "coverPages": cover_pages,
        "bodyPages": running_body_pages,
        "mergedPages": cover_pages + running_body_pages,
        "chunkCount": len(chunk_paths),
        "chunkOffsets": chunk_offsets,
    }
    return doc, merge_info, global_dest_map


def merge_cover_and_body_legacy(
    cover_path: Path,
    body_path: Path,
    merged_tmp: Path,
) -> tuple[fitz.Document, dict, dict[str, dict]]:
    """Legacy monolithic merge via pypdf for --body mode."""
    cover_reader = PdfReader(str(cover_path))
    body_reader = PdfReader(str(body_path))
    cover_pages = len(cover_reader.pages)
    body_pages = len(body_reader.pages)
    if cover_pages < 1 or body_pages < 1:
        raise RuntimeError("Cover or body PDF has no pages")

    writer = PdfWriter(clone_from=body_reader)
    writer.merge(position=0, fileobj=cover_reader)
    with open(merged_tmp, "wb") as fh:
        writer.write(fh)

    doc = fitz.open(str(merged_tmp))
    merge_info = {
        "coverPages": cover_pages,
        "bodyPages": body_pages,
        "mergedPages": cover_pages + body_pages,
        "chunkCount": 1,
    }
    return doc, merge_info, {}


def _rewrite_non_stream_refs(doc: fitz.Document, remap: dict[int, int]) -> int:
    """Rewrite indirect references in non-stream PDF objects according to remap."""
    if not remap:
        return 0
    n_xref = doc.xref_length()
    token_re = re.compile(r"\((?:\\.|[^\\()]|\((?:\\.|[^\\()])*\))*\)|\b(\d+)\s+0\s+R\b")
    rewritten = 0

    for x in range(1, n_xref):
        if x in remap or doc.xref_is_stream(x):
            continue
        obj = doc.xref_object(x, compressed=True)
        if " 0 R" not in obj:
            continue
        changed = False

        def _repl(m: re.Match) -> str:
            nonlocal changed
            g = m.group(1)
            if g is None:
                return m.group(0)
            target = remap.get(int(g))
            if target is not None:
                changed = True
                return f"{target} 0 R"
            return m.group(0)

        new_obj = token_re.sub(_repl, obj)
        if changed:
            doc.update_object(x, new_obj)
            rewritten += 1
    return rewritten


def deduplicate_identical_streams(doc: fitz.Document) -> dict:
    """Two-stage O(N) blake2b deduplication of leaf streams and Image/SMask XObject streams.

    Stage 1 deduplicates pure leaf streams (Type3 CharProcs, standalone SMasks, CMaps,
    standalone Images) and canonicalizes /SMask references inside Image XObjects safely
    via xref_set_key (without detaching stream payloads).
    Stage 2 deduplicates identical /Subtype /Image XObjects (including those referencing
    canonicalized /SMask streams) and rewrites non-stream XObject resource references.
    """
    n_xref = doc.xref_length()
    len_re = re.compile(r"/Length\s+\d+")

    # Stage 1: pure leaf streams (no indirect references in dictionary)
    canon_leaf: dict[bytes, int] = {}
    remap_leaf: dict[int, int] = {}
    for x in range(1, n_xref):
        if not doc.xref_is_stream(x):
            continue
        obj = doc.xref_object(x, compressed=True)
        if (
            " 0 R" in obj
            or "/Type/XRef" in obj
            or "/Type /XRef" in obj
            or "/Type/ObjStm" in obj
            or "/Type /ObjStm" in obj
        ):
            continue
        raw = doc.xref_stream_raw(x)
        if raw is None:
            continue
        norm_dict = len_re.sub("", obj)
        sig = hashlib.blake2b(norm_dict.encode("latin1", errors="ignore") + b"\0" + raw, digest_size=16).digest()
        existing = canon_leaf.get(sig)
        if existing is not None:
            remap_leaf[x] = existing
        else:
            canon_leaf[sig] = x

    rewritten_leaf = _rewrite_non_stream_refs(doc, remap_leaf)

    # Safely update /SMask indirect references on Image XObjects to canonical Stage-1 SMasks
    smask_rebound = 0
    if remap_leaf:
        for x in range(1, n_xref):
            if x in remap_leaf or not doc.xref_is_stream(x):
                continue
            sm_type, sm_val = doc.xref_get_key(x, "SMask")
            if sm_type == "xref":
                sm_xref = int(sm_val.split()[0])
                target = remap_leaf.get(sm_xref)
                if target is not None:
                    doc.xref_set_key(x, "SMask", f"{target} 0 R")
                    smask_rebound += 1

    # Stage 2: deduplicate Image XObject streams (including those carrying /SMask refs)
    canon_img: dict[bytes, int] = {}
    remap_img: dict[int, int] = {}
    for x in range(1, n_xref):
        if x in remap_leaf or not doc.xref_is_stream(x):
            continue
        st_type, st_val = doc.xref_get_key(x, "Subtype")
        if st_val != "/Image":
            continue
        obj = doc.xref_object(x, compressed=True)
        raw = doc.xref_stream_raw(x)
        if raw is None:
            continue
        norm_dict = len_re.sub("", obj)
        sig = hashlib.blake2b(norm_dict.encode("latin1", errors="ignore") + b"\0" + raw, digest_size=16).digest()
        existing = canon_img.get(sig)
        if existing is not None:
            remap_img[x] = existing
        else:
            canon_img[sig] = x

    rewritten_img = _rewrite_non_stream_refs(doc, remap_img)

    return {
        "uniqueStreams": len(canon_leaf),
        "dedupedStreams": len(remap_leaf),
        "rewrittenObjects": rewritten_leaf,
        "smaskRebound": smask_rebound,
        "uniqueImages": len(canon_img),
        "dedupedImages": len(remap_img),
        "rewrittenImageRefs": rewritten_img,
    }


def count_embedded_fonts(doc: fitz.Document) -> dict:
    """Count distinct embedded font stream xrefs and unique page font references."""
    font_stream_xrefs: set[int] = set()
    page_font_xrefs: set[int] = set()
    font_stream_bytes = 0
    for x in range(1, doc.xref_length()):
        if not doc.xref_is_stream(x):
            continue
        obj = doc.xref_object(x, compressed=True)
        if "/Length1" in obj or "/Subtype/CIDFontType0C" in obj or "/Subtype /CIDFontType0C" in obj or "/Subtype/OpenType" in obj or "/Subtype /OpenType" in obj:
            raw = doc.xref_stream_raw(x) or b""
            font_stream_xrefs.add(x)
            font_stream_bytes += len(raw)
    for page in doc:
        for f in page.get_fonts(full=True):
            page_font_xrefs.add(int(f[0]))
    return {
        "embeddedFontStreams": len(font_stream_xrefs),
        "embeddedFontBytes": font_stream_bytes,
        "embeddedFontMiB": round(font_stream_bytes / (1024 * 1024), 3),
        "uniquePageFontRefs": len(page_font_xrefs),
    }


def stamp_running_headers_and_footers(
    doc: fitz.Document,
    body_start_0: int,
    skip_pages_0: set[int],
    edition: str,
) -> int:
    """Stamp crisp hairline running header & 0-offset page footer on regular body pages.

    Skips cover, TOC (@page toc), and part divider (@page part) pages completely while
    maintaining continuous 1-based printed Arabic page numbers starting at body_start_0
    so footer '第 N 页' matches /PageLabels and printed TOC page numbers with 0 offset.
    """
    total_pages = len(doc)
    body_total = total_pages - body_start_0
    if body_total <= 0:
        return 0

    # Shared Type0 / CIDFontType0 / FontDescriptor (matches PyMuPDF built-in china-ss, 0-byte font stream)
    fd_xref = doc.get_new_xref()
    doc.update_object(
        fd_xref,
        "<</Type/FontDescriptor/FontName(Song)/FontBBox[-200 -200 1200 1200]"
        "/Flags 6/ItalicAngle 0/Ascent 1000/Descent -200/StemV 80>>",
    )
    cid_xref = doc.get_new_xref()
    doc.update_object(
        cid_xref,
        f"<</Type/Font/Subtype/CIDFontType0/BaseFont/Song"
        f"/CIDSystemInfo<</Registry(Adobe)/Ordering(GB1)/Supplement 5>>"
        f"/FontDescriptor {fd_xref} 0 R/DW 1000/W[1 95 500]>>",
    )
    font_xref = doc.get_new_xref()
    doc.update_object(
        font_xref,
        f"<</Type/Font/Subtype/Type0/BaseFont/Song/Encoding/UniGB-UTF16-H"
        f"/DescendantFonts[{cid_xref} 0 R]>>",
    )

    # Shared q / Q streams isolate Chrome's page graphics state without parsing its content stream
    q_xref = doc.get_new_xref()
    doc.update_object(q_xref, "<<>>")
    doc.update_stream(q_xref, b"q\n")
    Q_xref = doc.get_new_xref()
    doc.update_object(Q_xref, "<<>>")
    doc.update_stream(Q_xref, b"\nQ\n")

    right_label = f"{edition} 版" if edition else "离线精排本"
    # Exact Song CIDFont advance width matching /DW 1000 and /W[1 95 500] (0.5em ASCII, 1.0em CJK)
    def song_width(s: str, fs: float = 7.4) -> float:
        return sum(0.5 if ord(ch) < 128 else 1.0 for ch in s) * fs

    right_w = song_width(right_label, 7.4)
    left_hex = BOOK_HEADER_LEFT.encode("utf-16-be").hex().upper()
    right_hex = right_label.encode("utf-16-be").hex().upper()

    rr, rg, rb = HEADER_RULE_COLOR
    tr, tg, tb = HEADER_TEXT_COLOR
    stamped = 0

    for idx in range(body_start_0, total_pages):
        if idx in skip_pages_0:
            continue
        page = doc[idx]
        pw = float(page.rect.width)
        ph = float(page.rect.height)
        body_num = idx - body_start_0 + 1
        footer_label = f"第 {body_num} 页 / 共 {body_total} 页"
        footer_w = song_width(footer_label, 7.4)
        footer_hex = footer_label.encode("utf-16-be").hex().upper()

        # Register /F_QCH_HF in page /Resources/Font (handles indirect or inline Resources/Font dicts)
        res_type, res_val = doc.xref_get_key(page.xref, "Resources")
        if res_type == "xref":
            res_xref = int(res_val.split()[0])
            ft_type, ft_val = doc.xref_get_key(res_xref, "Font")
            if ft_type == "xref":
                doc.xref_set_key(int(ft_val.split()[0]), "F_QCH_HF", f"{font_xref} 0 R")
            else:
                doc.xref_set_key(res_xref, "Font/F_QCH_HF", f"{font_xref} 0 R")
        else:
            ft_type, ft_val = doc.xref_get_key(page.xref, "Resources/Font")
            if ft_type == "xref":
                doc.xref_set_key(int(ft_val.split()[0]), "F_QCH_HF", f"{font_xref} 0 R")
            else:
                doc.xref_set_key(page.xref, "Resources/Font/F_QCH_HF", f"{font_xref} 0 R")

        # PDF coordinates are bottom-up: top/bottom margin band is 17.5mm = 49.61 pt
        header_rule_y = ph - 33.5
        header_text_y = ph - 29.0
        footer_rule_y = 33.5
        footer_text_y = 22.5
        right_x = pw - MARGIN_X_PT - right_w
        footer_x = (pw - footer_w) / 2.0

        overlay_stream = (
            f"q\n"
            f"{rr:.4f} {rg:.4f} {rb:.4f} RG 0.5 w\n"
            f"{MARGIN_X_PT:.2f} {header_rule_y:.2f} m {pw - MARGIN_X_PT:.2f} {header_rule_y:.2f} l S\n"
            f"{MARGIN_X_PT:.2f} {footer_rule_y:.2f} m {pw - MARGIN_X_PT:.2f} {footer_rule_y:.2f} l S\n"
            f"{tr:.4f} {tg:.4f} {tb:.4f} rg\n"
            f"BT /F_QCH_HF 7.4 Tf 1 0 0 1 {MARGIN_X_PT:.2f} {header_text_y:.2f} Tm <{left_hex}> Tj ET\n"
            f"BT /F_QCH_HF 7.4 Tf 1 0 0 1 {right_x:.2f} {header_text_y:.2f} Tm <{right_hex}> Tj ET\n"
            f"BT /F_QCH_HF 7.4 Tf 1 0 0 1 {footer_x:.2f} {footer_text_y:.2f} Tm <{footer_hex}> Tj ET\n"
            f"Q\n"
        ).encode("ascii")

        ov_xref = doc.get_new_xref()
        doc.update_object(ov_xref, "<<>>")
        doc.update_stream(ov_xref, overlay_stream)

        ct_type, ct_val = doc.xref_get_key(page.xref, "Contents")
        if ct_type == "xref":
            doc.xref_set_key(page.xref, "Contents", f"[{q_xref} 0 R {ct_val} {Q_xref} 0 R {ov_xref} 0 R]")
        elif ct_type == "array":
            inner = ct_val.strip()[1:-1].strip()
            doc.xref_set_key(page.xref, "Contents", f"[{q_xref} 0 R {inner} {Q_xref} 0 R {ov_xref} 0 R]")
        else:
            doc.xref_set_key(page.xref, "Contents", f"[{ov_xref} 0 R]")
        stamped += 1

    return stamped


def rewrite_internal_sentinel_links(
    doc: fitz.Document,
    dest_map: dict[str, dict],
    cross_prefix: str,
    toc_pages_0: set[int],
) -> dict:
    """Convert sentinel TOC & internal URI links into real internal PDF GoTo links."""
    resolved = 0
    toc_resolved = 0
    dropped = 0
    total_pages = len(doc)

    for p0 in range(total_pages):
        page = doc[p0]
        links = page.get_links()
        if not links:
            continue
        for link in links:
            if link.get("kind") != fitz.LINK_URI:
                continue
            uri = link.get("uri") or ""
            if not uri.startswith(cross_prefix):
                continue
            raw_target = uri[len(cross_prefix):]
            target_id = urllib.parse.unquote(raw_target)
            rect = fitz.Rect(link["from"])
            page.delete_link(link)

            info = dest_map.get(target_id)
            if info is None and "--" in target_id:
                info = dest_map.get(target_id.split("--", 1)[0])
            if info is not None and 0 <= info["page"] < total_pages:
                y_dest = float(info["y_top"]) if info.get("y_top") is not None else 0.0
                page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "from": rect,
                    "page": int(info["page"]),
                    "to": fitz.Point(0.0, y_dest),
                })
                resolved += 1
                if p0 in toc_pages_0:
                    toc_resolved += 1
            else:
                dropped += 1

    return {
        "resolved": resolved,
        "tocResolved": toc_resolved,
        "dropped": dropped,
    }


def resolve_outline_entries(
    doc: fitz.Document,
    manifest: dict,
    cover_pages: int,
    chunk_dest_map: dict[str, dict] | None = None,
) -> tuple[list[list], dict]:
    """Build PyMuPDF 3-level TOC list using chunk Named Destinations + doc names + text fallback."""
    dest_map: dict[str, dict] = {}
    for key, val in doc.resolve_names().items():
        if isinstance(val, dict) and isinstance(val.get("page"), int) and val["page"] >= 0:
            p0 = val["page"]
            y_top: float | None = None
            if p0 < len(doc) and isinstance(val.get("to"), (tuple, list)) and len(val["to"]) >= 2:
                page_h = float(doc[p0].rect.height)
                y_top = max(0.0, min(page_h - 12.0, page_h - float(val["to"][1])))
            entry = {"page": p0, "y_top": y_top, "to": val.get("to")}
            norm_key = key[1:] if key.startswith("/") else key
            dest_map[norm_key] = entry
            dest_map["/" + norm_key] = entry

    if chunk_dest_map:
        dest_map.update(chunk_dest_map)

    page_texts_norm: list[str] | None = None

    def ensure_page_texts() -> list[str]:
        nonlocal page_texts_norm
        if page_texts_norm is None:
            page_texts_norm = [normalize_for_match(p.get_text("text")) for p in doc]
        return page_texts_norm

    def locate_anchor(
        anchor_id: str,
        title: str,
        min_page_1: int,
        use_y: bool,
    ) -> tuple[int, float | None, str]:
        info = dest_map.get(anchor_id)
        if info is not None and isinstance(info.get("page"), int) and 0 <= info["page"] < len(doc):
            p1 = info["page"] + 1
            y_top = info.get("y_top") if use_y else None
            return p1, y_top, "named_dest"

        needle = normalize_for_match(title)
        texts = ensure_page_texts()
        if needle:
            start_idx = max(cover_pages, min_page_1 - 1)
            for idx in range(start_idx, len(texts)):
                if needle in texts[idx]:
                    return idx + 1, None, "text_match"
            short_needle = needle[:16]
            if len(short_needle) >= 5:
                for idx in range(start_idx, len(texts)):
                    if short_needle in texts[idx]:
                        return idx + 1, None, "text_prefix"

        return max(cover_pages + 1, min_page_1), None, "fallback_cursor"

    toc: list[list] = []
    stats = {
        "namedDestHits": 0,
        "textMatchHits": 0,
        "fallbackCursorHits": 0,
        "level1": 0,
        "level2": 0,
        "level3": 0,
        "chapterPages": {},
        "partPages": [],
    }

    toc.append([1, "封面 · 量子计算手册", 1])
    stats["level1"] += 1

    toc_page_num, _, _ = locate_anchor("toc-page", "全书目录", cover_pages + 1, use_y=False)
    toc.append([1, "目录", toc_page_num])
    stats["level1"] += 1

    cursor_page = toc_page_num

    front = manifest.get("frontmatter")
    if front and front.get("id"):
        fm_title = clean_outline_title(front.get("title", "导读与统一约定"))
        p1, _, src = locate_anchor(front["id"], fm_title, cursor_page, use_y=False)
        toc.append([1, fm_title, p1])
        stats["level1"] += 1
        cursor_page = max(cursor_page, p1)
        if src == "named_dest":
            stats["namedDestHits"] += 1
        elif src.startswith("text_"):
            stats["textMatchHits"] += 1
        else:
            stats["fallbackCursorHits"] += 1

        fm_cursor = p1
        for sec in front.get("sections", []):
            sec_title = clean_outline_title(sec.get("title", ""))
            sec_id = sec.get("id", "")
            if not sec_title:
                continue
            sec_page, sec_y, sec_src = locate_anchor(sec_id, sec_title, fm_cursor, use_y=True)
            if sec_y is not None:
                toc.append([2, sec_title, sec_page, sec_y])
            else:
                toc.append([2, sec_title, sec_page])
            stats["level2"] += 1
            fm_cursor = max(fm_cursor, sec_page)
            if sec_src == "named_dest":
                stats["namedDestHits"] += 1
            elif sec_src.startswith("text_"):
                stats["textMatchHits"] += 1
            else:
                stats["fallbackCursorHits"] += 1

    for part in manifest.get("parts", []):
        part_title = clean_outline_title(part.get("title", ""))
        part_id = part.get("id", "")
        part_page, _, src = locate_anchor(part_id, part_title, cursor_page, use_y=False)
        toc.append([1, part_title, part_page])
        stats["level1"] += 1
        stats["partPages"].append(part_page)
        cursor_page = max(cursor_page, part_page)
        if src == "named_dest":
            stats["namedDestHits"] += 1
        elif src.startswith("text_"):
            stats["textMatchHits"] += 1
        else:
            stats["fallbackCursorHits"] += 1

        for ch in part.get("chapters", []):
            ch_title = clean_outline_title(ch.get("title", ""))
            ch_id = ch.get("id", "")
            ch_page, _, ch_src = locate_anchor(ch_id, ch_title, cursor_page, use_y=False)
            toc.append([2, ch_title, ch_page])
            stats["level2"] += 1
            cursor_page = max(cursor_page, ch_page)
            stats["chapterPages"][ch_id] = ch_page
            if ch_src == "named_dest":
                stats["namedDestHits"] += 1
            elif ch_src.startswith("text_"):
                stats["textMatchHits"] += 1
            else:
                stats["fallbackCursorHits"] += 1

            sec_cursor = ch_page
            for sec in ch.get("sections", []):
                sec_title = clean_outline_title(sec.get("title", ""))
                sec_id = sec.get("id", "")
                if not sec_title:
                    continue
                sec_page, sec_y, sec_src = locate_anchor(sec_id, sec_title, sec_cursor, use_y=True)
                if sec_y is not None:
                    toc.append([3, sec_title, sec_page, sec_y])
                else:
                    toc.append([3, sec_title, sec_page])
                stats["level3"] += 1
                sec_cursor = max(sec_cursor, sec_page)
                if sec_src == "named_dest":
                    stats["namedDestHits"] += 1
                elif sec_src.startswith("text_"):
                    stats["textMatchHits"] += 1
                else:
                    stats["fallbackCursorHits"] += 1

    return toc, stats


def pick_sample_pages(doc: fitz.Document, chapter_pages: dict[str, int]) -> dict[str, int]:
    """Select 4 representative 1-based page numbers for visual preview PNGs."""
    total = len(doc)
    cover_p = 1
    toc_p = min(2, total)

    sample1_p = min(15, total)
    candidate_ids = ["ch-02", "ch-20", "ch-03", "ch-q1", "ch-01"]
    for cid in candidate_ids:
        start_p = chapter_pages.get(cid)
        if not start_p:
            continue
        best_score = -1
        best_p = start_p
        end_p = min(total, start_p + 12)
        for p1 in range(start_p, end_p + 1):
            page = doc[p1 - 1]
            txt = page.get_text("text")
            drawings = len(page.get_drawings())
            images = len(page.get_images())
            score = min(drawings, 250) + images * 40 + (60 if len(txt.strip()) > 300 else 0)
            if score > best_score:
                best_score = score
                best_p = p1
        sample1_p = best_p
        break

    sample2_p = min(max(total - 10, 3), total)
    for cid in ["app-exercises", "app-notation", "lab-foundations"]:
        if cid in chapter_pages:
            sample2_p = min(total, chapter_pages[cid] + 1)
            break

    return {
        "cover": cover_p,
        "toc": toc_p,
        "sample1": sample1_p,
        "sample2": sample2_p,
    }


def render_previews(doc: fitz.Document, preview_pages: dict[str, int], preview_dir: Path, dpi: int = 150) -> dict[str, dict]:
    """Render 4 sample PNG previews at 150 DPI for manual visual QA."""
    preview_dir.mkdir(parents=True, exist_ok=True)
    mapping = {
        "cover": "pdf-preview-cover.png",
        "toc": "pdf-preview-toc.png",
        "sample1": "pdf-preview-sample1.png",
        "sample2": "pdf-preview-sample2.png",
    }
    rendered: dict[str, dict] = {}
    matrix = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    for key, filename in mapping.items():
        p1 = preview_pages[key]
        out_path = preview_dir / filename
        pix = doc[p1 - 1].get_pixmap(matrix=matrix, alpha=False)
        pix.save(str(out_path))
        rendered[key] = {
            "page": p1,
            "file": str(out_path.relative_to(REPO_ROOT)) if out_path.is_relative_to(REPO_ROOT) else str(out_path),
            "width": pix.width,
            "height": pix.height,
            "dpi": dpi,
        }
    return rendered


def run_qa_audit(
    final_pdf: Path,
    manifest: dict,
    outline_stats: dict,
    merge_info: dict,
    link_stats: dict,
    dedup_stats: dict,
    subset_stats: dict,
    headers_stamped: int,
    body_start_0: int,
    toc_pages_0: set[int],
    part_pages_0: set[int],
    dest_map: dict[str, dict],
    timings: dict,
    preview_dir: Path,
) -> dict:
    """Execute full PDF publication quality-assurance checks via PyMuPDF + pypdf."""
    file_bytes = final_pdf.stat().st_size
    file_mib = round(file_bytes / (1024 * 1024), 3)

    pypdf_reader = PdfReader(str(final_pdf))
    root = pypdf_reader.trailer["/Root"]
    mark_info = root.get("/MarkInfo")
    if mark_info is not None and hasattr(mark_info, "get_object"):
        mark_info = mark_info.get_object()
    marked_val = mark_info.get("/Marked") if isinstance(mark_info, dict) else None
    if marked_val is not None and hasattr(marked_val, "get_object"):
        marked_val = marked_val.get_object()
    marked_true = (isinstance(marked_val, BooleanObject) and marked_val.value is True) or (marked_val is True)
    st_root = root.get("/StructTreeRoot")
    if st_root is not None and hasattr(st_root, "get_object"):
        st_root = st_root.get_object()
    has_struct_tree = isinstance(st_root, dict)
    pdf_lang = str(root.get("/Lang", ""))
    struct_parents_pages = sum(1 for p in pypdf_reader.pages if "/StructParents" in p)

    doc = fitz.open(str(final_pdf))
    total_pages = len(doc)
    struct_parents_coverage_ratio = round(struct_parents_pages / total_pages, 4) if total_pages > 0 else 0.0
    toc = doc.get_toc(simple=True)
    outline_count = len(toc)
    font_stats = count_embedded_fonts(doc)
    page_labels_raw = doc.get_page_labels()

    part_pages_1 = {p0 + 1 for p0 in part_pages_0}
    part_pages_1.update(outline_stats.get("partPages", []))

    cross_prefix = manifest.get("crossLinkPrefix", DEFAULT_CROSS_LINK_PREFIX)
    kangxi_hits: list[dict] = []
    blank_pages: list[int] = []
    sparse_pages: list[dict] = []
    overflow_samples: list[dict] = []
    prose_font_sizes: list[float] = []
    unrendered_tex_pages: list[dict] = []
    residual_sentinel_links = 0
    footer_mismatches: list[dict] = []
    suppressed_header_leaks: list[int] = []
    footer_num_re = re.compile(r"第\s*(\d+)\s*页\s*/\s*共\s*(\d+)\s*页")
    raw_tex_bookmarks = [
        item[1] for item in toc
        if "$" in item[1] or UNRENDERED_TEX_RE.search(item[1])
    ]

    sample_step = max(1, total_pages // 80)
    for idx in range(total_pages):
        p1 = idx + 1
        page = doc[idx]
        pw = float(page.rect.width)
        ph = float(page.rect.height)
        text = page.get_text("text") or ""

        for lk in page.get_links():
            if lk.get("kind") == fitz.LINK_URI and (lk.get("uri") or "").startswith(cross_prefix):
                residual_sentinel_links += 1

        # Verify running header/footer suppression on TOC & Part Divider pages
        if idx in toc_pages_0 or idx in part_pages_0:
            if footer_num_re.search(text) or BOOK_HEADER_LEFT in text:
                suppressed_header_leaks.append(p1)
        elif idx >= body_start_0 and (idx == body_start_0 or idx == total_pages - 1 or idx % sample_step == 0):
            m_ft = footer_num_re.search(text)
            lbl = page.get_label()
            expected_num = idx - body_start_0 + 1
            if not m_ft or int(m_ft.group(1)) != expected_num or lbl != str(expected_num):
                if len(footer_mismatches) < 10:
                    footer_mismatches.append({
                        "physicalPage": p1,
                        "expected": expected_num,
                        "pageLabel": lbl,
                        "footer": m_ft.group(0) if m_ft else None,
                    })

        # 1. CJK Kangxi radical check across EVERY page (including running headers/footers)
        radicals = KANGXI_RADICAL_RE.findall(text)
        if radicals:
            kangxi_hits.append({
                "page": p1,
                "count": len(radicals),
                "codepoints": sorted({f"U+{ord(ch):04X}" for ch in radicals})[:10],
            })

        # 2. Honest blank / orphan page detection inside the body content area (excluding header/footer bands)
        if p1 > merge_info["coverPages"]:
            total_non_ws = len(re.sub(r"\s+", "", text))
            if total_non_ws < 120:
                body_clip = fitz.Rect(0.0, 37.0, pw, ph - 37.0)
                body_text = page.get_text("text", clip=body_clip) or ""
                body_non_ws = len(re.sub(r"\s+", "", body_text))
                if body_non_ws < 45:
                    images_n = len(page.get_images())
                    drawings_n = max(0, len(page.get_drawings()) - 2)
                    if body_non_ws < 20 and images_n == 0 and drawings_n < 5:
                        blank_pages.append(p1)
                    elif p1 not in part_pages_1 and images_n == 0 and drawings_n < 8:
                        sparse_pages.append({
                            "page": p1,
                            "chars": body_non_ws,
                            "images": images_n,
                            "drawings": drawings_n,
                        })

        # 3. Font readability & right margin overflow probe
        if idx % sample_step == 0:
            margin_limit = pw - 20.0
            page_dict = page.get_text("dict")
            for block in page_dict.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        stext = (span.get("text") or "").strip()
                        sz = float(span.get("size", 0.0))
                        bbox = span.get("bbox", (0, 0, 0, 0))
                        if bbox[1] >= 37.0 and bbox[3] <= ph - 37.0:
                            cjk_len = len(re.findall(r"[\u4e00-\u9fff]", stext))
                            if cjk_len >= 6 and 7.0 <= sz <= 13.0:
                                prose_font_sizes.append(round(sz, 2))
                        if len(stext) >= 3 and bbox[2] > margin_limit and len(overflow_samples) < 20:
                            overflow_samples.append({
                                "page": p1,
                                "x1": round(bbox[2], 1),
                                "pageWidth": round(pw, 1),
                                "text": stext[:40],
                            })

        if "$$" in text and "\\documentclass" not in text and "katex" not in text.lower():
            if len(unrendered_tex_pages) < 15:
                unrendered_tex_pages.append({"page": p1, "hint": "$$"})

    # 4. Verify TOC printed page-number coverage and 0-offset alignment against merged GoTo targets
    toc_entries = manifest.get("tocEntries") or []
    toc_text_all = "\n".join((doc[p0].get_text("text") or "") for p0 in sorted(toc_pages_0) if 0 <= p0 < total_pages)
    toc_total = len(toc_entries)
    toc_numbered = 0
    toc_aligned = 0
    toc_mismatches: list[dict] = []
    for entry in toc_entries:
        p_printed = entry.get("printedPage")
        aid = entry.get("id", "")
        if isinstance(p_printed, int) and p_printed > 0:
            toc_numbered += 1
            info = dest_map.get(aid)
            actual_logical = (int(info["page"]) - body_start_0 + 1) if info and isinstance(info.get("page"), int) else None
            if actual_logical == p_printed and str(p_printed) in toc_text_all:
                toc_aligned += 1
            elif len(toc_mismatches) < 10:
                toc_mismatches.append({
                    "id": aid,
                    "printedPage": p_printed,
                    "actualLogicalPage": actual_logical,
                })
    toc_coverage_pct = round(100.0 * toc_aligned / toc_total, 2) if toc_total > 0 else 0.0

    # Verify /PageLabels sample labels (Cover / i / 1)
    cover_label_ok = total_pages > 0 and doc[0].get_label() == "Cover"
    toc_label_ok = (not toc_pages_0) or (min(toc_pages_0) < total_pages and doc[min(toc_pages_0)].get_label() == "i")
    body_label_ok = body_start_0 < total_pages and doc[body_start_0].get_label() == "1"
    page_labels_ok = cover_label_ok and toc_label_ok and body_label_ok

    last_page_text = doc[-1].get_text("text") if total_pages > 0 else ""
    has_end_sentinel = "全书完" in last_page_text

    median_body_pt = round(statistics.median(prose_font_sizes), 2) if prose_font_sizes else 0.0
    p10_body_pt = (
        round(sorted(prose_font_sizes)[max(0, int(len(prose_font_sizes) * 0.10))], 2)
        if prose_font_sizes
        else 0.0
    )

    preview_pages = pick_sample_pages(doc, outline_stats.get("chapterPages", {}))
    previews = render_previews(doc, preview_pages, preview_dir, dpi=150)

    metadata = doc.metadata or {}
    doc.close()

    kangxi_total = sum(h["count"] for h in kangxi_hits)
    has_all_3_outline_levels = (
        outline_stats["level1"] > 0
        and outline_stats["level2"] > 0
        and outline_stats["level3"] > 0
    )
    metadata_title = (metadata.get("title") or "").strip()
    metadata_author = (metadata.get("author") or "").strip()
    checks = {
        "fileUnder50MiB": file_mib < 50.0,
        "outlineOver100": outline_count > 100,
        "outlineHasAll3Levels": has_all_3_outline_levels,
        "outlineZeroRawTex": len(raw_tex_bookmarks) == 0,
        "catalogMetadataAndOutlineIntact": (
            pdf_lang == "zh-CN"
            and bool(metadata_title)
            and bool(metadata_author)
            and outline_count > 100
            and has_all_3_outline_levels
            and residual_sentinel_links == 0
        ),
        "langZhCN": pdf_lang == "zh-CN",
        "pageLabelsAlignedZeroOffset": (
            page_labels_ok and len(footer_mismatches) == 0 and len(suppressed_header_leaks) == 0
        ),
        "tocPrintedPageNumbersComplete": (toc_total == 0) or (toc_aligned == toc_total),
        "noMisleadingPartialTagTree": (not marked_true and not has_struct_tree) or (struct_parents_coverage_ratio >= 0.98),
        "zeroKangxiRadicals": kangxi_total == 0,
        "zeroBlankPages": len(blank_pages) == 0,
        "bodyFontReadable": median_body_pt >= 8.5,
        "hasEndSentinel": has_end_sentinel,
    }
    passed = all(checks.values()) and residual_sentinel_links == 0

    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "output": str(final_pdf.relative_to(REPO_ROOT)) if final_pdf.is_relative_to(REPO_ROOT) else str(final_pdf),
        "edition": manifest.get("edition", ""),
        "passed": passed,
        "checks": checks,
        "metrics": {
            "totalPages": total_pages,
            "coverPages": merge_info["coverPages"],
            "tocPages": len(toc_pages_0),
            "bodyPages": max(0, total_pages - body_start_0),
            "chunkCount": merge_info.get("chunkCount", 1),
            "headersStamped": headers_stamped,
            "suppressedHeaderLeaks": suppressed_header_leaks,
            "footerMismatches": footer_mismatches,
            "pageLabels": page_labels_raw,
            "tocPageNumberCoverage": {
                "total": toc_total,
                "numbered": toc_numbered,
                "alignedZeroOffset": toc_aligned,
                "coveragePct": toc_coverage_pct,
                "mismatches": toc_mismatches,
            },
            "internalLinks": {
                **link_stats,
                "residualSentinels": residual_sentinel_links,
            },
            "embeddedFonts": font_stats,
            "fontSubsetting": subset_stats,
            "streamDedup": dedup_stats,
            "timingsSec": timings,
            "fileSizeBytes": file_bytes,
            "fileSizeMiB": file_mib,
            "outlineTotal": outline_count,
            "outlineLevels": {
                "level1": outline_stats["level1"],
                "level2": outline_stats["level2"],
                "level3": outline_stats["level3"],
            },
            "outlineResolution": {
                "namedDestHits": outline_stats["namedDestHits"],
                "textMatchHits": outline_stats["textMatchHits"],
                "fallbackCursorHits": outline_stats["fallbackCursorHits"],
            },
            "kangxiRadicalCount": kangxi_total,
            "kangxiHits": kangxi_hits[:20],
            "blankPages": blank_pages,
            "sparsePages": sparse_pages[:30],
            "bodyFontPt": {
                "samples": len(prose_font_sizes),
                "median": median_body_pt,
                "p10": p10_body_pt,
            },
            "rightMarginOverflowSamples": overflow_samples,
            "unrenderedTexHints": unrendered_tex_pages,
            "rawTexBookmarks": raw_tex_bookmarks[:15],
            "taggedPdf": {
                "marked": marked_true,
                "structTreeRoot": has_struct_tree,
                "lang": pdf_lang,
                "structParentsPages": struct_parents_pages,
                "totalPages": total_pages,
                "structParentsCoverageRatio": struct_parents_coverage_ratio,
                "accessibilityPreferredFormat": "EPUB 3 (Native MathML 3)",
                "note": manifest.get(
                    "accessibilityNote",
                    "本 PDF 为无半残标签树的干净高保真印刷版；无障碍屏幕朗读请优先使用配套原生 MathML 3 EPUB 3 版本。",
                ),
            },
            "metadata": {
                "title": metadata_title,
                "author": metadata_author,
                "subject": metadata.get("subject", ""),
                "keywords": metadata.get("keywords", ""),
            },
        },
        "previews": previews,
    }


def main(argv: list[str] | None = None) -> int:
    t_start = time.time()
    parser = argparse.ArgumentParser(description="Merge, stamp, link, bookmark, subset, compress, and QA-gate the A4 Handbook PDF.")
    parser.add_argument("--probe-pages", dest="probe_pages", type=Path, default=None)
    parser.add_argument("--cover", type=Path, default=DEFAULT_COVER)
    parser.add_argument("--body", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--chunks-manifest", dest="chunks_manifest", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--preview-dir", type=Path, default=DEFAULT_PREVIEW_DIR)
    args = parser.parse_args(argv)

    if args.probe_pages is not None:
        if not args.probe_pages.exists():
            print(f"[postprocess-pdf] Missing probe input: {args.probe_pages}", file=sys.stderr)
            return 2
        result = probe_body_chunk_pages(args.probe_pages)
        print(json.dumps(result, ensure_ascii=False))
        return 0

    manifest_path = args.chunks_manifest or args.manifest or DEFAULT_MANIFEST
    if not manifest_path.exists():
        print(f"[postprocess-pdf] Missing required manifest input: {manifest_path}", file=sys.stderr)
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    cover_path = args.cover
    if not cover_path.exists() and manifest.get("cover"):
        cover_path = Path(manifest["cover"])
    if not cover_path.exists():
        print(f"[postprocess-pdf] Missing required cover input: {cover_path}", file=sys.stderr)
        return 2

    chunk_entries = manifest.get("chunks") or []
    is_chunked = bool(chunk_entries) and args.body is None
    if is_chunked:
        chunk_paths = [Path(c["path"]) for c in chunk_entries]
    else:
        body_path = args.body or DEFAULT_BODY
        if not body_path.exists():
            print(f"[postprocess-pdf] Missing required body input: {body_path}", file=sys.stderr)
            return 2
        chunk_paths = [body_path]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)

    fd, merged_name = tempfile.mkstemp(prefix="qch-merged-", suffix=".pdf", dir=str(cover_path.parent))
    os.close(fd)
    merged_tmp = Path(merged_name)

    fd2, out_tmp_name = tempfile.mkstemp(prefix="qch-final-", suffix=".pdf", dir=str(args.output.parent))
    os.close(fd2)
    out_tmp = Path(out_tmp_name)

    try:
        t0 = time.time()
        if is_chunked:
            doc, merge_info, global_dest_map = merge_cover_and_chunks_fitz(cover_path, chunk_paths)
        else:
            doc, merge_info, global_dest_map = merge_cover_and_body_legacy(cover_path, chunk_paths[0], merged_tmp)
        t_merge = round(time.time() - t0, 2)

        t2 = time.time()
        cover_pages = merge_info["coverPages"]
        front_id = (manifest.get("frontmatter") or {}).get("id", "front-readme")
        front_dest = global_dest_map.get(front_id)
        toc_chunk_id = manifest.get("tocChunkId")
        chunk_offsets = merge_info.get("chunkOffsets") or []
        if front_dest and isinstance(front_dest.get("page"), int) and front_dest["page"] > cover_pages:
            body_start_0 = int(front_dest["page"])
        elif toc_chunk_id and chunk_entries and chunk_entries[0].get("id") == toc_chunk_id and chunk_offsets:
            body_start_0 = cover_pages + int(chunk_offsets[0]["pages"])
        else:
            body_start_0 = min(len(doc), cover_pages + 1)

        toc_pages_0 = set(range(cover_pages, max(cover_pages, body_start_0)))

        toc, outline_stats = resolve_outline_entries(
            doc,
            manifest,
            cover_pages,
            chunk_dest_map=global_dest_map,
        )
        part_pages_0: set[int] = {p1 - 1 for p1 in outline_stats.get("partPages", []) if p1 >= 1}
        for part in manifest.get("parts", []):
            pid = part.get("id", "")
            pinfo = global_dest_map.get(pid)
            if pinfo and isinstance(pinfo.get("page"), int):
                part_pages_0.add(int(pinfo["page"]))

        cross_prefix = manifest.get("crossLinkPrefix", DEFAULT_CROSS_LINK_PREFIX)
        link_stats = rewrite_internal_sentinel_links(doc, global_dest_map, cross_prefix, toc_pages_0)

        doc.set_toc(toc, collapse=2)
        doc.set_metadata({
            "title": BOOK_TITLE,
            "author": BOOK_AUTHOR,
            "subject": BOOK_SUBJECT,
            "keywords": BOOK_KEYWORDS,
            "creator": "tools/reader/build-pdf.mjs + postprocess-pdf.py (V4)",
        })
        catalog_xref = doc.pdf_catalog()
        doc.xref_set_key(catalog_xref, "Lang", "(zh-CN)")

        # Honestly clear any partial /StructTreeRoot or /MarkInfo when untagged (EPUB 3 is accessible edition)
        if manifest.get("tagged") is False or is_chunked:
            doc.xref_set_key(catalog_xref, "StructTreeRoot", "null")
            doc.xref_set_key(catalog_xref, "MarkInfo", "null")

        # Set exact /PageLabels: Cover (page 0) / i, ii (TOC) / 1..N (body starting at front-readme)
        page_labels = [{"startpage": 0, "prefix": "Cover", "style": "", "firstpagenum": 1}]
        if toc_pages_0:
            page_labels.append({"startpage": cover_pages, "prefix": "", "style": "r", "firstpagenum": 1})
        if body_start_0 < len(doc):
            page_labels.append({"startpage": body_start_0, "prefix": "", "style": "D", "firstpagenum": 1})
        doc.set_page_labels(page_labels)
        t_links_toc = round(time.time() - t2, 2)

        t1 = time.time()
        headers_stamped = 0
        if is_chunked:
            skip_pages_0 = set(range(cover_pages)) | toc_pages_0 | part_pages_0
            headers_stamped = stamp_running_headers_and_footers(
                doc,
                body_start_0,
                skip_pages_0,
                manifest.get("edition", ""),
            )
        t_stamp = round(time.time() - t1, 2)

        t3 = time.time()
        # Compact and renumber deleted/free xref slots before font subsetting, CMap fix, and deduplication
        fitz.TOOLS.mupdf_display_errors(False)
        doc.save(str(merged_tmp), garbage=2)
        doc.close()
        doc = fitz.open(str(merged_tmp))
        fitz.TOOLS.mupdf_display_errors(True)

        fonts_before = count_embedded_fonts(doc)
        subset_ok = False
        subset_error = None
        subset_tmp = merged_tmp.with_name(merged_tmp.name + ".subset.pdf")
        if hasattr(doc, "subset_fonts"):
            try:
                fitz.TOOLS.mupdf_display_errors(False)
                doc.subset_fonts()
                subset_ok = True
            except Exception as exc:  # noqa: BLE001
                subset_error = str(exc)
            finally:
                fitz.TOOLS.mupdf_display_errors(True)
            if subset_ok:
                fitz.TOOLS.mupdf_display_errors(False)
                doc.save(str(subset_tmp), garbage=2)
                doc.close()
                doc = fitz.open(str(subset_tmp))
                fitz.TOOLS.mupdf_display_errors(True)
                try:
                    merged_tmp.unlink(missing_ok=True)
                except OSError:
                    pass
                merged_tmp = subset_tmp
        fonts_after = count_embedded_fonts(doc)
        subset_stats = {
            "enabled": subset_ok,
            "error": subset_error,
            "before": fonts_before,
            "after": fonts_after,
        }

        cmap_stats = normalize_kangxi_tounicode_cmaps(doc)
        dedup_stats = deduplicate_identical_streams(doc)
        dedup_stats["kangxiCmapFix"] = cmap_stats
        t_dedup = round(time.time() - t3, 2)

        t4 = time.time()
        doc.save(
            str(out_tmp),
            garbage=4,
            deflate=True,
            deflate_images=True,
            deflate_fonts=True,
            clean=True,
            use_objstms=True,
        )
        doc.close()
        t_save = round(time.time() - t4, 2)

        os.replace(out_tmp, args.output)

        t5 = time.time()
        timings = {
            "merge": t_merge,
            "stampHeadersFooters": t_stamp,
            "linksAndOutline": t_links_toc,
            "subsetAndDedup": t_dedup,
            "save": t_save,
        }
        report = run_qa_audit(
            args.output,
            manifest,
            outline_stats,
            merge_info,
            link_stats,
            dedup_stats,
            subset_stats,
            headers_stamped,
            body_start_0,
            toc_pages_0,
            part_pages_0,
            global_dest_map,
            timings,
            args.preview_dir,
        )
        report["metrics"]["timingsSec"]["qaAuditAndPreviews"] = round(time.time() - t5, 2)
        report["metrics"]["timingsSec"]["postprocessTotal"] = round(time.time() - t_start, 2)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        summary = {
            "output": report["output"],
            "passed": report["passed"],
            "totalPages": report["metrics"]["totalPages"],
            "tocPages": report["metrics"]["tocPages"],
            "bodyPages": report["metrics"]["bodyPages"],
            "chunkCount": report["metrics"]["chunkCount"],
            "fileSizeMiB": report["metrics"]["fileSizeMiB"],
            "embeddedFonts": report["metrics"]["embeddedFonts"],
            "tocPageNumberCoverage": report["metrics"]["tocPageNumberCoverage"],
            "pageLabels": report["metrics"]["pageLabels"],
            "outlineTotal": report["metrics"]["outlineTotal"],
            "outlineLevels": report["metrics"]["outlineLevels"],
            "outlineResolution": report["metrics"]["outlineResolution"],
            "internalLinks": report["metrics"]["internalLinks"],
            "streamDedup": report["metrics"]["streamDedup"],
            "headersStamped": report["metrics"]["headersStamped"],
            "kangxiRadicalCount": report["metrics"]["kangxiRadicalCount"],
            "blankPages": report["metrics"]["blankPages"],
            "bodyFontMedianPt": report["metrics"]["bodyFontPt"]["median"],
            "taggedPdf": report["metrics"]["taggedPdf"],
            "timingsSec": report["metrics"]["timingsSec"],
            "checks": report["checks"],
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if report["passed"] else 1
    finally:
        merged_tmp.unlink(missing_ok=True)
        out_tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
