from clickhouse_driver import Client
import pandas as pd

client = Client('192.168.99.100')

avg_price = client.execute(
    '''
    SELECT
        passenger_count,
        ceil(avg(total_amount),2) AS average_total_amount
    FROM trips
    GROUP BY passenger_count
    '''
)
df = pd.DataFrame(avg_price, columns=("passenger_count", "average_total_amount"))

print(df)