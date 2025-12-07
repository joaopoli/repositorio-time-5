"""
URL configuration for SosAluno project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from professores.views import index, professores_page, professor_page, login_page, cadastro_page, logout_user, avaliar_page, salvar_avaliacao

urlpatterns = [
    path("", index, name="index"),
    path("professores-page/", professores_page, name="professores-page"),
    path("professor/", professor_page, name="professor-page"),
    path("professor/<str:id_slug>/", professor_page, name="professor-page-detail"),
    path("login/", login_page, name="login-page"),
    path("cadastro/", cadastro_page, name="cadastro-page"),
    path("logout/", logout_user, name="logout"),
    path("avaliar/", avaliar_page, name="avaliar-page"),
    path("api/avaliacoes/", salvar_avaliacao, name="salvar-avaliacao"),
    path("admin/", admin.site.urls),
    path("professores/", include("professores.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
