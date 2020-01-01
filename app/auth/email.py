from flask import render_template, current_app
from app.email import send_mail

def send_password_reset_email(user):
    token = user.generate_password_reset_token(600)
    send_mail(
        subject='Password Reset',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/password_reset.txt', user=user, token=token),
        html_body=render_template('email/password_reset.html', user=user, token=token)
    )
