from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ToNaBes.urls')),
    path('users/', include('users.urls')),
    path('sistema/', include('sistema.urls'))
]
