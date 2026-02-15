import json
from django.http import HttpRequest, JsonResponse
from .dtos import ClassifierRequestDto, ClassifierResponseDto

class ClassifierMapper:
    
    @staticmethod
    def request_to_dto(request: HttpRequest) -> ClassifierRequestDto:
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                return ClassifierRequestDto(data=data.get('data', []))
            else:
                data_str = request.POST.get('data', '[]')
                if isinstance(data_str, str):
                    data = json.loads(data_str)
                else:
                    data = data_str
                return ClassifierRequestDto(data=data)
        except Exception as e:
            raise ValueError(f"Ошибка парсинга запроса: {e}")
    
    @staticmethod
    def response_to_json(response_dto: ClassifierResponseDto) -> dict:
        return response_dto.to_dict()
    
    @staticmethod
    def create_error_response(error_message: str, status_code: int = 400) -> JsonResponse:
        return JsonResponse(
            ClassifierResponseDto.error_response(error_message),
            status=status_code
        )