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
    Returns a tuple: (name, timestamp) or (None, None) if file is empty.
    """
    
    if not os.path.exists(FILENAME):
        return None, None
    
    with open(FILENAME, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return None, None
    
    last_line = lines[-1].strip()
    
    parts = last_line.split(" | ")
    if len(parts) == 2:
        name = parts[0]
        timestamp_str = parts[1]
       
        timestamp = datetime.fromisoformat(timestamp_str)
        return name, timestamp
    
    return None, None

def add_visitor(visitor_name):
    """
    Adds a visitor to the file.
    
    RULE 1: Raises DuplicateVisitorError if same as last visitor.
    RULE 2: Raises EarlyEntryError if less than 5 minutes since last visitor.
    """
    last_visitor_name, last_visitor_time = get_last_visitor()
    
    if last_visitor_name == visitor_name:
        raise DuplicateVisitorError(f"{visitor_name} cannot visit twice in a row")
    
    # ===== RULE 2: Check 5-minute wait time =====
    if last_visitor_time is not None:
       
        current_time = datetime.now()
        time_difference = current_time - last_visitor_time
        
        minutes_passed = time_difference.total_seconds() / 60
        
        if minutes_passed < 5:
            raise EarlyEntryError(f"Must wait {5 - minutes_passed:.1f} more minutes")
    
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
