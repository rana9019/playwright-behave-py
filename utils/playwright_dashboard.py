#playwright_dashboard.py file
import argparse
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import uuid
import os

COLORS = {
    "primary": "#2E86AB",
    "secondary": "#A23B72",
    "success": "#F18F01",
    "warning": "#C73E1D",
    "neutral": "#6B7280",
    "light_bg": "#F8FAFC",
    "dark_text": "#1F2937"
}

STATUS_COLORS = {
    "passed": "#10B981",
    "failed": "#EF4444",
    "skipped": "#6B7280",
}


def setup_database():
    conn = sqlite3.connect("cucumber_tests.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_name TEXT NOT NULL,
            scenario_name TEXT NOT NULL,
            status TEXT NOT NULL,
            duration REAL DEFAULT 0.0,
            tags TEXT,
            error_msg TEXT,
            failed_step TEXT,
            run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
            error_msg TEXT,
            failed_step TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_name TEXT NOT NULL UNIQUE,
            total_runs INTEGER DEFAULT 0,
            passed_count INTEGER DEFAULT 0,
            failed_count INTEGER DEFAULT 0,
            skipped_count INTEGER DEFAULT 0,
            avg_duration REAL DEFAULT 0.0,
            last_run TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success_percentage REAL DEFAULT 0.0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS step_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            passed_steps INTEGER DEFAULT 0,
            failed_steps INTEGER DEFAULT 0,
            skipped_steps INTEGER DEFAULT 0,
            undefined_steps INTEGER DEFAULT 0,
            pending_steps INTEGER DEFAULT 0,
            total_steps INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_feature_scenario ON test_results(feature_name, scenario_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON test_runs(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON test_results(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_run_id ON step_statistics(run_id)')

    conn.commit()
    conn.close()

def determine_scenario_status(steps):
    if not steps:
        return "skipped"

    failed_count = 0
    passed_count = 0
    skipped_count = 0
    undefined_count = 0

    for step in steps:
        result = step.get("result", {})
        status = result.get("status", "")

        if not result or not status:
            skipped_count += 1
            continue

        if status == "failed":
            failed_count += 1
        elif status == "passed":
            passed_count += 1
        elif status in ["skipped", "untested"]:
            skipped_count += 1
        elif status == "undefined":
            undefined_count += 1
        else:
            skipped_count += 1

    if failed_count > 0:
        return "failed"
    elif undefined_count > 0:
        return "failed"
    elif passed_count == 0 and skipped_count > 0:
        return "skipped"
    elif passed_count > 0:
        return "passed"
    else:
        return "skipped"


def parse_cucumber_json(json_data):
    scenarios = []
    steps_data = []
    feature_stats = {}

    global_step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}
    feature_step_stats = {}
    feature_level_stats = {"passed": 0, "failed": 0, "skipped": 0}

    print(f"DEBUG: Processing {len(json_data)} features from JSON")

    for feature in json_data:
        feature_name = feature.get("name", "Unknown Feature")
        if feature_name not in feature_stats:
            feature_stats[feature_name] = {"passed": 0, "failed": 0, "skipped": 0}

        if feature_name not in feature_step_stats:
            feature_step_stats[feature_name] = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}

        print(f"DEBUG: Processing feature: {feature_name}")

        feature_has_failures = False
        feature_has_passed = False

        for element in feature.get("elements", []):
            if element.get("type") not in ["scenario", "scenario_outline"]:
                continue

            scenario_name = element.get("name", "Unnamed Scenario")
            print(f"DEBUG: Processing scenario: {scenario_name}")

            tag_list = element.get("tags", [])
            if tag_list:
                tags = " ".join([tag.get("name", "") if isinstance(tag, dict) else str(tag) for tag in tag_list])
            else:
                tags = ""

            steps = element.get("steps", [])
            print(f"DEBUG: Found {len(steps)} steps in scenario: {scenario_name}")

            total_duration = 0.0
            error_message = ""
            failed_step_info = ""

            step_statuses = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}

            for step in steps:
                result = step.get("result", {})
                step_status = result.get("status", "")
                step_duration = result.get("duration", 0.0)

                print(f"DEBUG: Step status: '{step_status}', duration: {step_duration}")

                if step_duration and step_duration > 1000000:  # Likely nanoseconds
                    step_duration = step_duration / 1e9

                total_duration += step_duration

                if not result or not step_status:
                    normalized_status = "skipped"
                elif step_status == "passed":
                    normalized_status = "passed"
                elif step_status == "failed":
                    normalized_status = "failed"
                elif step_status in ["skipped", "untested"]:
                    normalized_status = "skipped"
                elif step_status == "undefined":
                    normalized_status = "undefined"
                elif step_status == "pending":
                    normalized_status = "pending"
                else:
                    normalized_status = "skipped"
                    print(f"DEBUG: Unknown step status '{step_status}' treated as skipped")

                if normalized_status in step_statuses:
                    step_statuses[normalized_status] += 1

                if normalized_status in global_step_stats:
                    global_step_stats[normalized_status] += 1

                if normalized_status in feature_step_stats[feature_name]:
                    feature_step_stats[feature_name][normalized_status] += 1

                if normalized_status == "failed":
                    error_message = result.get("error_message", "")
                    if not error_message:
                        error_message = result.get("failure", {}).get("message", "")
                        if not error_message:
                            error_message = str(result.get("error", ""))
                    failed_step_info = f"{step.get('keyword', '')} {step.get('name', '')}"

                steps_data.append({
                    "feature": feature_name,
                    "scenario": scenario_name,
                    "keyword": step.get("keyword", ""),
                    "step_name": step.get("name", ""),
                    "status": normalized_status,
                    "duration": step_duration
                })

            scenario_status = determine_scenario_status(steps)

            if scenario_status == "failed":
                feature_has_failures = True
            elif scenario_status == "passed":
                feature_has_passed = True

            if scenario_status in feature_stats[feature_name]:
                feature_stats[feature_name][scenario_status] += 1

            scenarios.append({
                "feature": feature_name,
                "name": scenario_name,
                "tags": tags,
                "status": scenario_status,
                "duration": total_duration,
                "error_message": error_message,
                "failed_step": failed_step_info,
                "step_counts": step_statuses
            })

        if feature_has_failures:
            feature_level_stats["failed"] += 1
        elif feature_has_passed:
            feature_level_stats["passed"] += 1
        else:
            feature_level_stats["skipped"] += 1

    print(f"DEBUG: Global step stats: {global_step_stats}")
    print(f"DEBUG: Feature step stats: {feature_step_stats}")

    scenarios_df = pd.DataFrame(scenarios)
    steps_df = pd.DataFrame(steps_data)

    scenarios_df.attrs['global_step_stats'] = global_step_stats
    scenarios_df.attrs['feature_level_stats'] = feature_level_stats
    scenarios_df.attrs['feature_step_stats'] = feature_step_stats

    feature_summary = []
    for feature, stats in feature_stats.items():
        total_tests = stats["passed"] + stats["failed"] + stats["skipped"]
        if scenarios_df.empty:
            avg_duration = 0
            total_duration = 0
        else:
            feature_scenarios = scenarios_df[scenarios_df["feature"] == feature]
            avg_duration = feature_scenarios["duration"].mean() if not feature_scenarios.empty else 0
            total_duration = feature_scenarios["duration"].sum() if not feature_scenarios.empty else 0

        feature_summary.append({
            "feature_name": feature,
            "total_scenarios": total_tests,
            "passed": stats["passed"],
            "failed": stats["failed"],
            "skipped": stats["skipped"],
            "total_duration": total_duration,
            "avg_duration": avg_duration if not pd.isna(avg_duration) else 0,
            "pass_rate": round((stats["passed"] / total_tests) * 100, 2) if total_tests > 0 else 0
        })

    features_df = pd.DataFrame(feature_summary)
    return scenarios_df, steps_df, features_df

def store_test_results(scenarios_df, run_id=None):
    if run_id is None:
        run_id = str(uuid.uuid4())

    setup_database()

    conn = sqlite3.connect("cucumber_tests.db")
    cursor = conn.cursor()

    current_timestamp = datetime.now()

    if hasattr(scenarios_df, 'attrs') and 'global_step_stats' in scenarios_df.attrs:
        step_stats = scenarios_df.attrs['global_step_stats']
        total_steps = sum(step_stats.values())

        cursor.execute('''
            INSERT INTO step_statistics (
                run_id, passed_steps, failed_steps, skipped_steps, 
                undefined_steps, pending_steps, total_steps, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            run_id,
            step_stats.get('passed', 0),
            step_stats.get('failed', 0),
            step_stats.get('skipped', 0),
            step_stats.get('undefined', 0),
            step_stats.get('pending', 0),
            total_steps,
            current_timestamp
        ))

    if hasattr(scenarios_df, 'attrs') and 'feature_step_stats' in scenarios_df.attrs:
        feature_step_stats = scenarios_df.attrs['feature_step_stats']

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feature_step_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                feature_name TEXT NOT NULL,
                passed_steps INTEGER DEFAULT 0,
                failed_steps INTEGER DEFAULT 0,
                skipped_steps INTEGER DEFAULT 0,
                undefined_steps INTEGER DEFAULT 0,
                pending_steps INTEGER DEFAULT 0,
                total_steps INTEGER DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        for feature_name, step_stats in feature_step_stats.items():
            total_steps = sum(step_stats.values())
            if total_steps > 0:
                cursor.execute('''
                    INSERT INTO feature_step_statistics (
                        run_id, feature_name, passed_steps, failed_steps, skipped_steps, 
                        undefined_steps, pending_steps, total_steps, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    run_id,
                    str(feature_name),
                    step_stats.get('passed', 0),
                    step_stats.get('failed', 0),
                    step_stats.get('skipped', 0),
                    step_stats.get('undefined', 0),
                    step_stats.get('pending', 0),
                    total_steps,
                    current_timestamp
                ))

    for _, scenario in scenarios_df.iterrows():
        feature_name = str(scenario.get('feature', ''))
        scenario_name = str(scenario.get('name', ''))
        status = str(scenario.get('status', ''))
        duration = float(scenario.get('duration', 0.0)) if pd.notna(scenario.get('duration')) else 0.0

        tags = scenario.get('tags', '')
        if isinstance(tags, list):
            tags_str = ' '.join(str(tag) for tag in tags)
        elif tags is None or pd.isna(tags):
            tags_str = ''
        else:
            tags_str = str(tags)

        error_msg = str(scenario.get('error_message', '')) if scenario.get('error_message') else ''
        failed_step = str(scenario.get('failed_step', '')) if scenario.get('failed_step') else ''

        cursor.execute('''
            INSERT INTO test_results (
                feature_name, scenario_name, status, duration, tags, 
                error_msg, failed_step, updated_at, run_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(feature_name, scenario_name) DO UPDATE SET
                status = excluded.status,
                duration = excluded.duration,
                tags = excluded.tags,
                error_msg = excluded.error_msg,
                failed_step = excluded.failed_step,
                updated_at = excluded.updated_at,
                run_count = run_count + 1
        ''', (
            feature_name, scenario_name, status,
            duration, tags_str,
            error_msg, failed_step,
            current_timestamp
        ))

        cursor.execute('''
            INSERT INTO test_runs (
                run_id, feature_name, scenario_name, status, duration, 
                tags, error_msg, failed_step, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            run_id, feature_name, scenario_name, status,
            duration, tags_str,
            error_msg, failed_step,
            current_timestamp
        ))

    for feature_name in scenarios_df['feature'].unique():
        feature_data = scenarios_df[scenarios_df['feature'] == feature_name]

        total_runs = len(feature_data)
        passed_count = len(feature_data[feature_data['status'] == 'passed'])
        failed_count = len(feature_data[feature_data['status'] == 'failed'])
        skipped_count = len(feature_data[feature_data['status'] == 'skipped'])
        avg_duration = feature_data['duration'].mean()
        if pd.isna(avg_duration):
            avg_duration = 0.0
        success_rate = (passed_count / total_runs * 100) if total_runs > 0 else 0

        cursor.execute('''
            INSERT INTO performance_history (
                feature_name, total_runs, passed_count, failed_count, 
                skipped_count, avg_duration, last_run, success_percentage
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(feature_name) DO UPDATE SET
                total_runs = total_runs + excluded.total_runs,
                passed_count = passed_count + excluded.passed_count,
                failed_count = failed_count + excluded.failed_count,
                skipped_count = skipped_count + excluded.skipped_count,
                avg_duration = (avg_duration + excluded.avg_duration) / 2,
                last_run = excluded.last_run,
                success_percentage = excluded.success_percentage
        ''', (
            str(feature_name), total_runs, passed_count, failed_count,
            skipped_count, float(avg_duration), current_timestamp, float(success_rate)
        ))

    conn.commit()
    conn.close()

    feature_stats = scenarios_df.attrs.get('feature_level_stats', {"passed": 0, "failed": 0, "skipped": 0})
    step_stats = scenarios_df.attrs.get('global_step_stats', {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0})

    scenario_passed = len(scenarios_df[scenarios_df['status'] == 'passed'])
    scenario_failed = len(scenarios_df[scenarios_df['status'] == 'failed'])
    scenario_skipped = len(scenarios_df[scenarios_df['status'] == 'skipped'])

    print(f"Successfully saved {len(scenarios_df)} test results with run ID: {run_id}")
    print(f"\n{'='*60}")
    print("Test Results Summary")
    print(f"{'='*60}")
    print(f"Run ID: {run_id}")
    print(f"{feature_stats['passed']} features passed, {feature_stats['failed']} failed, {feature_stats['skipped']} skipped")
    print(f"{scenario_passed} scenarios passed, {scenario_failed} failed, {scenario_skipped} skipped")
    print(f"{step_stats['passed']} steps passed, {step_stats['failed']} failed, {step_stats['skipped']} skipped, {step_stats['undefined']} undefined, {step_stats['pending']} pending")
    print(f"{'='*60}")

    return run_id

def load_test_data():
    setup_database()

    conn = sqlite3.connect("cucumber_tests.db")

    try:
        scenarios_df = pd.read_sql_query("""
            SELECT feature_name as feature, scenario_name as name, status, duration, 
                   tags, error_msg, failed_step, updated_at, run_count
            FROM test_results 
            ORDER BY updated_at DESC
        """, conn)

        history_df = pd.read_sql_query("""
            SELECT feature_name, total_runs, passed_count, failed_count, 
                   skipped_count, avg_duration, success_percentage, last_run
            FROM performance_history
            ORDER BY last_run DESC
        """, conn)

        runs_df = pd.read_sql_query("""
            SELECT run_id, feature_name, scenario_name, status, duration, timestamp
            FROM test_runs 
            WHERE timestamp >= datetime('now', '-30 days')
            ORDER BY timestamp DESC
        """, conn)

        step_stats_df = pd.read_sql_query("""
            SELECT passed_steps, failed_steps, skipped_steps, 
                   undefined_steps, pending_steps, total_steps
            FROM step_statistics 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, conn)

        feature_step_stats_df = pd.read_sql_query("""
            SELECT fss.feature_name, 
                   SUM(fss.passed_steps) as passed_steps,
                   SUM(fss.failed_steps) as failed_steps, 
                   SUM(fss.skipped_steps) as skipped_steps,
                   SUM(fss.undefined_steps) as undefined_steps, 
                   SUM(fss.pending_steps) as pending_steps,
                   SUM(fss.total_steps) as total_steps
            FROM feature_step_statistics fss
            INNER JOIN (
                SELECT feature_name, MAX(timestamp) as latest_timestamp
                FROM feature_step_statistics
                GROUP BY feature_name
            ) latest ON fss.feature_name = latest.feature_name 
                    AND fss.timestamp = latest.latest_timestamp
            GROUP BY fss.feature_name
        """, conn)

        if not step_stats_df.empty:
            row = step_stats_df.iloc[0]
            scenarios_df.attrs['global_step_stats'] = {
                'passed': int(row['passed_steps']),
                'failed': int(row['failed_steps']),
                'skipped': int(row['skipped_steps']),
                'undefined': int(row['undefined_steps']),
                'pending': int(row['pending_steps'])
            }
        else:
            scenarios_df.attrs['global_step_stats'] = {
                'passed': 0, 'failed': 0, 'skipped': 0, 'undefined': 0, 'pending': 0
            }

        if not feature_step_stats_df.empty:
            feature_step_stats = {}
            for _, row in feature_step_stats_df.iterrows():
                feature_name = row['feature_name']
                feature_step_stats[feature_name] = {
                    'passed': int(row['passed_steps']),
                    'failed': int(row['failed_steps']),
                    'skipped': int(row['skipped_steps']),
                    'undefined': int(row['undefined_steps']),
                    'pending': int(row['pending_steps'])
                }
            scenarios_df.attrs['feature_step_stats'] = feature_step_stats
        else:
            scenarios_df.attrs['feature_step_stats'] = {}

        expected_columns = {
            'feature': '',
            'name': '',
            'status': 'unknown',
            'duration': 0.0,
            'tags': '',
            'error_msg': '',
            'failed_step': '',
            'updated_at': '',
            'run_count': 0
        }

        for col, default_val in expected_columns.items():
            if col not in scenarios_df.columns:
                scenarios_df[col] = default_val
            else:
                scenarios_df[col] = scenarios_df[col].fillna(default_val)

    except Exception as e:
        print(f"Database read error: {e}")
        scenarios_df = pd.DataFrame()
        history_df = pd.DataFrame()
        runs_df = pd.DataFrame()

        scenarios_df = pd.DataFrame(columns=[
            'feature', 'name', 'status', 'duration', 'tags',
            'error_msg', 'failed_step', 'updated_at', 'run_count'
        ])

        scenarios_df.attrs = {
            'global_step_stats': {'passed': 0, 'failed': 0, 'skipped': 0, 'undefined': 0, 'pending': 0},
            'feature_step_stats': {}
        }

    finally:
        conn.close()

    return scenarios_df, history_df, runs_df

def format_test_duration(seconds):
    if pd.isna(seconds) or seconds == 0:
        return "0.00s"

    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.2f}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}h {mins}m {secs:.2f}s"

def create_trend_analysis(runs_df):
    if runs_df.empty:
        return None, None

    runs_df['date'] = pd.to_datetime(runs_df['timestamp']).dt.date

    daily_stats = runs_df.groupby('date').agg({
        'status': ['count', lambda x: (x == 'passed').sum()]
    }).reset_index()
    daily_stats.columns = ['date', 'total_tests', 'passed_tests']
    daily_stats['success_rate'] = (daily_stats['passed_tests'] / daily_stats['total_tests'] * 100).round(2)

    trend_chart = px.line(
        daily_stats, x='date', y='success_rate',
        title='Daily Success Rate Trend (Last 30 Days)',
        labels={'success_rate': 'Success Rate (%)', 'date': 'Date'}
    )
    trend_chart.update_traces(line_color=COLORS["primary"], line_width=3)
    trend_chart.update_layout(yaxis=dict(range=[0, 100]))

    feature_trends = runs_df.groupby(['feature_name', 'date']).agg({
        'status': lambda x: (x == 'passed').sum() / len(x) * 100
    }).reset_index()
    feature_trends.columns = ['feature', 'date', 'success_rate']

    feature_chart = px.line(
        feature_trends, x='date', y='success_rate', color='feature',
        title='Feature Success Rate Trends',
        labels={'success_rate': 'Success Rate (%)', 'date': 'Date'}
    )
    feature_chart.update_layout(yaxis=dict(range=[0, 100]))

    return trend_chart, feature_chart

def apply_filters(scenarios_df, selected_feature, selected_status, search_query):
    if scenarios_df.empty:
        return scenarios_df

    filtered_df = scenarios_df.copy()

    if selected_feature != "All":
        filtered_df = filtered_df[filtered_df["feature"] == selected_feature]

    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]

    if search_query:
        search_columns = []

        if "feature" in filtered_df.columns:
            search_columns.append(filtered_df["feature"].str.contains(search_query, case=False, na=False))
        if "name" in filtered_df.columns:
            search_columns.append(filtered_df["name"].str.contains(search_query, case=False, na=False))
        if "tags" in filtered_df.columns:
            search_columns.append(filtered_df["tags"].str.contains(search_query, case=False, na=False))
        if "error_msg" in filtered_df.columns:
            search_columns.append(filtered_df["error_msg"].str.contains(search_query, case=False, na=False))
        if "failed_step" in filtered_df.columns:
            search_columns.append(filtered_df["failed_step"].str.contains(search_query, case=False, na=False))

        if search_columns:
            search_mask = search_columns[0]
            for condition in search_columns[1:]:
                search_mask = search_mask | condition
            filtered_df = filtered_df[search_mask]

    return filtered_df

def calculate_metrics_by_level(scenarios_df, level="scenario", selected_feature="All"):
    if scenarios_df.empty:
        return {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'undefined_tests': 0,
            'pending_tests': 0,
            'success_rate': 0,
            'stats_label': level.capitalize() + 's'
        }

    if level == "step":
        if hasattr(scenarios_df, 'attrs'):
            if selected_feature != "All" and 'feature_step_stats' in scenarios_df.attrs:
                feature_step_stats = scenarios_df.attrs['feature_step_stats']
                if selected_feature in feature_step_stats:
                    step_stats = feature_step_stats[selected_feature]
                    stats_label = f"Steps ({selected_feature})"
                else:
                    step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}
                    stats_label = f"Steps ({selected_feature}) - No Data"
            elif selected_feature == "All":
                if 'feature_step_stats' in scenarios_df.attrs:
                    feature_step_stats = scenarios_df.attrs['feature_step_stats']
                    step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}

                    for feature_stats in feature_step_stats.values():
                        for status, count in feature_stats.items():
                            if status in step_stats:
                                step_stats[status] += count

                    stats_label = "Steps (All Features)"
                elif 'global_step_stats' in scenarios_df.attrs:
                    step_stats = scenarios_df.attrs['global_step_stats']
                    stats_label = "Steps (All Features)"
                else:
                    step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}
                    stats_label = "Steps (No Data)"
            else:
                step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}
                stats_label = "Steps (No Data)"

            total_tests = sum(step_stats.values())
            passed_tests = step_stats.get('passed', 0)
            failed_tests = step_stats.get('failed', 0)
            skipped_tests = step_stats.get('skipped', 0)
            undefined_tests = step_stats.get('undefined', 0)
            pending_tests = step_stats.get('pending', 0)
            success_rate = round((passed_tests / total_tests) * 100, 2) if total_tests > 0 else 0
        else:
            return {
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 0,
                'skipped_tests': 0,
                'undefined_tests': 0,
                'pending_tests': 0,
                'success_rate': 0,
                'stats_label': "Steps (No Data)"
            }

    elif level == "feature":
        if selected_feature != "All":
            feature_scenarios = scenarios_df[scenarios_df['feature'] == selected_feature]
            total_tests = len(feature_scenarios)
            passed_tests = len(feature_scenarios[feature_scenarios['status'] == 'passed'])
            failed_tests = len(feature_scenarios[feature_scenarios['status'] == 'failed'])
            skipped_tests = len(feature_scenarios[feature_scenarios['status'] == 'skipped'])
            stats_label = f"Scenarios in {selected_feature}"
        else:
            feature_stats = {}
            for feature in scenarios_df['feature'].unique():
                feature_data = scenarios_df[scenarios_df['feature'] == feature]

                has_failures = len(feature_data[feature_data['status'] == 'failed']) > 0
                has_passed = len(feature_data[feature_data['status'] == 'passed']) > 0

                if has_failures:
                    feature_status = 'failed'
                elif has_passed:
                    feature_status = 'passed'
                else:
                    feature_status = 'skipped'

                feature_stats[feature] = feature_status

            total_tests = len(feature_stats)
            passed_tests = sum(1 for status in feature_stats.values() if status == 'passed')
            failed_tests = sum(1 for status in feature_stats.values() if status == 'failed')
            skipped_tests = sum(1 for status in feature_stats.values() if status == 'skipped')
            stats_label = "Features"

        undefined_tests = 0
        pending_tests = 0
        success_rate = round((passed_tests / total_tests) * 100, 2) if total_tests > 0 else 0

    else:
        if selected_feature != "All":
            filtered_scenarios = scenarios_df[scenarios_df['feature'] == selected_feature]
        else:
            filtered_scenarios = scenarios_df

        total_tests = len(filtered_scenarios)
        passed_tests = len(filtered_scenarios[filtered_scenarios["status"] == "passed"])
        failed_tests = len(filtered_scenarios[filtered_scenarios["status"] == "failed"])
        skipped_tests = len(filtered_scenarios[filtered_scenarios["status"] == "skipped"])
        undefined_tests = 0
        pending_tests = 0
        success_rate = round((passed_tests / total_tests) * 100, 2) if total_tests > 0 else 0

        if selected_feature != "All":
            stats_label = f"Scenarios ({selected_feature})"
        else:
            stats_label = "Scenarios"

    return {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'skipped_tests': skipped_tests,
        'undefined_tests': undefined_tests,
        'pending_tests': pending_tests,
        'success_rate': success_rate,
        'stats_label': stats_label
    }

def get_level_specific_dataframe(scenarios_df, level="scenario", selected_feature="All"):
    if level == "feature":
        if selected_feature != "All":
            feature_data = scenarios_df[scenarios_df['feature'] == selected_feature].copy()
            return feature_data
        else:
            feature_summary = []
            for feature in scenarios_df['feature'].unique():
                feature_data = scenarios_df[scenarios_df['feature'] == feature]

                total_scenarios = len(feature_data)
                passed_scenarios = len(feature_data[feature_data['status'] == 'passed'])
                failed_scenarios = len(feature_data[feature_data['status'] == 'failed'])
                skipped_scenarios = len(feature_data[feature_data['status'] == 'skipped'])

                if failed_scenarios > 0:
                    feature_status = 'failed'
                elif passed_scenarios > 0:
                    feature_status = 'passed'
                else:
                    feature_status = 'skipped'

                total_duration = feature_data['duration'].sum()
                avg_duration = feature_data['duration'].mean()
                success_rate = round((passed_scenarios / total_scenarios) * 100, 2) if total_scenarios > 0 else 0

                if 'updated_at' in feature_data.columns:
                    last_run = feature_data['updated_at'].max()
                else:
                    last_run = "Unknown"

                total_runs = feature_data['run_count'].sum() if 'run_count' in feature_data.columns else 0

                feature_summary.append({
                    'feature': feature,
                    'name': feature,
                    'status': feature_status,
                    'total_scenarios': total_scenarios,
                    'passed_scenarios': passed_scenarios,
                    'failed_scenarios': failed_scenarios,
                    'skipped_scenarios': skipped_scenarios,
                    'success_rate': success_rate,  # This ensures success_rate is always present
                    'total_duration': total_duration,
                    'duration': avg_duration if not pd.isna(avg_duration) else 0,
                    'last_run': last_run,
                    'run_count': total_runs,
                    'tags': ""
                })

            return pd.DataFrame(feature_summary)

    elif level == "step":
        if hasattr(scenarios_df, 'attrs'):
            if selected_feature != "All" and 'feature_step_stats' in scenarios_df.attrs:
                feature_step_stats = scenarios_df.attrs['feature_step_stats']
                if selected_feature in feature_step_stats:
                    step_stats = feature_step_stats[selected_feature]
                else:
                    step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}
            elif selected_feature == "All":
                if 'feature_step_stats' in scenarios_df.attrs:
                    feature_step_stats = scenarios_df.attrs['feature_step_stats']
                    step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}

                    for feature_stats in feature_step_stats.values():
                        for status, count in feature_stats.items():
                            if status in step_stats:
                                step_stats[status] += count
                elif 'global_step_stats' in scenarios_df.attrs:
                    step_stats = scenarios_df.attrs['global_step_stats']
                else:
                    step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}
            else:
                step_stats = {"passed": 0, "failed": 0, "skipped": 0, "undefined": 0, "pending": 0}

            step_summary = []
            total_steps = sum(step_stats.values())

            for status, count in step_stats.items():
                if count > 0:
                    step_summary.append({
                        'name': f"{status.capitalize()} Steps",
                        'status': status,
                        'count': count,
                        'percentage': round((count / total_steps) * 100, 2) if total_steps > 0 else 0
                    })

            return pd.DataFrame(step_summary)
        else:
            return pd.DataFrame()

    else:
        if selected_feature != "All":
            return scenarios_df[scenarios_df['feature'] == selected_feature].copy()
        else:
            return scenarios_df.copy()

def apply_detailed_search(display_df, search_query, view_level):
    if not search_query or display_df.empty:
        return display_df

    filtered_df = display_df.copy()
    search_columns = []

    if view_level == "feature":
        if "name" in filtered_df.columns:
            search_columns.append(filtered_df["name"].str.contains(search_query, case=False, na=False))
        if "status" in filtered_df.columns:
            search_columns.append(filtered_df["status"].str.contains(search_query, case=False, na=False))

    elif view_level == "step":
        if "name" in filtered_df.columns:
            search_columns.append(filtered_df["name"].str.contains(search_query, case=False, na=False))
        if "status" in filtered_df.columns:
            search_columns.append(filtered_df["status"].str.contains(search_query, case=False, na=False))

    else:
        if "feature" in filtered_df.columns:
            search_columns.append(filtered_df["feature"].str.contains(search_query, case=False, na=False))
        if "name" in filtered_df.columns:
            search_columns.append(filtered_df["name"].str.contains(search_query, case=False, na=False))
        if "status" in filtered_df.columns:
            search_columns.append(filtered_df["status"].str.contains(search_query, case=False, na=False))
        if "tags" in filtered_df.columns:
            search_columns.append(filtered_df["tags"].str.contains(search_query, case=False, na=False))
        if "error_msg" in filtered_df.columns:
            search_columns.append(filtered_df["error_msg"].str.contains(search_query, case=False, na=False))
        if "failed_step" in filtered_df.columns:
            search_columns.append(filtered_df["failed_step"].str.contains(search_query, case=False, na=False))

    if search_columns:
        search_mask = search_columns[0]
        for condition in search_columns[1:]:
            search_mask = search_mask | condition
        filtered_df = filtered_df[search_mask]

    return filtered_df

def build_dashboard():
    st.set_page_config(
        page_title="Cucumber Test Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2rem 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    .main > div {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .metric-container {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin: 12px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 16px 16px 0 0;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .metric-number {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .metric-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-passed {
        color: #059669;
        text-shadow: 0 2px 4px rgba(5, 150, 105, 0.1);
    }
    .status-failed {
        color: #dc2626;
        text-shadow: 0 2px 4px rgba(220, 38, 38, 0.1);
    }
    .status-skipped {
        color: #6b7280;
        text-shadow: 0 2px 4px rgba(107, 114, 128, 0.1);
    }
    
    .main-header {
        color: #1e293b;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
        margin: 2rem 0 3rem 0;
        position: relative;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    .level-selector {
        background: linear-gradient(135deg, #e0e7ff 0%, #f0f9ff 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 24px;
        border-left: 5px solid #4f46e5;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
    }
    
    .search-container {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 24px;
        border-left: 5px solid #0ea5e9;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        border-radius: 0 16px 16px 0;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.05);
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        transition: border-color 0.2s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .element-container .stMarkdown h1,
    .element-container .stMarkdown h2,
    .element-container .stMarkdown h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1e293b;
    }
    
    .stDataFrame {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .filter-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        margin: 4px 8px 4px 0;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #10b981;
        margin: 12px 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #f59e0b;
        margin: 12px 0;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        font-family: 'Inter', sans-serif;
        position: relative;
        padding-bottom: 8px;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

    try:
        scenarios_df, history_df, runs_df = load_test_data()
    except Exception as e:
        st.error(f"Error loading test data: {str(e)}")
        scenarios_df, history_df, runs_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    with st.sidebar:
        st.title("Test Dashboard")
        st.markdown("### Configuration")

        st.markdown("**View Level**")
        view_level = st.selectbox(
            "Choose analysis level:",
            ["scenario", "feature", "step"],
            format_func=lambda x: {
                "feature": "Feature Level",
                "scenario": "Scenario Level",
                "step": "Step Level"
            }[x],
            help="Select whether to view statistics at the feature, scenario, or step level"
        )

        if not scenarios_df.empty:
            search_query = ""

            all_features = ["All"] + sorted(scenarios_df["feature"].unique().tolist())
            selected_feature = st.selectbox("Feature", all_features)

            all_statuses = ["All", "passed", "failed", "skipped"]
            selected_status = st.selectbox("Status", all_statuses)

            filtered_df = apply_filters(scenarios_df, selected_feature, selected_status, search_query)
        else:
            filtered_df = scenarios_df
            search_query = ""
            selected_feature = "All"

        st.markdown("---")
        st.markdown("**Statistics**")
        st.markdown(f"**Total Records:** {len(scenarios_df)}")
        st.markdown(f"**Showing:** {len(filtered_df)}")
        if not scenarios_df.empty:
            last_update = scenarios_df['updated_at'].max() if 'updated_at' in scenarios_df.columns else "Unknown"
            st.markdown(f"**Last Update:** {last_update}")

    st.markdown('<h1 class="main-header">Cucumber Test Results Dashboard</h1>', unsafe_allow_html=True)

    if scenarios_df.empty:
        st.markdown("""
        <div class="warning-card">
            <h3>No test data available</h3>
            <p>Use the command line interface to upload test results: <code>python script.py --file your_results.json</code></p>
        </div>
        """, unsafe_allow_html=True)
        return

    level_icon = {"scenario": "", "feature": "", "step": ""}[view_level]
    level_name = {"scenario": "Scenario", "feature": "Feature", "step": "Step"}[view_level]

    st.markdown(f"""
    <div class="level-selector">
        <strong>Currently viewing: {level_name} Level Analysis</strong><br>
        <small>Switch levels using the sidebar to see different perspectives of your test results.</small>
    </div>
    """, unsafe_allow_html=True)

    metrics = calculate_metrics_by_level(filtered_df, view_level, selected_feature)

    if view_level == "step" and (metrics['undefined_tests'] > 0 or metrics['pending_tests'] > 0):
        col1, col2, col3, col4, col5, col6 = st.columns(6)
    else:
        col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-number">{metrics['total_tests']}</div>
            <div class="metric-label">Total {metrics['stats_label']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-number status-passed">{metrics['passed_tests']}</div>
            <div class="metric-label">Passed</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-number status-failed">{metrics['failed_tests']}</div>
            <div class="metric-label">Failed</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-number status-skipped">{metrics['skipped_tests']}</div>
            <div class="metric-label">Skipped</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        success_color = "status-passed" if metrics['success_rate'] >= 80 else "status-failed"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-number {success_color}">{metrics['success_rate']}%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)

    if view_level == "step" and (metrics['undefined_tests'] > 0 or metrics['pending_tests'] > 0):
        with col6:
            other_steps = metrics['undefined_tests'] + metrics['pending_tests']
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-number status-skipped">{other_steps}</div>
                <div class="metric-label">Undefined/Pending</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    active_filters = []
    if 'selected_feature' in locals() and selected_feature != "All":
        active_filters.append(f'<span class="filter-badge">Feature: {selected_feature}</span>')
    if 'selected_status' in locals() and selected_status != "All":
        active_filters.append(f'<span class="filter-badge">Status: {selected_status}</span>')

    if active_filters:
        st.markdown('<h3 class="section-header">Active Filters</h3>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin: 16px 0;">{"".join(active_filters)}</div>', unsafe_allow_html=True)

    st.markdown(f'<h2 class="section-header">{level_name} Results Overview</h2>', unsafe_allow_html=True)

    display_df = get_level_specific_dataframe(filtered_df, view_level, selected_feature)

    if not display_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            if view_level == "step":
                pie_data = display_df[['status', 'count']].copy()
                pie_data.columns = ['Status', 'Count']
            else:
                status_counts = display_df["status"].value_counts().reset_index()
                status_counts.columns = ["Status", "Count"]
                pie_data = status_counts

            pie_chart = px.pie(
                pie_data,
                names="Status",
                values="Count",
                title=f"{level_name} Status Distribution",
                color="Status",
                color_discrete_map=STATUS_COLORS,
                hole=0.4
            )
            st.plotly_chart(pie_chart, use_container_width=True)

        with col2:
            if view_level == "feature":
                if 'success_rate' in display_df.columns and not display_df.empty:
                    feature_perf = display_df[['name', 'success_rate']].sort_values('success_rate', ascending=False)

                    bar_chart = px.bar(
                        feature_perf,
                        y='name',
                        x='success_rate',
                        orientation='h',
                        title='Success Rate by Feature',
                        color_discrete_sequence=[COLORS["primary"]]
                    )
                    bar_chart.update_layout(xaxis=dict(range=[0, 100]))
                    st.plotly_chart(bar_chart, use_container_width=True)
                else:
                    st.markdown("""
                    <div class="info-card">
                        <p>No feature performance data available</p>
                    </div>
                    """, unsafe_allow_html=True)

            elif view_level == "step":
                if 'percentage' in display_df.columns and not display_df.empty:
                    step_perf = display_df[['name', 'percentage']].sort_values('percentage', ascending=False)

                    bar_chart = px.bar(
                        step_perf,
                        y='name',
                        x='percentage',
                        orientation='h',
                        title='Step Distribution by Type (%)',
                        color_discrete_sequence=[COLORS["primary"]]
                    )
                    st.plotly_chart(bar_chart, use_container_width=True)
                else:
                    st.markdown("""
                    <div class="info-card">
                        <p>No step performance data available</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                if 'duration' in display_df.columns and not display_df.empty:
                    feature_perf = display_df.groupby('feature').agg({
                        'duration': 'mean'
                    }).reset_index()
                    feature_perf.columns = ['Feature', 'Avg_Duration']

                    bar_chart = px.bar(
                        feature_perf.sort_values('Avg_Duration', ascending=False),
                        y='Feature',
                        x='Avg_Duration',
                        orientation='h',
                        title='Average Duration by Feature',
                        color_discrete_sequence=[COLORS["primary"]]
                    )
                    st.plotly_chart(bar_chart, use_container_width=True)
                else:
                    st.markdown("""
                    <div class="info-card">
                        <p>No duration data available</p>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown(f'<h2 class="section-header">Detailed {level_name} Results</h2>', unsafe_allow_html=True)

        display_df_filtered = display_df

        if view_level == "feature":
            display_columns = ["name", "status", "total_scenarios", "passed_scenarios", "failed_scenarios",
                               "success_rate", "formatted_duration", "run_count", "last_run"]

            display_df_filtered["formatted_duration"] = display_df_filtered["duration"].apply(format_test_duration)

            if 'last_run' in display_df_filtered.columns:
                display_df_filtered["last_run"] = pd.to_datetime(display_df_filtered["last_run"]).dt.strftime('%Y-%m-%d %H:%M')

            available_columns = [col for col in display_columns if col in display_df_filtered.columns]
            display_final = display_df_filtered[available_columns].rename(columns={
                "name": "Feature",
                "status": "Status",
                "total_scenarios": "Total Scenarios",
                "passed_scenarios": "Passed",
                "failed_scenarios": "Failed",
                "success_rate": "Success Rate (%)",
                "formatted_duration": "Avg Duration",
                "run_count": "Total Runs",
                "last_run": "Last Run"
            })

        elif view_level == "step":
            display_final = display_df_filtered.rename(columns={
                "name": "Step Type",
                "status": "Status",
                "count": "Count",
                "percentage": "Percentage (%)"
            })

        else:
            display_df_filtered["formatted_duration"] = display_df_filtered["duration"].apply(format_test_duration)

            if 'updated_at' in display_df_filtered.columns:
                display_df_filtered["last_run"] = pd.to_datetime(display_df_filtered["updated_at"]).dt.strftime('%Y-%m-%d %H:%M')
            else:
                display_df_filtered["last_run"] = "Unknown"

            display_columns = ["feature", "name", "status", "formatted_duration", "run_count", "last_run", "tags"]
            available_columns = [col for col in display_columns if col in display_df_filtered.columns]
            display_final = display_df_filtered[available_columns].rename(columns={
                "feature": "Feature",
                "name": "Scenario",
                "status": "Status",
                "formatted_duration": "Duration",
                "run_count": "Runs",
                "last_run": "Last Run",
                "tags": "Tags"
            })

        if not display_final.empty:
            st.dataframe(display_final, use_container_width=True)
        else:
            st.markdown(f"""
            <div class="info-card">
                <p>No {level_name.lower()}s match your search criteria. Try a different search term.</p>
            </div>
            """, unsafe_allow_html=True)

        if view_level in ["scenario", "feature"]:
            failed_items = display_df_filtered[display_df_filtered["status"] == "failed"]
            if not failed_items.empty:
                failure_type = "features" if view_level == "feature" else "scenarios"
                with st.expander(f"Failure Details ({len(failed_items)} failed {failure_type})"):
                    for _, item in failed_items.iterrows():
                        if view_level == "feature":
                            st.markdown(f"**{item['name']}**")
                            st.markdown(f"*Failed Scenarios:* {item.get('failed_scenarios', 0)}")
                            st.markdown(f"*Success Rate:* {item.get('success_rate', 0)}%")
                        else:
                            st.markdown(f"**{item['feature']} - {item['name']}**")
                            if item.get('failed_step'):
                                st.markdown(f"*Failed Step:* {item['failed_step']}")
                            if item.get('error_msg'):
                                error_preview = item['error_msg'][:400] + "..." if len(item['error_msg']) > 400 else item['error_msg']
                                st.code(error_preview)
                        st.markdown("---")
    else:
        if view_level == "step":
            st.markdown("""
            <div class="info-card">
                <p>No step data available or no steps match your current filters.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-card">
                <p>No results match your current filters. Try adjusting your search criteria.</p>
            </div>
            """, unsafe_allow_html=True)

def main():
    setup_database()

    parser = argparse.ArgumentParser(description="Cucumber Test Results Dashboard")
    parser.add_argument("--file", type=str, help="Path to cucumber JSON report")
    parser.add_argument("--save-only", action="store_true", help="Save to database without showing UI")

    try:
        args = parser.parse_args()
    except:
        args = None

    if args and args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            scenarios_df, _, _ = parse_cucumber_json(json_data)
            run_id = store_test_results(scenarios_df)

            if args.save_only:
                return

        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return

    build_dashboard()

if __name__ == "__main__":
    main()