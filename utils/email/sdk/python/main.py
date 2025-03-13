# Importing basic Libraries
import datetime
import inspect
import os

# Importing packes for e-mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tabulate import tabulate
import smtplib
from email.mime.base import MIMEBase
from email import encoders



def Email_Error(TO_email_list, message):
    DT = str(datetime.datetime.now())
    DT = DT[:-7]
    # Getting the filepath of the file that called the function
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = str(module.__file__)

    # Trimming the filepath to only include the filename
    position = []
    for i, c in enumerate(filename):
        if c == "/":
            position.append(i)
    position = position[-1] + 1
    filename = filename[position:]       
    
    # Creating and sending message
    msg = MIMEMultipart()
    
    recipients = TO_email_list
    msg["To"] = ", ".join(TO_email_list)
    msg["From"] = "do-not-reply@org.com"
    msg["Subject"] = ("Error: " + filename + " " + DT)
    bodymsg = ("Hello,\n\nThe " + filename + " script has encountered the following error:\n\n" + message + "\n" + DT + "\n\nPlease resolve at your earliest convenience.\n\nPython")
    body_for_email = MIMEText(bodymsg, 'plain')
    msg.attach(body_for_email)

    smtp = smtplib.SMTP()
    smtp.connect("smtp.org.com")
    smtp.sendmail("do-not-reply@org.com", recipients, msg.as_string())
    smtp.quit()


def Email_Table(TO_emails, CC_emails, subject, message, df):
    msg = MIMEMultipart()
    
    text = """Hello,
    
    This is an automated e-mail.
    
    """ + message + """
    
    {table}
    
    Regards,
    
    Python
    """
    html = """
    <html>
    <head>
    <style> 
     table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
      th, td {{ padding: 5px; }}
    </style>
    </head>
    <body><p>Hello,</p>
    <p>This is an automated e-mail.</p>
    <p>""" + message + """</p>
    {table}
    <p>Regards,</p>
    <p>Python</p>
    </body></html>
    """
    col_list = list(df.columns.values)
    data = df
    
    # above line took every col inside csv as list
    text = text.format(table=tabulate(data, headers=col_list, tablefmt="grid"))
    html = html.format(table=tabulate(data, headers=col_list, tablefmt="html"))
    
    msg = MIMEMultipart(
        "alternative", None, [MIMEText(text), MIMEText(html,'html')])
    
    msg["To"] = ", ".join(TO_emails)
    msg["CC"] = ", ".join(CC_emails)
    msg["From"] = "do-not-reply@org.com"
    msg["Subject"] = subject
    
    recipients = TO_emails + CC_emails
    smtp = smtplib.SMTP()
    smtp.connect("smtp.org.com")
    smtp.sendmail("do-not-reply@org.com", recipients, msg.as_string())
    smtp.quit()

def send_email(recipient=[], CC=[], BCC=[], subject="", message="", file_list=[]):
    msg = MIMEMultipart()
##    recipients = recipient
    attachment_path_list = file_list
    msg["To"] = ", ".join(recipient)
    msg["CC"] = ", ".join(CC)
    msg["BCC"] = ", ".join(BCC)
    msg["From"] = "do-not-reply@org.com"
    msg["Subject"] = subject
    bodymsg = message
    body_for_email = MIMEText(bodymsg, 'plain')
    msg.attach(body_for_email)
    flag = 0
    
    if attachment_path_list is not None:
        for each_file_path in attachment_path_list:
            try:
                file_name=each_file_path.split("\\")[-1]
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(each_file_path, "rb").read())

                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment' ,filename=file_name)
                msg.attach(part)
            except:
                print("could not attach file")
                flag = 1
        
    if flag == 0:
        recipient = recipient + CC + BCC
        smtp = smtplib.SMTP()
        smtp.connect('smtp.org.com')
        smtp.sendmail('do-not-reply@org.com', recipient, msg.as_string())
        smtp.quit() 

#file_path = r"\\pat\to\\"
#folder_path = os.path.dirname(file_path)

"""
Test functions
"""

## Testing Email_Error
#Email_Error("joedoe@org.com", "Test body text")

## Testing send_email
#file1 = (r"\\path\to\Book1.xlsx")
#send_email(recipient=["joedoe@org.com"], 
#           CC=["joedoe@org.com"], 
#           BCC=["joedoe@org.com"], 
#           subject="test1", 
#           message="message", 
#           file_list=[file1])
#
#send_email(recipient=["joedoe@org.com"], 
#           CC=["joedoe@org.com"], 
#           BCC=["joedoe@org.com"], 
#           subject="test2", 
#           message="message")
#
#send_email(recipient=["joedoe@org.com"], 
#           subject="test3", 
#           message="message", 
#           file_list=[file1])
#
#long_message = """Hello,
#
#This is a VERY VERY LOOOOOOOOOOOOOONNNNNNNNNNNNNGGGGGGGGG message.
#
#This has many sentences.
#
#It has many paragraphs.
#
#Even a lot of new lines.
#
#All e-mails have to come to an end though.
#
#Adios Amigo!
#
#Python
#"""
#
#send_email(recipient=["joedoe@org.com"], 
#           subject="test4", 
#           message=long_message)