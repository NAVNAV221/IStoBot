from twilio.rest import Client

from Alerts.alert import Alert
from consts.alerts.sms import Twilio


class Sms(Alert):
    def __init__(self):
        super().__init__()
        self.client = Client(Twilio.ACCOUNT_SID, Twilio.AUTH_TOKEN)

    def send_sms(self, body: str, sender: str, receiver: str):
        message = self.client.messages.create(from_=sender,
                                              body=body,
                                              to=receiver)

        return message.sid

if __name__ == '__main__':
    s = Sms()
    s.send_sms(body='aaa', sender='whatsapp:+14155238886', receiver='whatsapp:+972526368078')
