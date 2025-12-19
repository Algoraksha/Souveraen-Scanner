# Souveraen-Scanner
Digitaler Antivirus gegen Behördenwillkür. Scannt PDF-Bescheide auf Verstöße gegen das Zitiergebot (Art. 19 GG) und NS-Kontinuitäten.

🛡️ Handlungsanweisung: So nutzt du deinen Souverän-Scanner
1. Vorbereitung (Einmalig)

Installiere Python von python.org.

WICHTIG: Setze während der Installation den Haken bei "Add Python to PATH", sonst findet dein Computer den Scanner nicht.

2. Installation des Scanners

Lade die Datei Souveran-Scanner-1.0.exe von GitHub herunter.

Führe die Datei aus. Sie entpackt den Scanner-Ordner direkt auf deinen Desktop.

3. Das Dokument prüfen

Speichere das Behördenschreiben, das du prüfen willst, als PDF ab.

Kopiere diese PDF in den Ordner Souverän-Scanner.

Ganz wichtig: Benenne deine PDF-Datei um in: check.pdf.

4. Den Scan-Befehl ausführen

Halte die Umschalt-Taste (Shift) gedrückt und mache einen Rechtsklick in den Ordner.

Wähle "PowerShell-Fenster hier öffnen".

Kopiere diesen Befehl komplett hinein und drücke Enter:

PowerShell

py -m pip install PyMuPDF; $env:PDF="check.pdf"; py -c "import os,scanner_logic,output_generator,pathlib; p=os.environ['PDF']; (r:=scanner_logic.scan_pdf(p)) and (s:=output_generator.generate_mangelruege(r)) and print(r) and pathlib.Path('Maengelruege.txt').write_text(s,encoding='utf-8') if os.path.exists(p) else print(f'FEHLER: Datei {p} nicht gefunden!')"

5. Das Ergebnis auswerten

Im Fenster: Du siehst sofort, ob ein Verstoß gegen das Zitiergebot (Art. 19 GG) vorliegt.

Im Ordner: Wenn der Schweregrad hoch ist, erscheint die Datei Maengelruege.txt.

Deine Antwort: Nutze den Text aus der Maengelruege.txt als Antwort an die Behörde, um den Rechtsbruch und die Selbstdemontage des Amtsträgers (§ 9 DRiG) aktenkundig zu machen.
