from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Apuntamos a las vistas de 'core' que es donde están los modelos nuevos
    path('', include('core.urls')), 
]