# OSM Location Data Collection

This repository contains text datasets derived from OpenStreetMap (OSM) for German points of interest. The data was collected via the OSM Overpass API and further filtered to remove person names.

The repository is provided as an example of how we retrieved and processed the data. It includes the raw text files as well as the Jupyter notebooks used to download and clean the data. You are free to adapt the notebooks or the simple Python scripts below to replicate our procedure or to collect other types of OSM data.

## Directory structure

```
.
├── data
│   ├── location_hospital
│   ├── location_organization
│   └── location_other
└── notebook
```

- **data/** contains the resulting text lists with one location name per line. Each subfolder represents a group of locations (e.g. hospitals, organisations or other features).
- **notebook/** contains the original Jupyter notebooks used during the collection.

## Usage

The notebooks can be executed with Python 3.10+. The required packages are listed in `requirements.txt`.

Example to recreate the list of healthcare facility names:

```bash
python scripts/fetch_hospitals.py --output data/location_hospital/location_hospital.txt
```

The scripts use the Overpass API which has rate limits. If you encounter HTTP errors, please try again later.

## License

The scripts in this repository are released under the MIT License. The text data was generated from public OpenStreetMap data which is licensed under the Open Database License (ODbL). Please credit OpenStreetMap contributors if you redistribute the data.
