# Einfache Taschenrechner-App (Python + Tkinter)

Eine simple grafische Taschenrechner-App in Python mit Tkinter. Unterstützt Grundrechenarten, mehrstellige Zahlen und Dezimalzahlen. Fehler (z. B. Division durch 0) werden verständlich angezeigt.

## Voraussetzungen
- Python 3 (keine externen Bibliotheken erforderlich)

## Start
```
python calculator.py
```

## Bedienung und Funktionen
- Ziffern 0–9, Dezimalpunkt "."
- Operatoren: +, -, *, /
- = zur Auswertung
- C zum Zurücksetzen
- Mehrstellige Zahlen und Dezimalzahlen werden unterstützt
- Division durch 0 zeigt: "Fehler: Division durch 0"

Hinweise:
- Ungültige Eingaben (z. B. mehrfacher Dezimalpunkt in derselben Zahl) werden verhindert.
- Nach einer Fehlermeldung kann der Rechner über C zurückgesetzt werden.

## Tests ausführen
Es gibt Unit-Tests für die Rechenlogik (ohne GUI), damit das Verhalten automatisiert geprüft werden kann.

```
python -m unittest
```

Die GUI lässt sich manuell prüfen, indem man die App startet und die Buttons bedient.

## Struktur
- `calculator.py`: Tkinter-GUI und `CalculatorEngine` (Rechenlogik)
- `tests/test_calculator_engine.py`: Unit-Tests für die Engine
