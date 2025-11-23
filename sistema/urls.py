from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'sistema'

#@login_required (login_url='/users/login/')       
 #def sistema(request):
    #if request.user.is_authenticated:
        #return HttpResponse('Autenticado no sistema')

urlpatterns = [
    path('paginaprincipal/', views.pagina_principal, name='pagina_principal'),
]