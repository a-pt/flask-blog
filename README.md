# Flask Blog Application

A full-featured blog application built with Flask, following modern best practices including modular blueprints, custom error handling, and secure user authentication.

## 🚀 Features

### User Management
- **Secure Authentication**: User registration and login using hashed passwords (Bcrypt).
- **Session Management**: Persistent login sessions with Flask-Login.
- **Account Dashboard**: Users can update their username, email, and upload a profile picture.
- **Profile Customization**: Automatic image resizing for profile pictures (Pillow).
- **Password Reset**: Secure token-based password reset functionality via email.

### Blog Functionality
- **Full CRUD**: Create, Read, Update, and Delete blog posts.
- **Post Ownership**: Users can only edit or delete their own posts.
- **Pagination**: Browse posts efficiently with built-in pagination on home and user-specific post pages.
- **User Activity**: View all posts from a specific user.

### Technical Excellence
- **Blueprints**: Modular structure for Users, Posts, Main, and Error handling.
- **Custom Error Handling**: Professional error pages for 404 (Not Found), 403 (Forbidden), and 500 (Internal Server Error).
- **Configuration Management**: Environment variable based configuration using `python-dotenv`.
- **Database Architecture**: Managed via Flask-SQLAlchemy with relationships.

## 🛠️ Technology Stack

- **Framework**: Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Forms**: Flask-WTF / WTForms
- **Security**: Flask-Bcrypt, Itsdangerous
- **Mail**: Flask-Mail
- **Imaging**: Pillow
- **Environment**: python-dotenv

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask-blog
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory and add the following:
   ```env
   SECRET_KEY=your_secret_key_here
   SQLALCHEMY_DATABASE_URI=sqlite:///site.db
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   ```

5. **Initialize Database**
   ```bash
   python
   >>> from flask_blog import db, create_app
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

6. **Run the application**
   ```bash
   python run.py
   ```
   Open `http://localhost:5000` in your browser.

## 📂 Project Structure

```text
flask_blog/
├── errors/          # Custom error handlers and blueprints
├── main/            # Core routes (home, about)
├── posts/           # Blog post CRUD logic
├── static/          # CSS, JS, and profile pictures
├── templates/       # Jinja2 HTML templates
├── users/           # User authentication and profile logic
├── __init__.py      # App factory and extension initialization
├── config.py        # Configuration class
└── models.py        # Database models (User, Post)
run.py               # Application entry point
```

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
