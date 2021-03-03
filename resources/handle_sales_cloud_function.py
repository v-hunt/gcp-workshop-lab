from google.cloud import storage
from google.cloud import bigquery

storage_client = storage.Client()
bigquery_client = client = bigquery.Client()

TABLE_ID = "landing.sales"
TRIGGER_FILENAME = "sales.csv"


def main(data, context):
    file_name: str = data["name"]
    bucket_name: str = data["bucket"]

    if not file_name.endswith(TRIGGER_FILENAME):
        return

    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    lines = blob.download_as_string().splitlines()

    rows_to_insert = []
    for line in lines[1:]:
        client, purchase_date, product, price = line.decode().split(",")
        first_name, last_name = client.split()

        rows_to_insert.append({
            "first_name": first_name,
            "last_name": last_name,
            "purchase_date": purchase_date,
            "product": product,
            "price": price,
        })


    # insertation to Bigquery is limited by 10000 rows,
    # so we need to insert by chunks:
    chunk_size = 500
    chunks = [rows_to_insert[i:i + chunk_size]
              for i in range(0, len(rows_to_insert), chunk_size)]

    errors = []
    for chunk in chunks:
        chunk_errors = bigquery_client.insert_rows_json(TABLE_ID, chunk)
        errors.extend(chunk_errors)

    if not errors:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))