# -*- coding: utf-8 -*-

"""
The mail backends provided by the app.
"""

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


class MailMixin(object):
    """Base class for all Mail classes."""

    from_address = None
    subject = None
    body_template = None

    def __init__(self, to, context):
        """
        Initializer.

        :param to: A list of email addresses, where the emal should be sent to.
        :param context: A ``Context`` instance that will be used to populate
            the email template.
        """
        self.to_addresses = to
        self.body = self._render_body(context)
        super(MailMixin, self).__init__(
            self.subject, self.body, self.from_address, self.to_addresses
        )

    def _render_body(self, context):
        """Render the body of the email message."""
        return render_to_string(self.body_template, context)


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

    def __init__(self, to, context):
        self.html_part = self._render_html_body(context)
        super(TextAltHtmlMail, self).__init__(to, context)
        self.attach_alternative(self.html_part, "text/html")

    def _render_html_body(self, context):
        """Render the HTML part of the mail."""
        return render_to_string(self.html_template, context)
