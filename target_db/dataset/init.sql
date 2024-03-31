CREATE TABLE signal (
    id INT NOT NULL PRIMARY,
    name DECIMAL
);

CREATE TABLE data (
    timestamp TIMESTAMP,
    signal_id DECIMAL,
    value DECIMAL
);
