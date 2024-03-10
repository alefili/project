"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from app import views
from app.api import router
from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.welcome, name="home"),
    path('meal-plan', views.meal_plan),
    path('lista-cumparaturi', views.lista_cumparaturi),
    path("contact", views.contact, name='contact'),
    path("reteta/lista", views.lista_retete, name="pagina-retete"),
    path("reteta/detaliu/<int:id>/", views.reteta, name="pagina-reteta"),
    path("reteta/adauga/", views.adauga_reteta),
    path("reteta/edit/<int:reteta_id>/", views.editare_reteta, name="edit-reteta"),
    path("reteta/editeaza/<int:pk>/", views.retetaUpdateView.as_view()),
    path("aliment/lista", views.aliment, name="pagina-alimente"),
    path("aliment/adauga/", views.adauga_aliment),
    path("aliment/edit/<int:aliment_id>/", views.editare_aliment, name="edit-aliment"),
    path("aliment/editeaza/<int:pk>/", views.alimentUpdateView.as_view()),
    path("quiz", views.quiz),
    path("contact", views.contact, name='contact'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('login', views.custom_login, name='login'),
    path('logout',  views.logout_view, name='logout'),
    path('test_api', views.api_view),
    path('api/', include(router.urls)),
    path('tinymce/', include('tinymce.urls')),
    path('api-auth/', include('rest_framework.urls'))
    
] +  static(MEDIA_URL, document_root=MEDIA_ROOT)
