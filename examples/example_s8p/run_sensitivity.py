"""Parameter sensitivity analysis example (s8p)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ccms.core import compute_ccms, load_csv_map, print_report
from ccms.utils import compute_twi, count_intersections

HERE = os.path.dirname(__file__)
er1_map = load_csv_map(os.path.join(HERE, "er1_baseline.csv"))

configs = [
    ("mu=0.77", "er2_mu077.csv"),
    ("mu=0.57", "er2_mu057.csv"),
]

for label, fname in configs:
    er2_map = load_csv_map(os.path.join(HERE, fname))
    result = compute_ccms(er1_map, er2_map)
    n = count_intersections(er1_map, er2_map)
    twi = compute_twi(result["CC1"], result["CC2"], n)
    print(f"\n{'='*40}")
    print(f"Configuration: {label}")
    print(f"{'='*40}")
    print_report(result)
    print(f"TWI: {twi:.4f}")
