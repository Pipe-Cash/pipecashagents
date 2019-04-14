import datetime
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl

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
        assert "to_emails" in self.options, "'to_emails' not present in options"
        assert "subject" in self.options, "'subject' not present in options"
        assert "body" in self.options, "'body' not present in options"

    def receive(self, event, create_event):
        try:
            self.send_email(event, create_event)
            create_event({ 'state': 'success' })
        except Exception as e:
            create_event({ 'state': 'error', 'error': str(e) })

    def send_email(self, event, create_event):
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
        
        try:
            if SMTP_USE_TLS: 
                server.starttls()
            if SMTP_LOGIN:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(from_addr=from_email, to_addrs=to_emails, msg=message.as_string())
        finally:
            server.quit()



class OnNewEmail:

    description = '''Checks for new emails in your inbox.
    Creates a new event for each email received after the last time it checked.
    
    Options:
        "max_emails": Nimber - only check the last N emails. (leave 0 to check all new emails)
        "mail_folder": String - the folder being checked
        "search_filter": String - fiter for the mails to consider or ignore.
                        Default is "ALL". Example "FROM foo@gmail.com"

    Multiple secret values are required to read your email.
    They describe the connection to the IMAP server:

        "IMAP_SERVER": address of the server (for example: imap.gmail.com)
        "IMAP_PORT": port or the smtp server (usually 993)
        "IMAP_LOGIN": Boolean - true login is required
        "IMAP_USE_SSL": Boolean - true if the connection should use SSL
        "IMAP_USERNAME": your username (your email)
        "IMAP_PASSWORD": your password

    In case of failure, the created event will look like this:
    { 'state': 'error', 'error': 'Error Message' }

    In case of success, a separate event will be created for each new email.
    {
        'Subject': 'subject',
        'From': 'Foo Bar <foobar@gmail.com>', 
        'Date': 'Sat, 30 Mar 2019 00:15:58 +0200', 
        'Text': 'Text Text Text Text', 
        'To': 'Bar Foo <barfoo@gmail.com>'
    }
    '''

    event_description = {
        'Subject': 'subject',
        'From': 'Foo Bar <foobar@gmail.com>', 
        'Date': 'Sat, 30 Mar 2019 00:15:58 +0200', 
        'Text': 'Text Text Text Text', 
        'To': 'Bar Foo <barfoo@gmail.com>'
    }

    default_options = {
        "max_emails": 0,
        "mail_folder": "inbox",
        "search_filter": "ALL",
    }
    uses_secret_variables = [
        "IMAP_SERVER",
        "IMAP_PORT",
        "IMAP_LOGIN",
        "IMAP_USE_SSL",
        "IMAP_USERNAME",
        "IMAP_PASSWORD",
    ]

    def start(self, log):
        self.log = log

    def __init__(self):
        self.options = {}
        self.secrets = {}

        self.first_check = True

    def validate_options(self):
        assert "max_emails" in self.options, "'max_emails' not present in options"
        assert "mail_folder" in self.options, "'mail_folder' not present in options"

    def check(self, create_event):
        try:
            self.read_emails(create_event)
        except Exception as e:
            create_event({ 'state': 'error', 'error': str(e) })
            raise(e)

    def selectFolder(self, mail, mail_folder):
        try:
            mail.select(mail_folder)
        except Exception as e1:
            try:
                # try to get names of all folders
                listOfFolders = mail.list()
                raise AttributeError("Error while selecting '%s': %s.\nDetails:\n%s" % (
                    mail_folder, str(e1), str(listOfFolders)))
            except Exception as e2:
                raise e1 # failed to get extra data - just rethrow the original error

    def read_emails(self, create_event):
        
        max_emails = abs(int(self.options["max_emails"]))
        mail_folder = str(self.options["mail_folder"])
        search_filter = str(self.options["search_filter"])

        IMAP_SERVER = self.secrets["IMAP_SERVER"]
        IMAP_PORT = self.secrets["IMAP_PORT"]
        IMAP_LOGIN = self.secrets["IMAP_LOGIN"]
        IMAP_USE_SSL = self.secrets["IMAP_USE_SSL"]
        IMAP_USERNAME = self.secrets["IMAP_USERNAME"]
        IMAP_PASSWORD = self.secrets["IMAP_PASSWORD"]
        
        
        if IMAP_USE_SSL:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        else:
            mail = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)

        if IMAP_LOGIN:
            mail.login(user=IMAP_USERNAME, password=IMAP_PASSWORD)

        self.selectFolder(mail, mail_folder)
        
        code, id_list = mail.search(None, search_filter)
        id_list = list(map(lambda i: i.decode("utf-8"), id_list[0].split()))

        if self.first_check:
            self.latest_email_id = id_list[-1]
            self.first_check = False
            return

        id_list = id_list[-max_emails:]

        new_list = []
        for i in reversed(id_list):
            if i != self.latest_email_id:
                new_list.append(i)
            else:
                self.latest_email_id = id_list[-1]
                break

        if not any(new_list):
            return
        
        for em in self.fetchEmail(mail, new_list):
            create_event(em)
        
    def fetchEmail(self, mail, id_list):
        typ, data = mail.fetch(','.join(id_list), '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode("utf-8"))

                payload = ""            
                for part in msg.walk():
                    pType = part.get_content_type()
                    if pType == 'text/plain':
                        payload = part.get_payload()
                        break

                yield {
                    'Subject': msg['Subject'],
                    'From': msg['From'],
                    'Date': msg['Date'],
                    'Text': payload,
                    'To': msg['To'],
                }