"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from api.views import (
    AuteurViewSet,
    LivreViewSet,
    CategorieViewSet,
    ExemplaireViewSet,
    EmpruntViewSet,
    CommentaireViewSet,
    EditeurViewSet,
    EvaluationViewSet,
    CustomTokenObtainPairView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

schema_view = get_schema_view(
   openapi.Info(
        title="API",
        default_version='v1',
        description="Documentation de l'API",
   ),
   public=True,
   permission_classes=[permissions.AllowAny], 
)

router = DefaultRouter()
router.register(r'auteurs', AuteurViewSet)
router.register(r'livres', LivreViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'exemplaires', ExemplaireViewSet)
router.register(r'emprunts', EmpruntViewSet)
router.register(r'commentaires', CommentaireViewSet)
router.register(r'editeurs', EditeurViewSet)
router.register(r'evaluations', EvaluationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
