from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# ============================================
# نماذج Django - Training Management System
# ============================================

class Organization(models.Model):
    id_organization = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    training_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='DZD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'organization'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class FunctionPosition(models.Model):
    id_function = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'function_position'
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Direction(models.Model):
    id_direction = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'direction'
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Department(models.Model):
    id_department = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    id_direction = models.ForeignKey(Direction, on_delete=models.CASCADE, db_column='id_direction')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'department'
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.id_direction.name}"


class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'

    class Category(models.TextChoices):
        EXECUTIVE = 'Executive'
        SUPERVISION = 'Supervision'
        EXECUTION = 'Execution'

    class Status(models.TextChoices):
        ACTIVE = 'Active'
        INACTIVE = 'Inactive'
        RETIRED = 'Retired'
        ON_LEAVE = 'On_Leave'

    id_employee = models.AutoField(primary_key=True)
    employee_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    birth_date = models.DateField(blank=True, null=True)
    recruitment_date = models.DateField(blank=True, null=True)
    
    id_direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, db_column='id_direction')
    id_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, db_column='id_department')
    id_function = models.ForeignKey(FunctionPosition, on_delete=models.SET_NULL, null=True, db_column='id_function')
    
    category = models.CharField(max_length=20, choices=Category.choices)
    domain = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_number})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # لتشفير كلمة المرور
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'Admin') # تعيين رتبة أدمن تلقائياً
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = 'Admin'
        FORMATION_SERVICE = 'Formation_Service'
        DEPARTMENT_HEAD = 'Department_Head'
        DIRECTOR = 'Director'
        EMPLOYEE = 'Employee'
        ADMIN_SERVICE_FORMATION = 'Admin_Service_Formation'

    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128) # هذا الحقل سيخزن التشفير التلقائي
    email = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=30, choices=Role.choices)
    first_login = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    id_employee = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True, unique=True, db_column='id_employee')
    managed_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='managed_by', db_column='managed_department')
    managed_direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, related_name='managed_by', db_column='managed_direction')
    
    can_view_all_employees = models.BooleanField(default=False)
    can_manage_catalogs = models.BooleanField(default=False)
    can_approve_registrations = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # --- أضف هذه الأسطر الثلاثة هنا بالضبط لحل مشكلة الـ AttributeError ---
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    # -------------------------------------------------------------------

    class Meta:
        db_table = 'user'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"

    # أضف هذه الدوال أيضاً لضمان عمل لوحة التحكم (Admin)
    def has_perm(self, perm, obj=None): return True
    def has_module_perms(self, app_label): return True
    
    @property
    def is_staff(self):
        return self.role in ['Admin', 'Admin_Service_Formation']


