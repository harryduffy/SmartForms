from email.message import EmailMessage
import smtplib, os
from dotenv import load_dotenv

load_dotenv()

class Email:

    def __init__(self, name, phone_number, role):
        self.name = name
        self.phone_number = phone_number
        self.role = role
        self.email_address = "harry.duffy@integralprivatewealth.com.au"

        smtp_obj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(self.email_address, "1nt3gr@L")

        self.smtp_obj = smtp_obj

    def create_signature(self):
        """Creates the email signature for the email to be sent and returns this signature in HTML format.
        
        :return: An HTML string representing the signature of the sender.
        :rtype: str
        """
        
        self.signature = f'''
        
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><strong><span style='font-family:"Georgia",serif;color:#004169;'>{self.name}</span></strong><span style='font-family:"Georgia",serif;color:#004169;'>&nbsp;| {self.role} | Integral Private Wealth</span></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-family:"Georgia",serif;color:#004169;'>&nbsp;</span></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-family:"Georgia",serif;color:#004169;'>Level 10, 83 Clarence Street Sydney NSW 2000 | <strong>M&nbsp;</strong>{self.phone_number} <strong>| E <a href="mailto:{self.email_address}" title="mailto:{self.email_address}"><span style="color:#004169;font-weight:normal;">{self.email_address}</span></a></strong> | <strong>W <a href="http://www.integralprivatewealth.com.au/" title="http://www.integralprivatewealth.com.au/"><span style="color:#004169;font-weight:normal;">www.integralprivatewealth.com.au</span></a></strong></span></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-family:"Georgia",serif;color:#004169;'>&nbsp;</span></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><strong><span style='font-size:12px;font-family:"Georgia",serif;color:#004169;'><img width="305" src="data:image/png;base64,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" alt="signature_491294588"></span></strong></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><strong><span style='font-size:12px;font-family:"Georgia",serif;color:#004169;'>&nbsp;</span></strong></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><strong><span style='font-size:12px;font-family:"Georgia",serif;color:#004169;'>Disclaimer</span></strong></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:11px;font-family:"Georgia",serif;color:#004169;'>&nbsp;</span></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:11px;font-family:"Georgia",serif;color:#004169;'>This message and any attachment is confidential and may be privileged or otherwise protected from disclosure. You should immediately delete the message if you are not the intended recipient. If you have received this email by mistake please delete it from your system; you should not copy the message or disclose its content to anyone. &nbsp;This electronic communication may contain general financial product advice but should not be relied upon or construed as a recommendation of any financial product. The information has been prepared without taking into account your objectives, financial situation or needs. &nbsp;Past performance is not a reliable indicator of future performance. &nbsp;Integral Private Wealth Group Pty Ltd is a corporate authorised representative of SIRA Group Pty Ltd ABN 15 106 922 641 AFSL 278423. &nbsp;The information in this email is current as at the date this email is sent.</span></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-family:"Times New Roman",serif;color:#283140;'>&nbsp;</span></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><strong><span style='font-size:12px;font-family:"Georgia",serif;color:#004169;'>Confidential communication</span></strong></p>
        <p style='margin:0cm;font-size:15px;font-family:"Calibri",sans-serif;'><strong><span style='font-size:12px;font-family:"Georgia",serif;color:#004169;'>Integral Private Wealth Group Pty Ltd (ABN 24 634 124 520)</span></strong></p>

        '''

        return self.signature

    def send_email(self, subject, body, receiver):

        self.create_signature()
        
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email_address
        msg["To"] = receiver
        msg.set_content(f'''
        <!DOCTYPE html>
        <html>
            <body style="font-family: Calibri, , sans-serif;
                        font-size: 15px">{body}<body>
                <footer style="text-align: left">
                    {self.signature}
                </footer>
        <html>
        ''', subtype="html")
        
        self.smtp_obj.send_message( msg, from_addr=self.email_address, to_addrs=receiver)   