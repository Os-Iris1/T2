from django.urls import path
from .views import ClassifierDataView, ClassifierHealthView, ClassifierPredictView

app_name = 'ml_classifier'

urlpatterns = [
    path('predict/', ClassifierPredictView.as_view(), name='predict'),
    path('health/', ClassifierHealthView.as_view(), name='health'),
    path('data/', ClassifierDataView.as_view(), name='data')
]