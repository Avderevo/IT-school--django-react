from django.contrib import admin
from .models import Course, Lesson, Message, LessonStatistic, CourseStatistic


@admin.register(Course, Lesson, Message, LessonStatistic, CourseStatistic)
class StudyAdmin(admin.ModelAdmin):
    pass