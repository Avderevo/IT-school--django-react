from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django_rq import job


def send_mail(to, template, context):
    html_content = render_to_string(
        'emails/{}.html'.format(template), context)
    text_content = render_to_string(
        'emails/{}.txt'.format(template), context)

    msg = EmailMultiAlternatives(
        context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@job('default')
def send_confirm_email(request, email, code):
    context = {
        'subject': ('Profile activation'),
        'uri': request.build_absolute_uri(
            reverse('users:confirm', kwargs={'code': code})),
    }
    send_mail(email, 'activate_profile', context)

