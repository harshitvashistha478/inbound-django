from django.urls import path
from .views import InboundCallView

urlpatterns = [
    # path('health/', HealthCheckView.as_view(), name='health'),
    path('incoming/', InboundCallView.as_view(), name='inbound-call'),
]