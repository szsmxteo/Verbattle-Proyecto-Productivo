from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend
    path('', include('verbattle.urls')),

    # Backend API
    path('api/', include('core.urls')),
]