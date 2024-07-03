from django.contrib import admin
from .models import State, ExamType, EducationalLevel, Exam, PreparationResource, UserProfile, UserExamRegistration, UserDashboard

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(EducationalLevel)
class EducationalLevelAdmin(admin.ModelAdmin):
    list_display = ['level']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'exam_type', 'educational_level']
    search_fields = ['name', 'description']
    list_filter = ['state', 'exam_type', 'educational_level']

@admin.register(PreparationResource)
class PreparationResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam', 'resource_type']
    search_fields = ['title', 'description']
    list_filter = ['exam', 'resource_type']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_bookmarked_exams']
    search_fields = ['user__username']
    filter_horizontal = ['bookmarked_exams']

    def get_bookmarked_exams(self, obj):
        return ", ".join([exam.name for exam in obj.bookmarked_exams.all()])

@admin.register(UserExamRegistration)
class UserExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'registration_date']
    search_fields = ['user__username', 'exam__name']
    list_filter = ['exam', 'registration_date']

@admin.register(UserDashboard)
class UserDashboardAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['registered_exams', 'recommended_exams']
