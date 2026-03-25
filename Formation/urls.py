from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views
from . import views

router = DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'functions', views.FunctionPositionViewSet)
router.register(r'directions', views.DirectionViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'catalogs', views.CatalogViewSet)
router.register(r'trainings', views.TrainingViewSet)
router.register(r'registrations', views.RegistrationViewSet)
router.register(r'audits', views.AuditViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # 2. إضافة رابط تسجيل الدخول (Login)
    # هذا الرابط سيستقبل POST request يحتوي على username و password
    path('api-login/', auth_views.obtain_auth_token),
]