"""
Core CCMS computation module.

Compares two ER clustering outcomes and classifies each ER1 cluster
transformation into: Unchanged, Merged, Partitioned, or Overlapping.
"""
from collections import defaultdict
import csv
import sys


def compute_ccms(er1_map, er2_map):
    """
    Compute CCMS case counts and per-cluster details.

    Parameters
    ----------
    er1_map : dict
        {record_id: er1_cluster_id}
    er2_map : dict
        {record_id: er2_cluster_id}

    Returns
    -------
    dict
        UC, MC, PC, OC, CC1, CC2, SC1, SC2, details
    """
    er1_clusters = defaultdict(set)
    er2_clusters = defaultdict(set)
    for rec_id, cid in er1_map.items():
        er1_clusters[cid].add(rec_id)
    for rec_id, cid in er2_map.items():
        er2_clusters[cid].add(rec_id)

    UC = MC = PC = OC = 0
    details = []

    for er1_cid, er1_recs in er1_clusters.items():
        # Find intersecting ER2 clusters
        er2_hits = defaultdict(set)
        for r in er1_recs:
            er2_hits[er2_map[r]].add(r)

        # Union of all intersecting ER2 clusters
        union_er2 = set()
        for er2_cid in er2_hits:
            union_er2 |= er2_clusters[er2_cid]

        # Classify
        if len(er2_hits) == 1:
            er2_cid = next(iter(er2_hits))
            if er1_recs == er2_clusters[er2_cid]:
                case = "Unchanged"
                UC += 1
            else:
                case = "Merged"
                MC += 1
        else:
            if union_er2 == er1_recs:
                case = "Partitioned"
                PC += 1
            else:
                case = "Overlapping"
                OC += 1

        details.append({
            "er1_cluster": er1_cid,
            "er1_records": sorted(er1_recs),
            "er2_intersecting": {
                k: sorted(v) for k, v in er2_hits.items()
            },
            "case": case,
        })

    SC1 = sum(1 for r in er1_clusters.values() if len(r) == 1)
    SC2 = sum(1 for r in er2_clusters.values() if len(r) == 1)

    return {
        "UC": UC, "MC": MC, "PC": PC, "OC": OC,
        "CC1": len(er1_clusters), "CC2": len(er2_clusters),
        "SC1": SC1, "SC2": SC2,
        "details": details,
    }


def load_csv_map(filepath):
    """Read a two-column CSV (RecID, ClusterID) into a dict."""
    mapping = {}
    with open(filepath, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            mapping[row[0]] = row[1]
    return mapping


def print_report(result):
    """Print aggregate CCMS counts to stdout."""
    print(f"ER1 clusters (CC1): {result['CC1']}"
          f"  Singletons (SC1): {result['SC1']}")
    print(f"ER2 clusters (CC2): {result['CC2']}"
          f"  Singletons (SC2): {result['SC2']}")
    print(f"Unchanged (UC):     {result['UC']}")
    print(f"Merged    (MC):     {result['MC']}")
    print(f"Partitioned (PC):   {result['PC']}")
    print(f"Overlapping (OC):   {result['OC']}")
    total = result["UC"] + result["MC"] + result["PC"] + result["OC"]
    print(f"Total (UC+MC+PC+OC): {total}")


def print_case_details(result, case_filter=None):
    """Print per-cluster drill-down details."""
    for d in result["details"]:
        if case_filter and d["case"] != case_filter:
            continue
        print(f"\n--- ER1 Cluster: {d['er1_cluster']}"
              f" [{d['case']}] ---")
        print(f"  ER1 records: {d['er1_records']}")
        for er2_cid, shared in d["er2_intersecting"].items():
            print(f"  -> ER2 cluster {er2_cid}: shared {shared}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m ccms.core er1.csv er2.csv")
        sys.exit(1)
    er1_map = load_csv_map(sys.argv[1])
    er2_map = load_csv_map(sys.argv[2])
    result = compute_ccms(er1_map, er2_map)
    print_report(result)
    print("\n=== MERGED CASES ===")
    print_case_details(result, "Merged")
    print("\n=== PARTITIONED CASES ===")
    print_case_details(result, "Partitioned")
    print("\n=== OVERLAPPING CASES ===")
    print_case_details(result, "Overlapping")
