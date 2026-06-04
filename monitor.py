import requests
from bs4 import BeautifulSoup
import os

def fetch_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def save_content(content, filename="last_content.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def load_previous_content(filename="last_content.txt"):
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def get_changes(previous, current):
    previous_lines = set(previous.splitlines())
    current_lines = set(current.splitlines())
    
    added = current_lines - previous_lines
    removed = previous_lines - current_lines
    
    return added, removed

def check_for_changes(url):
    print(f"Checking {url}...")
    
    current = fetch_website(url)
    previous = load_previous_content()
    
    if previous is None:
        print("First time checking — saving content.")
        save_content(current)
        return
    
    if current != previous:
        print("CHANGE DETECTED!")
        added, removed = get_changes(previous, current)
        
        print(f"\n--- NEW CONTENT ---")
        for line in list(added)[:5]:
            if line.strip():
                print(f"+ {line.strip()}")
        
        print(f"\n--- REMOVED CONTENT ---")
        for line in list(removed)[:5]:
            if line.strip():
                print(f"- {line.strip()}")
        
        save_content(current)
    else:
        print("No changes found.")

url = "https://news.ycombinator.com/newest"
check_for_changes(url)