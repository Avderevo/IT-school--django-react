import pytest
from .factories import (
    CourseFactory,
    LessonFactory,
    UserFactory,
    CourseStatisticFactory,
    LessonStatisticFactory,
    MessageFactory,
)

@pytest.mark.django_db
def test_create_course():
    course = CourseFactory(full_name="Python developer", name="Python", homework_all=10)

    assert course.name == 'Python'


@pytest.mark.django_db
def test_create_lesson():
    course = CourseFactory(full_name="Python developer", name="Python", homework_all=10)
    lesson = LessonFactory(lesson_title='pytest', homework_title='create pytest', lesson_number=1, course=course)

    assert lesson.course == course
    assert lesson.course.name == 'Python'
    assert lesson.lesson_title == 'pytest'

@pytest.mark.django_db
def test_create_course_statistic():
    course = CourseFactory(full_name="Python developer", name="Python", homework_all=10)
    user = UserFactory(username='student', email='student@mail.com')
    course_statistic = CourseStatisticFactory(course=course, user=user)

    assert course_statistic.course == course
    assert course_statistic.course.name == 'Python'
    assert course_statistic.user.username == 'student'
    assert course_statistic.homework_done == 0


@pytest.mark.django_db
def test_create_lesson_statistic():
    course = CourseFactory(full_name="Python developer", name="Python", homework_all=10)
    user = UserFactory(username='student', email='student@mail.com')
    lesson = LessonFactory(lesson_title='pytest', homework_title='create pytest', lesson_number=1, course=course)
    lesson_statistic = LessonStatisticFactory(course=course, lesson=lesson, user=user)

    assert lesson_statistic.user == user
    assert lesson_statistic.course.name == 'Python'
    assert lesson_statistic.lesson == lesson
    assert lesson_statistic.homework_status == 1

@pytest.mark.django_db
def test_create_message():
    message = MessageFactory(message_body = 'Hello!')
    assert message.message_body == 'Hello!'