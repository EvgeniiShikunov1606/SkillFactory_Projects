from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Stopover
from .serializers import StopoverSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class StopoverViewSet(viewsets.ModelViewSet):
    queryset = Stopover.objects.all()
    serializer_class = StopoverSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email']


@api_view(['POST'])
def create_stopover(request):
    serializer = StopoverSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'status': 400,
            'message': 'Bad Request',
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        stopover = serializer.save()
        return Response({
            'status': 200,
            'message': 'Отправлено успешно',
            'id': stopover.id
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 500,
            'message': f'Ошибка подключения: {str(e)}',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_stopover(request, id):
    try:
        stopover = Stopover.objects.get(id=id)
        serializer = StopoverSerializer(stopover)
        return Response(serializer.data)
    except Stopover.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Запись не найдена',
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 500,
            'message': f'Ошибка подключения: {str(e)}',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

