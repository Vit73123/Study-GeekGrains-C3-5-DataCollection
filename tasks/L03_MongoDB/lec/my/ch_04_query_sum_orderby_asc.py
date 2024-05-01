from clickhouse_driver import Client
import pandas as pd

client = Client('192.168.99.100')

pickup_num = client.execute(
    '''
    SELECT
        pickup_date,
        pickup_ntaname,
        SUM(1) AS number_of_trips
    FROM trips
    GROUP BY pickup_date, pickup_ntaname
    ORDER BY pickup_date ASC
    '''
)
df = pd.DataFrame(pickup_num, columns=("pickup_date", "pickup_ntaname", "number_of_trips"))

print(df)
