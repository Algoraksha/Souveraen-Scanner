from typing import Dict, Any


def generate_mangelruege(scan_result: Dict[str, Any]) -> str:
    severity = scan_result.get("severity")
    if severity not in ("severe", "high"):
        return ""

    pdf_path = scan_result.get("pdf_path", "(unbekannt)")
    zitier_info = scan_result.get("zitiergebot", {})
    ns_info = scan_result.get("ns_vocab", {})
    shaef_info = scan_result.get("shaef", {})

    zitier_details = []
    for v in zitier_info.get("violations", []):
        p = v.get("page")
        s = v.get("snippet", "")
        if p:
            zitier_details.append(f"- Seite {p}: {s}")
        else:
            zitier_details.append(f"- {s}")

    ns_details = []
    found = ns_info.get("found", {})
    for term, pages in found.items():
        if pages:
            ns_details.append(f"- Begriff '{term}' auf Seiten: {', '.join(map(str, pages))}")

    shaef_detail = None
    if shaef_info.get("flag"):
        shaef_detail = (
            "Zusatzhinweis: Der diffamierende Begriff 'Reichsbürger' entspricht NS-Terminologie; "
            "das entsprechende Gesetz wurde durch SHAEF-Gesetz Nr. 1 aufgehoben."
        )

    text_parts = [
        "Betreff: Mängelrüge – dokumentierter Rechtsbruch und Dienstunfähigkeit",
        "",
        "Sehr geehrte Damen und Herren,",
        "",
        "im Zusammenhang mit dem vorliegenden Dokument wird ein schwerwiegender Rechtsverstoß festgestellt.",
        f"Quelle: {pdf_path}",
        "",
        "1) Verstoß gegen das Zitiergebot gemäß Art. 19 Abs. 1 Satz 2 GG:",
        "Im Kontext von Grundrechtseinschränkungen fehlt die unmittelbare Zitierung der einschlägigen Artikel des Grundgesetzes (z. B. Art. 2, Art. 11, Art. 13).",
        "Nachweise:",
    ]
    text_parts += (zitier_details if zitier_details else ["- (keine Details)"])

    text_parts += [
        "",
        "2) Verwendung von NS-Rhetorik:",
        "Es wurden belastete Begriffe (u. a. 'Totalverweigerer', 'sozialwidrig') festgestellt.",
        "Rosenow-Expertise (2025) weist die Problematik dieser Terminologie nach.",
        "Fundorte:",
    ]
    text_parts += (ns_details if ns_details else ["- (keine Details)"])

    if shaef_detail:
        text_parts += ["", shaef_detail]

    text_parts += [
        "",
        "Bewertung:",
        "Die Kombination aus fehlendem Zitiergebot und NS-Rhetorik dokumentiert einen eklatanten Rechtsbruch.",
        "Hierdurch hat der Verfasser seine Dienstfähigkeit gemäß § 9 DRiG selbst demontiert.",
        "",
        "Forderung:",
        "1. Unverzügliche Abhilfe und Entfernung rechtswidriger Passagen.",
        "2. Schriftliche Bestätigung der Maßnahmen.",
        "3. Prüfung disziplinarischer Schritte gemäß § 9 DRiG.",
        "",
        "Mit freundlichen Grüßen",
        ""
    ]

    return "\n".join(text_parts)
