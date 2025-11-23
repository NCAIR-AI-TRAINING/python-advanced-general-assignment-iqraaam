from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            pass

def get_last_visitor():
    if not os.path.exists(FILENAME):
        return None, None
    
    with open(FILENAME, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return None, None
    
    last_line = lines[-1].strip()
    
    if not last_line:
        return None, None
    
    parts = last_line.split(" | ")
    
    if len(parts) == 2:
        name = parts[0]
        timestamp_str = parts[1]
        timestamp = datetime.fromisoformat(timestamp_str)
        return name, timestamp
    
    return None, None

def add_visitor(visitor_name):
    last_visitor_name, last_visitor_time = get_last_visitor()
    current_time = datetime.now()
    
    if last_visitor_name == visitor_name:
        raise DuplicateVisitorError(f"{visitor_name} cannot visit twice in a row")
    
    if last_visitor_time is not None:
        time_difference = current_time - last_visitor_time
        minutes_passed = time_difference.total_seconds() / 60
        
        if minutes_passed < 5:
            raise EarlyEntryError(f"Must wait {5 - minutes_passed:.1f} more minutes")
    
    timestamp_str = current_time.isoformat()
    
    with open(FILENAME, 'a') as f:
        f.write(f"{visitor_name} | {timestamp_str}\n")

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