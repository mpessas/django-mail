# -*- coding: utf-8 -*-

"""
The mail backends provided by the app.
"""

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
