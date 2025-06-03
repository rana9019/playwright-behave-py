import sqlite3
import os
from datetime import datetime

def check_column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns

def check_table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

def migrate_database():
    db_path = "../reports/test_results.db"

    print("Starting database migration...")
    print(f"Database path: {os.path.abspath(db_path)}")

    if not os.path.exists(db_path):
        print("Database doesn't exist. Creating new database...")
        init_db()
        return True

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if not check_table_exists(cursor, 'test_results'):
            print("test_results table doesn't exist. Creating new database...")
            conn.close()
            init_db()
            return True

        print("Found existing test_results table. Checking schema...")

        missing_columns = []

        required_columns = [
            ('error_message', 'TEXT'),
            ('failed_step', 'TEXT'),
            ('run_count', 'INTEGER DEFAULT 1'),
            ('last_updated', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
        ]

        for column_name, column_type in required_columns:
            if not check_column_exists(cursor, 'test_results', column_name):
                missing_columns.append((column_name, column_type))

        for column_name, column_type in missing_columns:
            try:
                cursor.execute(f"ALTER TABLE test_results ADD COLUMN {column_name} {column_type}")
                print(f" Added column '{column_name}' to test_results table")
            except sqlite3.OperationalError as e:
                print(f" Column '{column_name}' might already exist: {e}")

        if not check_table_exists(cursor, 'test_runs'):
            cursor.execute('''
                CREATE TABLE test_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    feature_name TEXT NOT NULL,
                    scenario_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    duration REAL DEFAULT 0.0,
                    tags TEXT,
                    error_message TEXT,
                    failed_step TEXT,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print(" Created test_runs table")

        if not check_table_exists(cursor, 'test_history'):
            cursor.execute('''
                CREATE TABLE test_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feature_name TEXT NOT NULL UNIQUE,
                    total_runs INTEGER DEFAULT 0,
                    total_passed INTEGER DEFAULT 0,
                    total_failed INTEGER DEFAULT 0,
                    total_skipped INTEGER DEFAULT 0,
                    avg_duration REAL DEFAULT 0.0,
                    last_run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success_rate REAL DEFAULT 0.0
                )
            ''')
            print(" Created test_history table")

        indexes = [
            ('idx_feature_scenario', 'test_results(feature_name, scenario_name)'),
            ('idx_run_timestamp', 'test_runs(run_timestamp)'),
            ('idx_status', 'test_results(status)')
        ]

        for index_name, index_definition in indexes:
            try:
                cursor.execute(f'CREATE INDEX IF NOT EXISTS {index_name} ON {index_definition}')
                print(f" Created index '{index_name}'")
            except sqlite3.OperationalError as e:
                print(f" Index '{index_name}' might already exist: {e}")

        cursor.execute("UPDATE test_results SET run_count = 1 WHERE run_count IS NULL")

        if check_column_exists(cursor, 'test_results', 'run_timestamp'):
            cursor.execute("UPDATE test_results SET last_updated = run_timestamp WHERE last_updated IS NULL")
        else:
            cursor.execute("UPDATE test_results SET last_updated = CURRENT_TIMESTAMP WHERE last_updated IS NULL")

        print(" Updated existing records with default values")

        try:
            cursor.execute('''
                CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_test 
                ON test_results(feature_name, scenario_name)
            ''')
            print(" Added unique constraint to test_results")
        except sqlite3.OperationalError as e:
            print(f"Unique constraint handling: {e}")

        conn.commit()
        print("\n Database migration completed successfully!")

        # Show final schema
        print("\nFinal schema for test_results table:")
        cursor.execute("PRAGMA table_info(test_results)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        return True

    except Exception as e:
        print(f" Error during migration: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect("../reports/test_results.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_name TEXT NOT NULL,
            scenario_name TEXT NOT NULL,
            status TEXT NOT NULL,
            duration REAL DEFAULT 0.0,
            tags TEXT,
            error_message TEXT,
            failed_step TEXT,
            run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            run_count INTEGER DEFAULT 1,
            UNIQUE(feature_name, scenario_name)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            feature_name TEXT NOT NULL,
            scenario_name TEXT NOT NULL,
            status TEXT NOT NULL,
            duration REAL DEFAULT 0.0,
            tags TEXT,
            error_message TEXT,
            failed_step TEXT,
            run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_name TEXT NOT NULL UNIQUE,
            total_runs INTEGER DEFAULT 0,
            total_passed INTEGER DEFAULT 0,
            total_failed INTEGER DEFAULT 0,
            total_skipped INTEGER DEFAULT 0,
            avg_duration REAL DEFAULT 0.0,
            last_run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success_rate REAL DEFAULT 0.0
        )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_feature_scenario ON test_results(feature_name, scenario_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_run_timestamp ON test_runs(run_timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON test_results(status)')

    conn.commit()
    conn.close()
    print(" Database initialized successfully!")

def reset_database():
    db_path = "../reports/test_results.db"

    if os.path.exists(db_path):
        os.remove(db_path)
        print(" Existing database deleted")

    init_db()
    print(" Database reset successfully!")

def check_database_schema():
    db_path = "../reports/test_results.db"

    if not os.path.exists(db_path):
        print(" Database file doesn't exist!")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Current database schema:")
    print("=" * 60)

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in database!")
        conn.close()
        return False

    for table in tables:
        table_name = table[0]
        print(f"\n Table: {table_name}")
        print("-" * 40)

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for col in columns:
            nullable = "NOT NULL" if col[3] else "NULL"
            primary = "PRIMARY KEY" if col[5] else ""
            print(f"  • {col[1]:20} {col[2]:15} {nullable:8} {primary}")

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  Records: {count}")

    conn.close()
    return True

def main():
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--migrate":
            success = migrate_database()
            if success:
                print("\n Migration completed! You can now run your dashboard.")
            else:
                print("\n Migration failed! Please check the errors above.")
                sys.exit(1)

        elif command == "--reset":
            reset_database()

        elif command == "--check":
            if not check_database_schema():
                sys.exit(1)

        elif command == "--init":
            init_db()

        else:
            print("Unknown command. Available options:")
            print("  --migrate   # Migrate existing database to latest schema")
            print("  --reset     # Reset database completely (deletes all data)")
            print("  --check     # Check current database schema")
            print("  --init      # Initialize new database")
            sys.exit(1)
    else:
        print("Database Migration Tool for Cucumber Dashboard")
        print("=" * 50)
        print("Usage:")
        print("  python db_migration.py --migrate   # Migrate existing database")
        print("  python db_migration.py --reset     # Reset database (deletes all data)")
        print("  python db_migration.py --check     # Check current schema")
        print("  python db_migration.py --init      # Initialize new database")
        print("\nTo fix the current error, run:")
        print("  python db_migration.py --migrate")

if __name__ == "__main__":
    main()