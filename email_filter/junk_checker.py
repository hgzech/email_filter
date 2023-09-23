# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_junk_checker.ipynb.

# %% auto 0
__all__ = ['USERNAME', 'PASSWORD', 'email_client', 'since_date', 'emails', 'good_emails', 'extract_domain', 'get_domain_age',
           'check_domain_age', 'likely_spam', 'EmailObject', 'EmailClient']

# %% ../nbs/01_junk_checker.ipynb 4
import whois
from datetime import datetime
import tldextract

# %% ../nbs/01_junk_checker.ipynb 5
def extract_domain(email):
    domain = email.split('@')[1]
    # Extract main domain from subdomain
    main_domain = tldextract.extract(domain)
    return f"{main_domain.domain}.{main_domain.suffix}"

# %% ../nbs/01_junk_checker.ipynb 6
# This function gets the domain age. It's less useful than expected as not all domains reveal their age on whois. Nevertheless, it could be used to remove emails whose creation date is very young
def get_domain_age(email):
    domain = extract_domain(email)
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        #if creation_date == None:
        #    creation_date = w.updated_date[0] if isinstance(w.updated_date, list) else w.updated_date
        if creation_date:
            domain_age = (datetime.now() - creation_date).days
            return domain_age/365
        else:
            return None
    except Exception as e:
        return str(e)

# %% ../nbs/01_junk_checker.ipynb 8
def check_domain_age(email):
    domain = extract_domain(email)
    age_in_years = get_domain_age(domain)
    return age_in_years

# %% ../nbs/01_junk_checker.ipynb 14
def likely_spam(email):
    return check_domain_age(email)<3
likely_spam("jack_nathan@cognition-behaviour.com")

# %% ../nbs/01_junk_checker.ipynb 17
import imaplib
import email
from email.header import decode_header
from datetime import datetime
import os

# %% ../nbs/01_junk_checker.ipynb 18
class EmailObject:
    def __init__(self, sender, subject, email_id):
        self.sender = sender
        self.subject = subject
        self.email_id = email_id

class EmailClient:
    def __init__(self, server, port, username, password):
        self.mail = imaplib.IMAP4_SSL(server, port)
        self.mail.login(username, password)

    def get_emails(self, since_date=None):
        self.mail.select('"Sent Items"')
        
        if since_date:
            since_date_str = since_date.strftime('%d-%b-%Y')
            status, messages = self.mail.search(None, f'SINCE {since_date_str}')
        else:
            status, messages = self.mail.search(None, "ALL")
            
        email_ids = messages[0].split()
        email_objects = []
        
        for e_id in email_ids:
            status, msg_data = self.mail.fetch(e_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            # Extract sender
            sender = msg["To"]
            
            # Create email object and add to list
            email_objects.append(EmailObject(sender, subject, e_id))
        
        return email_objects


    def logout(self):
        self.mail.logout()

# %% ../nbs/01_junk_checker.ipynb 29
class EmailObject:
    def __init__(self, sender, subject, email_id):
        self.sender = sender
        self.subject = subject
        self.email_id = email_id

class EmailClient:
    def __init__(self, server, port, username, password):
        self.mail = imaplib.IMAP4_SSL(server, port)
        self.mail.login(username, password)

    def get_emails(self, since_date=None):
        self.mail.select('"Sent Items"')
        
        if since_date:
            since_date_str = since_date.strftime('%d-%b-%Y')
            status, messages = self.mail.search(None, f'SINCE {since_date_str}')
        else:
            status, messages = self.mail.search(None, "ALL")
            
        email_ids = messages[0].split()
        email_objects = []
        
        for e_id in email_ids:
            status, msg_data = self.mail.fetch(e_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            # Extract sender
            sender = msg["To"]
            
            # Create email object and add to list
            email_objects.append(EmailObject(sender, subject, e_id))
        
        return email_objects


    def logout(self):
        self.mail.logout()



USERNAME = os.environ.get("EXCHANGE_USER")
PASSWORD = os.environ.get("EXCHANGE_PASSWORD")

# Usage example
email_client = EmailClient("msx.tu-dresden.de", 993, USERNAME, PASSWORD)

# Fetch emails since a specific date
since_date = datetime(2022, 8, 22)  # Replace with actual date
emails = email_client.get_emails(since_date=since_date)

good_emails = []
# Print and move emails
for e in emails:
    good_emails.append(parseaddr(e.sender)[1])

# Logout to close the connection
email_client.logout()

good_emails = list(set(good_emails))
print(good_emails)
