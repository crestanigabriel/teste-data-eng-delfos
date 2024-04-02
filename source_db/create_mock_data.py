# SCRIPT USED TO GENERATE MOCK DATA FOR `DATA` TABLE.

import csv
import datetime as dt
import os
import random


def generate_csv(initial_date: dt.datetime, freq: int, interval: int) -> None:
    final_date = initial_date + dt.timedelta(days=interval)

    with open(
        os.path.dirname(os.path.abspath(__file__)) + "/dataset/data.csv", "w"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "wind_speed", "power", "ambient_temperature"])

        current_date = initial_date
        while current_date < final_date:
            writer.writerow(
                [
                    current_date,
                    random.uniform(20, 30),
                    random.uniform(20, 30),
                    random.uniform(20, 30),
                ]
            )

            current_date += dt.timedelta(minutes=freq)


if __name__ == "__main__":
    random.seed(12345)
    initial_date = dt.datetime(year=2024, month=1, day=1, hour=1, minute=30, second=0)
    TIMESTAMP_FREQ = 1  # in minutes
    TOTAL_TIMESTAMP_INTERVAL = 10  # in days

    generate_csv(initial_date, TIMESTAMP_FREQ, TOTAL_TIMESTAMP_INTERVAL)
    print("source_db/dataset/data.csv generated!")
