import requests


class MailgunApi:
    """
    This class will be used to send emails
    """

    API_URL = "https://api.mailgun.net/v3/{}/messages"

    def __init__(self, domain, api_key):
        """
        Initializes the mail gun api required fields
        :param domain: mailgun domain
        :param api_key: api_key
        """
        self.domain = domain
        self.api_key = api_key
        self.base_url = self.API_URL.format(self.domain)

    def send_email(self, to, subject, text, html=None) -> requests.Response:
        """
        This method is used to send email
        :param to: destination
        :param subject: subject
        :param text: text
        :param html: html
        :return: response
        """

        if not isinstance(to, (list, tuple)):
            to = [to, ]

        data = {
            'from': f"InstaCook <no-replay@{self.domain}>",
            'to': to,
            'subject': subject,
            'text': text,
            'html': html,
        }

        response = requests.post(url=self.base_url,
                                 auth=('api', self.api_key),
                                 data=data)
        return response
