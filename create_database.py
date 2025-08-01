#!/usr/bin/env python3
"""
Database Creation Script for PI Management System
This script creates the database and all tables
"""

import pymysql
import sys
from urllib.parse import quote_plus

def create_database():
    """Create the database if it doesn't exist"""
    
    # Database connection parameters
    host = 'pmc6-devbd.c63wim4ayano.us-east-1.rds.amazonaws.com'
    port = 3306
    user = 'admin'
    password = 'bLy?rXQDy~c43da1U$Fzh<y.BUYP.'
    database_name = 'pmc6db'
    
    try:
        # Connect to MySQL server (without specifying database)
        print("Connecting to MySQL server...")
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        print(f"Creating database '{database_name}' if it doesn't exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        print(f"✅ Database '{database_name}' created successfully!")
        
        # Close connection
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error creating database: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_tables():
    """Create all application tables"""
    try:
        from app import create_app, db
        
        print("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            print("Creating all database tables...")
            db.create_all()
            print("✅ All tables created successfully!")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == '__main__':
    print("=== PI Management System Database Setup ===")
    
    # Step 1: Create database
    if create_database():
        print("\n=== Creating Tables ===")
        # Step 2: Create tables
        if create_tables():
            print("\n🎉 Database setup completed successfully!")
            print("\nYou can now run the application with: python run.py")
        else:
            print("\n❌ Failed to create tables")
            sys.exit(1)
    else:
        print("\n❌ Failed to create database")
        sys.exit(1)