# CCMS SQL Implementation

Standard SQL queries for computing CCMS case counts when ER outputs are stored in a relational database.

## Prerequisites

A single table with three columns:

| Column          | Type    | Description              |
|-----------------|---------|--------------------------|
| RecID           | VARCHAR | Unique record identifier |
| ER1_ClusterID   | VARCHAR | Cluster ID from ER1      |
| ER2_ClusterID   | VARCHAR | Cluster ID from ER2      |

## Usage Order

1. `create_tables.sql`   — Create the records table
2. `example_data.sql`    — Load the 16-reference example
3. `ccms_views.sql`      — Create analysis and case views
4. `ccms_case_counts.sql`— Aggregate case counts
5. `ccms_drilldown.sql`  — Drill-down by case type

Tested on PostgreSQL 15, MySQL 8, and SQLite 3.
