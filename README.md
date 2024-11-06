**1. Python Home Security System**
A security monitoring system that uses your computer's camera for motion detection, video recording, and email notifications.
Description
The system uses computer vision technologies to detect faces and human figures in the camera's field of view. When motion is detected:

Plays an alert sound
Starts video recording
Sends the video via email

Technical Features

Uses OpenCV for face and body detection
Video recording in MP4 format
Email sending via SMTP with video attachment
Uses Haar Cascades for detection

**Prerequisites**

Python 3.6+
Webcam
Gmail account
Google App Password

**2. Install required libraries:**
pip install -r requirements.txt

Setting up Gmail for sending emails

Enable 2-Factor Authentication on your Gmail account:

Go to Google Account settings
Select "Security"
Enable "2-Step Verification"


**3 Create an App Password:**

Go to Google Account Security
Select "App Passwords"
Choose "Other (Custom name)"
Give it a name (e.g., "Python Security System")
Copy the 16-digit code that will be generated

**4. Configuration**
In the Motion_Detection_Security_Camera.py file, modify the following lines with your details:
sender_email = 'YOUR EMAIL'  # Your email
sender_password = 'YOUR GMAIL SENDER PASSWORD FOR APPLICATION'  # Your 16-digit app password
recipient_email = 'YOUR EMAIL'  # Email that will receive notifications

**Notes**

Make sure to place an alert_sound.mp3 file in the same folder as the script
The system records for 7 seconds after the last motion detection
Use in a well-lit area for better detection
Ensure stable internet connection for email notifications

**5. Security Consideration**

Store your email credentials securely
Use App Passwords instead of your main Gmail password
Consider running the system on a dedicated device
Regularly check the system's functionality

**Troubleshooting**

If the camera doesn't open, check if it's being used by another application
If emails aren't sending, verify your Gmail App Password
For video recording issues, ensure sufficient disk space
Check internet connection if notifications aren't received
