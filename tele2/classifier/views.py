from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import ClassifierService
from .mappers import ClassifierMapper
from .dtos import ClassifierRequestDto
from .repository import ChurnDataRepository
from .serializers import ChurnDataSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ClassifierDataView(APIView):
    def get(self, request):
        records = ChurnDataRepository.get_first_n_records(15)
        serializer = ChurnDataSerializer(records, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def post(self, request):
        limit = request.data.get('limit', 15)
        offset = request.data.get('offset', 0)
        
        records = ChurnDataRepository.get_records_with_offset(limit, offset)
        serializer = ChurnDataSerializer(records, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
        
@method_decorator(csrf_exempt, name='dispatch')
class ClassifierPredictView(APIView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ClassifierService()
        self.mapper = ClassifierMapper()
    
    def post(self, request) -> Response:
        try:
            request_dto = self.mapper.request_to_dto(request)
            response_dto = self.service.predict(request_dto)
            response_data = self.mapper.response_to_json(response_dto)
            
            return Response(response_data, status=200)
            
        except ValueError as e:
            return self.mapper.create_error_response(str(e), 400)
        except Exception as e:
            return self.mapper.create_error_response(
                "Внутренняя ошибка сервера", 500
            )
    
    def get(self, request) -> Response:
        return Response({
            "status": "online",
            "message": "",
            "example": {
                "data": [1.5, 2.3, 0.8, 1.1]
            }
        })
        
@method_decorator(csrf_exempt, name='dispatch')
class ClassifierHealthView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ClassifierService()
    
    def get(self, request) -> Response:
        try:
            test_dto = ClassifierRequestDto(data=[0] * 18) 
            result = self.service.predict(test_dto)
            
            return Response({
                "status": "healthy" if result.pred is not None else "degraded",
                "model_loaded": self.service._classifier is not None,
                "message": "Модель работает нормально" if result.pred is not None 
                          else "Модель загружена, но не отвечает"
            })
        except Exception as e:
            return Response({
                "status": "unhealthy",
                "model_loaded": False,
                "error": str(e)
            }, status=503)
            