from django.core.management.base import BaseCommand
from app.models import PlentificRecord
from dask import dataframe as ddf

class Command(BaseCommand):
  
    def handle(self, *args, **kwargs):
        cols = ['uuid', 'amount', 'create_date', 'location', 'price', 'col6', 'col7', 'col8', 'col9', 'col10', 'col11', 'col12', 'col13', 'col14', 'col15', 'col16']
        csv_data = ddf.read_csv('http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv', dtype=({'1':'object', 'Unnamed: 8':'object'}))
        csv_data.columns = cols
        csv_data['create_date'] = ddf.to_datetime(csv_data['create_date'], format= '%m/%d/%Y %H:%M')
        csv_data_generator = (x for x in csv_data.iterrows())
        csv_data_row_count = len(csv_data)
        base = 1_00_000
        k = csv_data_row_count//base
        for i in range(k+1):
            c = 0
            xy = []
            for x in  csv_data_generator:
                xy.append(PlentificRecord(None, *x[1]))

                if c > base:
                    PlentificRecord.objects.bulk_create(xy)
                    break
                c += 1
