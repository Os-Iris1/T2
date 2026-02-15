from django.views import View
from django.http import JsonResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .services import ClassifierService
from .mappers import ClassifierMapper
from .dtos import ClassifierRequestDto

@method_decorator(csrf_exempt, name='dispatch')
class ClassifierPredictView(View):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ClassifierService()
        self.mapper = ClassifierMapper()
    
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            request_dto = self.mapper.request_to_dto(request)
            response_dto = self.service.predict(request_dto)
            response_data = self.mapper.response_to_json(response_dto)
            
            return JsonResponse(response_data, status=200)
            
        except ValueError as e:
            return self.mapper.create_error_response(str(e), 400)
        except Exception as e:
            return self.mapper.create_error_response(
                "Внутренняя ошибка сервера", 500
            )
    
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({
            "status": "online",
            "message": "",
            "example": {
                "data": [1.5, 2.3, 0.8, 1.1]
            }
        })

@method_decorator(csrf_exempt, name='dispatch')
class ClassifierHealthView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ClassifierService()
    
    def get(self, request: HttpRequest) -> JsonResponse:
        try:
            test_dto = ClassifierRequestDto(data=[0] * 19) 
            result = self.service.predict(test_dto)
            
            return JsonResponse({
                "status": "healthy" if result.pred is not None else "degraded",
                "model_loaded": self.service._classifier is not None,
                "message": "Модель работает нормально" if result.pred is not None 
                          else "Модель загружена, но не отвечает"
            })
        except Exception as e:
            return JsonResponse({
                "status": "unhealthy",
                "model_loaded": False,
                "error": str(e)
            }, status=503)
