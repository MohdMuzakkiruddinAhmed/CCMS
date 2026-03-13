"""Industry-scale CCMS example."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ccms.core import compute_ccms, load_csv_map, print_report, print_case_details
from ccms.utils import compute_twi, count_intersections, disaggregate_by_size

if len(sys.argv) != 3:
    print("Usage: python run_industry.py er1.csv er2.csv")
    sys.exit(1)

er1_map = load_csv_map(sys.argv[1])
er2_map = load_csv_map(sys.argv[2])

result = compute_ccms(er1_map, er2_map)

print("=" * 60)
print("CCMS Industry Analysis")
print("=" * 60)
print_report(result)

n_intersections = count_intersections(er1_map, er2_map)
twi = compute_twi(result["CC1"], result["CC2"], n_intersections)
print(f"\nNon-empty intersections: {n_intersections}")
print(f"TWI: {twi:.4f}")

print("\n--- Disaggregation by ER1 Cluster Size ---")
size_table = disaggregate_by_size(result)
print(f"{'Size':>5} {'Count':>6} {'UC':>4} {'MC':>4} {'PC':>4} {'OC':>4}")
for size, counts in size_table.items():
    print(f"{size:>5} {counts['count']:>6} {counts['UC']:>4} "
          f"{counts['MC']:>4} {counts['PC']:>4} {counts['OC']:>4}")
