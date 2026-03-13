-- Create the input table for CCMS analysis
CREATE TABLE IF NOT EXISTS records (
    RecID           VARCHAR(50) NOT NULL,
    ER1_ClusterID   VARCHAR(50) NOT NULL,
    ER2_ClusterID   VARCHAR(50) NOT NULL,
    PRIMARY KEY (RecID)
);
