import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()
    
class EmailSender:
    def __init__(self):
        self.email = os.getenv("email")
        self.apppassword = os.getenv("apppassword")
        self.receipt_email = os.getenv("receipt_email")
        pass
    
    def message_prep(self, subject:str, email: str, body:str):
        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.email
        msg['To'] = email
        
        return msg
        pass
    
    def _send_email(self, msg:MIMEText, recipient:str):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(self.email, self.apppassword)
            smtp_server.sendmail(self.email, recipient, msg.as_string())
        pass
    
    def send_email(self, reason:str, email:str, body:str):
        
        if reason == "Job Opportunity":
            subject = "Your time has comeee !!!! get up  !!!!"
        elif reason == "Collaboration":
            subject = "Time to build somthing !! getup !"
        elif reason == "General":
            subject = "Someone is saying hii !!"
        else:
            subject = "hmmm !! what could it be :)"
        # send email to self 
        reciept_email = self.message_prep(subject=subject, email=self.receipt_email, body=body + f"\n \n {email} has contacted you ")
        
        self._send_email(msg=reciept_email, recipient=self.receipt_email)
        # send email to the contact person
        
        contact_person_email = self.message_prep(subject=os.getenv("contact_subject"), email=email, body=os.getenv("contact_body"))
        self._send_email(msg=contact_person_email, recipient=email)
        
        
        pass