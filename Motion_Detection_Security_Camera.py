from playsound import playsound
import cv2
import time
import datetime
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
import os

cap = cv2.VideoCapture(0)
detection = False
detection_stopped_time = None
timer_starter = False
SECONDS_TO_RECORD_AFTER_DETECTION = 7

sender_email = 'YOUR EMAIL'
sender_password = 'YOUR GMAIL SENDER PASSWORD FOR APLICATION'
recipient_email = 'YOUR EMAIL'
subject = '##### ALARM HOUSE NOW #######'
message = 'This email contains an attachment.'

def send_email(sender_email, sender_password, recipient_email, subject, message, video_data):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message
    msg.attach(MIMEText(message, 'plain'))

    # Attach the video file
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(video_data.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="video.mp4"')
    msg.attach(part)
    # Convert message to string
    text = msg.as_string()
    # Connect to the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Login to the email account
    server.login(sender_email, sender_password)
    # Send email
    server.sendmail(sender_email, recipient_email, text)
    # Quit SMTP server
    server.quit()

# Record a video
frame_size = int(cap.get(3)), int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

video_frames = []  # List to store video frames

while True:
    _, frame = cap.read()
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayscale, 1.3, 5)
    bodies = body_cascade.detectMultiScale(grayscale, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if not detection:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            print("Start Recording...")
            playsound('./alert_sound.mp3')

    elif detection:
        if timer_starter:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_starter = False
                video_buffer = BytesIO()
                out = cv2.VideoWriter('temp_video.mp4', fourcc, 20.0, frame_size)
                for frame in video_frames:
                    out.write(frame)
                out.release()
                video_buffer.write(open('temp_video.mp4', 'rb').read())  # Write file contents to BytesIO
                os.remove('temp_video.mp4')  # Remove temporary file
                video_buffer.seek(0)  # Rewind the BytesIO object to the beginning
                send_email(sender_email, sender_password, recipient_email, subject, message, video_buffer)  # Send email with video attachment
                print("Stop Recording and sending email")
                video_frames = []  # Clear the list of video frames
        else:
            timer_starter = True
            detection_stopped_time = time.time()

    if detection:
        video_frames.append(frame)

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

