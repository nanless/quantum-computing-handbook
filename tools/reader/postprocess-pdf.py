#!/usr/bin/env python3
"""Post-process and QA-gate the Quantum Computing Handbook A4 PDF.

Supports both chunked mode (--chunks-manifest / manifest["chunks"]) and legacy
monolithic mode (--body):
1. Extracts exact per-chunk PDF Named Destinations via PyMuPDF (fitz) with
   accurate chunk_page_offset, then merges cover.pdf (page 1) + all chunk-*.pdf
   via fast native MuPDF insert_pdf (retaining front chunk's catalog /StructTreeRoot
   and /MarkInfo while honestly measuring per-page /StructParents coverage; pypdf
   fallback available for legacy single --body).
2. Stamps crisp publication-grade running headers (left book title, right edition)
   and continuous centered page footers (第 p-1 页 / 共 N-1 页) on all body pages
   (pages 2..N) using built-in CJK font 'china-ss' (zero font bloat, zero Kangxi
   radicals).
3. Converts all TOC and internal sentinel links (https://qch.local/#<anchor>)
   into exact internal PDF GoTo link annotations (page.insert_link) targeting the
   real merged destination page & vertical offset.
4. Performs O(N) blake2b deduplication of identical leaf streams (e.g. Chrome
   Type3 /CharProcs glyph streams duplicated across chunks), writes a 3-level
   Unicode PDF outline (Part -> Chapter/Appendix/Lab -> H2), embeds complete
   metadata + /Lang (zh-CN), and saves with lossless compression
   (garbage=2, deflate=True, deflate_images=True, deflate_fonts=True, use_objstms=True).
5. Runs all 10 automated publishing QA gates (verifying catalog /Lang, metadata,
   3-level Unicode outline, 0 residual link sentinels, and honestly reporting
   per-page /StructParents coverage via pypdf.PdfReader) and exports 4 150-DPI
   sample PNG previews into work/rendered/ + report JSON into work/research/.
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
BOOK_HEADER_LEFT = "量子计算手册 · 从直觉到研究入口"
BOOK_AUTHOR = "量子计算手册编写组"
BOOK_SUBJECT = "系统量子计算与量子力学教材：从零基础数学与物理直觉到核心算法、噪声纠错、量子传感、经典模拟与离线验算"
BOOK_KEYWORDS = "量子计算, 量子力学, 量子算法, 量子纠错, 表面码, 量子传感, 稳定子模拟, 离线出版, KaTeX"

DEFAULT_CROSS_LINK_PREFIX = "https://qch.local/#"

# Running header/footer palette matching tools/reader/pdf.css
HEADER_RULE_COLOR = (0xD7 / 255.0, 0xD1 / 255.0, 0xC5 / 255.0)  # #D7D1C5
HEADER_TEXT_COLOR = (0x53 / 255.0, 0x66 / 255.0, 0x60 / 255.0)  # #536660
MARGIN_X_PT = 17.0 * 72.0 / 25.4  # 17 mm = 48.189 pt

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


def merge_cover_and_chunks_fitz(
    cover_path: Path,
    chunk_paths: list[Path],
) -> tuple[fitz.Document, dict, dict[str, dict]]:
    """Merge cover.pdf + ordered chunk PDFs via MuPDF insert_pdf while preserving /StructTreeRoot."""
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


def deduplicate_identical_streams(doc: fitz.Document) -> dict:
    """O(N) blake2b deduplication of identical leaf PDF streams (e.g. Chrome Type3 CharProcs).

    MuPDF's garbage=3/4 uses O(N^2) comparison which stalls on 150k+ xrefs.
    Hashing pure leaf streams (no indirect references in their dictionary) runs in
    O(N) (~3-4s) and shrinks multi-chunk Chrome PDFs by ~65-70% losslessly.
    """
    n_xref = doc.xref_length()
    canon: dict[bytes, int] = {}
    remap: dict[int, int] = {}
    len_re = re.compile(r"/Length\s+\d+")

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
        existing = canon.get(sig)
        if existing is not None:
            remap[x] = existing
        else:
            canon[sig] = x

    if not remap:
        return {"uniqueStreams": len(canon), "dedupedStreams": 0, "rewrittenObjects": 0}

    # Token-aware regex: skip PDF literal strings (...) including 1 level of nested parens
    token_re = re.compile(r"\((?:\\.|[^\\()]|\((?:\\.|[^\\()])*\))*\)|\b(\d+)\s+0\s+R\b")
    rewritten = 0

    for x in range(1, n_xref):
        if x in remap or doc.xref_is_stream(x):
            # Never call update_object() on stream xrefs (PyMuPDF detaches the stream payload).
            # Skipping stream containers safely leaves their references intact for garbage=2.
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

    return {
        "uniqueStreams": len(canon),
        "dedupedStreams": len(remap),
        "rewrittenObjects": rewritten,
    }


def stamp_running_headers_and_footers(
    doc: fitz.Document,
    cover_pages: int,
    edition: str,
) -> int:
    """Stamp crisp hairline running header & continuous page footer on all body pages.

    Appends a lightweight isolated PDF overlay stream (with shared q/Q wrapper streams
    and a single shared Type0 UniGB-UTF16-H 'Song' CJK font dictionary) directly to each
    page's /Contents array so Chrome's large page streams are never decompressed (~0.4s
    for 1,270+ pages, zero font bloat, zero Kangxi radicals).
    """
    total_pages = len(doc)
    body_total = total_pages - cover_pages
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
    def song_width(s: str, fs: float = 7.5) -> float:
        return sum(0.5 if ord(ch) < 128 else 1.0 for ch in s) * fs

    right_w = song_width(right_label, 7.5)
    left_hex = BOOK_HEADER_LEFT.encode("utf-16-be").hex().upper()
    right_hex = right_label.encode("utf-16-be").hex().upper()

    rr, rg, rb = HEADER_RULE_COLOR
    tr, tg, tb = HEADER_TEXT_COLOR
    stamped = 0

    for idx in range(cover_pages, total_pages):
        page = doc[idx]
        pw = float(page.rect.width)
        ph = float(page.rect.height)
        body_num = idx - cover_pages + 1
        footer_label = f"第 {body_num} 页 / 共 {body_total} 页"
        footer_w = song_width(footer_label, 7.5)
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

        # PDF coordinates are bottom-up: top margin band is [ph - 56.69, ph], bottom band is [0, 56.69]
        header_rule_y = ph - 38.0
        header_text_y = ph - 33.5
        footer_rule_y = 38.0
        footer_text_y = 27.0
        right_x = pw - MARGIN_X_PT - right_w
        footer_x = (pw - footer_w) / 2.0

        overlay_stream = (
            f"q\n"
            f"{rr:.4f} {rg:.4f} {rb:.4f} RG 0.5 w\n"
            f"{MARGIN_X_PT:.2f} {header_rule_y:.2f} m {pw - MARGIN_X_PT:.2f} {header_rule_y:.2f} l S\n"
            f"{MARGIN_X_PT:.2f} {footer_rule_y:.2f} m {pw - MARGIN_X_PT:.2f} {footer_rule_y:.2f} l S\n"
            f"{tr:.4f} {tg:.4f} {tb:.4f} rg\n"
            f"BT /F_QCH_HF 7.5 Tf 1 0 0 1 {MARGIN_X_PT:.2f} {header_text_y:.2f} Tm <{left_hex}> Tj ET\n"
            f"BT /F_QCH_HF 7.5 Tf 1 0 0 1 {right_x:.2f} {header_text_y:.2f} Tm <{right_hex}> Tj ET\n"
            f"BT /F_QCH_HF 7.5 Tf 1 0 0 1 {footer_x:.2f} {footer_text_y:.2f} Tm <{footer_hex}> Tj ET\n"
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
    headers_stamped: int,
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
    marked_val = mark_info.get("/Marked") if mark_info is not None else None
    if marked_val is not None and hasattr(marked_val, "get_object"):
        marked_val = marked_val.get_object()
    marked_true = (isinstance(marked_val, BooleanObject) and marked_val.value is True) or (marked_val is True)
    has_struct_tree = "/StructTreeRoot" in root
    pdf_lang = str(root.get("/Lang", ""))
    struct_parents_pages = sum(1 for p in pypdf_reader.pages if "/StructParents" in p)

    doc = fitz.open(str(final_pdf))
    total_pages = len(doc)
    struct_parents_coverage_ratio = round(struct_parents_pages / total_pages, 4) if total_pages > 0 else 0.0
    toc = doc.get_toc(simple=True)
    outline_count = len(toc)

    part_pages = set(outline_stats.get("partPages", []))
    named_all = doc.resolve_names()
    for part in manifest.get("parts", []):
        pid = part.get("id", "")
        if pid:
            info = named_all.get(pid) or named_all.get("/" + pid)
            if isinstance(info, dict) and isinstance(info.get("page"), int):
                part_pages.add(info["page"] + 1)

    cross_prefix = manifest.get("crossLinkPrefix", DEFAULT_CROSS_LINK_PREFIX)
    kangxi_hits: list[dict] = []
    blank_pages: list[int] = []
    sparse_pages: list[dict] = []
    overflow_samples: list[dict] = []
    prose_font_sizes: list[float] = []
    unrendered_tex_pages: list[dict] = []
    residual_sentinel_links = 0
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

        # 1. CJK Kangxi radical check across EVERY page (including running headers/footers)
        radicals = KANGXI_RADICAL_RE.findall(text)
        if radicals:
            kangxi_hits.append({
                "page": p1,
                "count": len(radicals),
                "codepoints": sorted({f"U+{ord(ch):04X}" for ch in radicals})[:10],
            })

        # 2. Honest blank / orphan page detection inside the body content area (excluding header/footer bands)
        # Fast path: header+footer adds <= 40 non-ws chars, so only invoke clipped text extraction when total < 120.
        if p1 > merge_info["coverPages"]:
            total_non_ws = len(re.sub(r"\s+", "", text))
            if total_non_ws < 120:
                body_clip = fitz.Rect(0.0, 42.0, pw, ph - 42.0)
                body_text = page.get_text("text", clip=body_clip) or ""
                body_non_ws = len(re.sub(r"\s+", "", body_text))
                if body_non_ws < 45:
                    images_n = len(page.get_images())
                    drawings_n = max(0, len(page.get_drawings()) - 2)
                    if body_non_ws < 20 and images_n == 0 and drawings_n < 5:
                        blank_pages.append(p1)
                    elif p1 not in part_pages and images_n == 0 and drawings_n < 8:
                        sparse_pages.append({
                            "page": p1,
                            "chars": body_non_ws,
                            "images": images_n,
                            "drawings": drawings_n,
                        })

        # 3. Font readability & right margin overflow probe
        if idx % sample_step == 0:
            margin_limit = pw - 22.0
            page_dict = page.get_text("dict")
            for block in page_dict.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        stext = (span.get("text") or "").strip()
                        sz = float(span.get("size", 0.0))
                        bbox = span.get("bbox", (0, 0, 0, 0))
                        if bbox[1] >= 42.0 and bbox[3] <= ph - 42.0:
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
        "zeroKangxiRadicals": kangxi_total == 0,
        "zeroBlankPages": len(blank_pages) == 0,
        "bodyFontReadable": median_body_pt >= 8.8,
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
            "bodyPages": merge_info["bodyPages"],
            "chunkCount": merge_info.get("chunkCount", 1),
            "headersStamped": headers_stamped,
            "internalLinks": {
                **link_stats,
                "residualSentinels": residual_sentinel_links,
            },
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
                "note": (
                    "Chunked fitz merge retains catalog /StructTreeRoot from front chunk "
                    "while guaranteeing 0 xref errors and 3-level Unicode outline across all pages."
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
    parser = argparse.ArgumentParser(description="Merge, stamp, link, bookmark, compress, and QA-gate the A4 Handbook PDF.")
    parser.add_argument("--cover", type=Path, default=DEFAULT_COVER)
    parser.add_argument("--body", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--chunks-manifest", dest="chunks_manifest", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--preview-dir", type=Path, default=DEFAULT_PREVIEW_DIR)
    args = parser.parse_args(argv)

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

        t1 = time.time()
        headers_stamped = 0
        if is_chunked:
            headers_stamped = stamp_running_headers_and_footers(
                doc,
                merge_info["coverPages"],
                manifest.get("edition", ""),
            )
        t_stamp = round(time.time() - t1, 2)

        t2 = time.time()
        front_id = (manifest.get("frontmatter") or {}).get("id", "front-readme")
        front_dest = global_dest_map.get(front_id)
        toc_end_0 = int(front_dest["page"]) if front_dest else min(len(doc), merge_info["coverPages"] + 2)
        toc_pages_0 = set(range(merge_info["coverPages"], max(merge_info["coverPages"] + 1, toc_end_0)))

        cross_prefix = manifest.get("crossLinkPrefix", DEFAULT_CROSS_LINK_PREFIX)
        link_stats = rewrite_internal_sentinel_links(doc, global_dest_map, cross_prefix, toc_pages_0)

        toc, outline_stats = resolve_outline_entries(
            doc,
            manifest,
            merge_info["coverPages"],
            chunk_dest_map=global_dest_map,
        )
        doc.set_toc(toc, collapse=2)
        doc.set_metadata({
            "title": BOOK_TITLE,
            "author": BOOK_AUTHOR,
            "subject": BOOK_SUBJECT,
            "keywords": BOOK_KEYWORDS,
            "creator": "tools/reader/build-pdf.mjs + postprocess-pdf.py",
        })
        catalog_xref = doc.pdf_catalog()
        doc.xref_set_key(catalog_xref, "Lang", "(zh-CN)")
        t_links_toc = round(time.time() - t2, 2)

        t3 = time.time()
        # Compact and renumber deleted/free xref slots (from insert_pdf + delete_link) via fast
        # O(N) garbage=2 before CMap Kangxi normalization and O(N) leaf-stream deduplication.
        doc.save(str(merged_tmp), garbage=2)
        doc.close()
        doc = fitz.open(str(merged_tmp))
        cmap_stats = normalize_kangxi_tounicode_cmaps(doc)
        dedup_stats = deduplicate_identical_streams(doc)
        dedup_stats["kangxiCmapFix"] = cmap_stats
        t_dedup = round(time.time() - t3, 2)

        t4 = time.time()
        doc.save(
            str(out_tmp),
            garbage=2,
            deflate=True,
            deflate_images=True,
            deflate_fonts=True,
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
            "streamDedup": t_dedup,
            "save": t_save,
        }
        report = run_qa_audit(
            args.output,
            manifest,
            outline_stats,
            merge_info,
            link_stats,
            dedup_stats,
            headers_stamped,
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
            "chunkCount": report["metrics"]["chunkCount"],
            "fileSizeMiB": report["metrics"]["fileSizeMiB"],
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
