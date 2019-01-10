import factory
from ..models import Course, Lesson, CourseStatistic, LessonStatistic, Message
from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User
    username = 'test_username'
    email = 'test_email@mail.com'


class CourseFactory(factory.Factory):
    class Meta:
        model = Course

    full_name = "test_full_name"
    name = "test_name"
    homework_all = 10


class LessonFactory(factory.Factory):
    class Meta:
        model = Lesson

    lesson_title = 'test_lesson_title'
    homework_title = 'test_homework_title'
    lesson_number = 1

    course = factory.SubFactory(CourseFactory)


class CourseStatisticFactory(factory.Factory):
    class Meta:
        model = CourseStatistic

    user = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)


class LessonStatisticFactory(factory.Factory):
    class Meta:
        model = LessonStatistic

    user = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    lesson = factory.SubFactory(LessonFactory)


class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    user = factory.SubFactory(UserFactory)
    lesson_statistic = factory.SubFactory(LessonStatisticFactory)