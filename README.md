# Flask Todo Task Master

A modern, responsive task management application built with Flask, SQLAlchemy, and vanilla JavaScript. Organize your tasks with categories, priorities, and due dates in a clean, intuitive interface.

## ✨ Features

- ✅ Create, read, update, and delete tasks
- 🎯 Set task priorities (High, Medium, Low)
- 📂 Categorize tasks for better organization
- 📅 Add due dates to tasks
- ✅ Toggle task completion status
- 🔍 Filter tasks by category and priority
- 🔒 CSRF protection for secure form submissions
- 📱 Responsive design that works on all devices
- ✨ Modern UI with smooth animations

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flask-todo-app.git
   cd flask-todo-app
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following content:
   ```
   SECRET_KEY=your-secret-key-here
   WTF_CSRF_SECRET_KEY=your-csrf-secret-key-here
   DATABASE_URI=sqlite:///test.db
   ```

5. **Initialize the database**
   ```bash
   python
   >>> from app import db, create_app
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Visit `http://localhost:5000` to see the application in action.

## 🛠 Project Structure

```
flask-todo-app/
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── main.js
├── templates/
│   ├── base.html
│   ├── index.html
│   └── update.html
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

## 🌐 Deployment

### Deploying to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set the following environment variables in the Render dashboard:
   - `SECRET_KEY`: Your secret key
   - `WTF_CSRF_SECRET_KEY`: Your CSRF secret key
   - `DATABASE_URI`: Your production database URI
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `gunicorn app:app`
6. Deploy!

### Using a Production Database

For production, it's recommended to use PostgreSQL:

1. Create a PostgreSQL database on Render or another provider
2. Update the `DATABASE_URI` to use your PostgreSQL connection string:
   ```
   DATABASE_URI=postgresql://user:password@host:port/dbname
   ```

## 🛡 Security

- CSRF protection is enabled by default
- Secret keys are stored in environment variables
- Database queries use parameterized statements to prevent SQL injection

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Font Awesome](https://fontawesome.com/)
- [Google Fonts](https://fonts.google.com/)

---

<div align="center">
  Made with ❤️ by Your Name | [Buy Me a Coffee](https://www.buymeacoffee.com/yourusername)
</div>
