import json
import pandas as pd
import argparse
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
from collections import Counter
import os
import uuid

def parse_cucumber_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading cucumber json file: {str(e)}")
        return None

def extract_failure_data(cucumber_data):
    records = []

    for feature in cucumber_data:
        feature_name = feature.get('name', '')

        for element in feature.get('elements', []):
            if element.get('type') != 'scenario':
                continue

            scenario_name = element.get('name', '')
            tags = ' '.join([t['name'] for t in element.get('tags', [])]) if 'tags' in element else ''

            for step in element.get('steps', []):
                step_name = step.get('name', '')
                step_keyword = step.get('keyword', '').strip()
                result = step.get('result', {})
                status = result.get('status', '')
                error_message = result.get('error_message', '') if status == 'failed' else ''

                records.append({
                    'feature': feature_name,
                    'scenario': scenario_name,
                    'tags': tags,
                    'step': f"{step_keyword} {step_name}",
                    'status': status,
                    'error_message': error_message
                })

    return pd.DataFrame(records)

def clean_error_message(error):
    if not isinstance(error, str):
        return ""

    cleaned = re.sub(r'at [\w\.$]+\([^)]*\)', '', error)
    cleaned = re.sub(r'at .+\.java:\d+', '', cleaned)
    cleaned = re.sub(r'at .+\.js:\d+', '', cleaned)
    cleaned = re.sub(r'at .+\.py:\d+', '', cleaned)
    cleaned = re.sub(r'[\\/]?[\w\\/\.-]+:\d+', '', cleaned)
    cleaned = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', '', cleaned)

    cleaned = re.sub(r'[^\w\s\.\,\!\?]', ' ', cleaned)

    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned

def extract_error_type(error):
    if not isinstance(error, str):
        return "Unknown"

    patterns = {
        'Assertion Error': [r'assert', r'expected .* but .*', r'assertion'],
        'Element Not Found': [r'no such element', r'element not found', r'could not find', r'element .* not .*visible'],
        'Timeout Error': [r'timeout', r'timed out', r'wait.*expired'],
        'Connection Error': [r'connection refused', r'connection reset', r'network error'],
        'Null Pointer': [r'null pointer', r'NullPointerException', r'undefined is not an object'],
        'Syntax Error': [r'syntax error', r'SyntaxError', r'parsing error'],
        'Permission Error': [r'permission denied', r'not authorized', r'access denied'],
        'Data Error': [r'invalid data', r'data.*not match', r'unexpected value']
    }

    for error_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, error.lower()):
                return error_type

    return "Other"

def analyze_results(json_path, output_dir='reports'):
    with open(json_path, 'r') as f:
        cucumber_data = json.load(f)

    df = extract_failure_data(cucumber_data)

    if df.empty:
        print("No test data found.")
        return

    os.makedirs(output_dir, exist_ok=True)
    run_id = str(uuid.uuid4())
    csv_output_path = os.path.join(output_dir, f"test_results_{run_id}.csv")
    df.to_csv(csv_output_path, index=False)

    scenario_summary = df.groupby(['feature', 'scenario'])['status'].apply(
        lambda x: 'failed' if 'failed' in x.values else 'skipped' if all(s == 'skipped' for s in x.values) else 'passed'
    ).reset_index(name='scenario_status')

    total = scenario_summary.shape[0]
    failed = (scenario_summary['scenario_status'] == 'failed').sum()
    skipped = (scenario_summary['scenario_status'] == 'skipped').sum()
    passed = total - failed - skipped

    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    print(f"Run ID: {run_id}")
    print(f"Total Scenarios: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print("="*60)

    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, y='status', order=df['status'].value_counts().index)
    plt.title('Step Status Distribution (Failed / Skipped / Passed)')
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "step_status_distribution.png")
    plt.savefig(plot_path)
    print(f"Saved step status distribution to {plot_path}")

    return run_id, scenario_summary, df, plot_path

