import datetime
import pytz
import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from barrow.models import Application, SpiderResult, Spider
from barrow.serializers import SpiderResultSerializer


class FetchUnreadResultView(APIView):
    """ fetch result view
    """

    def get(self, request, application):
        if application and Application.objects.filter(name=application).exists():
            application = Application.objects.get(name=application)
            return Response(SpiderResultSerializer(SpiderResult.objects.fetch_unread_result_application(application)).data)
        else:
            return Response(status=403)


class FetchByTimestampView(APIView):
    """ fetch by timestamp
    """

    def get(self, requst, application, timestamp):
        if application and Application.objects.filter(name=application).exists():
            application = Application.objects.get(name=application)
            local_tz = pytz.timezone('Asia/Shanghai')

            request_time = datetime.datetime.fromtimestamp(int(timestamp)).replace(tzinfo=local_tz)

            objects = SpiderResult.objects.fetch_result_application_and_time(application, request_time)

            return Response(SpiderResultSerializer(objects).data)


class IndexView(APIView):
    """ index
    """

    def get(self, request):
        return redirect('/xadmin/')


class ResetSpiderView(APIView):
    """ reset spider view
    """

    def get(self, request):
        Spider.objects.reset_spider_state()
        return Response({'result': 'ok'})