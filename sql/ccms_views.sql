-- Step 1: Per-ER1-cluster analysis
CREATE OR REPLACE VIEW er1_analysis AS
SELECT
    a.ER1_ClusterID,
    COUNT(DISTINCT a.RecID) AS er1_size,
    COUNT(DISTINCT a.ER2_ClusterID) AS er2_cluster_count,
    (
        SELECT COUNT(DISTINCT r2.RecID)
        FROM records r2
        WHERE r2.ER2_ClusterID IN (
            SELECT DISTINCT ER2_ClusterID
            FROM records
            WHERE ER1_ClusterID = a.ER1_ClusterID
        )
    ) AS er2_union_size
FROM records a
GROUP BY a.ER1_ClusterID;

-- Step 2: Case classification
CREATE OR REPLACE VIEW er1_cases AS
SELECT
    ER1_ClusterID,
    er1_size,
    er2_cluster_count,
    er2_union_size,
    CASE
        WHEN er2_cluster_count = 1
         AND er1_size = er2_union_size
            THEN 'Unchanged'
        WHEN er2_cluster_count = 1
         AND er1_size < er2_union_size
            THEN 'Merged'
        WHEN er2_cluster_count > 1
         AND er1_size = er2_union_size
            THEN 'Partitioned'
        WHEN er2_cluster_count > 1
         AND er1_size < er2_union_size
            THEN 'Overlapping'
    END AS case_type
FROM er1_analysis;
