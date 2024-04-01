CREATE TABLE signal (
    id INT,
    name VARCHAR(20),
    func VARCHAR(10),

    PRIMARY KEY (id)
);

CREATE TABLE data (
    timestamp TIMESTAMP,
    signal_id INT,
    value DECIMAL,

    PRIMARY KEY (timestamp, signal_id),
    FOREIGN KEY (signal_id) REFERENCES signal(id)
);

COPY signal
FROM '/docker-entrypoint-initdb.d/signal.csv'
DELIMITER ','
CSV HEADER;
