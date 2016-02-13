import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from nameko.events import event_handler, BROADCAST

import CONFIG

class MailService(object):
    name = 'mail'

    SUBJECT = "Payment Received"
    TEXT = """\
Dear {payee},

You have received a payment of {amount} {currency} from {client} ({email}).

Yours,
student.com
"""

    @event_handler('payments', 'payment_received', handler_type=BROADCAST)
    def on_payment_received(self, param):
        "Returns True if succeeded, False if failed."
        succ = False
        try:
            self._send_mail(**param)
            succ = True
        except Exception as e:
            print e.message
        finally:
            return succ

    def _send_mail(self, client, payee, payment):
        s = None
        try:
            text = MailService.TEXT.format(
                client = client['name'],
                email = client['email'],
                payee = payee['name'],
                amount = payment['amount'],
                currency = payment['currency'],
            )

            msg = MIMEText(text)
            msg['Subject'] = MailService.SUBJECT
            msg['From'] = CONFIG.MAIL_FROM
            msg['To'] = payee['email']

            s = smtplib.SMTP(CONFIG.MAIL_HOST, CONFIG.MAIL_PORT)
            s.ehlo(); s.starttls(); s.ehlo()
            s.login(CONFIG.MAIL_USERNAME, CONFIG.MAIL_PASSWORD)
            s.sendmail(msg['From'], msg['To'], msg.as_string())
        except Exception as e:
            raise e
        finally:
            if s:
                s.quit()
