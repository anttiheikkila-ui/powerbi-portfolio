# DAX Measures Summary

## Executive Overview Measures

### Total Stock
Calculates the total inventory quantity across all warehouses.

```DAX
Total Stock =
SUM(Inventory[StockQty])
```

### Product Count
Counts the number of unique products.

```DAX
Product Count =
DISTINCTCOUNT(Products[ProductID])
```

### Inventory Value
Calculates the total inventory value.

```DAX
Inventory Value =
SUMX(
    Inventory,
    Inventory[StockQty] *
    RELATED(Products[UnitCost])
)
```

### Total Goods Issues
Calculates the total quantity of inventory issued from stock.

```DAX
Total Goods Issues =
ABS(
    CALCULATE(
        SUM(Transactions[Qty]),
        Transactions[MovementType] = "Goods Issue"
    )
)
```

---

## Inventory Analysis Measures

### Products Below Reorder Point
Counts products below reorder point.

```DAX
Products Below Reorder Point =
COUNTROWS(
    FILTER(
        Inventory,
        Inventory[StockQty] < Inventory[ReorderPoint]
    )
)
```

### Products Below Safety Stock
Counts products below safety stock.

```DAX
Products Below Safety Stock =
COUNTROWS(
    FILTER(
        Inventory,
        Inventory[StockQty] < Inventory[SafetyStock]
    )
)
```

### Inventory Turnover
Measures inventory movement efficiency.

```DAX
Inventory Turnover =
DIVIDE(
    [Total Goods Issues],
    [Total Stock]
)
```

### Inventory Health %
Measures inventory health based on reorder point compliance.

```DAX
Inventory Health % =
DIVIDE(
    [Product Count] - [Products Below Reorder Point],
    [Product Count]
)
```

### Reorder Gap
Measures the difference between stock quantity and reorder point.

```DAX
Reorder Gap =
SUM(Inventory[ReorderPoint]) -
SUM(Inventory[StockQty])
```

---

## Warehouse Operations Measures

### Total Goods Receipts
Calculates the total quantity of received inventory.

```DAX
Total Goods Receipts =
CALCULATE(
    SUM(Transactions[Qty]),
    Transactions[MovementType] = "Goods Receipt"
)
```

### Total Goods Issues
Calculates the total quantity of issued inventory.

```DAX
Total Goods Issues =
ABS(
    CALCULATE(
        SUM(Transactions[Qty]),
        Transactions[MovementType] = "Goods Issue"
    )
)
```

### Total Transfers
Calculates the total quantity of inventory transfers.

```DAX
Total Transfers =
ABS(
    CALCULATE(
        SUM(Transactions[Qty]),
        Transactions[MovementType] = "Transfer"
    )
)
```

### Inventory Adjustments
Calculates inventory corrections and stock adjustments.

```DAX
Inventory Adjustments =
COALESCE(
    ABS(
        CALCULATE(
            SUM(Transactions[Qty]),
            Transactions[MovementType] = "Adjustment"
        )
    ),
    0
)
```