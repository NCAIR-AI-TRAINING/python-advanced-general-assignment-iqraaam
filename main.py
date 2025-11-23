from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    """
    Creates the visitors.txt file if it doesn't exist.
    """
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            pass  

def get_last_visitor():
    """
    Reads the last visitor from the file.
    Returns the visitor's name or None if file is empty.
    """
    if not os.path.exists(FILENAME):
        return None
    
    with open(FILENAME, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return None
    
    last_line = lines[-1].strip()
    
    parts = last_line.split(" | ")
    if parts:
        return parts[0]  
    
    return None

def add_visitor(visitor_name):
    """
    Adds a visitor to the file.
    
    RULE 1 ONLY: Raises DuplicateVisitorError if same as last visitor.
    """
    last_visitor = get_last_visitor()
    
    if last_visitor == visitor_name:
        raise DuplicateVisitorError(f"{visitor_name} cannot visit twice in a row")
    
    current_time = datetime.now().isoformat()
    
    with open(FILENAME, 'a') as f:
        f.write(f"{visitor_name} | {current_time}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
