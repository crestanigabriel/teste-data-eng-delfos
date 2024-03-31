# SCRIPT USED TO GENERATE MOCK DATA FOR `DATA` TABLE.

import csv
import datetime as dt
import random


def generate_csv(initial_date: dt.datetime, freq: int, interval: int) -> None:
    final_date = initial_date + dt.timedelta(days=interval)

    with open("dataset/data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "wind_speed", "power", "ambient_temperature"])

        current_date = initial_date
        while current_date < final_date:
            print(current_date)
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
    initial_date = dt.datetime(year=2024, month=1, day=31, hour=7, minute=22, second=37)
    TIMESTAMP_FREQ = 10  # in minutes
    TOTAL_TIMESTAMP_INTERVAL = 2  # in days

    generate_csv(initial_date, TIMESTAMP_FREQ, TOTAL_TIMESTAMP_INTERVAL)
