# Emails used and sent for authentication purposes
from django.conf import settings

# NOTE:  String format keywords with double braces around them will be formatted at a later point

report_link = "{}/report/".format(settings.SITE_BASE_URL)

activate_account = {
    'subject': 'JamJar Account Activation',
    'from_email': 'JamJar Support <support@projectjamjar.com>',
    'headers': {
        'Reply-To': 'support@projectjamjar.com'
    },
    'text': """
Hello from JamJar!

Thanks for signing up for JamJar!  We know you're excited to get started, so click this link:
{{activate_link}}
to activate your account!

If this was unintentional you may ignore this email.
If you never signed up please report this issue at {report_link}.

Thanks,
JamJar Support
""".format(report_link=report_link),
    'html': """
<a href="http://projectjamjar.com">
    <img src="http://projectjamjar.com/assets/images/logo.png" alt="logo" width="400" height="200"/>
</a>
<p>Hello from JamJar!</p>

<p>
Thanks for signing up for JamJar!  We know you're excited to get started, so click this link:
<a href="{{activate_link}}" alt="Activation link">{{activate_link}}</a>
to activate your account!
</p>

<p>
If this was unintentional you may ignore this email.
If you never signed up please report this issue <a href="{report_link}" alt="Report link">here</a>.
</p>

<p>
Thanks,
JamJar Support
</p>
""".format(report_link=report_link)
}

activation_successful = {
    'subject': 'JamJar Account Activation Successful',
    'from_email': 'JamJar Support <support@projectjamjar.com>',
    'headers': {
        'Reply-To': 'support@projectjamjar.com'
    },
    'text': """
Hello from JamJar!

You've succesfully activated your jamjar account!  You can now go to:
{{login_link}}
to sign in and get started!

If this was unintentional you may ignore this email.
If you never signed up please report this issue at {report_link}.

Thanks,
JamJar Support
""".format(report_link=report_link),
    'html': """
<a href="http://projectjamjar.com">
    <img src="http://projectjamjar.com/assets/images/logo.png" alt="logo" width="400" height="200"/>
</a>
<p>Hello from JamJar!</p>

<p>
You've succesfully activated your jamjar account!  You can now go to:
<a href="{{login_link}}" alt="Login link">{{login_link}}</a>
to sign in and get started!
</p>

<p>
If this was unintentional you may ignore this email.
If you never signed up please report this issue <a href="{report_link}" alt="Report link">here</a>.
</p>

<p>
Thanks,
JamJar Support
</p>
""".format(report_link=report_link)
}

password_reset = {
    'subject': 'JamJar Password Reset',
    'from_email': 'JamJar Support <support@projectjamjar.com>',
    'headers': {
        'Reply-To': 'support@projectjamjar.com'
    },
    'text': """
Hello from JamJar!

You requested a password reset.  If you really did, go to this link:
{{reset_link}}
to reset your password.

If this was unintentional you may ignore this email, your old password is still active.
If you never requested a password reset please report this issue {report_link}.

Thanks,
JamJar Support
""".format(report_link=report_link),
    'html': """
<a href="http://projectjamjar.com">
    <img src="http://projectjamjar.com/assets/images/logo.png" alt="logo" width="400" height="200"/>
</a>
<p>Hello from JamJar!</p>

<p>
You requested a password reset.  If you really did, go to this link:
<a href="{{reset_link}}" alt="Reset link">{{reset_link}}</a>
to reset your password.
</p>

<p>
If this was unintentional you may ignore this email, your old password is still active.
If you never requested a password reset please report this issue <a href="{report_link}" alt="Report link">here</a>.
</p>

<p>
Thanks,
JamJar Support
</p>
""".format(report_link=report_link)
}

# This is a static link where the user can request a password reset
static_reset_link = "{}/password/reset".format(settings.SITE_BASE_URL)

password_reset_success = {
    'subject': 'JamJar Password Reset Successful',
    'from_email': 'JamJar Support <support@projectjamjar.com>',
    'headers': {
        'Reply-To': 'support@projectjamjar.com'
    },
    'text': """
Hello from JamJar!

Your password has been successfully reset.

If this was unintentional or this was not you, please go to {static_reset_link} to change your password again.
If you never requested a password reset please report this issue <a href="{report_link}" alt="Report link">here</a>.

Thanks,
JamJar Support
""".format(static_reset_link=static_reset_link,report_link=report_link),
    'html': """
<a href="http://projectjamjar.com">
    <img src="http://projectjamjar.com/assets/images/logo.png" alt="logo" width="400" height="200"/>
</a>
<p>Hello from JamJar!</p>

<p>
Your password has been successfully reset.
</p>

<p>
If this was unintentional or this was not you, please go to <a href="{static_reset_link}" alt="Reset link">{static_reset_link}</a> to change your password again.
If you never requested a password reset please report this issue <a href="{report_link}" alt="Report link">here</a>.
</p>

<p>
Thanks,
JamJar Support
</p>
""".format(static_reset_link=static_reset_link,report_link=report_link)
}

# This is a static link where the user can request a password reset
static_signup_link = "{}/signup/".format(settings.SITE_BASE_URL)

invite = {
    'subject': 'You\'ve been invited to join JamJar!',
    'from_email': 'JamJar Support <support@projectjamjar.com>',
    'headers': {
        'Reply-To': 'support@projectjamjar.com'
    },
    'text': """
Hello from JamJar!

You've been invited by {{invitor_name}} ({{invitor_email}}) to sign up for JamJar, the newest Tour Mangement Platform on the market!
{{message}}


To sign up, simply go to
{{invite_link}}

If you would like to stop recieving invites to JamJar, please let us know at {report_link}.

Thanks,
JamJar Support
""".format(report_link=report_link),
    'html': """
<a href="http://projectjamjar.com">
    <img src="http://projectjamjar.com/assets/images/logo.png" alt="logo" width="400" height="200"/>
</a>
<p>Hello from JamJar!</p>

<p>
You've been invited by {{invitor_name}} to sign up for JamJar, the newest Tour Mangement Platform on the market!
<i>{{message}}</i>
</p>

<p>
To sign up, simply head to
<a href="{{invite_link}}" alt="Invite link">{{invite_link}}</a>
</p>

<p>
If you would like to stop recieving invites to JamJar, please let us know at <a href="{report_link}" alt="Report link">here</a>.
</p>

<p>
Thanks,
JamJar Support
</p>
""".format(report_link=report_link)
}
