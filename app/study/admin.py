from django.contrib import admin
from .models import Course, Lesson, Message, LessonStatistic, CourseStatistic


@admin.register(Message, CourseStatistic)
class StudyAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'name', 'homework_all', 'date_start', 'label')
    list_filter = ("name", "homework_all", "date_start",)

    def courses_count(self, obj):
        return obj.full_name.count()


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = ('lesson_title', 'lesson_number', 'is_homework','date', 'course')
    list_filter = ("course", "date")


@admin.register(LessonStatistic)
class LessonStatisticAdmin(admin.ModelAdmin):

    list_display = ('course', 'user', 'homework_status', 'lesson', )
    list_filter = ('homework_status', "course", "user",)
