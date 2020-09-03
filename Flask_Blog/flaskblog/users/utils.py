import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail



def save_picture(form_picture):
    ''' we want random file name '''
    random_hex = secrets.token_hex(8)
    # random_hex = os.urandom(64).decode('latin1')
    f_name, f_ext = os.path.splitext(form_picture.filename)  # f_ext -> file extetion
    # del f_name  # for memmory saving
    picture_fn = random_hex + f_ext  # picture file name
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (200, 200)
    resized_img = Image.open(form_picture)
    resized_img.thumbnail(output_size)
    # resized_img.rotate(90)  # 90 degrees
    # resized_img.filter(ImageFilter.GaussianBlur(15))

    resized_img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request',
                    sender='noreply@demo.com',
                    recipients=[user.email])
    msg.body = f'''
To Reset your password, visit the fallowing link:
{url_for('users.reset_token', token=token, _external=True)}

if you did not request then simply ignore this email and no changes will be made.
    '''
    # `_external=True` means set full domain becaus it will be a foreign link
    mail.send(msg)
