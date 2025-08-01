#!/usr/bin/env python3
"""
Database Connection Test Script
This script tests various connection scenarios to help diagnose the issue
"""

import pymysql
import sys
from urllib.parse import quote_plus

def test_connection_scenarios():
    """Test different connection scenarios"""
    
    # Connection parameters
    host = 'pmc6-devbd.c63wim4ayano.us-east-1.rds.amazonaws.com'
    port = 3306
    user = 'admin'
    password = 'bLy?rXQDy~c43da1U$Fzh<y.BUYP.'
    
    print("=== Database Connection Troubleshooting ===\n")
    
    # Test 1: Basic connection without database
    print("Test 1: Testing basic connection to MySQL server...")
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4',
            connect_timeout=10
        )
        print("✅ Successfully connected to MySQL server!")
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"   MySQL Version: {version[0]}")
        
        # Check if database exists
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print(f"   Available databases: {[db[0] for db in databases]}")
        
        # Check if pmc6db exists
        cursor.execute("SHOW DATABASES LIKE 'pmc6db'")
        db_exists = cursor.fetchone()
        if db_exists:
            print("   ✅ Database 'pmc6db' already exists!")
        else:
            print("   ❌ Database 'pmc6db' does not exist - will need to create it")
        
        cursor.close()
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def create_database_if_needed():
    """Create database if connection is successful"""
    
    host = 'pmc6-devbd.c63wim4ayano.us-east-1.rds.amazonaws.com'
    port = 3306
    user = 'admin'
    password = 'bLy?rXQDy~c43da1U$Fzh<y.BUYP.'
    
    print("\nTest 2: Attempting to create database...")
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS pmc6db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Database 'pmc6db' created successfully!")
        
        cursor.close()
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ Failed to create database: {e}")
        return False

def test_connection_with_database():
    """Test connection to the specific database"""
    
    host = 'pmc6-devbd.c63wim4ayano.us-east-1.rds.amazonaws.com'
    port = 3306
    user = 'admin'
    password = 'bLy?rXQDy~c43da1U$Fzh<y.BUYP.'
    database = 'pmc6db'
    
    print("\nTest 3: Testing connection to pmc6db database...")
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        print("✅ Successfully connected to pmc6db database!")
        
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()
        print(f"   Current database: {current_db[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ Failed to connect to database: {e}")
        return False

def check_user_privileges():
    """Check user privileges"""
    
    host = 'pmc6-devbd.c63wim4ayano.us-east-1.rds.amazonaws.com'
    port = 3306
    user = 'admin'
    password = 'bLy?rXQDy~c43da1U$Fzh<y.BUYP.'
    
    print("\nTest 4: Checking user privileges...")
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
        grants = cursor.fetchall()
        print("   User privileges:")
        for grant in grants:
            print(f"   - {grant[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ Failed to check privileges: {e}")
        return False

if __name__ == '__main__':
    # Run all tests
    if test_connection_scenarios():
        if create_database_if_needed():
            if test_connection_with_database():
                print("\n🎉 All tests passed! Your database is ready.")
                print("\nYou can now run: python run.py")
            else:
                print("\n❌ Database connection test failed")
        else:
            print("\n❌ Database creation failed")
    else:
        print("\n❌ Basic connection test failed")
        print("\nPossible issues:")
        print("1. Check if your IP address is whitelisted in RDS security groups")
        print("2. Verify the username and password are correct")
        print("3. Check if the RDS instance is publicly accessible")
        print("4. Verify the endpoint URL is correct")