class Catalog(models.Model):
    id_catalog = models.AutoField(primary_key=True)
    exercise_year = models.IntegerField()  # YEAR type in MySQL
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_link = models.CharField(max_length=500, blank=True, null=True)
    cover_image = models.CharField(max_length=500, blank=True, null=True)
    
    registration_start_date = models.DateField()
    registration_end_date = models.DateField()
    training_start_date = models.DateField()
    training_end_date = models.DateField()
    
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='published_catalogs', db_column='published_by')
    
    id_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, db_column='id_organization')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_catalogs', db_column='created_by')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog'
        ordering = ['-exercise_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.exercise_year})"


class Training(models.Model):
    class TrainingType(models.TextChoices):
        RECRUITMENT = 'Recruitment'
        ENHANCEMENT = 'Enhancement'
        RECONVERSION = 'Reconversion'
        PROFESSIONAL_INTERNSHIP = 'Professional_Internship'
        INTEGRATION = 'Integration'
        CORPORATE = 'Corporate'

    class Level(models.TextChoices):
        BEGINNER = 'Beginner'
        INTERMEDIATE = 'Intermediate'
        ADVANCED = 'Advanced'

    class Code(models.TextChoices):
        CDI = 'CDI'
        CDA = 'CDA'
        CDF = 'CDF'
        CDJ = 'CDJ'
        LDA = 'LDA'
        LDC = 'LDC'

    class Mode(models.TextChoices):
        REMOTE = 'Remote'
        IN_PERSON = 'In_Person'
        BLENDED = 'Blended'
        ON_JOB_TRAINING = 'On_Job_Training'

    class Source(models.TextChoices):
        STRATEGIC = 'Strategic'
        SUPPLIER = 'Supplier'
        REGULATORY = 'Regulatory'
        NEW_RECEIVED = 'New_Received'
        STRUCTURE = 'Structure'
        CAREER_EVOLUTION = 'Career_Evolution'

    class Domain(models.TextChoices):
        TECHNICAL = 'Technical'
        MANAGEMENT = 'Management'
        IT = 'IT'
        SAFETY = 'Safety'
        QUALITY = 'Quality'
        HSE = 'HSE'
        FINANCE = 'Finance'
        HR = 'HR'

    class Nature(models.TextChoices):
        UPGRADE = 'Upgrade'
        CERTIFIED = 'Certified'
        QUALIFYING = 'Qualifying'
        DIPLOMA = 'Diploma'
        SPECIFIC = 'Specific'
        TRAINING_PATH = 'Training_Path'

    class Status(models.TextChoices):
        ACTIVE = 'Active'
        INACTIVE = 'Inactive'
        COMPLETED = 'Completed'

    id_training = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration_hours = models.IntegerField()
    duration_days = models.IntegerField()
    location = models.CharField(max_length=255, blank=True, null=True)
    sessions_number = models.IntegerField(default=1)
    recurrence_years = models.IntegerField(default=3)
    
    custom_training_start_date = models.DateField(null=True, blank=True)
    custom_training_end_date = models.DateField(null=True, blank=True)
    
    training_type = models.CharField(max_length=30, choices=TrainingType.choices)
    level = models.CharField(max_length=20, choices=Level.choices)
    code = models.CharField(max_length=10, choices=Code.choices)
    mode = models.CharField(max_length=20, choices=Mode.choices)
    source = models.CharField(max_length=20, choices=Source.choices)
    domain = models.CharField(max_length=20, choices=Domain.choices)
    nature = models.CharField(max_length=20, choices=Nature.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    id_catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, db_column='id_catalog')
    is_published = models.BooleanField(default=False)
    published_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='published_trainings', db_column='published_by')
    published_date = models.DateTimeField(null=True, blank=True)
    
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'training'
        ordering = ['title']

    def __str__(self):
        return self.title


class Registration(models.Model):
    class FinalStatus(models.TextChoices):
        PENDING = 'Pending'
        APPROVED = 'Approved'
        REJECTED = 'Rejected'
        CANCELLED = 'Cancelled'

    id_registration = models.AutoField(primary_key=True)
    exercise_year = models.IntegerField()
    objective = models.TextField(blank=True, null=True)
    
    dept_head_validation = models.SmallIntegerField(default=0)  # 0:Pending, 1:Approved, 2:Rejected
    dept_head_observations = models.TextField(blank=True, null=True)
    dept_head_date = models.DateTimeField(null=True, blank=True)
    dept_head_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_as_dept_head', db_column='dept_head_id')
    
    director_validation = models.SmallIntegerField(default=0)
    director_observations = models.TextField(blank=True, null=True)
    director_date = models.DateTimeField(null=True, blank=True)
    director_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_as_director', db_column='director_id')
    

    formation_validation = models.SmallIntegerField(default=0)
    formation_observations = models.TextField(blank=True, null=True)
    formation_date = models.DateTimeField(null=True, blank=True)
    formation_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_as_formation', db_column='formation_id')
    
    final_status = models.CharField(max_length=20, choices=FinalStatus.choices, default=FinalStatus.PENDING)
    
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='id_employee')
    id_training = models.ForeignKey(Training, on_delete=models.CASCADE, db_column='id_training')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_registrations', db_column='created_by')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registration'
        ordering = ['-created_at']

    def __str__(self):
        return f"Registration #{self.id_registration} - {self.id_employee} - {self.id_training}"


class Audit(models.Model):
    id_audit = models.BigAutoField(primary_key=True)
    action_timestamp = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=100)
    pc_name = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='id_user')

    class Meta:
        db_table = 'audit'
        ordering = ['-action_timestamp']

    def __str__(self):
        return f"{self.action_timestamp} - {self.action_type}"