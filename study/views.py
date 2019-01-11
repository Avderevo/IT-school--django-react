from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Course, Lesson, LessonStatistic, CourseStatistic, Message
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from . import serializers
from study.fixtures.teachers import Teachers


class LessonVieSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def lesson_vs_statistic(self, request, courseId):
        qs = LessonStatistic.objects.filter(user=request.user, course_id=courseId)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)
        return Response(serializer.data)

    def course_statistic(self, request, courseId):
        c = CourseStatistic.objects.filter(user=request.user, course_id=courseId).first()
        serializer = serializers.CourseStatisticSerializer(c)
        return  Response(serializer.data)

    def user_course_list(self, request):
        course_stat = CourseStatistic.objects.filter(user = request.user)
        serializer = serializers.CourseStatisticSerializer(course_stat, many=True)
        return Response(serializer.data)

    def get_students_statistics(self, request, userId, courseId):
        qs = LessonStatistic.objects.filter(course_id=courseId, user__profile__status=1, user_id=userId)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)
        return Response(serializer.data)

    def get_teacher_courses(self, request):
        user = request.user
        if user.profile.status==2:
            course_stat = CourseStatistic.objects.filter(user=request.user)
        else:
            course_stat=[]
        serializer = serializers.CourseStatisticSerializer(course_stat, many=True)
        return Response(serializer.data)


class CourseVieSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def get_one_course(self, request, courseId):
        course = Course.objects.filter(id=courseId).first()
        serializer = serializers.CourseSerializer(course)
        return Response(serializer.data)

    def get_all_courses(self, request):
        course = Course.objects.all()
        serializer = serializers.CourseSerializer(course, many=True)
        return Response(serializer.data)


class TeachersVieSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def get_short_teacher_list(self, request):
        return Response(Teachers)


class HomeworkStatusChange(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, statisticId):
        statistic = LessonStatistic.objects.filter(id=statisticId).first()
        stat = request.data['status']
        statistic.homework_status = int(stat)
        statistic.save()
        self.save_done_status(stat, statistic.user_id)
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def save_done_status(status, userId):
        if int(status) == 4:
            course_stat = CourseStatistic.objects.filter(user_id=userId).first()
            course_stat.homework_done += 1
            course_stat.save()


class CourseTest(APIView):

    def post(self, request, courseId):
        test = request.data['testResult']
        user = request.user
        course = Course.objects.filter(id=courseId).first()
        statistic = CourseStatistic.objects.filter(user_id=user.id).filter(course_id=course.id).exists()
        content = {'message': 'Вы уже прошли тест и зачислены на курс'}

        if not statistic:
            content = {'message': 'Тест не пройден'}

            if test['testResult'] and test['testResult'] == '4':
                CourseStatistic.objects.create(user = user, course = course, is_active = True)
                lessons = Lesson.objects.filter(course_id=course.id)

                for lesson in lessons:
                    LessonStatistic.objects.create(lesson = lesson, user = user, course = course)
            else:
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class SaveChatMessage(APIView):

    def post(self, request ):
        data = request.data
        user = request.user
        statistic = LessonStatistic.objects.filter(id = data['statisticId']).first()
        Message.objects.create(lesson_statistic = statistic, message_body = data['message'], user = user)
        return Response(status=status.HTTP_201_CREATED)


class GetChatMessage(viewsets.ViewSet):

    def get_message(self, request, statisticId):
        message = Message.objects.filter(lesson_statistic__id = statisticId)
        s = serializers.MessageSerializer(message, many=True)
        return Response(s.data)


class RegisterTeacherOnCourse(APIView):

    def post(self, request, courseId):

        if request.user.profile.status == 2:
            stat = CourseStatistic.objects.filter(user_id=request.user.id, course_id=courseId).exists()
            content = {'message': 'Вы уже зарегестрированны на этот курс'}

            if not stat:
                CourseStatistic.objects.create(user=request.user, course_id=courseId)
                return Response(status=status.HTTP_201_CREATED)
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
