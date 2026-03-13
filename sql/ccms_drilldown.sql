-- Drill-down: Overlapping cases
SELECT
    c.ER1_ClusterID,
    c.er1_size,
    r.ER2_ClusterID,
    COUNT(r.RecID) AS shared_records
FROM er1_cases c
JOIN records r ON r.ER1_ClusterID = c.ER1_ClusterID
WHERE c.case_type = 'Overlapping'
GROUP BY c.ER1_ClusterID, c.er1_size, r.ER2_ClusterID
ORDER BY c.ER1_ClusterID, r.ER2_ClusterID;

-- Drill-down: Merged cases
SELECT
    c.ER1_ClusterID,
    c.er1_size,
    r.ER2_ClusterID,
    COUNT(r.RecID) AS shared_records,
    c.er2_union_size AS total_er2_size
FROM er1_cases c
JOIN records r ON r.ER1_ClusterID = c.ER1_ClusterID
WHERE c.case_type = 'Merged'
GROUP BY c.ER1_ClusterID, c.er1_size,
         r.ER2_ClusterID, c.er2_union_size
ORDER BY c.ER1_ClusterID;

-- Drill-down: Partitioned cases
SELECT
    c.ER1_ClusterID,
    c.er1_size,
    r.ER2_ClusterID,
    COUNT(r.RecID) AS fragment_size
FROM er1_cases c
JOIN records r ON r.ER1_ClusterID = c.ER1_ClusterID
WHERE c.case_type = 'Partitioned'
GROUP BY c.ER1_ClusterID, c.er1_size, r.ER2_ClusterID
ORDER BY c.ER1_ClusterID, r.ER2_ClusterID;

-- Summary: all cases with details
SELECT
    c.ER1_ClusterID,
    c.case_type,
    c.er1_size,
    c.er2_cluster_count,
    c.er2_union_size
FROM er1_cases c
ORDER BY c.case_type, c.ER1_ClusterID;
