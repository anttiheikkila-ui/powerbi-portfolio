# DAX Measures

## Total Stock

Calculates the total inventory quantity across all warehouses.

```DAX
Total Stock =
SUM(Inventory[StockQty])
```

## Product Count

Counts the number of unique products.

```DAX
Product Count =
DISTINCTCOUNT(Products[ProductID])
```

## Inventory Value

Calculates the total inventory value.

```DAX
Inventory Value =
SUMX(
    Inventory,
    Inventory[StockQty] *
    RELATED(Products[UnitCost])
)
```

## Products Below Reorder Point

Counts products that are below their reorder point.

```DAX
Products Below Reorder Point =
COUNTROWS(
    FILTER(
        Inventory,
        Inventory[StockQty] < Inventory[ReorderPoint]
    )
)
```

## Products Below Safety Stock

Counts products that are below their safety stock level.

```DAX
Products Below Safety Stock =
COUNTROWS(
    FILTER(
        Inventory,
        Inventory[StockQty] < Inventory[SafetyStock]
    )
)
```

## Inventory Turnover

Measures how efficiently inventory is moving.

```DAX
Inventory Turnover =
DIVIDE(
    [Total Goods Issues],
    [Total Stock]
)
```

## Inventory Health %

Measures the percentage of products above reorder point.

```DAX
Inventory Health % =
DIVIDE(
    [Product Count] - [Products Below Reorder Point],
    [Product Count]
)
```

