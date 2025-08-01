from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.notification import Notification

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
        try:
            print("Initializing database...")
            db.create_all()
            print("✅ Database initialized successfully!")
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)