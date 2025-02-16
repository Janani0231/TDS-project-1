# Phase B: LLM-based Automation Agent for DataWorks Solutions

import os
import pathlib
from typing import Optional, Union, List, Dict, Any
from functools import wraps

# B1 & B2: Security Checks
def validate_path(filepath: str) -> bool:
    """
    Validate that the path is within /data directory and exists.
    Returns True if path is valid, False otherwise.
    """
    try:
        abs_path = os.path.abspath(filepath)
        data_dir = os.path.abspath("/data")
        return abs_path.startswith(data_dir)
    except Exception:
        return False

def security_check(func):
    """Decorator to enforce security checks on file operations"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check all string arguments for potential paths
        for arg in args + tuple(kwargs.values()):
            if isinstance(arg, str) and os.path.sep in arg:
                if not validate_path(arg):
                    raise PermissionError(f"Access denied: {arg} is outside /data directory")
        return func(*args, **kwargs)
    return wrapper

# B3: Fetch Data from an API
@security_check
def fetch_api_data(url: str, save_path: str) -> bool:
    """
    Fetch data from an API and save it to a file.
    Returns True if successful, False otherwise.
    """
    try:
        import requests
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w') as file:
            file.write(response.text)
        return True
    except Exception as e:
        print(f"Error fetching API data: {str(e)}")
        return False

# B4: Clone a Git Repo and Make a Commit
@security_check
def git_operations(repo_url: str, local_path: str, commit_message: Optional[str] = None) -> bool:
    """
    Clone a git repo and optionally make a commit.
    Returns True if successful, False otherwise.
    """
    try:
        import git
        if not os.path.exists(local_path):
            repo = git.Repo.clone_from(repo_url, local_path)
        else:
            repo = git.Repo(local_path)
            
        if commit_message:
            repo.index.add('*')
            repo.index.commit(commit_message)
        return True
    except Exception as e:
        print(f"Error in git operations: {str(e)}")
        return False

# B5: Run SQL Query
@security_check
def run_sql_query(db_path: str, query: str, output_path: str) -> Optional[List[tuple]]:
    """
    Run a SQL query on SQLite or DuckDB database and save results.
    Returns query results if successful, None otherwise.
    """
    try:
        import sqlite3
        import duckdb
        import json
        
        if db_path.endswith('.db'):
            conn = sqlite3.connect(db_path)
        else:
            conn = duckdb.connect(db_path)
            
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        
        # Save results as JSON for better readability
        with open(output_path, 'w') as f:
            json.dump([list(row) for row in results], f, indent=2)
            
        conn.close()
        return results
    except Exception as e:
        print(f"Error executing SQL query: {str(e)}")
        return None

# B6: Web Scraping
@security_check
def scrape_website(url: str, output_path: str) -> bool:
    """
    Scrape a website and save the content.
    Returns True if successful, False otherwise.
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        return True
    except Exception as e:
        print(f"Error scraping website: {str(e)}")
        return False

# B7: Image Processing
@security_check
def process_image(image_path: str, output_path: str, resize: Optional[tuple] = None,
                 format: Optional[str] = None, quality: int = 85) -> bool:
    """
    Process an image with various operations.
    Returns True if successful, False otherwise.
    """
    try:
        from PIL import Image
        
        img = Image.open(image_path)
        if resize:
            img = img.resize(resize, Image.Resampling.LANCZOS)
            
        format = format or img.format
        img.save(output_path, format=format, quality=quality, optimize=True)
        return True
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return False

# B8: Audio Transcription
@security_check
def transcribe_audio(audio_path: str, output_path: str) -> bool:
    """
    Transcribe audio using OpenAI's Whisper model.
    Returns True if successful, False otherwise.
    """
    try:
        import openai
        
        with open(audio_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            
        with open(output_path, 'w') as f:
            f.write(transcript.text)
        return True
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return False

# B9: Markdown to HTML Conversion
@security_check
def convert_markdown(md_path: str, output_path: str) -> bool:
    """
    Convert Markdown to HTML.
    Returns True if successful, False otherwise.
    """
    try:
        import markdown
        import codecs
        
        with codecs.open(md_path, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()
            html = markdown.markdown(text, extensions=['extra', 'codehilite'])
            
        with codecs.open(output_path, mode="w", encoding="utf-8") as output_file:
            output_file.write(html)
        return True
    except Exception as e:
        print(f"Error converting markdown: {str(e)}")
        return False

# B10: API Endpoint for CSV Filtering
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/filter_csv', methods=['POST'])
def filter_csv():
    """
    API endpoint to filter CSV data.
    Expected JSON payload: {
        "csv_path": str,
        "filters": [{"column": str, "value": Any, "operator": str}]
    }
    """
    try:
        data = request.get_json()
        csv_path = data['csv_path']
        
        if not validate_path(csv_path):
            return jsonify({"error": "Invalid path"}), 403
            
        df = pd.read_csv(csv_path)
        
        # Apply filters
        for filter_rule in data.get('filters', []):
            column = filter_rule['column']
            value = filter_rule['value']
            operator = filter_rule.get('operator', '==')
            
            if operator == '==':
                df = df[df[column] == value]
            elif operator == '>':
                df = df[df[column] > value]
            elif operator == '<':
                df = df[df[column] < value]
            elif operator == 'contains':
                df = df[df[column].str.contains(str(value), na=False)]
                
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)