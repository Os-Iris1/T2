from django.urls import path
from .views import ClassifierPredictView, ClassifierHealthView, ClassifierReloadView

app_name = 'ml_classifier'

urlpatterns = [
    path('predict/', ClassifierPredictView.as_view(), name='predict'),
    path('health/', ClassifierHealthView.as_view(), name='health')
]