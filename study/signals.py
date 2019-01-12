from .models import LessonStatistic, CourseStatistic
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F


@receiver(post_save, sender=LessonStatistic)
def update_course_homework_done(sender, instance, **kwargs):

    if instance.homework_status == 4:
        CourseStatistic.objects.filter(user=instance.user, course=instance.course).update(homework_done=F('homework_done')+1)

