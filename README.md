# plemeo.ai Onepage Landingpage

Diese Repository-Version enthält eine eigenständige HTML-Onepage für plemeo.ai.
Die Seite stellt Produktinformationen bereit und endet mit einem Kontaktformular.

## Inhalt
- `index.html`: komplette Landingpage in reinem HTML, CSS und minimalem JavaScript
- `tests/test_plemeo_onepage.py`: automatisierte Prüfungen für Seitenstruktur und Kontaktformular
- `calculator.py`: vorhandene Beispielanwendung aus dem Repository bleibt unverändert erhalten

## Lokales Öffnen
Die Seite kann direkt im Browser geöffnet werden:

```bash
xdg-open index.html
```

Falls das auf deinem System nicht verfügbar ist, kannst du die Datei auch über einen lokalen Webserver ausliefern, zum Beispiel:

```bash
python3 -m http.server 8000
```

## Tests ausführen
Die automatisierten Prüfungen laufen mit der Standardbibliothek:

```bash
python3 -m unittest
```

## Was die Seite enthält
- Hero-Bereich mit plemeo.ai Positionierung
- Produktbeschreibung und Vorteile
- Ablauf-/Nutzenabschnitte
- Kontaktbereich mit Formular am Seitenende
- Kleine Rückmeldung nach dem Absenden des Formulars
