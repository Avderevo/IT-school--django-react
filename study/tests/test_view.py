import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from users.tests.test import TokenTestCase


class StudyViewApiTest(TokenTestCase):
    client = APIClient()
    fixtures = ['course.json', 'lessons.json']

    def setUp(self):
        super(StudyViewApiTest, self).setUp()

        self.course_1_id = 1
        self.course_2_id = 2

        self.student = self.client.post(
            reverse(
                "users:create_user",

            ),
            data=json.dumps(
                {
                    "username": 'student',
                    "password": 'password',
                    "email": 'sdudent@gmail.com',
                    "status": 1
                }
            ),
            content_type='application/json'
        )

        self.teacher = self.client.post(
            reverse(
                "users:create_user",

            ),
            data=json.dumps(
                {
                    "username": 'teacher',
                    "password": 'password',
                    "email": 'teachert@gmail.com',
                    "status": 2
                }
            ),
            content_type='application/json'
        )

    def course_test_done(self, courseId):
        token = self.get_token('student', 'password')
        url = reverse('study:course_test', kwargs={'courseId': courseId})
        self.client.post(url, headers={'token': token}, data={"testResult": {'testResult': '4'}},
                                    format='json')

    def register_teacher_on_course(self, courseId):
        token = self.get_token('teacher', "password")
        url = reverse('study:register_teacher_course', kwargs={'courseId': courseId})
        self.client.post(url, headers={'token': token})

    def save_chat_message(self, statisticId, message):
        self.course_test_done(self.course_1_id)
        token = self.get_token('student', "password")
        url = reverse('study:save_chat_message')
        self.client.post(url, headers={'token': token}, data={'statisticId': statisticId, 'message': message})


    def test_course_test_done(self):
        token = self.get_token('student', "password")
        url = reverse('study:course_test', kwargs={'courseId': self.course_1_id})
        response = self.client.post(url,  headers={'token':token},
                                    data={"testResult":{'testResult':'4'}}, format='json')
        self.assertEqual(201, response.status_code)

    def test_repeated_course_test_done(self):
        token = self.get_token('student', "password")
        url = reverse('study:course_test', kwargs={'courseId': self.course_1_id})
        self.client.post(url, headers={'token': token}, data={"testResult": {'testResult': '4'}},
                                    format='json')
        response = self.client.post(url, headers={'token': token}, data={"testResult": {'testResult': '4'}},
                                    format='json')

        self.assertEqual(400, response.status_code)

    def test_lesson_vs_statistic(self):
        self.course_test_done(self.course_1_id)

        token = self.get_token('student', "password")
        url = reverse(
            "study:user_statistics", kwargs={'courseId':self.course_1_id}
        )
        response = self.client.get(url, headers={'token':token})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data[0]['lesson']['id'], 1)
        self.assertEqual(response.data[1]['lesson']['id'], 2)

    def test_course_statistic(self):
        token = self.get_token('student', "password")
        url = reverse(
            "study:course_statistic", kwargs={'courseId': self.course_1_id}
        )
        response = self.client.get(url, headers={'token': token})
        self.assertEqual(200, response.status_code)

    def test_user_course_list(self):
        token = self.get_token('teacher', "password")
        self.course_test_done(self.course_1_id)
        self.course_test_done(self.course_2_id)
        url = reverse(
            "study:user_courses"
        )
        response = self.client.get(url, headers={'token': token})
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.data), 2)

    def test_get_students_statistics(self):
        token = self.get_token('teacher', "password")
        self.course_test_done(self.course_1_id)
        url = reverse('study:student_statistics', kwargs={'userId':2, 'courseId':self.course_1_id})
        response = self.client.get(url, headers={'token': token})
        self.assertEqual(response.status_code, 200)

    def test_register_teacher_on_course(self):
        token = self.get_token('teacher', "password")
        url = reverse('study:register_teacher_course', kwargs={'courseId': self.course_1_id})
        response = self.client.post(url, headers={'token': token})
        self.assertEqual(response.status_code, 201)

    def test_get_teacher_courses(self):
        token = self.get_token('teacher', "password")
        self.register_teacher_on_course(self.course_1_id)
        self.register_teacher_on_course(self.course_2_id)
        url = reverse('study:teacher-courses')
        response = self.client.get(url, headers={'token': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_one_course(self):
        url = reverse('study:get_one_course', kwargs={'courseId': self.course_1_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.course_1_id)

    def test_get_all_courses(self):
        url = reverse('study:get_all_courses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_homework_status_change(self):
        self.course_test_done(self.course_1_id)
        token = self.get_token('teacher', "password")
        url = reverse('study:change_homework_status', kwargs={'statisticId':1})
        response = self.client.post(url, headers={'token': token}, data={'status':2} )
        self.assertEqual(response.status_code, 201)


    def test_save_chat_message(self):
        self.course_test_done(self.course_1_id)
        token = self.get_token('student', "password")
        url = reverse('study:save_chat_message')
        response = self.client.post(url, headers={'token': token}, data={'statisticId': 1, 'message':'Hello'})
        self.assertEqual(response.status_code, 201)


    def test_get_chat_message(self):
        self.course_test_done(self.course_1_id)
        token = self.get_token('student', "password")
        self.save_chat_message(1, 'Hello world!')
        url = reverse('study:get_chat_message', kwargs={'statisticId':1})
        response=self.client.get(url, headers={'token': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['message_body'], 'Hello world!')



