from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from barrow.models import Application, SpiderResult
from barrow.serializers import SpiderResultSerializer


class FetchResultView(APIView):
    """ fetch result view
    """

    def get(self, request, application):
        if application and Application.objects.filter(name=application).exists():
            application = Application.objects.get(name=application)
            return Response(SpiderResultSerializer(SpiderResult.objects.fetch_result_application(application)).data)
        else:
            return Response(status=403)


class IndexView(APIView):
    """ index
    """

    def get(self, request):
        return redirect('/xadmin/')