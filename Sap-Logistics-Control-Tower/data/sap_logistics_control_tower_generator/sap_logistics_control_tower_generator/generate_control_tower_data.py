from __future__ import annotations

import argparse
import random
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

SEED = 42
START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 6, 30)
SNAPSHOT_DATE = date(2026, 6, 30)

MATERIAL_GROUPS = [
    "Bearings", "Electrical", "Hydraulics", "Pneumatics", "Fasteners",
    "Motors", "Packaging", "Safety", "Tools", "Belts"
]
WAREHOUSES = [
    ("WH01", "Tampere Central Warehouse", "Tampere"),
    ("WH02", "Oulu Regional Warehouse", "Oulu"),
    ("WH03", "Jyväskylä Distribution Center", "Jyväskylä"),
]
COUNTRIES = [
    ("FI", "Finland", "Nordics", 250), ("SE", "Sweden", "Nordics", 650),
    ("NO", "Norway", "Nordics", 900), ("DK", "Denmark", "Nordics", 1000),
    ("DE", "Germany", "Central Europe", 1650), ("NL", "Netherlands", "Western Europe", 1850),
    ("PL", "Poland", "Central Europe", 1450), ("FR", "France", "Western Europe", 2400),
    ("IT", "Italy", "Southern Europe", 2900), ("ES", "Spain", "Southern Europe", 3500),
    ("US", "United States", "North America", 7200), ("CN", "China", "Asia", 7700),
]
CARRIERS = [
    ("CAR01", "DHL Freight", "Road", 0.92), ("CAR02", "DB Schenker", "Road", 0.90),
    ("CAR03", "DSV", "Road", 0.93), ("CAR04", "Kuehne+Nagel", "Road", 0.91),
    ("CAR05", "FedEx", "Air", 0.94), ("CAR06", "UPS", "Air", 0.93),
    ("CAR07", "Maersk", "Sea", 0.84), ("CAR08", "MSC", "Sea", 0.82),
]
INCOTERMS = [
    ("EXW", "Ex Works", False), ("FCA", "Free Carrier", False),
    ("CPT", "Carriage Paid To", True), ("CIP", "Carriage and Insurance Paid To", True),
    ("DAP", "Delivered At Place", True), ("DDP", "Delivered Duty Paid", True),
]


