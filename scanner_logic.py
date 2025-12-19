import re
from typing import Any, Dict, List

try:
    import fitz  # PyMuPDF
except ImportError as e:
    raise ImportError("PyMuPDF (fitz) ist erforderlich. Bitte installieren: pip install PyMuPDF") from e


def _extract_pages_text(pdf_path: str) -> List[str]:
    doc = fitz.open(pdf_path)
    try:
        texts = []
        for i in range(doc.page_count):
            page = doc.load_page(i)
            texts.append(page.get_text("text"))
        return texts
    finally:
        doc.close()


def scan_pdf(pdf_path: str) -> Dict[str, Any]:
    texts = _extract_pages_text(pdf_path)

    re_mention = re.compile(r"(?is)\bGrundrecht\w*\b.{0,300}?(einschränk\w*|beschränk\w*)")
    re_citation_generic = re.compile(r"(?i)\b(Art\.?|Artikel)\s*\d+\s*(GG|Grundgesetz)\b")
    re_citation_specific = re.compile(r"(?i)\bArt\.?\s*(2|11|13)\s*(GG|Grundgesetz)\b")

    re_totalverweigerer = re.compile(r"(?i)\bTotalverweigerer\b")
    re_sozialwidrig = re.compile(r"(?i)\bsozialwidrig\b")
    re_reichsbuerger = re.compile(r"(?i)\bReichsbürger\b")

    # Zitiergebot-Automatik: Art. 19 Abs. 1 Satz 2 GG
    re_art19_zitier = re.compile(r"(?i)\bArt\.?\s*19\s*Abs\.?\s*1\s*(Satz|S\.? )\s*2\b(?:\s*(GG|Grundgesetz))?")

    # Administratives Übergriffsvokabular (Datenanforderungen, potentieller Eingriff in Art. 2 GG)
    admin_terms: Dict[str, re.Pattern] = {
        "Schufa-Auskunft": re.compile(r"(?i)\bSchufa[- ]?Auskunft\b"),
        "Gläubiger": re.compile(r"(?i)\b(Gläubiger|Glaeubiger)\b"),
        "Schuldenhöhe": re.compile(r"(?i)\b(Schuldenhöhe|Schuldenhoehe)\b"),
        "Verbraucherinsolvenzverfahren": re.compile(r"(?i)\bVerbraucherinsolvenzverfahren\b"),
    }

    zitier_mentions = 0
    zitier_violations: List[Dict[str, Any]] = []

    ns_hits: Dict[str, List[int]] = {"Totalverweigerer": [], "sozialwidrig": []}
    shaef_pages: List[int] = []
    admin_hits: Dict[str, List[int]] = {k: [] for k in admin_terms.keys()}
    info_sd_violations: List[Dict[str, Any]] = []

    for page_index, text in enumerate(texts, start=1):
        for m in re_mention.finditer(text):
            zitier_mentions += 1
            start, end = m.start(), m.end()
            s = max(0, start - 250)
            e = min(len(text), end + 250)
            window = text[s:e]
            has_citation = bool(re_citation_generic.search(window) or re_citation_specific.search(window))
            if not has_citation:
                snippet = window.strip().replace("\n", " ")
                zitier_violations.append({
                    "page": page_index,
                    "snippet": snippet[:600]
                })

        if re_totalverweigerer.search(text):
            ns_hits["Totalverweigerer"].append(page_index)
        if re_sozialwidrig.search(text):
            ns_hits["sozialwidrig"].append(page_index)
        if re_reichsbuerger.search(text):
            shaef_pages.append(page_index)

        # Administratives Übergriffsvokabular + Zitiergebot-Automatik
        for label, pat in admin_terms.items():
            for mm in pat.finditer(text):
                admin_hits[label].append(page_index)
                s = max(0, mm.start() - 400)
                e = min(len(text), mm.end() + 400)
                window = text[s:e]
                # Prüfe, ob Art. 19 Abs. 1 S. 2 GG im Kontext zitiert ist
                has_art19 = bool(re_art19_zitier.search(window)) or bool(re_art19_zitier.search(text))
                if not has_art19:
                    snippet = window.strip().replace("\n", " ")
                    info_sd_violations.append({
                        "page": page_index,
                        "term": label,
                        "snippet": snippet[:600],
                        "message": "Eingriff in Grundrechte ohne verfassungsrechtliche Ermächtigung durch Zitierung"
                    })

    ns_flag = any(v for v in ns_hits.values())
    zitier_flag = len(zitier_violations) > 0
    shaef_flag = len(shaef_pages) > 0
    info_sd_flag = len(info_sd_violations) > 0

    ns_warnings: List[str] = []
    if ns_hits["Totalverweigerer"]:
        ns_warnings.append("NS-Vokabular erkannt: 'Totalverweigerer' – siehe Rosenow-Expertise (2025)")
    if ns_hits["sozialwidrig"]:
        ns_warnings.append("NS-Vokabular erkannt: 'sozialwidrig' – siehe Rosenow-Expertise (2025)")

    shaef_message = None
    if shaef_flag:
        shaef_message = (
            "Hinweis: Der Begriff 'Reichsbürger' zur Diffamierung entspricht NS-Terminologie; "
            "das entsprechende Gesetz wurde durch SHAEF-Gesetz Nr. 1 aufgehoben."
        )

    severity = "severe" if (zitier_flag and ns_flag) else ("warning" if (zitier_flag or ns_flag or shaef_flag) else "none")
    special_admin_violation = any(v.get("term") in ("Schufa-Auskunft", "Gläubiger") for v in info_sd_violations)
    if special_admin_violation and severity != "severe":
        severity = "high"

    return {
        "pdf_path": pdf_path,
        "pages": len(texts),
        "zitiergebot": {
            "mentions": zitier_mentions,
            "violations": zitier_violations,
            "flag": zitier_flag,
            "message": "Verstoß gegen Art. 19 Abs. 1 S. 2 GG" if zitier_flag else None,
        },
        "ns_vocab": {
            "found": ns_hits,
            "warnings": ns_warnings,
            "flag": ns_flag,
        },
        "shaef": {
            "found_pages": shaef_pages,
            "message": shaef_message,
            "flag": shaef_flag,
        },
        "admin_overreach": {
            "found": admin_hits,
        },
        "info_self_determination": {
            "violations": info_sd_violations,
            "flag": info_sd_flag,
            "message": (
                "Eingriff in Grundrechte ohne verfassungsrechtliche Ermächtigung durch Zitierung"
                if info_sd_flag else None
            ),
        },
        "severity": severity,
    }
