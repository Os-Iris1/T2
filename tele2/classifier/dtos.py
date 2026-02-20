from dataclasses import dataclass
from typing import Any, List, Optional
import json

@dataclass
class ClassifierRequestDto:

    data: List[Any]
    
    def __post_init__(self):
        if not isinstance(self.data, list):
            raise ValueError("data должен быть списком")
    
    def to_json(self) -> str:
        return json.dumps({"data": self.data})
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ClassifierRequestDto':
        try:
            data_dict = json.loads(json_str)
            return cls(data=data_dict.get('data', []))
        except json.JSONDecodeError as e:
            raise ValueError(f"Неверный формат JSON: {e}")

@dataclass
class ClassifierResponseDto:
    proba: Optional[List[float]]
    pred: Optional[Any]
    
    def to_dict(self) -> dict:
        return {
            "probability": self.proba,
            "prediction": self.pred,
            "success": self.proba is not None and self.pred is not None
        }
    
    @classmethod
    def error_response(cls, error_message: str) -> dict:
        return {
            "probability": None,
            "prediction": None,
            "success": False,
            "error": error_message
        }
