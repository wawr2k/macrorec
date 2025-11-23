#!/usr/bin/env python3
"""
Script to add AutoFishMultiSpotTask to config.py's onetime_tasks list
if it doesn't already exist.
"""

import os
import sys

CONFIG_FILE = "src/config.py"
TASK_ENTRY = '        ["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],'

def find_okdna_working_dir():
    """Try to find the ok-dna working directory"""
    # Method 1: Check if script is in the working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, CONFIG_FILE)
    if os.path.exists(config_path):
        return script_dir
    
    # Method 2: Search common ok-dna installation locations
    common_paths = [
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "ok-dna", "data", "apps", "ok-dna", "working"),
        os.path.join("C:", "ok-dna", "working"),
        os.path.join("D:", "ok-dna", "working"),
        os.path.join("E:", "ok-dna", "working"),
    ]
    
    for path in common_paths:
        config_path = os.path.join(path, CONFIG_FILE)
        if os.path.exists(config_path):
            return path
    
    # Method 3: Search parent directories up to 5 levels
    current = script_dir
    for _ in range(5):
        config_path = os.path.join(current, CONFIG_FILE)
        if os.path.exists(config_path):
            return current
        parent = os.path.dirname(current)
        if parent == current:  # Reached root
            break
        current = parent
    
    return None

def main():
    # Try to find ok-dna working directory
    working_dir = find_okdna_working_dir()
    
    if working_dir is None:
        print("Error: Could not find ok-dna installation!")
        print("Please make sure:")
        print("  1. ok-dna is installed")
        print("  2. This script is in the ok-dna working directory, OR")
        print("  3. ok-dna is in a standard location (AppData\\Local\\ok-dna\\...)")
        print(f"\nSearched for: {CONFIG_FILE}")
        return 1
    
    config_path = os.path.join(working_dir, CONFIG_FILE)
    print(f"Found ok-dna at: {working_dir}")
    
    # Read the file
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {config_path}: {e}")
        return 1
    
    # Check if entry already exists
    if 'AutoFishMultiSpotTask' in content:
        print("AutoFishMultiSpotTask entry already exists in config.py")
        return 0
    
    # Parse line by line to find onetime_tasks section
    lines = content.split('\n')
    new_lines = []
    in_onetime_tasks = False
    inserted = False
    bracket_count = 0
    
    for i, line in enumerate(lines):
        # Check if we're entering the onetime_tasks section
        if "'onetime_tasks'" in line and '[' in line:
            in_onetime_tasks = True
            bracket_count = line.count('[') - line.count(']')
            new_lines.append(line)
            continue
        
        # If we're in the onetime_tasks section
        if in_onetime_tasks:
            bracket_count += line.count('[') - line.count(']')
            new_lines.append(line)
            
            # Check if we should insert after this line
            # Insert after AutoFishTask line (but not if it's AutoFishMultiSpotTask)
            if 'AutoFishTask' in line and 'AutoFishMultiSpotTask' not in line and not inserted:
                new_lines.append(TASK_ENTRY)
                inserted = True
            
            # Check if we've closed the list
            if bracket_count <= 0 and '],' in line:
                # If we haven't inserted yet, add before the closing bracket
                if not inserted:
                    # Remove the last line (closing bracket), add our entry, then add closing back
                    closing_line = new_lines.pop()
                    new_lines.append(TASK_ENTRY)
                    new_lines.append(closing_line)
                    inserted = True
                in_onetime_tasks = False
        else:
            new_lines.append(line)
    
    if not inserted and not in_onetime_tasks:
        print("Error: Could not find 'onetime_tasks' section in config.py")
        return 1
    
    new_full_content = '\n'.join(new_lines)
    
    # Write back
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(new_full_content)
        print(f"Successfully added AutoFishMultiSpotTask to {config_path}")
        return 0
    except Exception as e:
        print(f"Error writing {config_path}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

