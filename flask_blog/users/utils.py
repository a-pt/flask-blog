import secrets
import os
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail
from supabase import create_client, Client
from io import BytesIO

def _get_supabase_client() -> Client | None:
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
        bucket_name = os.getenv('SUPABASE_BUCKET')
        try:
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format=image.format or 'PNG')
            img_byte_arr = img_byte_arr.getvalue()

            supabase.storage.from_(bucket_name).upload(
                path=f'profile_pics/{picture_fn}',
                file=img_byte_arr,
                content_type=f'image/{image.format or "PNG"}'
            )

            # Get the public URL
            public_url = supabase.storage.from_(bucket_name).get_public_url(f'profile_pics/{picture_fn}')
            return public_url
        except Exception as e:
            current_app.logger.error(f"Error uploading profile picture to Supabase: {e}")
            # Fallback to local storage if Supabase upload fails
            pass

    # Fallback to local storage if Supabase is not configured or upload fails
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