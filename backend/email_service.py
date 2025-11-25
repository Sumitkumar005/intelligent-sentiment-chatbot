import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
logger = logging.getLogger(__name__)
class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_pass = os.getenv('SMTP_PASS')
        self.email_sender = os.getenv('EMAIL_SENDER', self.smtp_user)
        self.is_development = os.getenv('FLASK_ENV') == 'development'
    def send_otp_email(self, to_email: str, otp: str, name: str = None) -> bool:
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Your Sentiment Chatbot Login Code'
            msg['From'] = self.email_sender
            msg['To'] = to_email
            text_body = self._create_text_body(otp, name)
            html_body = self._create_html_body(otp, name)
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            if self.smtp_user and self.smtp_pass:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_pass)
                    server.send_message(msg)
                logger.info(f"✅ OTP email sent successfully to {to_email}")
                return True
            else:
                logger.warning(f"⚠️ SMTP credentials not configured. Email not sent to {to_email}")
                if self.is_development:
                    logger.info("📧 Development mode: Skipping email send")
                    return True
                return False
        except Exception as e:
            logger.error(f"❌ Failed to send email to {to_email}: {e}")
            if self.is_development:
                logger.info("📧 Development mode: Returning success despite error")
                return True
            return False
    def _create_text_body(self, otp: str, name: str = None) -> str:
        greeting = f"Hello {name}!" if name else "Hello!"
        return f"""
{greeting}

Your login code for Sentiment Chatbot is:

{otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Sentiment Chatbot Team
"""
    
    def _create_html_body(self, otp: str, name: str = None) -> str:
        greeting = f"Hello {name}!" if name else "Hello!"
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .otp-box {{ background: white; border: 2px dashed #667eea; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; }}
        .otp-code {{ font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 5px; }}
        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Sentiment Chatbot</h1>
        </div>
        <div class="content">
            <p>{greeting}</p>
            <p>Your login code is:</p>
            <div class="otp-box">
                <div class="otp-code">{otp}</div>
            </div>
            <p>This code will expire in <strong>10 minutes</strong>.</p>
            <p>If you didn't request this code, please ignore this email.</p>
        </div>
        <div class="footer">
            <p>© 2025 Sentiment Chatbot. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""