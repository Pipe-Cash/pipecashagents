#TODO: implement agents

class EmailSend:

    description = '''Sends an email with the specified 'subject' and 'body' to the specified recipients (to_emails).
    
    Options:
        "to_emails": recepient emails, separated by commas (,)
        "subject": the title of the email
        "body": the content of the email

        (optional) from_email: a sender email. If not included, the SMTP_USERNAME secret will be used instead

    Multiple secret values are required to send an email.
    They describe the connection to the SMTP server:

        "SMTP_SERVER": address of the server (for example: smtp.gmail.com)
        "SMTP_PORT": port or the smtp server (usually 465)
        "SMTP_LOGIN": Boolean - true login is required
        "SMTP_USE_SSL": Boolean - true if the connection should use SSL
        "SMTP_USE_TLS": Boolean - true if the connection should use SSTARTTLS
        "SMTP_USERNAME": your username (your email)
        "SMTP_PASSWORD": your password
    '''

    event_description = { 'state': 'success' }

    default_options = {
        "to_emails": "addr1@gmail.com,addr2@gmail.com",
        "subject": "Automatic email from PipeCash",
        "body": "This email was sent automatically from PipeCash",
    }
    uses_secret_variables = [
        "SMTP_SERVER",
        "SMTP_PORT",
        "SMTP_LOGIN",
        "SMTP_USE_SSL",
        "SMTP_USE_TLS",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
    ]

    def start(self, log):
        self.log = log

    def __init__(self):
        self.options = {}
        self.secrets = {}

    def validate_options(self):
        assert hasattr(self.options, "to_emails")
        assert hasattr(self.options, "subject")
        assert hasattr(self.options, "body")
        pass

    def check_dependencies_missing(self):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib
        import ssl

    def receive(self, event, create_event):
        try:
            self.send_email(event, create_event)
            create_event({ 'state': 'success' })
        except Exception as e:
            create_event({ 'state': 'error', 'error': str(e) })

    def send_email(self, event, create_event):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib
        import ssl
        
        to_emails = self.options["to_emails"].split(",") # must be a list
        subject = str(self.options["subject"])
        body = str(self.options["body"])
        from_email = self.options["from_email"] if hasattr(self.options, "from_email") else None

        SMTP_SERVER = self.secrets["SMTP_SERVER"]
        SMTP_PORT = self.secrets["SMTP_PORT"]
        SMTP_LOGIN = self.secrets["SMTP_LOGIN"]
        SMTP_USE_SSL = self.secrets["SMTP_USE_SSL"]
        SMTP_USE_TLS = self.secrets["SMTP_USE_TLS"]
        SMTP_USERNAME = self.secrets["SMTP_USERNAME"]
        SMTP_PASSWORD = self.secrets["SMTP_PASSWORD"]
        
        if from_email is None:
            from_email = SMTP_USERNAME

        # Prepare actual message

        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = ",".join(to_emails)
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        # Send the mail
        
        if SMTP_USE_SSL:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        if SMTP_USE_TLS: 
            server.starttls()

        if SMTP_LOGIN:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)

        server.sendmail(from_addr=from_email, to_addrs=to_emails, msg=message.as_string())
        server.quit()