def analyze_failures(failures_df):
    if failures_df.empty:
        print("No failures to analyze")
        return

    print("\n" + "=" * 50)
    print("ML-Based Failure Analysis")
    print("=" * 50)

    failures_df['cleaned_error'] = failures_df['error_message'].apply(clean_error_message)

    failures_df['error_type'] = failures_df['error_message'].apply(extract_error_type)

    error_counts = failures_df['error_type'].value_counts()
    print("\nError Type Distribution:")
    for error_type, count in error_counts.items():
        print(f"{error_type}: {count} ({count/len(failures_df)*100:.1f}%)")

    feature_counts = failures_df['feature'].value_counts()
    most_failing_feature = feature_counts.index[0]
    print(f"\nMost Failing Feature: {most_failing_feature} with {feature_counts[0]} failures")

    if 'tags' in failures_df.columns and not failures_df['tags'].isna().all():
        all_tags = ' '.join(failures_df['tags'].fillna('').tolist())
        tag_counts = Counter([tag for tag in all_tags.split() if tag.startswith('@')])
        if tag_counts:
            print("\nMost Common Tags in Failing Tests:")
            for tag, count in tag_counts.most_common(5):
                print(f"{tag}: {count}")

    if len(failures_df) >= 5:
        try:
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            X = vectorizer.fit_transform(failures_df['cleaned_error'].fillna(''))

            max_clusters = min(5, len(failures_df)-1)
            if max_clusters >= 2:
                kmeans = KMeans(n_clusters=max_clusters, random_state=42)
                failures_df['cluster'] = kmeans.fit_predict(X)

                print("\nError Clusters (Similar Failures):")
                feature_names = vectorizer.get_feature_names_out()
                for i in range(max_clusters):
                    if sum(failures_df['cluster'] == i) > 0:
                        # Get cluster center and top terms
                        centroid = kmeans.cluster_centers_[i]
                        top_indices = centroid.argsort()[-5:][::-1]
                        top_terms = [feature_names[j] for j in top_indices]

                        print(f"Cluster {i+1} ({sum(failures_df['cluster'] == i)} failures): {', '.join(top_terms)}")
        except Exception as e:
            print(f"Clustering analysis error: {str(e)}")

    output_file = "failure_analysis.csv"
    failures_df.to_csv(output_file, index=False)
    print(f"\nDetailed failure analysis saved to {output_file}")

    try:
        plt.figure(figsize=(10, 6))
        sns.countplot(y='error_type', data=failures_df, order=failures_df['error_type'].value_counts().index)
        plt.title('Distribution of Error Types')
        plt.tight_layout()
        plt.savefig('error_types.png')
        print("Saved error type distribution to error_types.png")

        plt.figure(figsize=(12, 8))
        sns.countplot(y='feature', data=failures_df, order=failures_df['feature'].value_counts().index[:10])
        plt.title('Top 10 Failing Features')
        plt.tight_layout()
        plt.savefig('failing_features.png')
        print("Saved feature failure distribution to failing_features.png")

        if not failures_df['cleaned_error'].isna().all():
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(failures_df['cleaned_error'].fillna('')))
            plt.figure(figsize=(10, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout()
            plt.savefig('error_wordcloud.png')
            print("Saved error word cloud to error_wordcloud.png")

        if 'cluster' in failures_df.columns and len(failures_df) >= 5:
            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X.toarray())

            plt.figure(figsize=(10, 8))
            sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=failures_df['cluster'], palette='viridis')
            plt.title('Error Message Clusters')
            plt.xlabel('PCA Component 1')
            plt.ylabel('PCA Component 2')
            plt.tight_layout()
            plt.savefig('error_clusters.png')
            print("Saved error clusters visualization to error_clusters.png")
    except Exception as e:
        print(f"Error generating visualizations: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analyze cucumber failure data')
    parser.add_argument('--file', required=True, help='Path to the cucumber JSON file')
    args = parser.parse_args()

    data = parse_cucumber_json(args.file)
    if data is None:
        return

    df = extract_failure_data(data)

    analyze_failures(df)

if __name__ == '__main__':
    main()
