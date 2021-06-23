import datetime

from google.cloud.bigquery.dbapi import connect

def test_structs(bigquery_client, dataset_id):
    person_type = ('struct<name string,'
                   ' children array<struct<name string, bdate date>>>')
    table = dataset_id + ".test_struct"
    conn = connect(bigquery_client)
    cursor = conn.cursor()
    cursor.execute(f"create table {table} (person {person_type})")
    data = dict(name='par',
                children=[
                    dict(name='ch1', bdate=datetime.date(2021, 1, 1)),
                    dict(name='ch2', bdate=datetime.date(2021, 1, 2)),
                    ])
    cursor.execute(
        f"insert into {table} (person) values (%(v:{person_type})s)",
        dict(v=data),
        )

    cursor.execute(f"select * from {table}")
    [[result]] = list(cursor)
    assert result == data
