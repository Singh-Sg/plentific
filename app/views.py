from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from app.models import PlentificRecord
from datetime import datetime
import collections
# Create your views here.
import matplotlib.pyplot as plt

class TimeSeriesView(APIView):

    def post(self, request):
        data = {}
        datetime_object = datetime.strptime(request.data.get('start_date'), '%Y-%m-%d')
        datetime_end = datetime.strptime(request.data.get('end_date'), '%Y-%m-%d')
        diff = (datetime_end-datetime_object).days
        new = 0
        qs = PlentificRecord.objects.filter(create_date__range=[request.data.get('start_date'), request.data.get('end_date')])
        qs.update
        for record in qs:
            if record.price =="S":
                key = (record.create_date-datetime_object).days//30
                if  key in data.keys():
                    data[key]["samount"]=(data[key]["samount"]*data[key]["scount"]+record.amount)/(data[key]["scount"]+1)
                    data[key]["scount"]=data[key]["scount"]+1
                else:
                    data[key]={"tamount":0,"tcount":0,"samount":record.amount,"scount":1,"damount":0,"dcount":0,"famount":0,"fcount":0}
            elif record.price =="T":
                key = (record.create_date-datetime_object).days//30
                if  key in data.keys():
                    data[key]["tamount"]=(data[key]["tamount"]*data[key]["tcount"]+record.amount)/(data[key]["tcount"]+1)
                    data[key]["tcount"]=data[key]["tcount"]+1
                else:
                    data[key]={"tamount":record.amount,"tcount":1,"samount":0,"scount":0,"damount":0,"dcount":0,"famount":0,"fcount":0}
            elif record.price =="D":
                key = (record.create_date-datetime_object).days//30
                if  key in data.keys():
                    data[key]["damount"]=(data[key]["damount"]*data[key]["dcount"]+record.amount)/(data[key]["dcount"]+1)
                    data[key]["dcount"]=data[key]["dcount"]+1
                else:
                    data[key]={"tamount":0,"tcount":0,"samount":0,"scount":0,"damount":record.amount,"dcount":1,"famount":0,"fcount":0}
            elif record.price =="F":
                key = (record.create_date-datetime_object).days//30
                if  key in data.keys():
                    data[key]["famount"]=(data[key]["famount"]*data[key]["fcount"]+record.amount)/(data[key]["fcount"]+1)
                    data[key]["fcount"]=data[key]["fcount"]+1
                else:
                    data[key]={"tamount":0,"tcount":0,"samount":0,"scount":0,"damount":0,"dcount":0,"famount":record.amount,"fcount":1}
        new =collections.OrderedDict(sorted(data.items()))
        key_list = []
        tamount = []
        samount = []
        damount = []
        famount = []
        for key, values in new.items():
            key_list.append(key)
            tamount.append(int(values["tamount"]))
            samount.append(int(values["samount"]))
            damount.append(int(values["damount"]))
            famount.append(int(values["famount"]))
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
        # names = list(data_final.keys())
        # values = list(data_final.values())
        # plt.bar(range(len(data_final)), values, tick_label=names)
        # plt.show()
        return Response({"key":list(data_final.keys()),"values":list(data_final.values()),"total":data_final})


class NewAveragePriceView(APIView):

    def post(self, request):
        postcode = "CT5 4LR"
        lst = [0] * 8
        # date_data=request.data.get('date').split("-")
        data_final={"under 100K":0,"100K-250K":0,"250K-400K":0,"400K-550K":0,"550K-700K":0,"700K-850K":0,"850K-1m":0,"over 1m":0}
        data = PlentificRecord.objects.filter(create_date__year="2018",create_date__month="09").order_by("-amount")
        for record in data:
            t = (record.amount-100000)//150000 +1
            if t<0:
                lst[0]+=1
            elif t>7:
                lst[7]+=1
            else:
                lst[t]+=1
            # import pdb;pdb.set_trace()
            # if record.amount< 100000:
            #     data_final["under 100K"] +=1
            # elif record.amount< 250000 and record.amount>= 100000:
            #     data_final["100K-250K"] +=1
            # elif record.amount< 400000 and record.amount>= 250000:
            #     data_final["250K-400K"] +=1
            # elif record.amount< 550000 and record.amount>= 400000:
            #     data_final["400K-550K"] +=1
            # elif record.amount< 700000 and record.amount>= 550000:
            #     data_final["550K-700K"] +=1
            # elif record.amount< 850000 and record.amount>= 700000:
            #     data_final["700K-850K"] +=1
            # elif record.amount< 1000000 and record.amount>= 850000:
            #     data_final["850K-1m"] +=1
            # else:
            #     data_final["over 1m"] +=1
        # names = list(data_final.keys())
        # values = list(data_final.values())
        # plt.bar(range(len(data_final)), values, tick_label=names)
        # plt.show()
        return Response(lst)