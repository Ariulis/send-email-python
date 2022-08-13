import mimetypes
import os
import smtplib
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

from colorama import Fore, init
from dotenv import load_dotenv
from tqdm import tqdm

init()

dotenv_path = 'env/.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def send_email(text=None, template=None):
    sender = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        with open(template) as f:
            template = f.read()
    except IOError:
        template = None

    try:
        server.login(sender, password)
    except Exception as _ex:
        print('Check your login or password!')
        raise _ex
    else:
        msg = MIMEMultipart()
        msg['From'] = f'{sender}@gmail.com'
        msg['To'] = f'{sender}@gmail.com'
        msg['Subject'] = 'Happy birthday! Only today is discount on the promo code till 99%'

        if text:
            msg.attach(MIMEText(text))

        if template:
            msg.attach(MIMEText(template, 'html'))

        print(f'{Fore.GREEN}Collecting...')

        for file in tqdm(os.listdir('attachments')):
            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split('/')

            if file_type == 'text':
                with open(f'attachments/{file}') as f:
                    file = MIMEText(f.read())

            elif file_type == 'image':
                with open(f'attachments/{file}', 'rb') as f:
                    file = MIMEImage(f.read(), subtype)

            elif file_type == 'audio':
                with open(f'attachments/{file}', 'rb') as f:
                    file = MIMEAudio(f.read(), subtype)

            elif file_type == 'application':
                with open(f'attachments/{file}', 'rb') as f:
                    file = MIMEApplication(f.read(), subtype)

            else:
                with open(f'attachments/{file}', 'rb') as f:
                    file = MIMEBase(file_type, subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            file.add_header('content-disposition',
                            'attachment', filename=filename)
            msg.attach(file)

            sleep(.4)

        print(f'{Fore.BLUE}Sending...')
        server.sendmail(sender, sender, msg.as_string())

        return 'The message was sent successfully!'


def main():
    print(f'{Fore.CYAN}Type text or press enter: ')
    text = input()
    print(f'{Fore.MAGENTA}Type template name or press enter: ')
    template = input()
    print(send_email(text=text, template=template))


if __name__ == '__main__':
    main()
