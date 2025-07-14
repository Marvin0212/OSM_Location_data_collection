[![en](https://img.shields.io/badge/lang-EN-informational)](README.md)
[![de](https://img.shields.io/badge/lang-DE-informational)](README.de.md)

# OSM-Based Location Entity Datasets

Dieses Repository dient als ergänzende Ressource, um die Methodik zur Erstellung von Entitätenlisten für Standorte offenzulegen. Diese Listen wurden für die Erzeugung von Surrogatdaten in einem Forschungsprojekt verwendet und basieren vollständig auf Daten von OpenStreetMap (OSM).

## Überblick

Die Erstellung hochwertiger Surrogatdaten erfordert realistische und vielfältige Entitäten. Für standortbezogene Entitäten wie Organisationen, Gesundheitseinrichtungen und kategorienübergreifende Lokationsangaben ist OpenStreetMap eine ideale Datenquelle.

### Was ist OpenStreetMap (OSM)?

[OpenStreetMap](https://www.openstreetmap.org/) ist ein kollaboratives Projekt zur Erstellung einer freien, editierbaren Weltkarte. Ähnlich wie bei Wikipedia wird die riesige, von Freiwilligen beigetragene Datenbank ständig erweitert und aktualisiert. Die Daten sind unter der **Open Database License (ODbL)** verfügbar, was sie zu einer ausgezeichneten Quelle für Forschung und Entwicklung macht. Ihre Stärke liegt in der detaillierten Klassifizierung von Objekten durch ein flexibles Tagging-System (z. B. `shop=supermarket`, `amenity=hospital`).

Dieses Repository dokumentiert transparent, wie wir diese Ressource genutzt haben, um drei spezifische Datensätze für den deutschen Sprachraum zu erstellen:
1.  **Gesundheitseinrichtungen** (`hospital`)
2.  **Organisationen** (`organization`)
3.  **Sonstige Orte** (`other`)

## Datensätze und Erstellungsmethodik

Jeder Datensatz wurde durch eine spezifische Abfrage an die Overpass API von OSM und anschließende Filter- und Bereinigungsschritte erstellt. Die Jupyter Notebooks in diesem Repository (`/notebooks`) dokumentieren den gesamten Prozess im Detail.

### 1. Gesundheitseinrichtungen (`/data/hospital`)

Dieser Datensatz enthält Namen von Krankenhäusern, Arztpraxen und anderen medizinischen Einrichtungen in Deutschland.

**Methodik:**
1.  **Datenabfrage:** Es wurden alle Knoten (`node`), Wege (`way`) und Relationen (`relation`) in Deutschland abgefragt, die mit dem Tag `healthcare=*` versehen sind. Um den Kontext zu erweitern, wurde der Name um den Wert des `healthcare:speciality`-Tags ergänzt (z. B. "Klinikum Musterstadt / general").
2.  **Filterung von Personennamen (NER):** Viele Einträge in OSM sind Ärztenamen (z.B. "Dr. Max Mustermann"). Um diese zu entfernen, wurde ein NER-Modell (Named Entity Recognition) von SpaCy (`de_core_news_lg`) verwendet. Alle Entitäten, die als `PER` (Person) klassifiziert wurden, wurden vorläufig entfernt.
3.  **Keyword-basierte Reklassifizierung:** Da das NER-Modell auch legitime Einrichtungsnamen (z.B. "Praxis Dr. Schmidt") fälschlicherweise als Person klassifizieren kann, wurden die entfernten Namen erneut überprüft. Einträge, die medizinische Schlüsselwörter wie `Klinik`, `Praxis`, `Zentrum`, `Therapie` usw. enthielten, wurden wieder in die Liste der Gesundheitseinrichtungen aufgenommen.
4.  **RegEx-basierte Filterung:** Ein zusätzlicher Filter mit regulären Ausdrücken wurde angewendet, um verbleibende typische Ärztenamen (z. B. "Dr. med. M. Müller & Kollegen") zu identifizieren und zu entfernen.
5.  **Exklusion:** Einträge, die "Apotheke" enthielten, wurden in eine separate Datei verschoben, da sie eine eigene Kategorie darstellen.

### 2. Organisationen (`/data/organization`)

Dieser Datensatz umfasst eine breite Palette von Organisationen, einschließlich Unternehmen, Werkstätten, Vereinen und Industrieanlagen.

**Methodik:**
1.  **Datenabfrage:** Es wurden alle OSM-Knoten in Deutschland abgefragt, die mit einem der folgenden primären Tags versehen sind und einen Namen (`name`) haben:
    *   `office=*` (Büros, Agenturen, Kanzleien)
    *   `craft=*` (Handwerksbetriebe wie Bäcker, Schreiner, Werkstätten)
    *   `club=*` (Vereinshäuser und Treffpunkte)
    *   `industrial=*` (Industrielle Standorte)
2.  **Bereinigung:** Die resultierende Liste wurde dedupliziert und alphabetisch sortiert. Es wurden keine weiteren komplexen Filterungen vorgenommen, da die Tags bereits eine gute Abgrenzung bieten.

### 3. Sonstige Orte (`/data/other`)

Dieser Datensatz ist eine heterogene Sammlung benannter Orte, die nicht durch die kategorisierten Lokationsangaben abgedeckt werden. Er dient dazu, eine breite Abdeckung verschiedener Standorttypen zu gewährleisten.

**Methodik:**
1.  **Datenabfrage:** Es wurden OSM-Knoten für eine große Auswahl an primären OSM-Tags abgefragt (siehe [OSM Map Features](https://wiki.openstreetmap.org/wiki/Map_features)). Dazu gehören unter anderem:
    *   `amenity=*` (z.B. Restaurants, Schulen, Banken)
    *   `shop=*` (Geschäfte aller Art)
    *   `tourism=*` (z.B. Hotels, Museen, Sehenswürdigkeiten)
    *   `leisure=*` (z.B. Parks, Stadien, Fitnesscenter)
    *   `building=*` (benannte Gebäude)
    *   ... und viele weitere.
2.  **Bereinigung und Filterung:** Die Namen wurden dedupliziert und gefiltert, um Einträge ohne alphabetische Zeichen (z.B. reine Nummern) und gängige Platzhalter wie "no name" zu entfernen.

## Struktur des Repositories

```
.
├── data/
│   ├── hospital/         # Textdateien mit Namen von Gesundheitseinrichtungen
│   ├── organization/     # Textdateien mit Namen von Organisationen
│   └── other/            # Textdateien mit Namen sonstiger Orte
│
├── notebooks/            # Jupyter Notebooks zur Replikation der Datenerhebung und -filterung
│
└── README.de.md             # Diese Datei
```

## Wie man dieses Repository nutzt

*   **Verwendung der Daten:** Sie können die `.txt`-Dateien im `/data`-Verzeichnis direkt in Ihren Projekten verwenden. Beachten Sie bitte die Lizenz- und Attributionsanforderungen.
*   **Replikation des Prozesses:** Die `/notebooks` enthalten den gesamten Python-Code, um die Datenabfragen und Filterprozesse selbst auszuführen. Dies ist nützlich, wenn Sie die Methodik anpassen, Daten für eine andere Region sammeln oder aktuellere Daten abrufen möchten. Benötigte Hauptbibliotheken sind `overpy` und `spacy`.

## Lizenz und Attribution

Die Skripte und Notebooks in diesem Repository werden unter der **MIT-Lizenz** veröffentlicht.

Die Daten in den `.txt`-Dateien stammen von OpenStreetMap und unterliegen der **Open Database License (ODbL)**. Wenn Sie diese Daten verwenden oder weiterverbreiten, sind Sie verpflichtet, OpenStreetMap und seine Mitwirkenden zu nennen. 

Weitere Informationen finden Sie unter [www.openstreetmap.org/copyright](http://www.openstreetmap.org/copyright).

## Förderung

Diese Arbeit wurde vom Bundesministerium für Bildung und Forschung (BMBF) im Rahmen des GeMTeX-Projekts gefördert (Förderkennzeichen: 01ZZ2314I).

