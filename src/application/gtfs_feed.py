import csv
import os
from io import TextIOWrapper
from zipfile import ZipFile
from .crate_repository import CrateRepository

IMPORT_ROWS_PER_QUERY_AMOUNT = os.environ.get('IMPORT_ROWS_PER_QUERY_AMOUNT', default=500)


# Unarchive Zip file with GTFS data and import each file from
# archive one by one into CrateDB
def parse(file):
    with ZipFile(file, 'r') as zip_obj:
        file_names = zip_obj.namelist()
        repository = CrateRepository()
        for file_name in file_names:
            parse_single_file(zip_obj, file_name, repository)


# Execution of this function can be scaled horizontally by processing each
# file from Zip archive independently
def parse_single_file(zip_obj, file_name, repository):
    with zip_obj.open(file_name, 'r') as gtfs_data_file:
        text_file_wrapper = TextIOWrapper(gtfs_data_file, 'utf-8')
        reader = csv.reader(text_file_wrapper)
        header_row = next(reader)
        if len(header_row) == 0:
            return

        table_name = file_name.split('.')[0]
        repository.create_table(table_name, header_row)
        rows = []
        for row in reader:
            rows.append(tuple(row))
            if len(rows) == IMPORT_ROWS_PER_QUERY_AMOUNT:
                repository.insert_values(table_name, header_row, rows)
                rows = []
