[![en](https://img.shields.io/badge/lang-EN-informational)](README.md)
[![de](https://img.shields.io/badge/lang-DE-informational)](README.de.md)

# OSM-Based Location Entity Datasets

This repository serves as a supplementary resource to disclose the methodology used for creating location-based entity lists. These lists were used for generating surrogate data in a research project and are based entirely on data from OpenStreetMap (OSM).

## Overview

The creation of high-quality surrogate data requires realistic and diverse entities. For location-based entities such as organizations, healthcare facilities, and other categorical location types, OpenStreetMap is an ideal data source.

### What is OpenStreetMap (OSM)?

[OpenStreetMap](https://www.openstreetmap.org/) is a collaborative project to create a free, editable map of the world. Similar to Wikipedia, its vast database, contributed by volunteers, is constantly being expanded and updated. The data is available under the **Open Database License (ODbL)**, making it an excellent resource for research and development. Its strength lies in the detailed classification of objects through a flexible tagging system (e.g., `shop=supermarket`, `amenity=hospital`).

This repository transparently documents how we utilized this resource to create three specific datasets for the German-speaking region:
1.  **Healthcare Facilities** (`hospital`)
2.  **Organizations** (`organization`)
3.  **Other Locations** (`other`)

## Datasets and Creation Methodology

Each dataset was created through a specific query to the Overpass API of OSM, followed by filtering and cleaning steps. The Jupyter Notebooks in this repository (`/notebooks`) document the entire process in detail.

### 1. Healthcare Facilities (`/data/hospital`)

This dataset contains the names of hospitals, doctor's offices, and other medical facilities in Germany.

**Methodology:**
1.  **Data Query:** All nodes, ways, and relations in Germany tagged with `healthcare=*` were queried. To expand context, the name was supplemented with the value of the `healthcare:speciality` tag (e.g., "Klinikum Musterstadt / general").
2.  **Filtering of Person Names (NER):** Many entries in OSM are names of doctors (e.g., "Dr. Max Mustermann"). To remove these, a Named Entity Recognition (NER) model from SpaCy (`de_core_news_lg`) was used. All entities classified as `PER` (Person) were provisionally removed.
3.  **Keyword-based Reclassification:** Since the NER model can also misclassify legitimate facility names (e.g., "Praxis Dr. Schmidt") as persons, the removed names were reviewed again. Entries containing medical keywords such as `Klinik`, `Praxis`, `Zentrum`, `Therapie`, etc., were added back to the list of healthcare facilities.
4.  **RegEx-based Filtering:** An additional filter using regular expressions was applied to identify and remove remaining typical doctor's names (e.g., "Dr. med. M. Müller & Kollegen").
5.  **Exclusion:** Entries containing "Apotheke" (pharmacy) were moved to a separate file, as they represent a distinct category.

### 2. Organizations (`/data/organization`)

This dataset includes a wide range of organizations, including companies, workshops, clubs, and industrial sites.

**Methodology:**
1.  **Data Query:** All OSM nodes in Germany that were tagged with one of the following primary tags and had a name (`name`) were queried:
    *   `office=*` (Offices, agencies, firms)
    *   `craft=*` (Craft businesses like bakeries, carpenters, workshops)
    *   `club=*` (Clubhouses and meeting places)
    *   `industrial=*` (Industrial sites)
2.  **Cleaning:** The resulting list was deduplicated and sorted alphabetically. No further complex filtering was applied, as the tags already provide a good demarcation.

### 3. Other Locations (`/data/other`)

This dataset is a heterogeneous collection of named places not covered by the categorized location types. It serves to ensure broad coverage of various location types.

**Methodology:**
1.  **Data Query:** OSM nodes for a large selection of primary OSM tags were queried (see [OSM Map Features](https://wiki.openstreetmap.org/wiki/Map_features)). These include, among others:
    *   `amenity=*` (e.g., restaurants, schools, banks)
    *   `shop=*` (shops of all kinds)
    *   `tourism=*` (e.g., hotels, museums, attractions)
    *   `leisure=*` (e.g., parks, stadiums, fitness centers)
    *   `building=*` (named buildings)
    *   ... and many more.
2.  **Cleaning and Filtering:** The names were deduplicated and filtered to remove entries without alphabetic characters (e.g., pure numbers) and common placeholders like "no name".

## Repository Structure

```
.
├── data/
│ ├── hospital/         # Text files with names of healthcare facilities
│ ├── organization/     # Text files with names of organizations
│ └── other/            # Text files with names of other locations
│
├── notebooks/          # Jupyter Notebooks to replicate the data collection and filtering
│
└── README.md           # This file
```

## How to Use This Repository

*   **Using the Data:** You can use the `.txt` files in the `/data` directory directly in your projects. Please observe the license and attribution requirements.
*   **Replicating the Process:** The `/notebooks` contain the complete Python code to run the data queries and filtering processes yourself. This is useful if you want to adapt the methodology, collect data for a different region, or retrieve more current data. The main libraries required are `overpy` and `spacy`.

## License and Attribution

The scripts and notebooks in this repository are published under the **MIT License**.

The data in the `.txt` files originates from OpenStreetMap and is subject to the **Open Database License (ODbL)**. If you use or redistribute this data, you are required to credit OpenStreetMap and its contributors. For more information, please visit [www.openstreetmap.org/copyright](http://www.openstreetmap.org/copyright).

### Funding

This work was funded by the **German Federal Ministry of Education and Research (BMBF)** within the **GeMTeX project** (funding number: `01ZZ2314I`).