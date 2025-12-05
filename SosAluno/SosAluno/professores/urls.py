from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para as ViewSets da API REST
router = DefaultRouter()
router.register(r'api/professores', views.ProfessorViewSet, basename='professor-api')
router.register(r'api/comentarios', views.ComentarioViewSet, basename='comentario-api')

urlpatterns = [
    # URLs da API REST
    path('', include(router.urls)),
    
    # URLs para renderizar templates HTML (com dados do Django)
    path('list/', views.professores_list, name='professores-list'),
    path('<str:id_slug>/', views.professor_detail, name='professor-detail'),
    
    # URLs para JSON simples (API)
    path('api/professores-list/', views.professores_list_api, name='professores-list-api'),
    path('api/professor/<str:id_slug>/', views.professor_detail_api, name='professor-detail-api'),
]
