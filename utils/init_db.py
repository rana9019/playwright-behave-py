import sqlite3
from datetime import datetime
import os

def check_column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns

def migrate_database():
    db_path = "../reports/test_results.db"

    print("Starting database migration...")

    if not os.path.exists(db_path):
        print("Database doesn't exist. Creating new database...")
        init_db()
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_results'")
        if not cursor.fetchone():
            print("test_results table doesn't exist. Creating new database...")
            conn.close()
            init_db()
            return

        missing_columns = []

        if not check_column_exists(cursor, 'test_results', 'error_message'):
            missing_columns.append(('error_message', 'TEXT'))

        if not check_column_exists(cursor, 'test_results', 'failed_step'):
            missing_columns.append(('failed_step', 'TEXT'))

        if not check_column_exists(cursor, 'test_results', 'run_count'):
            missing_columns.append(('run_count', 'INTEGER DEFAULT 1'))

        if not check_column_exists(cursor, 'test_results', 'last_updated'):
            missing_columns.append(('last_updated', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'))

        for column_name, column_type in missing_columns:
            try:
                cursor.execute(f"ALTER TABLE test_results ADD COLUMN {column_name} {column_type}")
                print(f"Added column {column_name} to test_results table")
            except sqlite3.OperationalError as e:
                print(f"Column {column_name} might already exist: {e}")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_runs'")
        if not cursor.fetchone():
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
            print("Created test_runs table")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_history'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE test_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feature_name TEXT NOT NULL,
                    total_runs INTEGER DEFAULT 0,
                    total_passed INTEGER DEFAULT 0,
                    total_failed INTEGER DEFAULT 0,
                    total_skipped INTEGER DEFAULT 0,
                    avg_duration REAL DEFAULT 0.0,
                    last_run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success_rate REAL DEFAULT 0.0
                )
            ''')
            print("Created test_history table")

        try:
            cursor.execute('''
                CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_test 
                ON test_results(feature_name, scenario_name)
            ''')
            print("Added unique constraint to test_results")
        except sqlite3.OperationalError:
            print("Unique constraint already exists")

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_feature_scenario ON test_results(feature_name, scenario_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_run_timestamp ON test_runs(run_timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON test_results(status)')
        print("Created performance indexes")

        cursor.execute("UPDATE test_results SET run_count = 1 WHERE run_count IS NULL")
        cursor.execute("UPDATE test_results SET last_updated = run_timestamp WHERE last_updated IS NULL")

        conn.commit()
        print("Database migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        raise
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
    print("Database initialized successfully!")

def reset_db():
    db_path = "../reports/test_results.db"

    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database deleted")

    init_db()
    print("Database reset successfully!")

def check_db_schema():
    conn = sqlite3.connect("../reports/test_results.db")
    cursor = conn.cursor()

    print("Current database schema:")
    print("=" * 50)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        print("-" * 30)

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for col in columns:
            print(f"  {col[1]} ({col[2]}) {'NOT NULL' if col[3] else ''} {'PRIMARY KEY' if col[5] else ''}")

    conn.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--reset":
            reset_db()
        elif sys.argv[1] == "--check":
            check_db_schema()
        elif sys.argv[1] == "--migrate":
            migrate_database()
        else:
            print("Usage:")
            print("  python db_migration.py --migrate   # Migrate existing database")
            print("  python db_migration.py --reset     # Reset database completely")
            print("  python db_migration.py --check     # Check current schema")
            print("  python db_migration.py             # Initialize new database")
    else:
        init_db()