from clickhouse_driver import Client

client = Client('192.168.99.100')

tip_amount = client.execute("SELECT round(avg(tip_amount), 2) FROM trips")
print(tip_amount)