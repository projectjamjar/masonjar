from django.db import IntegrityError
from jamjar.base.views import BaseView, authenticate
from .serializers import FeedbackSerializer

import datetime
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

class FeedbackView(BaseView):
    serializer_class = FeedbackSerializer

    """
    Description:
        Create some feedback and send it to us :'(
        (hopefully it's good feedback)

    Request:
        POST /feedback/
        {
            "email": "user@email.com",
            "name": "User Name",
            "relevant_url": "http://www.projectjamjar.com/#/concerts/4", (this is optional)
            "feedback": "This is the message weeeeeeeeee!!!"
        }

    Response:
        The newly created feedback
    """
    def post(self, request):
        # Validate the request
        self.serializer = self.get_serializer(data=self.request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        try:
            obj = self.serializer.save()
        except IntegrityError as e:
            return self.error_response(str(e), 400)


        # If the feedback was created, lets send an email to ourselves
        email_subject = 'JamJar Feedback Submitted'

        for_url = "For URL: {}".format(obj.relevant_url) if obj.relevant_url else ""

        email_body = """
        *JamJar feedback submitted*

        Submitted by {} <{}>:
        {}

        {}
        {}
        """.format(obj.name, obj.email, obj.feedback, for_url, obj.created_at.strftime('%m-%d-%Y %I:%M%p'))

        to_emails = ['mark@markkoh.net',
                     'drewbanin@gmail.com']

        mail = EmailMessage(
            email_subject,
            email_body,
            'JamJar Support <support@projectjamjar.com>',
            to_emails
        )
        mail.content_subtype = 'html'

        # if not settings.DEBUG:
        mail.send()

        return self.success_response(self.serializer.data)
