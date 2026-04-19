import secrets
import os
from typing import Optional
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail
from supabase import create_client, Client
from io import BytesIO

def _get_supabase_client() -> Optional[Client]:
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    if url and key:
        return create_client(url, key)
    return None

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)

    supabase = _get_supabase_client()
    
    if supabase:
        buf = BytesIO()
        image.save(buf, format=image.format or 'PNG')
        buf.seek(0)
        bucket = os.getenv('SUPABASE_BUCKET')
        storage_path = f'profile_pics/{picture_fn}'
        res = supabase.storage.from_(bucket).upload(storage_path, buf.read(), {
            "content-type": f'image/{f_ext.lstrip(".").lower()}',
            "upsert": True,
        })
        if res.get('error'):
            current_app.logger.error(f"Supabase upload failed: {res['error']}")
        else:
            public_url = supabase.storage.from_(bucket).get_public_url(storage_path)
            return public_url.get('publicURL')
    
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    image.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''
    To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request, ignore this email.
    '''
    mail.send(msg)