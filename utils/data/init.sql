CREATE TABLE data (
    timestamp TIMESTAMP,
    wind_speed DECIMAL,
    power DECIMAL,
    ambient_temperature DECIMAL,
);

COPY data
FROM '/docker-entrypoint-initdb.d/data.csv'
DELIMITER ','
CSV HEADER;