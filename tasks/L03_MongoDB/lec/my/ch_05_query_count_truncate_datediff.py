from clickhouse_driver import Client
import pandas as pd

client = Client('192.168.99.100')

trip_minutes = client.execute(
    '''
    SELECT
        avg(tip_amount) AS avg_tip,
        avg(fare_amount) AS avg_fare,
        avg(passenger_count) AS avg_passenger,
        count() AS count,
        truncate(date_diff('second', pickup_datetime, dropoff_datetime) / 3600) as trip_minutes
    FROM trips
    WHERE trip_minutes > 0
    GROUP BY trip_minutes
    ORDER BY trip_minutes DESC
    '''
)
df = pd.DataFrame(trip_minutes, columns=("avg_tip", "avg_fare", "avg_passenger", "count", "trip_minutes"))

print(df)
