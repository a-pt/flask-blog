# Flask Blog

A full-featured blogging application built with Flask, following modern best
practices including modular blueprints, custom error handling, and secure user
authentication.

## 🚀 Features

### User Management

- **Secure Authentication**: User registration and login using hashed passwords
  (Bcrypt).
- **Session Management**: Persistent login sessions with Flask-Login.
- **Account Dashboard**: Users can update their username, email, and upload a
  profile picture.
- **Profile Customization**: Automatic image resizing for profile pictures
  (Pillow).
- **Password Reset**: Secure token-based password reset functionality via email.

### Blog Functionality

- **Full CRUD**: Create, Read, Update, and Delete blog posts.
- **Post Ownership**: Users can only edit or delete their own posts.
- **Pagination**: Browse posts efficiently with built-in pagination on home and
  user-specific post pages.
- **User Activity**: View all posts from a specific user.

### Technical Excellence

- **Blueprints**: Modular structure for Users, Posts, Main, and Error handling.
- **Custom Error Handling**: Professional error pages for 404 (Not Found), 403
  (Forbidden), and 500 (Internal Server Error).
- **Configuration Management**: Environment variable based configuration using
  `python-dotenv`.
- **Database Architecture**: Managed via Flask-SQLAlchemy with relationships.

- **Neon PostgreSQL** as the production database (configured via
  `DATABASE_URL`).
- **Flask‑Migrate** for database schema migrations.
- **Supabase Storage** for user profile pictures:
  - Images are resized to 125×125px.
  - Uploaded directly to a Supabase bucket (`profile_pics`).
  - The public URL is stored in `User.image_url` and used throughout the UI.
  - A default avatar is served from Supabase when a user has no custom picture.
- **Removed local filesystem storage** for profile pictures – all images are now
  hosted on Supabase, eliminating Vercel read‑only filesystem issues.
- **Responsive UI** that displays avatars on:
  - Account page (`/account`).
  - Home feed (`/home`).
  - Individual post view.
  - User posts page.
- **Environment configuration** via `.env` (or Vercel dashboard) for:
  - `SUPABASE_URL`
  - `SUPABASE_BUCKET`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `DATABASE_URL`
  - `SECRET_KEY`
- **Error handling** for image upload failures with graceful fallback.

## Setup (local development)

```bash
# Clone the repo
git clone https://github.com/a-pt/flask-blog.git
cd flask-blog

# Create a virtual environment
python -m venv venv
venv\Scripts\activate   # on Windows

# Install dependencies
pip install -r requirements.txt

# Create a .env file (copy from .env.example) and fill in your credentials
cp .env.example .env

# Initialise the database (Neon or local PostgreSQL)
flask db upgrade

# Run the development server
python run.py
```

## Deployment (Vercel)

1. Connect the repository to Vercel.
2. Add the same environment variables (`DATABASE_URL`, `SUPABASE_URL`,
   `SUPABASE_BUCKET`, `SUPABASE_SERVICE_ROLE_KEY`, `SECRET_KEY`).
3. Vercel will automatically run `python run.py` (or you can configure a custom
   start script).
4. All profile pictures are stored in Supabase, so the read‑only filesystem on
   Vercel is no longer a limitation.

## License

MIT License – see `LICENSE` for details.
