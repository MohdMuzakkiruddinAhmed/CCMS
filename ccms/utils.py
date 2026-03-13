"""Utility functions for CCMS analysis."""


def compute_twi(cc1, cc2, num_intersections):
    """
    Compute the TWI metric.

    TWI = sqrt(CC1 * CC2) / num_intersections
    """
    if num_intersections == 0:
        return 0.0
    return (cc1 * cc2) ** 0.5 / num_intersections


def count_intersections(er1_map, er2_map):
    """Count non-empty intersections between ER1 and ER2 clusters."""
    pairs = set()
    for rec_id in er1_map:
        if rec_id in er2_map:
            pairs.add((er1_map[rec_id], er2_map[rec_id]))
    return len(pairs)


def disaggregate_by_size(result):
    """
    Disaggregate CCMS case counts by ER1 cluster size.

    Returns dict: {size: {UC, MC, PC, OC, count}}
    """
    size_table = {}
    for d in result["details"]:
        size = len(d["er1_records"])
        if size not in size_table:
            size_table[size] = {
                "count": 0, "UC": 0, "MC": 0, "PC": 0, "OC": 0
            }
        size_table[size]["count"] += 1
        case_key = {
            "Unchanged": "UC", "Merged": "MC",
            "Partitioned": "PC", "Overlapping": "OC"
        }[d["case"]]
        size_table[size][case_key] += 1
    return dict(sorted(size_table.items()))
