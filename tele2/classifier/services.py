import os
import joblib
from typing import Any, List, Optional
from django.conf import settings
from .dtos import ClassifierRequestDto, ClassifierResponseDto

class ClassifierService:
    
    _instance = None
    _classifier = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        try:
            model_path = getattr(
                settings, 
                'ML_MODEL_PATH', 
                os.path.join(settings.BASE_DIR, 'classifier', 'data', 'ml_models', 'model.pkl')
            )
            
            self._classifier = joblib.load(model_path)
        except Exception as e:
            self._classifier = None
    
    def predict_proba(self, data: List[Any]) -> Optional[List[float]]:
        try:
            if self._classifier is None:
                raise ValueError("Модель не загружена")
            
            probabilities = self._classifier.predict_proba([data])
            return probabilities[0].tolist()  
        except Exception as e:
            return None
    
    def predict_class(self, data: List[Any]) -> Optional[Any]:
        try:
            if self._classifier is None:
                raise ValueError("Модель не загружена")
            
            prediction = self._classifier.predict([data])
            return prediction[0].item()  
        except Exception as e:
            return None
    
    def predict(self, request_dto: ClassifierRequestDto) -> ClassifierResponseDto:

        proba = self.predict_proba(request_dto.data)
        pred = self.predict_class(request_dto.data)
        
        return ClassifierResponseDto(proba=proba, pred=pred)
    
    def reload_model(self) -> bool:
        try:
            self._load_model()
            return self._classifier is not None
        except Exception as e:
            return False