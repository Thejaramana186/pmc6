from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.notification import Notification
from sqlalchemy import text

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Project': Project, 
        'Task': Task, 
        'Meeting': Meeting,
        'Notification': Notification
    }

if __name__ == '__main__':
    with app.app_context():
        # Check if title column exists, if not add it
        try:
            # Try to query the title column
            db.session.execute(text("SELECT title FROM user LIMIT 1"))
        except Exception:
            # Column doesn't exist, add it
            print("Adding title column to user table...")
            db.session.execute(text("ALTER TABLE user ADD COLUMN title VARCHAR(10) DEFAULT 'Mr'"))
            db.session.commit()
            print("Title column added successfully!")
        
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)