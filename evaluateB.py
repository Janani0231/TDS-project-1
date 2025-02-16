import os
import json
import requests
from pathlib import Path
from tasksB import *

def setup_test_data():
    """Create test data directory and files if they don't exist"""
    os.makedirs("data", exist_ok=True)
    
    # Test data for B3 (API)
    with open("data/api_data.json", "w") as f:
        json.dump({"test": "data"}, f)
    
    # Test data for B5 (SQL)
    import sqlite3
    conn = sqlite3.connect("data/database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS test_table
                 (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)''')
    conn.commit()
    conn.close()
    
    # Test data for B7 (Image)
    from PIL import Image
    img = Image.new('RGB', (100, 100), color='red')
    img.save("data/input.jpg")
    
    # Test data for B9 (Markdown)
    with open("data/input.md", "w") as f:
        f.write("# Test Heading\nThis is a test markdown file.")
    
    # Test data for B10 (CSV)
    import pandas as pd
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35]
    })
    df.to_csv("data/test.csv", index=False)

def evaluate_B3():
    """Test API data fetching"""
    try:
        result = B3("https://jsonplaceholder.typicode.com/todos/1")
        return "success" in result.get("status", "")
    except Exception as e:
        print(f"B3 error: {str(e)}")
        return False

def evaluate_B4():
    """Test Git operations"""
    try:
        result = B4("https://github.com/octocat/Hello-World.git")
        return "success" in result.get("status", "")
    except Exception as e:
        print(f"B4 error: {str(e)}")
        return False

def evaluate_B5():
    """Test SQL query execution"""
    try:
        result = B5("SELECT * FROM test_table")
        return "success" in result.get("status", "")
    except Exception as e:
        print(f"B5 error: {str(e)}")
        return False

def evaluate_B6():
    """Test web scraping"""
    try:
        result = B6("https://example.com")
        return "success" in result.get("status", "")
    except Exception as e:
        print(f"B6 error: {str(e)}")
        return False

def evaluate_B7():
    """Test image processing"""
    try:
        result = B7("data/input.jpg", "data/output.jpg")
        return "success" in result.get("status", "")
    except Exception as e:
        print(f"B7 error: {str(e)}")
        return False

def evaluate_B8():
    """Test audio transcription"""
    try:
        # Since this is a placeholder, we'll check if it raises NotImplementedError
        try:
            B8()
            return False
        except NotImplementedError:
            return True
    except Exception as e:
        print(f"B8 error: {str(e)}")
        return False

def evaluate_B9():
    """Test Markdown to HTML conversion"""
    try:
        result = B9("data/input.md", "data/output.html")
        return "success" in result.get("status", "")
    except Exception as e:
        print(f"B9 error: {str(e)}")
        return False

def evaluate_B10():
    """Test CSV filtering API"""
    try:
        app = B10()
        # Test if app is a FastAPI instance
        return hasattr(app, 'router')
    except Exception as e:
        print(f"B10 error: {str(e)}")
        return False

def main():
    print("Setting up test data...")
    setup_test_data()
    
    print("\nEvaluating Phase B tasks...")
    scores = {
        "B3": evaluate_B3(),
        "B4": evaluate_B4(),
        "B5": evaluate_B5(),
        "B6": evaluate_B6(),
        "B7": evaluate_B7(),
        "B8": evaluate_B8(),
        "B9": evaluate_B9(),
        "B10": evaluate_B10()
    }
    
    # Calculate total score
    total_score = sum(1 for score in scores.values() if score)
    
    print("\nResults:")
    for task, passed in scores.items():
        print(f"{task}: {'✅ PASSED' if passed else '❌ FAILED'}")
    
    print(f"\nTotal Score: {total_score}/8")

if __name__ == "__main__":
    main() 