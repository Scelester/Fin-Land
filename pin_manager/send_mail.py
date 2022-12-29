import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "official.bcu.finland@gmail.com"  # Enter your address
client_email = "saileshraj652@gmail.com"  # Enter receiver address
password = "bidkjqmgzvqzkeiw"


def send_mail(Subject,body):
    message = f"""\
    Subject: {Subject}

    {body} """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, client_email, message)