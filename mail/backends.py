# -*- coding: utf-8 -*-

"""
The mail backends provided by the app.
"""

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


class MailMixin(object):
    """Base class for all Mail classes."""

    from_address = None
    subject_template = None
    body_template = None

    def __init__(self, to, context, **kwargs):
        """
        Initializer.

        :param to: A list of email addresses, where the emal should be sent to.
        :param context: A ``Context`` instance that will be used to populate
            the email template.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.to_addresses = to
        if not hasattr(self, 'body'):
            self.body = self._render_body(context)
        if not hasattr(self, 'subject'):
            self.subject = self._render_subject(context)
        super(MailMixin, self).__init__(
            self.subject, self.body, self.from_address, self.to_addresses
        )

    def _render_body(self, context):
        """Render the body of the email message."""
        return render_to_string(self.body_template, context)

    def _render_subject(self, context):
        """Render the subject of the email message."""
        return ''.join(
            render_to_string(self.subject_template, context).splitlines()
        )


class TextMail(MailMixin, EmailMessage):
    """Send email as plain text."""


class HtmlMail(MailMixin, EmailMessage):
    """Send mail as HTML."""

    def __init__(self, *args, **kwargs):
        """Set the mimetype to html."""
        super(HtmlMail, self).__init__(*args, **kwargs)
        self.content_subtype = 'html'


class TextAltHtmlMail(MailMixin, EmailMultiAlternatives):
    """Send both text and HTML in the email."""

    html_template = None

    def __init__(self, to, context, **kwargs):
        super(TextAltHtmlMail, self).__init__(to, context, **kwargs)
        self.html_part = self._render_html_body(context)
        self.attach_alternative(self.html_part, "text/html")

    def _render_html_body(self, context):
        """Render the HTML part of the mail."""
        return render_to_string(self.html_template, context)
