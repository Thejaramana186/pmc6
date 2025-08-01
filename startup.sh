#!/bin/bash

echo "🚀 Starting PI Management System..."

# Set Flask app
export FLASK_APP=run.py

# Wait for database if using PostgreSQL
if [ ! -z "$DB_HOST" ] && [ ! -z "$DB_PORT" ]; then
    echo "⏳ Waiting for PostgreSQL to be ready..."
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        echo "Waiting for database at $DB_HOST:$DB_PORT..."
        sleep 2
    done
    echo "✅ Database is ready!"
fi

# Force initialize database tables (critical for AWS deployment)
echo "🔧 Initializing database..."
python3 -c "
import os
from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.notification import Notification
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Drop and recreate all tables to ensure clean state
        db.drop_all()
        db.create_all()
        print('✅ Database tables created successfully!')
        
        # Verify tables exist
        tables = db.engine.execute(text(\"SELECT name FROM sqlite_master WHERE type='table';\")).fetchall()
        print(f'📋 Created tables: {[table[0] for table in tables]}')
        
    except Exception as e:
        print(f'❌ Database initialization error: {e}')
        # Try alternative approach
        try:
            db.create_all()
            print('✅ Database tables created with fallback method!')
        except Exception as e2:
            print(f'❌ Fallback also failed: {e2}')
"

echo "✅ Database initialization complete!"

# Start the application
if [ \"\$FLASK_ENV\" = \"production\" ]; then
    echo \"🚀 Starting production server with Gunicorn...\"
    exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile - --error-logfile - run:app
else
    echo \"🚀 Starting development server...\"
    exec python3 run.py
fi