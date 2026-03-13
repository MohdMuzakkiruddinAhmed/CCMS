# CCMS Methodology

## Overview

CCMS classifies each ER1 cluster into one of four mutually exclusive cases based on its relationship to ER2 clusters.

## Case Definitions

Let **C1** be an ER1 cluster and **U(C1)** be the union of all ER2 clusters that share at least one record with C1.

| Case | Condition |
|------|-----------|
| **Unchanged** | C1 maps to exactly one ER2 cluster, and C1 = that ER2 cluster |
| **Merged** | C1 maps to exactly one ER2 cluster, but C1 ⊂ that ER2 cluster |
| **Partitioned** | C1 maps to multiple ER2 clusters, and C1 = U(C1) |
| **Overlapping** | C1 maps to multiple ER2 clusters, and C1 ⊂ U(C1) |

## Key Properties

- The four cases are **mutually exclusive** and **exhaustive**: every ER1 cluster belongs to exactly one case.
- UC + MC + PC + OC = CC1 (total number of ER1 clusters)

## Metrics

| Metric | Description |
|--------|-------------|
| **UC** | Unchanged Count |
| **MC** | Merged Count |
| **PC** | Partitioned Count |
| **OC** | Overlapping Count |
| **CC1** | Total ER1 cluster count |
| **CC2** | Total ER2 cluster count |
| **SC1** | ER1 singleton count (clusters of size 1) |
| **SC2** | ER2 singleton count (clusters of size 1) |
| **TWI** | Table Width Index = sqrt(CC1 × CC2) / num_intersections |

## Algorithm

1. Build a mapping from each ER1 cluster to all ER2 clusters it intersects.
2. For each ER1 cluster:
   - Count the number of intersecting ER2 clusters (N).
   - Compute the union size of all intersecting ER2 clusters.
   - Apply the case classification rules above.
3. Aggregate counts.
