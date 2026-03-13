-- Aggregate case counts
SELECT
    case_type,
    COUNT(*) AS case_count
FROM er1_cases
GROUP BY case_type
ORDER BY case_type;

-- Singleton counts
SELECT 'SC1' AS metric,
       COUNT(*) AS value
FROM (
    SELECT ER1_ClusterID
    FROM records
    GROUP BY ER1_ClusterID
    HAVING COUNT(*) = 1
) t

UNION ALL

SELECT 'SC2' AS metric,
       COUNT(*) AS value
FROM (
    SELECT ER2_ClusterID
    FROM records
    GROUP BY ER2_ClusterID
    HAVING COUNT(*) = 1
) t;

-- TWI computation
SELECT
    ROUND(
        SQRT(
            CAST((SELECT COUNT(DISTINCT ER1_ClusterID) FROM records) AS FLOAT)
            *
            CAST((SELECT COUNT(DISTINCT ER2_ClusterID) FROM records) AS FLOAT)
        )
        /
        CAST((SELECT COUNT(DISTINCT ER1_ClusterID || '|' || ER2_ClusterID)
              FROM records) AS FLOAT),
        4
    ) AS TWI;
