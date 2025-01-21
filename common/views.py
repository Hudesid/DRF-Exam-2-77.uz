from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from . import serializers, models


class BaseStaticPageListAPIView(APIView):
    @action(detail=False, methods=['get'])
    def static_page_list(self, request):
        data = models.StaticPage.objects.all()
        serializer = serializers.StaticPageSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegionListAPIView(ListAPIView):
    queryset = models.Region
    serializer_class = serializers.RegionListSerializer


class StaticPageRetrieveAPIView(BaseStaticPageListAPIView, RetrieveAPIView):
    queryset = models.StaticPage.objects.all()
    serializer_class = serializers.StaticPageSerializer

