import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from io import StringIO
from datetime import datetime
from celery_config import celery
from app import app
from model import db, User, Category
import csv


@celery.task
def generate_monthly_report():
    with app.app_context():
        current_month = datetime.now().strftime('%Y-%m')
        current_year = datetime.now().year
        users = User.query.all()

        for user in users:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Monthly Report</title>
            </head>
            <body>
                <h1>Monthly Report for {user.username}</h1>
                <p>Here is your report for the month of {current_month}.</p>
                <p>Total users registered: {len(users)}</p>
                <p>Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </body>
            </html>"""

            send_email(user.email,html_content)

def send_email(to_email, html_content):
    from_email = 'grocery@gmail.com'
    subject = 'Monthly Report'
    msg = MIMEMultipart(
        'alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject    

    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)
    
    smtp_server = 'localhost'
    smpt_port = 1025

    with smtplib.SMTP(smtp_server, smpt_port) as server:
        server.sendmail(from_email,to_email, msg.as_string())

@celery.task
def export_categories_details_as_csv():
    with app.app_context():
        categories = Category.query.all()
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(['ID', 'Name'])
        for category in categories:
            csv_writer.writerow([category.id, category.name])

        base_dir = os.path.abspath(os.path.dirname(__name__))
        csv_file_path = os.path.join(base_dir,'csv/category_report.csv')
        with open(csv_file_path, 'w') as csv_file:
            csv_file.write(csv_buffer.getvalue())
        return csv_buffer.getvalue()