import smtplib
from email.message import EmailMessage

def setupConnection():
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login('webbform@outlook.com', '1111111111')
    return server

def createMessage(formData , timeStamp):
    dateTime = str(timeStamp.strftime('%d')) + '-' + str(timeStamp.strftime('%b')) + '-' + str(timeStamp.year) +  ' ' + str(timeStamp.strftime('%I')) + ':' + str(timeStamp.strftime('%M')) +' ' + str(timeStamp.strftime('%p')) +' IST(Asia/Kolkata)'
    message='<div style="padding: 20px; margin: 0; background-color: #000;">' + f'<h3 style="color:#b0b0b0">{dateTime}</h3>'
    for key,values in formData.items():
        valueSet = ' '.join([value for value in values])
        message+=f"""\
    <div style="padding: 6px; border-radius: 5px; box-shadow: 0 0 5px 0 #d6d6d6; margin: 15px 0; background-color: #fff;">
        <span style="font-weight: 600; font-family: Baskerville, 'Baskerville Old Face';">{key}:</span> <span style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;">{valueSet}</span>
    </div>
"""
    message+="</div>"
    return message

def sendConfirmation(formName, to ,formData , timeStamp):
    message = EmailMessage()
    message['Subject'] = f"New entry in {formName} : Webb Forms"
    message['From'] = 'Webb Forms:webbform@outlook.com'
    message['to'] = to
    message.add_alternative(createMessage(formData, timeStamp), subtype = 'html')
    server = setupConnection()
    try:
        server.send_message(message)
    except Exception as E:
        print(E)