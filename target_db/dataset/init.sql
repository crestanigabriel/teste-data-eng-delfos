CREATE TABLE signal (
    id INT PRIMARY KEY,
    name DECIMAL
);

CREATE TABLE data (
    timestamp TIMESTAMP,
    signal_id INT,
    value DECIMAL,
    FOREIGN KEY (signal_id) REFERENCES signal(id)
);
