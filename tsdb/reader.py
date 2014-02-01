from struct import unpack, calcsize
import pandas as pd
import os

import config

def read_all(station_id):
    filename = os.path.join(config.tsdb_path, station_id + '_daily_ts.csv.tsdb')

    field_names = ['date', 'value', 'metaID']
    entry_format = 'ldi' # long, double, int; See field names above.
    entry_size = calcsize(entry_format)

    records = []
    with open(filename, mode='rb') as f:
        entry_count = os.fstat(f.fileno()).st_size / entry_size
        for i in range(entry_count):
            record = f.read(entry_size)
            records.append(unpack(entry_format, record))

    df = pd.DataFrame(records, columns = field_names)
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df = df.set_index('date')

    return df
