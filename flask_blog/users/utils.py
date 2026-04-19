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

    try:
        form_picture.stream.seek(0)
    except Exception:
        pass

    try:
        image = Image.open(form_picture)
        image.verify()          # checks the header only
        # Re‑open after verify because verify() may close the file
        form_picture.stream.seek(0)
        image = Image.open(form_picture)
    except Exception as e:
        raise ValueError("Uploaded file is not a valid image.") from e


    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)

    supabase = _get_supabase_client()
    
    if supabase:
        buf = BytesIO()
        image.save(buf, format=image.format or 'PNG')
        buf.seek(0)
        bucket = os.getenv('SUPABASE_BUCKET')
        supabase_url = os.getenv('SUPABASE_URL')
        storage_path = f'profile_pics/{picture_fn}'
        res = supabase.storage.from_(bucket).upload(storage_path, buf.read(), {
            "content-type": f'image/{f_ext.lstrip(".").lower()}',
            "upsert": "true",
        })
        
        # Parse the response
        result = res.json()
        if result.get('error'):
            # Log the error and fall back to local storage
            current_app.logger.error(f"Supabase upload failed: {result['error']}")
        
        # Build the public URL for the uploaded file
        public_url = f"{supabase_url}/storage/v1/object/public/{bucket}/{storage_path}"
        return public_url

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''
    To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request, ignore this email.
    '''
    mail.send(msg)