import datetime
import pytz
import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from barrow.models import Application, SpiderResult, Spider, SpiderTag
from barrow.serializers import SpiderResultSerializer, SpiderTagSerializer, PrioritizedSpiderResultSerializer


class FetchUnreadResultView(APIView):
    """ fetch result view
    """

    def get(self, request, application):
        prioritized = request.GET.get('prioritized', 0)
        if prioritized:
            serializer_class = PrioritizedSpiderResultSerializer
        else:
            serializer_class = SpiderResultSerializer

        if application and Application.objects.filter(name=application).exists():
            application = Application.objects.get(name=application)
            return Response(serializer_class(SpiderResult.objects.fetch_unread_result_application(application)).data)
        else:
            return Response(status=403)


class FetchByTimestampView(APIView):
    """ fetch by timestamp
    """

    def get(self, request, application, timestamp):
        prioritized = request.GET.get('prioritized', 0)
        if prioritized:
            serializer_class = PrioritizedSpiderResultSerializer
        else:
            serializer_class = SpiderResultSerializer

        if application and Application.objects.filter(name=application).exists():
            application = Application.objects.get(name=application)
            local_tz = pytz.timezone('Asia/Shanghai')

            request_time = datetime.datetime.fromtimestamp(int(timestamp)).replace(tzinfo=local_tz)

            objects = SpiderResult.objects.fetch_result_application_and_time(application, request_time)

            return Response(serializer_class(objects).data)
        else:
            return Response(status=403)


class ApplicationSpiderTagView(APIView):
    """ get all spider tags in application
    """

    def get(self, request, application):
        if application and Application.objects.filter(name=application).exists():
            application = Application.objects.get(name=application)

            tags = SpiderTag.objects.tags_in_application(application)
            return Response(SpiderTagSerializer(tags).data)
        else:
            return Response(status=403)


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