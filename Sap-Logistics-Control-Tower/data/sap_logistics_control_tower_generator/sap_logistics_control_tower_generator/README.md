# SAP Logistics Control Tower Data Generator

Python-ohjelma generoi realistisen mock-datan Power BI -portfoliohankkeeseen.

## Taulut

- Products
- Suppliers
- Warehouses
- Countries
- Carriers
- Incoterms
- Calendar
- PurchaseOrders
- InventorySnapshots
- Deliveries
- Shipments
- Exceptions

## Liiketoimintasäännöt

- EXW- ja FCA-lähetyksillä myyjän rahtikustannus on 0 euroa.
- Toimittajilla on erilaiset läpimenoajat ja toimitusvarmuudet.
- Varastoon syntyy alle tilauspisteen ja alle safety stockin tilanteita.
- Toimituksille lasketaan On Time, In Full ja OTIF.
- Poikkeamista muodostetaan erillinen Exceptions-taulu.
- Avainten viite-eheys tarkistetaan ennen tiedostojen vientiä.

## Asennus

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

PowerShellissä:

```powershell
.venv\Scripts\Activate.ps1
```

## Ajo

```bash
python generate_control_tower_data.py
```

Vaihtoehtoinen kohdekansio ja siemenluku:

```bash
python generate_control_tower_data.py --output data/processed --seed 42
```

## Tulokset

```text
data/processed/
├── sap_logistics_control_tower_data.xlsx
└── csv/
    ├── Products.csv
    ├── Suppliers.csv
    ├── PurchaseOrders.csv
    ├── InventorySnapshots.csv
    ├── Deliveries.csv
    ├── Shipments.csv
    └── Exceptions.csv
```
