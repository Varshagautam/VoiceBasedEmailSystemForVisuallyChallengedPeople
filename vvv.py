from __future__ import print_function
import pyttsx3
import speech_recognition as sr
import smtplib
from email.message import EmailMessage
import ssl
import imaplib
import email

EMAIL_SENDER = 'himanshupippal24@gmail.com'
PASS = 'zqfoubiietfooqtd'
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
 
    engine.setProperty('rate', rate-20)
 
    engine.say(text)
    engine.runAndWait()

speak("Welcome to mail service")

def is_confirm():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        said = r.recognize_google(audio)
        return said
    except:
        speak("Didn't get that")
        speak("Speak again")
        is_confirm()
    return said.lower()

def main_process():
    print("Please choose the options ")
    speak("Please choose the options ")
    print("1. Wanted to send an email")
    speak("1. Wanted to send an email")
    print("2. Read your inbox")
    speak("2. Read your inbox")
    print("Select send email or read email")
    speak("Select send email or read email")
    intial_status = is_confirm()
    if intial_status.find("send email" or "send" or "sendemail") != -1:
        print("You have selected option one")
        speak("You have selected option one")
        print("Enter your name: ")
        speak("Enter your name: ")
        name =  is_confirm()
        print(name)            
        speak("Enter the receiver's email id: ")
        print("Enter the receiver's email id :")
        mail = is_confirm()
        rec_mail = ""
        for val in mail:
            if val == ' ':
                continue
            else:
                rec_mail+=val
        print(rec_mail)
        print("Enter the data for your mail: ")
        speak("Enter data for your email")
        data = is_confirm()
        print(data)
        subject = f'This is test from {name}'
        body = f"""
        {data}
        """
        speak(f"The data you wanted to send is {data}")
        speak("Are you sure to send mail")
        print("Say yes or no ")
        valid = is_confirm()
        print(valid)
        if valid.find("yes" or "yas" or "yess") != -1:
            if rec_mail != '':
                em = EmailMessage()
                em['From'] = EMAIL_SENDER
                em['To'] = rec_mail
                em['Subject'] = subject
                em.set_content(body)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
                    smtp.login(EMAIL_SENDER, PASS)
                    smtp.sendmail(EMAIL_SENDER,rec_mail,em.as_string())
                speak("Email send successfully!!")
                print("Email send successfully!!")
            else:
                data = is_confirm()
        elif valid=="no" or valid.find('no')==-1 : 
            speak("You have cancelled the sending procedure")
            print("You have cancelled the sending procedure")
        else:
            speak("You said neither yes nor no")
            print("You said neithe yes nor no")
            speak("Process Ended!!")
            print("Process Ended!!")
    elif intial_status.find("read email" or "reademail" or "read") != -1 :
        speak("You have selected option 2")
        print("You have selected option 2")
        imap_server = "imap.gmail.com"
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(EMAIL_SENDER,PASS)
        imap.select("Inbox")
        _, msgnums = imap.search(None, "ALL")
        status = False
        for msgnum in msgnums[0].split():
            _, data = imap.fetch(msgnum, "(RFC822)")
            message = email.message_from_bytes(data[0][1])
            speak(f"Message Number: {msgnum}")
            print(f"Message Number: {msgnum}")
            print(f"From: {message.get('From')}")
            speak(f"From: {message.get('From')}")
            print(f"To: {message.get('To')}")
            speak(f"To: {message.get('To')}")
            print(f"BCC: {message.get('BCC')}")
            speak(f"BCC: {message.get('BCC')}")
            print(f"Date: {message.get('Date')}")
            print(f"Subject: {message.get('Subject')}")
            speak(f"Subject: {message.get('Subject')}")
            print("Content:")
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    print(part.as_string())
            break
            imap.close()
        else:
            speak("Process Terminated")
            print("Process Terminated!!")
    else:
        speak("You haven't choosen any of them, Try Again")
        print("You haven't choosen any of them, Try Again")
        main_process()

main_process()
speak("Thank you using our services")
print("Thank you using our services")