from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Course, Lesson, LessonStatistic, CourseStatistic, Message
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from . import serializers

from .datas.teachers import Teachers



class LessonVieSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def lesson_vs_statistic(self, request, courseId):
        try:
            qs = LessonStatistic.objects.filter(user=request.user).filter(course_id=courseId)
        except LessonStatistic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)

        return Response(serializer.data)

    def course_statistic(self, request, courseId):
        try:
            c = CourseStatistic.objects.filter(user=request.user).filter(course_id=courseId).first()
        except CourseStatistic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CourseStatisticSerializer(c)
        return  Response(serializer.data)

    def user_course_list(self, request):
        try:
            course_stat = CourseStatistic.objects.filter(user = request.user)
        except CourseStatistic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CourseStatisticSerializer(course_stat, many=True)
        return Response(serializer.data)

    def get_students_statistics(self, request, userId, courseId):
        try:
            qs = LessonStatistic.objects.filter(user_id=userId).filter(course_id=courseId).filter(user__profile__status=1)
        except LessonStatistic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)
        return Response(serializer.data)


    def get_teacher_courses(self, request):
        user = request.user
        if user.profile.status==2:
            try:
                course_stat = CourseStatistic.objects.filter(user=request.user)
            except CourseStatistic.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            course_stat=[]
        serializer = serializers.CourseStatisticSerializer(course_stat, many=True)
        return Response(serializer.data)



class CourseVieSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def get_one_course(self, request, courseId):
        try:
            course = Course.objects.filter(id=courseId).first()
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CourseSerializer(course)
        return Response(serializer.data)

    def get_all_courses(self, request):
        try:
            course = Course.objects.all()
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CourseSerializer(course, many=True)
        return Response(serializer.data)


class TeachersVieSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def get_short_teacher_list(self, request):
        return Response(Teachers)


class HomeworkStatusChange(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, statisticId):
        try:
            statistic = LessonStatistic.objects.filter(id = statisticId).first()
        except LessonStatistic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        stat = request.data['status']
        statistic.homework_status = int(stat)
        statistic.save()
        self.save_done_status(stat, statistic.user_id)
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def save_done_status(status, userId):
        if int(status) == 4:
            try:
                course_stat = CourseStatistic.objects.filter(user_id=userId).first()
            except CourseStatistic.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            course_stat.homework_done += 1
            course_stat.save()



class CourseTest(APIView):

    def post(self, request, courseId):
        test = request.data['testResult']
        user = request.user
        try:
            course = Course.objects.filter(id=courseId).first()
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        statistic = CourseStatistic.objects.filter(user_id=user.id).filter(course_id=course.id).exists()

        content = {'message': 'Вы уже прошли тест и зачислены на курс'}
        if not statistic:
            content = {'message': 'Тест не пройден'}
            if test['testResult'] and test['testResult'] == '4':

                course_stat = CourseStatistic()
                course_stat.user = user
                course_stat.course = course
                course_stat.is_active = True
                course_stat.save()
                try:
                    lessons = Lesson.objects.filter(course_id=course.id)
                except Lesson.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                for lesson in lessons:
                    lesson_stat = LessonStatistic()
                    lesson_stat.lesson = lesson
                    lesson_stat.user = user
                    lesson_stat.course = course
                    lesson_stat.save()
            else:
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class SaveChatMessage(APIView):

    def post(self, request ):
        data = request.data
        user = request.user
        try:
            statistic = LessonStatistic.objects.filter(id = data['statisticId']).first()
        except LessonStatistic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        message = Message()
        message.lesson_statistic = statistic
        message.message_body = data['message']
        message.user = user
        message.save()
        return Response(status=status.HTTP_201_CREATED)


class GetChatMessage(viewsets.ViewSet):

    def get_message(self, request, statisticId):
        try:
            message = Message.objects.filter(lesson_statistic__id = statisticId)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = serializers.MessageSerializer(message, many=True)

        return Response(s.data)


class RegisterTeacherOnCourse(APIView):

    def post(self, request, courseId):
        if request.user.profile.status == 2:
            stat = CourseStatistic.objects.filter(user_id=request.user.id).filter(course_id=courseId).exists()
            content = {'message': 'Вы уже зарегестрированны на этот курс'}
            if not stat:
                CourseStatistic.objects.create(user=request.user, course_id=courseId)

                return Response(status=status.HTTP_201_CREATED)
            return Response(content, status=status.HTTP_400_BAD_REQUEST)



