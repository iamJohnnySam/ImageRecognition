import imaplib
import email
import os
import time
import numpy as np

download_folder = "/home/pi/CCTV/Images"
output = 0.000001
foldersize = 0

em = 'server@outlook.com'
pw = 'password'

from pushbullet import Pushbullet
pb = Pushbullet('o.pushbulletAPIkey')

import tensorflow as tf
model = tf.lite.Interpreter(model_path="/home/pi/CCTV/model.tflite")
model.allocate_tensors()
input_details = model.get_input_details()
output_details = model.get_output_details()

from PIL import Image, ImageOps

for f in os.listdir(download_folder):
    foldersize = foldersize + os.path.getsize(os.path.join(download_folder, f))
print("Current Folder size -", "{:,}".format(foldersize))

while True:
    pbStatus = True
    
    outlook = imaplib.IMAP4_SSL('outlook.office365.com', 993)
    outlook.login(em, pw)
    outlook.select(mailbox = 'CCTV', readonly=False)

    (result, messages) = outlook.search(None, 'UnSeen')
    if result == "OK":
        for message in messages[0].split():
            try: 
                ret, data = outlook.fetch(message,'(RFC822)')
            except:
                print("No new emails to read.")
                outlook.connection.close()
                exit()

            msg = email.message_from_bytes(data[0][1])
            Date = msg['Date']
            Date = Date.replace(" +0530", "")
            
            att_path = "No attachment found."
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                saveas = Date+" "+filename
                att_path = os.path.join(download_folder, saveas)
                
                image = part.get_payload(decode=True)
                fp = open(att_path, 'wb')
                fp.write(image)
                fp.close()
                
                # IMAGE
                img = Image.open(att_path)
                img = ImageOps.grayscale(img)
                img = np.asarray(img,dtype="float32")/255
                img = np.expand_dims(img, axis=0)
                
                Sus = False
    
                model.set_tensor(input_details[0]['index'], img)
                model.invoke()
                output_data = model.get_tensor(output_details[0]['index'])
                output = output_data[0][0]
                if (output > 0.85):
                    Sus = True
                
                if not Sus:
                    os.remove(att_path)
                    
                else:
                    if pbStatus:
                        with open(att_path, "rb") as pic:
                            file_data = pb.upload_file(pic,"Sus lvl " + str(output))
                        try:
                            push = pb.push_file(**file_data)
                            os.remove(att_path)
                            print(filename, output)
                        except:
                            print("PB failed")
                            pbStatus = False
                            
                if Sus and not pbStatus:
                    foldersize = foldersize + os.path.getsize(att_path)
                    print(filename, output, "{:,}".format(foldersize))

            response, data = outlook.store(message, '+FLAGS','\\Deleted')
    
    outlook.close()
    
    if foldersize > 0:
        print("Preparing to send email")
        import smtplib, ssl
        from os.path import basename
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        from email.utils import COMMASPACE, formatdate
        
        send_to = ['mail1@mail.com', 'mail2@mail.com']
        body = """\
            <html>
                <body>
                    <p>Hi,<br>
                       We detected some activity on the CCTV in the last 5 minutes<br>
                    </p>
                </body>
            </html>
        """
        
        msg = MIMEMultipart()
        msg['From'] = em
        msg['To'] = ", ".join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Suspicious Activity"
        
        msg.attach(MIMEText(body, "html"))
        
        for f in os.listdir(download_folder):
            with open(os.path.join(download_folder, f), "rb") as fil:
                part = MIMEApplication(fil.read(),Name=basename(f))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls(context=context)
        server.login(em, pw)
        server.sendmail(em, send_to, msg.as_string())
        server.close()
            
        for f in os.listdir(download_folder):
            os.remove(os.path.join(download_folder, f))
        foldersize = 0
        
    print("Done")
    time.sleep(60*5)