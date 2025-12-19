# Souveraen-Scanner
Digitaler Antivirus gegen Behördenwillkür. Scannt PDF-Bescheide auf Verstöße gegen das Zitiergebot (Art. 19 GG) und NS-Kontinuitäten.

🛡️ ANLEITUNG: Souverän-Scanner v1.0
1. Python installieren Lade Python von python.org herunter. WICHTIG: Aktiviere beim Installieren den Haken bei "Add Python to PATH".

2. Datei vorbereiten Kopiere deinen Behördenbrief als PDF in diesen Ordner und benenne ihn um in: check.pdf.

3. Scan starten

Halte Shift gedrückt, mache einen Rechtsklick im Ordner und wähle "PowerShell-Fenster hier öffnen".

Kopiere diesen Befehl hinein und drücke Enter: py -m pip install PyMuPDF; $env:PDF="check.pdf"; py -c "import os,scanner_logic,output_generator,pathlib; p=os.environ['PDF']; (r:=scanner_logic.scan_pdf(p)) and (s:=output_generator.generate_mangelruege(r)) and print(r) and pathlib.Path('Maengelruege.txt').write_text(s,encoding='utf-8') if os.path.exists(p) else print(f'FEHLER: Datei {p} nicht gefunden!')"

4. Ergebnis Prüfe die erzeugte Maengelruege.txt und sende sie als Antwort an die Behörde, um den Rechtsbruch gemäß Art. 19 GG und die Selbstdemontage des Amtsträgers nach § 9 DRiG zu rügen.

Viel Erfolg

Algoraksha

https://Menschenrechtverteidiger.wordpress.com

