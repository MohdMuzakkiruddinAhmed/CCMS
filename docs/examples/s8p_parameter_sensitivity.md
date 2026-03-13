# S8P Parameter Sensitivity Example

This example demonstrates how CCMS can be used to analyze the effect of varying ER parameters on clustering outcomes.

## Overview

By running CCMS with the same ER1 baseline but different ER2 configurations (varying parameter mu), we can observe how the case distribution shifts.

## Running the Example

```bash
python examples/example_s8p/run_sensitivity.py
```

## Interpretation

- Higher mu values tend to produce more conservative merging, resulting in more Unchanged or Partitioned cases.
- Lower mu values allow more aggressive merging, leading to more Merged or Overlapping cases.

CCMS provides a quantitative lens for comparing these behavioral differences without requiring ground truth labels.
