-- 16-reference example from the paper (Table 2)
DELETE FROM records;

INSERT INTO records (RecID, ER1_ClusterID, ER2_ClusterID) VALUES
('1',  'a', 'x'),
('2',  'b', 'y'),
('3',  'b', 'y'),
('4',  'c', 'z'),
('5',  'c', 'z'),
('6',  'c', 'z'),
('7',  'd', 'z'),
('8',  'e', 'w'),
('9',  'e', 'w'),
('10', 'e', 't'),
('11', 'f', 'u'),
('12', 'f', 'u'),
('13', 'f', 'v'),
('14', 'g', 'u'),
('15', 'g', 'v'),
('16', 'g', 's');
