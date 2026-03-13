# 16-Reference Example

This example is taken directly from Table 2 of the paper.

## Input Data

**ER1 clustering:**

| RecID | ClusterID |
|-------|-----------|
| 1 | a |
| 2 | b |
| 3 | b |
| 4 | c |
| 5 | c |
| 6 | c |
| 7 | d |
| 8 | e |
| 9 | e |
| 10 | e |
| 11 | f |
| 12 | f |
| 13 | f |
| 14 | g |
| 15 | g |
| 16 | g |

**ER2 clustering:**

| RecID | ClusterID |
|-------|-----------|
| 1 | x |
| 2 | y |
| 3 | y |
| 4 | z |
| 5 | z |
| 6 | z |
| 7 | z |
| 8 | w |
| 9 | w |
| 10 | t |
| 11 | u |
| 12 | u |
| 13 | v |
| 14 | u |
| 15 | v |
| 16 | s |

## Expected Results

| Metric | Value |
|--------|-------|
| CC1 | 7 |
| CC2 | 8 |
| SC1 | 2 |
| SC2 | 3 |
| UC | 2 |
| MC | 2 |
| PC | 1 |
| OC | 2 |

## Running the Example

```bash
python examples/example_16ref/run_example.py
```
