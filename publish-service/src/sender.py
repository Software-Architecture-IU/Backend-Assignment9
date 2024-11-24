import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(smtp_server, port, username, password, recipients, subject, message_body):
    try:
        mail = MIMEMultipart()
        mail['From'] = username
        mail['Subject'] = subject

        mail.attach(MIMEText(message_body, 'plain'))

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(username, password)

            for recipient in recipients:
                mail['To'] = recipient
                server.sendmail(username, recipient, mail.as_string().encode('utf-8'))
            logging.info(f'Email sent to all the recipients: {recipients}')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
