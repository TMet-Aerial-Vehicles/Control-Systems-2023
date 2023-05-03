import smtplib
import ssl


class EmailHandler:

    def __init__(self):
        self.from_email = ""
        self.to_emails = []
        self.context = ssl.create_default_context()

    def send_email(self, subject, text):
        message = f"From: {self.from_email}\n" + \
            f"To: {', '.join(self.to_emails)}\nSubject: {subject}\n\n{text}"
        with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                              context=self.context) as server:
            print("SMTP Connection Created")
            server.login(self.from_email, "")
            server.sendmail(self.from_email, self.to_emails, message)
            server.quit()
            print("Email Sent")
        print("Unable to create connection with SMTP server")
