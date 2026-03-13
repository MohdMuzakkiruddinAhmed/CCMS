"""Run CCMS on the 16-reference example from the paper."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ccms.core import compute_ccms, load_csv_map, print_report, print_case_details
from ccms.utils import compute_twi, count_intersections, disaggregate_by_size

HERE = os.path.dirname(__file__)
er1_map = load_csv_map(os.path.join(HERE, "er1.csv"))
er2_map = load_csv_map(os.path.join(HERE, "er2.csv"))

result = compute_ccms(er1_map, er2_map)

print("=" * 50)
print("CCMS Report: 16-Reference Example")
print("=" * 50)
print_report(result)

# TWI
n_intersections = count_intersections(er1_map, er2_map)
twi = compute_twi(result["CC1"], result["CC2"], n_intersections)
print(f"\nNon-empty intersections: {n_intersections}")
print(f"TWI: {twi:.4f}")

# Disaggregate by cluster size
print("\n--- Disaggregation by ER1 Cluster Size ---")
size_table = disaggregate_by_size(result)
print(f"{'Size':>5} {'Count':>6} {'UC':>4} {'MC':>4} {'PC':>4} {'OC':>4}")
for size, counts in size_table.items():
    print(f"{size:>5} {counts['count']:>6} {counts['UC']:>4} "
          f"{counts['MC']:>4} {counts['PC']:>4} {counts['OC']:>4}")

# Drill-down details
for case in ["Merged", "Partitioned", "Overlapping"]:
    print(f"\n=== {case.upper()} CASES ===")
    print_case_details(result, case)
