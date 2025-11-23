#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to install Choaga's mod tasks:
- Copies Python files to correct folders
- Copies mod/fish/ folder with all PNG images
- Copies assets/ folder (with automatic backup if it exists)
- Adds AutoFishMultiSpotTask to config.py's onetime_tasks list
- Adds SkillSpeedTask to config.py's trigger_tasks list
"""

import os
import sys
import shutil
from pathlib import Path

# Check if this file has been corrupted with HTML (from GitHub web view)
def check_file_corruption():
    """Check if the script file itself has been corrupted with HTML"""
    script_path = os.path.abspath(__file__)
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            first_lines = ''.join([f.readline() for _ in range(5)])
            if '<title>' in first_lines or '<html' in first_lines.lower() or '·' in first_lines:
                print("=" * 70)
                print("ERROR: This Python file appears to be corrupted with HTML content!")
                print("=" * 70)
                print("\nThis usually happens when:")
                print("  1. You copied the file content from GitHub's web page")
                print("  2. You downloaded the file incorrectly")
                print("\nSOLUTION:")
                print("  1. Download the ZIP file from GitHub:")
                print("     https://github.com/wawr2k/macrorec/archive/refs/heads/main.zip")
                print("  2. Extract the ZIP file")
                print("  3. Run add_autofish_to_config.bat from the extracted folder")
                print("\nOR download the RAW file directly:")
                print("  https://raw.githubusercontent.com/wawr2k/macrorec/main/add_autofish_to_config.py")
                print("  (Right-click the link above and 'Save As...')")
                print("=" * 70)
                return True
    except Exception:
        pass
    return False

if check_file_corruption():
    sys.exit(1)

CONFIG_FILE = "src/config.py"
ONETIME_TASK_ENTRY = '        ["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],'
TRIGGER_TASK_ENTRY = '        ["src.tasks.trigger.SkillSpeedTask", "SkillSpeedTask"],'

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

def find_file_in_package(script_dir, relative_path, show_debug=False):
    """Find a file in the extracted package, checking multiple possible locations"""
    # Normalize the relative path
    path_parts = relative_path.replace('\\', '/').split('/')
    
    # Try multiple search strategies
    search_paths = [
        # Strategy 1: Same directory as script (extracted package root)
        os.path.join(script_dir, *path_parts),
        # Strategy 2: Parent of script directory (if script is in a subfolder)
        os.path.join(os.path.dirname(script_dir), *path_parts),
        # Strategy 3: Two levels up (if script is in backup/Choaga/)
        os.path.join(os.path.dirname(os.path.dirname(script_dir)), *path_parts),
        # Strategy 4: Three levels up (if script is in mod/backup/Choaga/)
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))), *path_parts),
    ]
    
    # Also try searching from script_dir up to 5 levels
    current = script_dir
    for _ in range(5):
        search_paths.append(os.path.join(current, *path_parts))
        parent = os.path.dirname(current)
        if parent == current:  # Reached root
            break
        current = parent
    
    # Remove duplicates while preserving order
    seen = set()
    unique_paths = []
    for path in search_paths:
        abs_path = os.path.abspath(path)
        if abs_path not in seen:
            seen.add(abs_path)
            unique_paths.append(abs_path)
    
    if show_debug:
        print(f"    Searching for: {relative_path}")
        print(f"    Tried {len(unique_paths)} locations...")
    
    for search_path in unique_paths:
        if os.path.exists(search_path) and os.path.isfile(search_path):
            if show_debug:
                print(f"    ✓ Found at: {search_path}")
            return search_path
    
    if show_debug:
        print(f"    ✗ Not found. First few search locations:")
        for i, path in enumerate(unique_paths[:3]):
            print(f"      {i+1}. {path}")
    
    return None

def copy_python_files(working_dir, script_dir):
    """Copy Python task files to correct folders"""
    print("\n[1/5] Copying Python task files...")
    print(f"  Searching for files from: {script_dir}")
    
    errors = []
    
    # AutoFishMultiSpotTask.py
    print("  Looking for AutoFishMultiSpotTask.py...")
    autofish_source = find_file_in_package(script_dir, "src/tasks/fullauto/AutoFishMultiSpotTask.py", show_debug=True)
    autofish_dest = os.path.join(working_dir, "src", "tasks", "fullauto", "AutoFishMultiSpotTask.py")
    autofish_dest_abs = os.path.abspath(autofish_dest)
    
    if autofish_source and autofish_source != autofish_dest_abs:
        dest_dir = os.path.dirname(autofish_dest)
        os.makedirs(dest_dir, exist_ok=True)
        try:
            shutil.copy2(autofish_source, autofish_dest)
            print(f"  ✓ Copied AutoFishMultiSpotTask.py to {dest_dir}")
        except Exception as e:
            errors.append(f"Failed to copy AutoFishMultiSpotTask.py: {e}")
            print(f"  ✗ ERROR: Failed to copy AutoFishMultiSpotTask.py: {e}")
    elif os.path.exists(autofish_dest):
        print(f"  ✓ AutoFishMultiSpotTask.py already exists in {os.path.dirname(autofish_dest)}")
    else:
        errors.append("AutoFishMultiSpotTask.py not found in package")
        print(f"  ✗ ERROR: AutoFishMultiSpotTask.py not found in extracted package")
        print(f"     Make sure you extracted the zip file and run the script from the extracted folder.")
        print(f"     Expected location: [extracted folder]/src/tasks/fullauto/AutoFishMultiSpotTask.py")
    
    # SkillSpeedTask.py
    print("  Looking for SkillSpeedTask.py...")
    skillspeed_source = find_file_in_package(script_dir, "src/tasks/trigger/SkillSpeedTask.py", show_debug=True)
    skillspeed_dest = os.path.join(working_dir, "src", "tasks", "trigger", "SkillSpeedTask.py")
    skillspeed_dest_abs = os.path.abspath(skillspeed_dest)
    
    if skillspeed_source and skillspeed_source != skillspeed_dest_abs:
        dest_dir = os.path.dirname(skillspeed_dest)
        os.makedirs(dest_dir, exist_ok=True)
        try:
            shutil.copy2(skillspeed_source, skillspeed_dest)
            print(f"  ✓ Copied SkillSpeedTask.py to {dest_dir}")
        except Exception as e:
            errors.append(f"Failed to copy SkillSpeedTask.py: {e}")
            print(f"  ✗ ERROR: Failed to copy SkillSpeedTask.py: {e}")
    elif os.path.exists(skillspeed_dest):
        print(f"  ✓ SkillSpeedTask.py already exists in {os.path.dirname(skillspeed_dest)}")
    else:
        errors.append("SkillSpeedTask.py not found in package")
        print(f"  ✗ ERROR: SkillSpeedTask.py not found in extracted package")
        print(f"     Make sure you extracted the zip file and run the script from the extracted folder.")
        print(f"     Expected location: [extracted folder]/src/tasks/trigger/SkillSpeedTask.py")
    
    if errors:
        print(f"\n  ⚠ WARNING: Some files could not be copied. Please check the errors above.")
        return False
    return True

def copy_mod_fish_folder(working_dir, script_dir):
    """Copy mod/fish/ folder with all PNG images"""
    print("\n[2/5] Copying mod/fish/ folder...")
    
    # Find mod/fish source - check multiple possible locations
    mod_fish_sources = [
        # Extracted package structure
        os.path.join(script_dir, "mod", "fish"),
        # Parent directory (if script is in backup folder)
        os.path.join(os.path.dirname(script_dir), "..", "..", "mod", "fish"),
        # Working directory (already installed)
        os.path.join(working_dir, "mod", "fish"),
    ]
    
    mod_fish_source = None
    for source in mod_fish_sources:
        abs_source = os.path.abspath(source)
        if os.path.exists(abs_source) and os.path.isdir(abs_source):
            # Check if it has PNG files
            png_files = [f for f in os.listdir(abs_source) if f.lower().endswith('.png')]
            if png_files:
                mod_fish_source = abs_source
                break
    
    mod_fish_dest = os.path.join(working_dir, "mod", "fish")
    mod_fish_dest_abs = os.path.abspath(mod_fish_dest)
    
    if mod_fish_source and mod_fish_source != mod_fish_dest_abs:
        # Create destination directory
        os.makedirs(mod_fish_dest, exist_ok=True)
        
        # Copy all PNG files
        png_files = [f for f in os.listdir(mod_fish_source) if f.lower().endswith('.png')]
        copied_count = 0
        for png_file in png_files:
            src_file = os.path.join(mod_fish_source, png_file)
            dest_file = os.path.join(mod_fish_dest, png_file)
            shutil.copy2(src_file, dest_file)
            copied_count += 1
        
        print(f"  ✓ Copied {copied_count} PNG files to mod/fish/")
    elif os.path.exists(mod_fish_dest):
        png_count = len([f for f in os.listdir(mod_fish_dest) if f.lower().endswith('.png')])
        print(f"  ✓ mod/fish/ folder already exists with {png_count} PNG files")
    else:
        print(f"  ⚠ WARNING: mod/fish/ folder not found")
        print(f"     Please manually copy mod/fish/ folder to [working folder]/mod/fish/")

def copy_assets_folder(working_dir, script_dir):
    """Copy assets/ folder with backup if it already exists"""
    print("\n[3/5] Copying assets/ folder...")
    
    # Find assets source - check multiple possible locations
    assets_sources = [
        # Extracted package structure
        os.path.join(script_dir, "assets"),
        # Parent directory (if script is in backup folder)
        os.path.join(os.path.dirname(script_dir), "..", "..", "assets"),
        # Working directory (already installed)
        os.path.join(working_dir, "assets"),
    ]
    
    assets_source = None
    for source in assets_sources:
        abs_source = os.path.abspath(source)
        if os.path.exists(abs_source) and os.path.isdir(abs_source):
            # Check if it has result.json or images folder
            if os.path.exists(os.path.join(abs_source, "result.json")) or os.path.exists(os.path.join(abs_source, "images")):
                assets_source = abs_source
                break
    
    assets_dest = os.path.join(working_dir, "assets")
    assets_dest_abs = os.path.abspath(assets_dest)
    assets_backup = os.path.join(working_dir, "assets - original")
    
    # If destination exists and is different from source, backup it first
    if os.path.exists(assets_dest_abs) and (not assets_source or os.path.abspath(assets_source) != assets_dest_abs):
        if not os.path.exists(assets_backup):
            print(f"  ℹ Backing up existing assets/ folder to assets - original/...")
            shutil.copytree(assets_dest_abs, assets_backup)
            print(f"  ✓ Backup created at: assets - original/")
        else:
            print(f"  ℹ Backup folder assets - original/ already exists, skipping backup")
    
    if assets_source and os.path.abspath(assets_source) != assets_dest_abs:
        # Create destination directory
        os.makedirs(assets_dest, exist_ok=True)
        
        # Copy result.json if it exists
        result_json_src = os.path.join(assets_source, "result.json")
        if os.path.exists(result_json_src):
            shutil.copy2(result_json_src, os.path.join(assets_dest, "result.json"))
            print(f"  ✓ Copied assets/result.json")
        
        # Copy images folder if it exists
        images_src = os.path.join(assets_source, "images")
        if os.path.exists(images_src) and os.path.isdir(images_src):
            images_dest = os.path.join(assets_dest, "images")
            if os.path.exists(images_dest):
                shutil.rmtree(images_dest)
            shutil.copytree(images_src, images_dest)
            png_count = len([f for f in os.listdir(images_dest) if f.lower().endswith('.png')])
            print(f"  ✓ Copied assets/images/ folder ({png_count} PNG files)")
    elif os.path.exists(assets_dest):
        print(f"  ✓ assets/ folder already exists")
    else:
        print(f"  ⚠ WARNING: assets/ folder not found (optional)")
        print(f"     If assets were included in the package, manually copy assets/ folder to [working folder]/assets/")

def add_task_to_config(working_dir, task_entry, list_name, task_name):
    """Add a task entry to config.py"""
    config_path = os.path.join(working_dir, CONFIG_FILE)
    
    # Read the file
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {config_path}: {e}")
        return False
    
    # Check if entry already exists
    if task_name in content:
        print(f"{task_name} entry already exists in config.py")
        return True
    
    # Find the appropriate list section
    list_pattern = f"'{list_name}'"
    lines = content.split('\n')
    new_lines = []
    in_list = False
    inserted = False
    bracket_count = 0
    
    for line in lines:
        # Check if we're entering the target list section
        if list_pattern in line and '[' in line:
            in_list = True
            bracket_count = line.count('[') - line.count(']')
            new_lines.append(line)
            continue
        
        # If we're in the target list section
        if in_list:
            bracket_count += line.count('[') - line.count(']')
            new_lines.append(line)
            
            # Check if we should insert after this line
            # Insert after similar task entries if found
            if task_name.split('Task')[0] in line and task_name not in line and not inserted:
                new_lines.append(task_entry)
                inserted = True
            
            # Check if we've closed the list
            if bracket_count <= 0 and '],' in line:
                # If we haven't inserted yet, add before the closing bracket
                if not inserted:
                    closing_line = new_lines.pop()
                    new_lines.append(task_entry)
                    new_lines.append(closing_line)
                    inserted = True
                in_list = False
        else:
            new_lines.append(line)
    
    if not inserted:
        print(f"Error: Could not find '{list_name}' section in config.py")
        return False
    
    new_full_content = '\n'.join(new_lines)
    
    # Write back
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(new_full_content)
        print(f"  ✓ Successfully added {task_name} to {list_name} in config.py")
        return True
    except Exception as e:
        print(f"Error writing {config_path}: {e}")
        return False

def main():
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
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
    print(f"Script location: {script_dir}")
    
    # Step 1: Copy Python files (critical - must succeed)
    if not copy_python_files(working_dir, script_dir):
        print("\n✗ ERROR: Failed to copy Python files. Installation aborted.")
        print("  Please ensure you run this script from the extracted package directory.")
        print("  The package should have this structure:")
        print("    package/")
        print("      src/tasks/fullauto/AutoFishMultiSpotTask.py")
        print("      src/tasks/trigger/SkillSpeedTask.py")
        print("      add_autofish_to_config.bat")
        print("      add_autofish_to_config.py")
        return 1
    
    # Step 2: Copy mod/fish/ folder
    copy_mod_fish_folder(working_dir, script_dir)
    
    # Step 3: Copy assets/ folder
    copy_assets_folder(working_dir, script_dir)
    
    # Step 4: Add AutoFishMultiSpotTask to onetime_tasks
    print("\n[4/5] Adding AutoFishMultiSpotTask to config.py...")
    add_task_to_config(working_dir, ONETIME_TASK_ENTRY, "onetime_tasks", "AutoFishMultiSpotTask")
    
    # Step 5: Add SkillSpeedTask to trigger_tasks
    print("\n[5/5] Adding SkillSpeedTask to config.py...")
    add_task_to_config(working_dir, TRIGGER_TASK_ENTRY, "trigger_tasks", "SkillSpeedTask")
    
    print("\n✓ Installation complete! Restart ok-dna to see the tasks.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