def dates_between(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def make_master_data(rng: random.Random, fake: Faker):
    products = []
    for i in range(1, 121):
        group = rng.choice(MATERIAL_GROUPS)
        safety = rng.randint(10, 120)
        reorder = safety + rng.randint(10, 160)
        products.append({
            "ProductID": f"MAT{100000+i}",
            "ProductName": f"{group} Item {i:03d}",
            "MaterialGroup": group,
            "Unit": rng.choice(["EA", "M", "KG", "SET"]),
            "StandardCostEUR": round(rng.uniform(2.5, 850), 2),
            "SafetyStock": safety,
            "ReorderPoint": reorder,
            "CriticalMaterial": "Yes" if rng.random() < 0.18 else "No",
        })

    suppliers = []
    supplier_countries = ["Finland", "Sweden", "Germany", "Poland", "Netherlands", "China", "Italy"]
    lead_times = {"Finland": 5, "Sweden": 7, "Germany": 10, "Poland": 9, "Netherlands": 11, "China": 32, "Italy": 14}
    for i in range(1, 25):
        country = rng.choice(supplier_countries)
        suppliers.append({
            "SupplierID": f"SUP{i:03d}",
            "SupplierName": fake.company(),
            "Country": country,
            "LeadTimeDays": lead_times[country] + rng.randint(-2, 5),
            "OTDTarget": round(rng.uniform(0.90, 0.98), 3),
            "ReliabilityScore": round(rng.uniform(0.78, 0.98), 3),
        })

    warehouses = pd.DataFrame(WAREHOUSES, columns=["WarehouseID", "WarehouseName", "City"])
    countries = pd.DataFrame(COUNTRIES, columns=["CountryID", "Country", "Region", "DistanceKm"])
    carriers = pd.DataFrame(CARRIERS, columns=["CarrierID", "CarrierName", "TransportMode", "ReliabilityScore"])
    incoterms = pd.DataFrame(INCOTERMS, columns=["Incoterm", "Description", "SellerPaysFreight"])

    calendar = pd.DataFrame({"Date": pd.to_datetime(dates_between(START_DATE, END_DATE))})
    calendar["Year"] = calendar["Date"].dt.year
    calendar["MonthNumber"] = calendar["Date"].dt.month
    calendar["MonthName"] = calendar["Date"].dt.month_name()
    calendar["YearMonth"] = calendar["Date"].dt.strftime("%Y-%m")
    calendar["Quarter"] = "Q" + calendar["Date"].dt.quarter.astype(str)

    return (
        pd.DataFrame(products), pd.DataFrame(suppliers), warehouses,
        countries, carriers, incoterms, calendar
    )


def make_purchase_orders(rng, products, suppliers, warehouses):
    supplier_lookup = suppliers.set_index("SupplierID").to_dict("index")
    rows = []
    order_dates = dates_between(START_DATE, END_DATE - timedelta(days=15))
    for i in range(1, 1601):
        supplier_id = rng.choice(suppliers["SupplierID"].tolist())
        s = supplier_lookup[supplier_id]
        order_date = rng.choice(order_dates)
        requested = order_date + timedelta(days=s["LeadTimeDays"])
        late = rng.random() > s["ReliabilityScore"]
        delay = rng.randint(1, 18) if late else rng.randint(-3, 1)
        actual = requested + timedelta(days=delay)
        qty = rng.randint(20, 600)
        unit_price = round(rng.uniform(5, 900), 2)
        status = "Open" if actual > SNAPSHOT_DATE else ("Late" if late else "Delivered")
        rows.append({
            "PurchaseOrderID": f"PO{4500000000+i}", "OrderDate": pd.Timestamp(order_date),
            "RequestedDeliveryDate": pd.Timestamp(requested), "ActualDeliveryDate": pd.Timestamp(actual),
            "SupplierID": supplier_id, "ProductID": rng.choice(products["ProductID"].tolist()),
            "WarehouseID": rng.choice(warehouses["WarehouseID"].tolist()), "OrderQty": qty,
            "UnitPriceEUR": unit_price, "POValueEUR": round(qty * unit_price, 2),
            "Status": status, "DelayDays": max(delay, 0), "Confirmed": "No" if rng.random() < 0.06 else "Yes",
        })
    return pd.DataFrame(rows)


def make_inventory(rng, products, warehouses):
    rows = []
    for p in products.to_dict("records"):
        for wh in warehouses["WarehouseID"]:
            stock = max(0, int(p["ReorderPoint"] * rng.uniform(0.6, 2.8)))
            roll = rng.random()
            if roll < 0.08:
                stock = rng.randint(0, max(1, p["SafetyStock"] - 1))
            elif roll < 0.22:
                stock = rng.randint(p["SafetyStock"], max(p["SafetyStock"], p["ReorderPoint"] - 1))
            blocked = int(stock * rng.uniform(0, 0.08))
            rows.append({
                "SnapshotDate": pd.Timestamp(SNAPSHOT_DATE), "ProductID": p["ProductID"],
                "WarehouseID": wh, "StockQty": stock, "BlockedStockQty": blocked,
                "AvailableStockQty": max(stock - blocked, 0), "SafetyStock": p["SafetyStock"],
                "ReorderPoint": p["ReorderPoint"], "InventoryValueEUR": round(stock * p["StandardCostEUR"], 2),
            })
    return pd.DataFrame(rows)


def choose_incoterm(rng, country_id):
    if country_id in {"FI", "SE", "NO", "DK"}:
        weights = [20, 25, 25, 10, 15, 5]
    elif country_id in {"US", "CN"}:
        weights = [5, 10, 20, 15, 25, 25]
    else:
        weights = [10, 15, 30, 15, 20, 10]
    return rng.choices([x[0] for x in INCOTERMS], weights=weights)[0]


def make_deliveries_and_shipments(rng, products, warehouses, countries, carriers):
    deliveries, shipments = [], []
    country_lookup = countries.set_index("CountryID").to_dict("index")
    carrier_lookup = carriers.set_index("CarrierID").to_dict("index")
    ship_dates = dates_between(START_DATE, END_DATE - timedelta(days=10))

    for i in range(1, 1401):
        country_id = rng.choice(countries["CountryID"].tolist())
        carrier_id = rng.choice(carriers["CarrierID"].tolist())
        country, carrier = country_lookup[country_id], carrier_lookup[carrier_id]
        incoterm = choose_incoterm(rng, country_id)
        requested = rng.choice(ship_dates)
        shipment_date = requested - timedelta(days=rng.randint(1, 5))
        base_transit = max(1, round(country["DistanceKm"] / 650))
        if carrier["TransportMode"] == "Air":
            base_transit = max(1, round(base_transit * 0.35))
        elif carrier["TransportMode"] == "Sea":
            base_transit = max(5, round(base_transit * 2.2))
        delayed = rng.random() > carrier["ReliabilityScore"]
        delay_days = rng.randint(1, 8) if delayed else rng.choice([0, 0, 0, 1])
        actual = requested + timedelta(days=delay_days)
        qty = rng.randint(1, 180)
        delivered_qty = qty if rng.random() > 0.07 else max(1, qty - rng.randint(1, max(1, qty // 3)))
        on_time, in_full = actual <= requested, delivered_qty >= qty
        delivery_id, shipment_id = f"DLV{800000000+i}", f"SHP{900000000+i}"

        deliveries.append({
            "DeliveryID": delivery_id, "RequestedDeliveryDate": pd.Timestamp(requested),
            "ActualDeliveryDate": pd.Timestamp(actual), "ProductID": rng.choice(products["ProductID"].tolist()),
            "WarehouseID": rng.choice(warehouses["WarehouseID"].tolist()), "CountryID": country_id,
            "OrderQty": qty, "DeliveredQty": delivered_qty,
            "DeliveryStatus": "Delayed" if delayed else "On Time",
            "OnTime": "Yes" if on_time else "No", "InFull": "Yes" if in_full else "No",
            "OTIF": "Yes" if on_time and in_full else "No", "DelayDays": max((actual-requested).days, 0),
        })

        seller_pays = incoterm not in {"EXW", "FCA"}
        weight = round(rng.uniform(30, 7000), 1)
        pallets = max(1, round(weight / rng.uniform(350, 700)))
        factor = {"Road": 1.0, "Air": 4.5, "Sea": 0.65}[carrier["TransportMode"]]
        cost = 0.0 if not seller_pays else round(
            (120 + country["DistanceKm"] * 0.55 + weight * 0.12) * factor * rng.uniform(0.85, 1.2), 2
        )
        shipments.append({
            "ShipmentID": shipment_id, "DeliveryID": delivery_id,
            "ShipmentDate": pd.Timestamp(shipment_date), "CarrierID": carrier_id,
            "CountryID": country_id, "Incoterm": incoterm,
            "TransportMode": carrier["TransportMode"], "DistanceKm": country["DistanceKm"],
            "WeightKg": weight, "Pallets": pallets, "TransitDays": max(1, base_transit + delay_days),
            "FreightCostEUR": cost, "SellerPaysFreight": "Yes" if seller_pays else "No",
            "OnTimeDelivery": "Yes" if on_time else "No", "Route": f"FI-{country_id}",
        })
    return pd.DataFrame(deliveries), pd.DataFrame(shipments)


def make_exceptions(purchase_orders, inventory, deliveries, shipments):
    rows, n = [], 1
    for r in purchase_orders.itertuples(index=False):
        if r.Status in {"Late", "Open"} and r.DelayDays > 0:
            rows.append({"ExceptionID": f"EXC{n:06d}", "ExceptionDate": r.RequestedDeliveryDate,
                         "Process": "Procurement", "ExceptionType": "Overdue Purchase Order",
                         "Severity": "Critical" if r.DelayDays >= 10 else "High",
                         "ReferenceID": r.PurchaseOrderID,
                         "Description": f"Purchase order delayed by {r.DelayDays} days", "Status": "Open"}); n += 1
        if r.Confirmed == "No":
            rows.append({"ExceptionID": f"EXC{n:06d}", "ExceptionDate": r.OrderDate,
                         "Process": "Procurement", "ExceptionType": "Missing Supplier Confirmation",
                         "Severity": "Medium", "ReferenceID": r.PurchaseOrderID,
                         "Description": "Supplier confirmation missing", "Status": "Open"}); n += 1
    for r in inventory.itertuples(index=False):
        if r.AvailableStockQty < r.SafetyStock:
            level, severity = "Below Safety Stock", "Critical"
        elif r.AvailableStockQty < r.ReorderPoint:
            level, severity = "Below Reorder Point", "High"
        else:
            continue
        rows.append({"ExceptionID": f"EXC{n:06d}", "ExceptionDate": r.SnapshotDate,
                     "Process": "Inventory", "ExceptionType": level, "Severity": severity,
                     "ReferenceID": f"{r.ProductID}-{r.WarehouseID}",
                     "Description": level, "Status": "Open"}); n += 1
    for r in deliveries.itertuples(index=False):
        if r.OTIF == "No":
            rows.append({"ExceptionID": f"EXC{n:06d}", "ExceptionDate": r.ActualDeliveryDate,
                         "Process": "Delivery", "ExceptionType": "OTIF Failure",
                         "Severity": "High" if r.DelayDays >= 3 else "Medium",
                         "ReferenceID": r.DeliveryID,
                         "Description": "Delivery failed on-time-in-full requirement", "Status": "Open"}); n += 1
    threshold = shipments.loc[shipments["FreightCostEUR"] > 0, "FreightCostEUR"].quantile(0.93)
    for r in shipments.itertuples(index=False):
        if r.FreightCostEUR > threshold:
            rows.append({"ExceptionID": f"EXC{n:06d}", "ExceptionDate": r.ShipmentDate,
                         "Process": "Transportation", "ExceptionType": "High Freight Cost",
                         "Severity": "Medium", "ReferenceID": r.ShipmentID,
                         "Description": "Freight cost exceeds portfolio threshold", "Status": "Open"}); n += 1
    return pd.DataFrame(rows)


def validate(products, suppliers, warehouses, countries, carriers, po, inventory, deliveries, shipments):
    assert po["ProductID"].isin(products["ProductID"]).all()
    assert po["SupplierID"].isin(suppliers["SupplierID"]).all()
    assert inventory["WarehouseID"].isin(warehouses["WarehouseID"]).all()
    assert deliveries["CountryID"].isin(countries["CountryID"]).all()
    assert shipments["CarrierID"].isin(carriers["CarrierID"]).all()
    assert (inventory["StockQty"] >= 0).all()
    assert (shipments.loc[shipments["Incoterm"].isin(["EXW", "FCA"]), "FreightCostEUR"] == 0).all()
    for df, key in [(products, "ProductID"), (suppliers, "SupplierID"), (deliveries, "DeliveryID"), (shipments, "ShipmentID")]:
        assert not df[key].duplicated().any()


def main():
    parser = argparse.ArgumentParser(description="Generate SAP Logistics Control Tower mock data")
    parser.add_argument("--output", default="data/processed")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    np.random.seed(args.seed)
    fake = Faker(); Faker.seed(args.seed)

    products, suppliers, warehouses, countries, carriers, incoterms, calendar = make_master_data(rng, fake)
    po = make_purchase_orders(rng, products, suppliers, warehouses)
    inventory = make_inventory(rng, products, warehouses)
    deliveries, shipments = make_deliveries_and_shipments(rng, products, warehouses, countries, carriers)
    exceptions = make_exceptions(po, inventory, deliveries, shipments)

    validate(products, suppliers, warehouses, countries, carriers, po, inventory, deliveries, shipments)

    tables = {
        "Products": products, "Suppliers": suppliers, "Warehouses": warehouses,
        "Countries": countries, "Carriers": carriers, "Incoterms": incoterms,
        "Calendar": calendar, "PurchaseOrders": po, "InventorySnapshots": inventory,
        "Deliveries": deliveries, "Shipments": shipments, "Exceptions": exceptions,
    }

    output = Path(args.output); output.mkdir(parents=True, exist_ok=True)
    csv_dir = output / "csv"; csv_dir.mkdir(exist_ok=True)
    for name, df in tables.items():
        df.to_csv(csv_dir / f"{name}.csv", index=False, encoding="utf-8-sig")
    excel_path = output / "sap_logistics_control_tower_data.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for name, df in tables.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
    print(f"Created {excel_path}")
    print(f"Created CSV files in {csv_dir}")


if __name__ == "__main__":
    main()
