# Project Summary

# Transportation Cost Dashboard

## Objective

The objective of this project is to demonstrate how Power BI can be used to analyze transportation costs, carrier performance and logistics operations through interactive dashboards and business-oriented KPIs.

The solution is inspired by real-world supply chain and SAP S/4HANA logistics processes, providing valuable insights into freight costs, transit times, carrier performance and transportation routes.

---

## Business Problem

Transportation costs represent a significant portion of supply chain expenses. Without proper visibility, organizations may struggle to identify inefficient carriers, expensive routes or poor delivery performance.

This dashboard helps answer key business questions such as:

- Which carriers provide the best overall performance?
- Which transportation routes generate the highest freight costs?
- What is the average transportation cost per shipment?
- Which countries generate the highest logistics costs?
- How do Incoterms affect freight responsibility?
- How reliable are carriers in terms of on-time delivery?

---

## Dashboard Pages

### Executive Overview

Provides a high-level summary of transportation performance through key logistics KPIs.

**Key Metrics**

- Total Shipments
- Total Freight Cost
- Average Cost per Shipment
- On-Time Delivery %

**Business Value**

- Supports executive decision-making
- Provides visibility into transportation performance
- Monitors logistics spending
- Tracks service level performance

---

### Carrier Performance

Analyzes carrier efficiency and service quality.

**Key Metrics**

- Cost per Shipment
- Average Transit Days
- On-Time Delivery %
- Freight Cost by Carrier

**Business Value**

- Compares carrier performance
- Identifies high-cost carriers
- Supports carrier selection
- Evaluates service quality

---

### Route Overview

Focuses on transportation routes and destination analysis.

**Key Metrics**

- Total Routes
- Average Distance
- Average Freight Cost

**Business Value**

- Identifies expensive destinations
- Compares transportation routes
- Supports route optimization
- Improves logistics planning

---

## Data Model

The dashboard follows a dimensional star schema.

### Fact Table

- Shipments

### Dimension Tables

- Carriers
- Countries
- Incoterms
- Calendar

---

## Technologies Used

- Power BI
- DAX
- Power Query
- Excel
- GitHub

---

## Skills Demonstrated

- Data Modeling
- Star Schema Design
- DAX Development
- Power Query Data Transformation
- KPI Design
- Transportation Cost Analysis
- Carrier Performance Analysis
- Supply Chain Analytics
- Interactive Dashboard Design
- Business Intelligence Reporting

---

## Business Rules

The mock data includes realistic logistics business rules.

- EXW and FCA shipments generate no freight cost for the seller.
- DAP, DDP, CPT and CIP shipments include freight costs.
- Transportation costs vary by carrier, destination and Incoterm.
- On-Time Delivery performance is measured for every shipment.

---

## Lessons Learned

During this project I gained practical experience in building a complete transportation analytics solution using Power BI.

Key learnings included:

- Designing a dimensional star schema
- Creating relationships between fact and dimension tables
- Building business-focused DAX measures
- Using Power Query for data transformation
- Designing dashboards for different business users
- Applying transportation and logistics concepts to business analytics
- Creating professional project documentation using GitHub

This project strengthened my understanding of how transportation data can be transformed into meaningful business insights through interactive reporting.

---

## Future Enhancements

Potential future improvements include:

- CO₂ Emissions Analysis
- Cost per Kilometer
- Cost per Kilogram
- Cost per Pallet
- Carrier Scorecard
- Route Profitability Analysis
- Delivery Delay Analysis
- Interactive Geographic Maps
- SAP Transportation Management (TM) Integration
- Power BI Service Deployment with Scheduled Refresh

---

## Conclusion

This project demonstrates how Power BI can transform transportation data into actionable business insights. By combining dimensional modeling, DAX calculations and interactive visualizations, the dashboard supports data-driven logistics decisions and reflects real-world transportation management practices.