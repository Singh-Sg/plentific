from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from app.models import PlentificRecord
from datetime import datetime
import collections
from django.db import connection

# Create your views here.
import matplotlib.pyplot as plt

class TimeSeriesView(APIView):

    def post(self, request):
        key_list = []
        tamount = []
        samount = []
        damount = []
        famount = []
        print(str(request.data.get('start_date')))
        cursor = connection.cursor()
        sql = f"select json_agg(s.op) from ( select jsonb_build_object(t.mon, t.data) op from (select jsonb_agg( cast(amount as bigint)) as data, p.mon from (select avg(amount) amount, ap.price, to_char(ap.create_date, 'yyyy-MM') mon from app_plentificrecord ap where ap.create_date between '{request.data.get('start_date')}' and '{request.data.get('end_date')}'  group by   to_char(ap.create_date, 'yyyy-MM'), ap.price order by  mon asc )p group by p.mon)t)s"
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        for row in result:
            for keyss, value in row.items():
                key_list.append(keyss)
                samount.append(value[0])
                tamount.append(value[1])
                damount.append(value[3])
                famount.append(value[4])
        # plt.plot(key_list, tamount)
        # plt.plot(key_list, samount)
        # plt.plot(key_list, damount)
        # plt.plot(key_list, famount)
        # plt.show()
        return Response({"key":key_list,"tamount":tamount,"samount":samount,"damount":damount,"famount":famount})


class AveragePriceView(APIView):

    def post(self, request):
        date_data=request.data.get('date').split("-")
        data_final={"under 100K":0,"100K-250K":0,"250K-400K":0,"400K-550K":0,"550K-700K":0,"700K-850K":0,"850K-1m":0,"over 1m":0}
        data = PlentificRecord.objects.filter(create_date__year=date_data[0],create_date__month=date_data[1]).order_by("-amount")
        for record in data:
            if record.amount< 100000:
                data_final["under 100K"] +=1
            elif record.amount< 250000 and record.amount>= 100000:
                data_final["100K-250K"] +=1
            elif record.amount< 400000 and record.amount>= 250000:
                data_final["250K-400K"] +=1
            elif record.amount< 550000 and record.amount>= 400000:
                data_final["400K-550K"] +=1
            elif record.amount< 700000 and record.amount>= 550000:
                data_final["550K-700K"] +=1
            elif record.amount< 850000 and record.amount>= 700000:
                data_final["700K-850K"] +=1
            elif record.amount< 1000000 and record.amount>= 850000:
                data_final["850K-1m"] +=1
            else:
                data_final["over 1m"] +=1
        return Response({"key":list(data_final.keys()),"values":list(data_final.values()),"total":data_final})
