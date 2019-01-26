# Generated by Django 2.1.4 on 2019-01-07 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='Полное название')),
                ('name', models.CharField(max_length=50, verbose_name='Короткое название')),
                ('homework_all', models.IntegerField(blank=True, verbose_name='Всего ДЗ')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('date_start', models.CharField(blank=True, max_length=50)),
                ('label', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='CourseStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework_done', models.IntegerField(default=0, verbose_name='Сделанных домашек')),
                ('is_active', models.BooleanField(default=False, verbose_name='Тестирование')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Курс оплачен')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Course', verbose_name='Курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Статистика курса',
                'verbose_name_plural': 'Статистика курсов',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_title', models.CharField(max_length=125, verbose_name='Название урока')),
                ('is_homework', models.BooleanField(default=False)),
                ('homework_title', models.CharField(blank=True, max_length=125, verbose_name='Домашнее задание')),
                ('lesson_number', models.IntegerField(verbose_name='Номер урока')),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
        migrations.CreateModel(
            name='LessonStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework_status', models.IntegerField(choices=[(1, 'Не активно'), (2, 'Активно'), (3, 'На проверке'), (4, 'Принято')], default=1, verbose_name='Статус домашнего задания')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Course', verbose_name='Курс')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Lesson', verbose_name='Урок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Статистика урока',
                'verbose_name_plural': 'Статистика уроков',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_body', models.TextField(blank=True, verbose_name='Текст сообщения')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата сообщения')),
                ('lesson_statistic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.LessonStatistic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]