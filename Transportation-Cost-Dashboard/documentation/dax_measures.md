# DAX Measures

This document contains the DAX measures used in the Transportation Cost Dashboard project.

---

## Executive Overview Measures

### Total Shipments

Calculates the total number of shipments.

```DAX
Total Shipments =
DISTINCTCOUNT(ShipmentsTable[ShipmentID])
```

### Freight Managed Shipments

Calculates shipments where the seller is responsible for freight cost.

```DAX
Freight Managed Shipments =
CALCULATE(
    DISTINCTCOUNT(ShipmentsTable[ShipmentID]),
    ShipmentsTable[CostEUR] > 0
)
```

### Total Freight Cost

Calculates total freight cost.

```DAX
Total Freight Cost =
SUM(ShipmentsTable[CostEUR])
```

### Average Cost per Shipment

Calculates average freight cost per freight-managed shipment.

```DAX
Average Cost per Shipment =
DIVIDE(
    [Total Freight Cost],
    [Freight Managed Shipments]
)
```

### On-Time Delivery %

Calculates the percentage of shipments delivered on time.

```DAX
On-Time Delivery % =
DIVIDE(
    CALCULATE(
        COUNTROWS(ShipmentsTable),
        ShipmentsTable[OnTimeDelivery] = "Yes"
    ),
    COUNTROWS(ShipmentsTable)
)
```

---

## Carrier Performance Measures

### Cost per Shipment

Calculates average cost per freight-managed shipment.

```DAX
Cost per Shipment =
DIVIDE(
    [Total Freight Cost],
    [Freight Managed Shipments]
)
```

### Average Transit Days

Calculates average shipment transit time.

```DAX
Average Transit Days =
AVERAGE(ShipmentsTable[TransitDays])
```

---

## Route Overview Measures

### Total Routes

Calculates the number of unique transportation routes.

```DAX
Total Routes =
DISTINCTCOUNT(ShipmentsTable[Route])
```

### Average Distance

Calculates average route distance.

```DAX
Average Distance =
AVERAGE(CountriesTable[DistanceKm])
```

### Average Freight Cost

Calculates average freight cost for freight-managed shipments.

```DAX
Average Freight Cost =
DIVIDE(
    [Total Freight Cost],
    [Freight Managed Shipments]
)
```