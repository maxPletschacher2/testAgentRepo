# QA-Testplan: Tkinter Taschenrechner

Ziel
- Verifizieren, dass die einfache Taschenrechner-App (Tkinter) den Anforderungen entspricht: GUI startbar, Buttons funktionieren, Grundrechenarten korrekt, Fehlerbehandlung (v. a. Division durch 0), wartbarer Code.

Umgebung
- Python 3.x
- Keine externen Bibliotheken notwendig (nur Standardbibliothek)

Start
- App: `python calculator.py`
- Tests: `python -m pytest -q`

Checkliste – Manuelle GUI-Tests
1) Start & Oberfläche
   - Fenster öffnet ohne Fehler
   - Display/Eingabefeld vorhanden
   - Buttons vorhanden: Ziffern 0–9; Operatoren +, -, *, /; Dezimalpunkt "."; C; =

2) Grundfunktionen
   - Addition: `12.3 + 4.7 =` -> Ergebnis `17.0` (oder äquivalenter Float)
   - Subtraktion: `9 - 2 =` -> `7`
   - Multiplikation: `5 * 6 =` -> `30`
   - Division: `8 / 4 =` -> `2`
   - Mehrstellige Zahlen: `123 + 456 =` -> `579`
   - Dezimalzahlen: `1.5 + 2.35 =` -> `3.85`

3) Fehlerbehandlung
   - Division durch 0: `9 / 0 =` -> verständliche Fehlermeldung (z. B. "Division durch 0" oder "Fehler")
   - Nach Fehler: `C` setzt den Rechner zurück (Display wieder leer oder `0`)

4) Eingabe-Robustheit
   - Mehrere Dezimalpunkte in einer Zahl verhindern: Eingabe `1..2` darf nicht akzeptiert werden bzw. muss klar behandelt werden
   - Keine Abstürze bei schneller/ungewöhnlicher Eingabe

5) Optional (falls vorhanden)
   - Wiederholtes `=` wiederholt letzte Operation sinnvoll
   - Tastatureingabe: Ziffern und Enter unterstützen (nicht zwingend gefordert)

Erwartete Ergebnisse
- Alle Funktionen liefern korrekte Ergebnisse
- UI bleibt responsiv, kein Crash
- Fehlerzustände werden verständlich kommuniziert und sind durch `C` rücksetzbar

Dokumentation der Ergebnisse
- Notieren: getestete Schritte, beobachtete Ergebnisse, Abweichungen (inkl. Repro-Schritte)
- Bei Fehlern: erwartetes vs. tatsächliches Verhalten, Logs/Konsolen-Output, ggf. Screenshots
