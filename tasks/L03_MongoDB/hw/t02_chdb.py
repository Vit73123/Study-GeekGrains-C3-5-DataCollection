# Курс: Сбор и разметка данных (семинары)
# Урок 3. Системы управления базами данных MongoDB и Кликхаус в Python

# Задания 4, 5
# 4. Зарегистрируйтесь в ClickHouse.
# 5. Загрузите данные в ClickHouse и создайте таблицу для их хранения.

# The UK property prices
# - Source: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
# - Description of the fields: https://www.gov.uk/guidance/about-the-price-paid-data
# - Contains HM Land Registry data © Crown copyright and database right 2021.

from clickhouse_driver import Client
from pprint import pprint
import pandas as pd

client = Client('192.168.99.100')


def load_data():
    client.execute(
        '''
        CREATE TABLE uk_price_paid
        (
            price UInt32,
            date Date,
            postcode1 LowCardinality(String),
            postcode2 LowCardinality(String),
            type Enum8('terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4, 'other' = 0),
            is_new UInt8,
            duration Enum8('freehold' = 1, 'leasehold' = 2, 'unknown' = 0),
            addr1 String,
            addr2 String,
            street LowCardinality(String),
            locality LowCardinality(String),
            town LowCardinality(String),
            district LowCardinality(String),
            county LowCardinality(String)
        )
        ENGINE = MergeTree
        ORDER BY (postcode1, postcode2, addr1, addr2);
        '''
    )

    client.execute(
        '''
        INSERT INTO uk_price_paid
        WITH
           splitByChar(' ', postcode) AS p
        SELECT
            toUInt32(price_string) AS price,
            parseDateTimeBestEffortUS(time) AS date,
            p[1] AS postcode1,
            p[2] AS postcode2,
            transform(a, ['T', 'S', 'D', 'F', 'O'], ['terraced', 'semi-detached', 'detached', 'flat', 'other']) AS type,
            b = 'Y' AS is_new,
            transform(c, ['F', 'L', 'U'], ['freehold', 'leasehold', 'unknown']) AS duration,
            addr1,
            addr2,
            street,
            locality,
            town,
            district,
            county
        FROM url(
            'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv',
            'CSV',
            'uuid_string String,
            price_string String,
            time String,
            postcode String,
            a String,
            b String,
            c String,
            addr1 String,
            addr2 String,
            street String,
            locality String,
            town String,
            district String,
            county String,
            d String,
            e String'
        )
        SETTINGS max_http_get_redirects=10;
        '''
    )


if __name__ == '__main__':
    # Загрузка данных
    try:
        load_data()
    except:
        pass

    # Проверка данных: количество строк
    rows = client.execute(
        '''
        SELECT count() FROM uk_price_paid;
        '''
    )
    print(f'Число строк:\t\t{rows}')            # [(29070420,)]

    # Размер хранилища данных
    size = client.execute(
        '''
        SELECT formatReadableSize(total_bytes)
        FROM system.tables
        WHERE name = 'uk_price_paid'
        '''
    )
    print(f'Размер хранилища:\t{size}')         # [(29070420,)]

    # Первые 10 записей
    df = pd.DataFrame(
        client.execute(
            '''
            SELECT *
            FROM uk_price_paid
            LIMIT 10 
            '''
        )
    )
    print('Первые 10 записей')
    pprint(df)
    #        0           1   ...                   12               13
    # 0  145000  2008-11-19  ...          SCARBOROUGH  NORTH YORKSHIRE
    # 1    5000  2020-06-28  ...  NORTH HERTFORDSHIRE    HERTFORDSHIRE
    # 2   70000  1995-08-04  ...               TORBAY           TORBAY
    # 3   43000  1995-04-21  ...              CARADON         CORNWALL
    # 4   60000  1995-01-27  ...  NORTH HERTFORDSHIRE    HERTFORDSHIRE
    # 5   54000  1995-08-04  ...       ST EDMUNDSBURY          SUFFOLK
    # 6   31000  1995-02-06  ...              CARRICK         CORNWALL
    # 7   70000  1995-05-01  ...             DARTFORD             KENT
    # 8   12500  1995-06-23  ...                CONWY            CONWY
    # 9   15000  1995-08-16  ...               WIRRAL       MERSEYSIDE

    # Среднегодовая цена
    avg_prices = client.execute(
        '''
        SELECT
           toYear(date) AS year,
           round(avg(price)) AS price,
           bar(price, 0, 1000000, 80
        )
        FROM uk_price_paid
        GROUP BY year
        ORDER BY year
        '''
    )
    print('Среднегодовая цена:')
    pprint(avg_prices)

    # [(1995, 67941.0, '█████▍'),
    #  (1996, 71516.0, '█████▋'),
    #  (1997, 78546.0, '██████▎'),
    #  (1998, 85445.0, '██████▊'),
    #  (1999, 96047.0, '███████▋'),
    #  (2000, 107497.0, '████████▌'),
    #  (2001, 118895.0, '█████████▌'),
    #  (2002, 137961.0, '███████████'),
    #  (2003, 155903.0, '████████████▍'),
    #  (2004, 178895.0, '██████████████▎'),
    #  (2005, 189366.0, '███████████████▏'),
    #  (2006, 203538.0, '████████████████▎'),
    #  (2007, 219383.0, '█████████████████▌'),
    #  (2008, 217137.0, '█████████████████▎'),
    #  (2009, 213426.0, '█████████████████'),
    #  (2010, 236116.0, '██████████████████▉'),
    #  (2011, 232808.0, '██████████████████▌'),
    #  (2012, 238389.0, '███████████████████'),
    #  (2013, 256952.0, '████████████████████▌'),
    #  (2014, 280061.0, '██████████████████████▍'),
    #  (2015, 297376.0, '███████████████████████▊'),
    #  (2016, 313602.0, '█████████████████████████'),
    #  (2017, 346803.0, '███████████████████████████▋'),
    #  (2018, 351164.0, '████████████████████████████'),
    #  (2019, 354843.0, '████████████████████████████▍'),
    #  (2020, 378300.0, '██████████████████████████████▎'),
    #  (2021, 387909.0, '███████████████████████████████'),
    #  (2022, 409483.0, '████████████████████████████████▊'),
    #  (2023, 386737.0, '██████████████████████████████▉'),
    #  (2024, 345843.0, '███████████████████████████▋')]