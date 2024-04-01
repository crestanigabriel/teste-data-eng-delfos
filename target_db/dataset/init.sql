CREATE TABLE signal (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    func VARCHAR(20)
);

CREATE TABLE data (
    timestamp TIMESTAMP,
    signal_id INT,
    value DECIMAL,
    FOREIGN KEY (signal_id) REFERENCES signal(id)
);

COPY signal
FROM '/docker-entrypoint-initdb.d/signal.csv'
DELIMITER ','
CSV HEADER;
