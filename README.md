# CCMS — Case Count Metric System

A tool for comparing entity resolution (ER) clustering outcomes without requiring ground truth.

[![Paper DOI](https://img.shields.io/badge/Paper-10.3389%2Ffdata.2026.1736939-087f8c)](https://doi.org/10.3389/fdata.2026.1736939)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://github.com/MohdMuzakkiruddinAhmed/CCMS/actions/workflows/tests.yml/badge.svg)](https://github.com/MohdMuzakkiruddinAhmed/CCMS/actions/workflows/tests.yml)

[Quick start](#quick-start) · [Paper](https://doi.org/10.3389/fdata.2026.1736939) · [Citation](#citation)

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
git clone https://github.com/MohdMuzakkiruddinAhmed/CCMS.git
cd CCMS
# The core module uses only the Python standard library.
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
@article{talburt2026ccms,
  title   = {Case Count Metric for Comparative Analysis
             of Entity Resolution Results},
  author  = {Talburt, John R. and Mohammed, Muzakkiruddin Ahmed
             and Cakmak, Mert Can and Mohammed, Onais Khan
             and Mohammed, Mahboob Khan and Syed, Khizer
             and Claassens, Leon},
  journal = {Frontiers in Big Data},
  year    = {2026},
  volume  = {9},
  pages   = {1736939},
  doi     = {10.3389/fdata.2026.1736939}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.
