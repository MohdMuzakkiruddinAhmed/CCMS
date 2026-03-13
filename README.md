# CCMS — Case Count Metric System

A tool for comparing entity resolution (ER) clustering outcomes without requiring ground truth.


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

## Overview

CCMS classifies how clusters from a baseline ER process (ER1) are transformed by a second ER process (ER2) into four mutually exclusive categories:

| Case          | Description                                      |
|---------------|--------------------------------------------------|
| **Unchanged** | ER1 cluster identical to an ER2 cluster          |
| **Merged**    | ER1 cluster is a proper subset of an ER2 cluster |
| **Partitioned** | ER1 cluster split into multiple ER2 clusters   |
| **Overlapping** | Complex reorganization across ER2 clusters     |

## Three Implementations

| Implementation     | Location   | Use Case                          |
|--------------------|------------|-----------------------------------|
| Python module      | `ccms/`    | Scripting, batch, automation      |
| Flask web app      | `webapp/`  | Interactive browser-based analysis|
| SQL queries        | `sql/`     | Database-resident ER outputs      |

## Quick Start

### Python Module
```bash
pip install -r requirements.txt
python -m ccms.core examples/example_16ref/er1.csv examples/example_16ref/er2.csv
```

### Flask Web App
```bash
cd webapp
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

### SQL
```bash
# Load into your database
psql -d your_db -f sql/create_tables.sql
psql -d your_db -f sql/example_data.sql
psql -d your_db -f sql/ccms_views.sql
psql -d your_db -f sql/ccms_case_counts.sql
```

## Input Format

Two CSV files, each with two columns:

**er1.csv**
```
RecID,ClusterID
1,a
2,b
3,b
```

**er2.csv**
```
RecID,ClusterID
1,x
2,y
3,y
```

## Citation

If you use CCMS in your research, please cite:

```bibtex
@article{talburt2025ccms,
  title   = {Case Count Metric for Comparative Analysis
             of Entity Resolution Results},
  author  = {Talburt, John R. and Mohammed, Muzakkiruddin Ahmed
             and Cakmak, Mert Can and Mohammed, Onais Khan
             and Mohammed, Mahboob Khan and Syed, Khizer
             and Claassens, Leon},
  journal = {Frontiers in Big Data},
  year    = {2025}
}
```

## License

MIT License. See LICENSE for details.
