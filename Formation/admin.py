from django.contrib import admin
from .models import *

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'training_price', 'currency']
    search_fields = ['code', 'name']

@admin.register(FunctionPosition)
class FunctionPositionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'id_direction']
    list_filter = ['id_direction']
    search_fields = ['code', 'name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_number', 'first_name', 'last_name', 'id_department', 'category', 'status']
    list_filter = ['category', 'status', 'id_department', 'id_direction']
    search_fields = ['employee_number', 'first_name', 'last_name']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email']

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['title', 'exercise_year', 'id_organization', 'is_published', 'registration_start_date', 'registration_end_date']
    list_filter = ['exercise_year', 'is_published', 'id_organization']
    search_fields = ['title']

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'id_catalog', 'duration_days', 'domain', 'level', 'status']
    list_filter = ['domain', 'level', 'status', 'training_type']
    search_fields = ['title']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['id_registration', 'id_employee', 'id_training', 'final_status', 'created_at']
    list_filter = ['final_status', 'exercise_year', 'dept_head_validation', 'director_validation', 'formation_validation']
    search_fields = ['id_employee__employee_number', 'id_employee__first_name', 'id_employee__last_name']

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ['action_timestamp', 'action_type', 'id_user']
    list_filter = ['action_type']
    readonly_fields = ['action_timestamp', 'action_type', 'pc_name', 'details', 'id_user']