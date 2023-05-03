import smtplib
import ssl


FROM = ""
TO = []

if __name__ == "__main__":
    context = ssl.create_default_context()
    subject = "Test Subject"
    text = "Test Text"
    message = f"""From: {FROM}\nTo: {", ".join(TO)}\nSubject: {subject}\n\n{text}"""

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(FROM, "")
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        server.sendmail(FROM, TO, message)
        server.quit()
