#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add advanced skill options from ImportTask.py to all fullauto tasks (except fishing tasks).
Adds:
- Skill 1 config options (Use Skill 1, Cast Count, Click Spam Type, Click Spam Duration, Release Frequency)
- Skill 2 config options (Use Skill 2, Release Frequency)
- use_skill() method with advanced casting and click spam
- use_skill_2() method for second skill
- Initialization of skill-related variables
"""

import os
import re
import shutil
from pathlib import Path

# Tasks to skip (fishing-related)
SKIP_TASKS = ['AutoFishTask', 'AutoFishMultiSpotTask', 'AutoFishChainTask', 'ImportTask']

# Skill config to add
SKILL_CONFIG = {
    'Use Skill 1': "Don't Use",
    'Skill 1 Cast Count': 1,
    'Skill 1 Click Spam Type': "None",
    'Skill 1 Click Spam Duration': 0.0,
    'Skill 1 Release Frequency': 5.0,
    'Use Skill 2': "Don't Use",
    'Skill 2 Release Frequency': 5.0
}

SKILL_CONFIG_TYPE = {
    'Use Skill 1': {
        "type": "drop_down",
        "options": ["Don't Use", "Combat Skill", "Ultimate Skill", "Geniemon Support"],
    },
    'Skill 1 Click Spam Type': {
        "type": "drop_down",
        "options": ["None", "Left Click", "Right Click"],
    },
    'Use Skill 2': {
        "type": "drop_down",
        "options": ["Don't Use", "Combat Skill", "Ultimate Skill", "Geniemon Support"],
    },
}

SKILL_CONFIG_DESCRIPTION = {
    'Use Skill 1': 'First skill to use automatically (e.g., Q)',
    'Skill 1 Cast Count': 'How many times to press Skill 1 before waiting for next frequency',
    'Skill 1 Click Spam Type': 'Type of click to spam after casting Skill 1 (None/Left Click/Right Click)',
    'Skill 1 Click Spam Duration': 'Duration in seconds to spam clicks after casting Skill 1',
    'Skill 1 Release Frequency': 'How many seconds between Skill 1 releases',
    'Use Skill 2': 'Second skill to use automatically (simple frequency only)',
    'Skill 2 Release Frequency': 'How many seconds between Skill 2 releases'
}

# Methods to add
USE_SKILL_METHOD = '''    def use_skill(self, skill_time):
        """
        Advanced skill casting with multiple casts and click spam support.
        Pattern: Cast skill N times -> spam clicks for duration -> wait frequency -> repeat
        """
        if not hasattr(self, "config"):
            return skill_time
        
        # Support both new and old config keys for backward compatibility
        skill_type = self.config.get("Use Skill 1") or self.config.get("Use Skill") or self.config.get("使用技能", "Don't Use")
        if skill_type == "Don't Use" or skill_type == "不使用":
            return skill_time
        
        skill_frequency = self.config.get("Skill 1 Release Frequency") or self.config.get("Skill Release Frequency") or self.config.get("技能释放频率", 5.0)
        cast_count = self.config.get('Skill 1 Cast Count') or self.config.get('Skill Cast Count', 1)
        click_spam_type = self.config.get('Skill 1 Click Spam Type') or self.config.get('Click Spam Type', "None")
        click_spam_duration = self.config.get('Skill 1 Click Spam Duration') or self.config.get('Click Spam Duration', 0.0)
        current_time = time.time()
        
        # Handle click spam phase - spam clicks continuously
        if self.in_click_spam_phase:
            if current_time - self.click_spam_start_time < click_spam_duration:
                # Continue spamming clicks rapidly
                if click_spam_type == "Left Click":
                    self.mouse_down(key='left')
                    self.sleep(0.05)
                    self.mouse_up(key='left')
                    self.sleep(0.05)  # Small delay between clicks
                elif click_spam_type == "Right Click":
                    self.mouse_down(key='right')
                    self.sleep(0.05)
                    self.mouse_up(key='right')
                    self.sleep(0.05)  # Small delay between clicks
                return skill_time
            else:
                # Click spam phase ended, reset for next skill cycle
                self.in_click_spam_phase = False
                self.skill_cast_count = 0
                skill_time = current_time  # Reset skill timer for next cycle
                return skill_time
        
        # Check if it's time to cast skills (after frequency wait)
        if current_time - skill_time >= skill_frequency:
            # Cast the skill multiple times
            for i in range(cast_count):
                if skill_type == "Combat Skill" or skill_type == "战技":
                    self.get_current_char().send_combat_key()
                elif skill_type == "Ultimate Skill" or skill_type == "终结技":
                    self.get_current_char().send_ultimate_key()
                elif skill_type == "Geniemon Support" or skill_type == "魔灵支援":
                    self.get_current_char().send_geniemon_key()
                
                # Small delay between multiple casts (except for last one)
                if i < cast_count - 1:
                    self.sleep(0.3)
            
            self.skill_cast_count = cast_count  # Mark as completed
            
            # Start click spam phase if configured
            if click_spam_type != "None" and click_spam_duration > 0:
                self.in_click_spam_phase = True
                self.click_spam_start_time = current_time
            else:
                # No click spam, reset for next cycle
                self.skill_cast_count = 0
                skill_time = current_time
        
        return skill_time'''

USE_SKILL_2_METHOD = '''    def use_skill_2(self, skill_time):
        """
        Simple second skill casting with frequency only (no cast count or click spam).
        """
        if not hasattr(self, "config"):
            return skill_time
        
        skill_type = self.config.get("Use Skill 2") or self.config.get("使用技能2", "Don't Use")
        if skill_type == "Don't Use" or skill_type == "不使用":
            return skill_time
        
        skill_frequency = self.config.get("Skill 2 Release Frequency") or self.config.get("Skill Release Frequency 2") or self.config.get("技能释放频率2", 5.0)
        current_time = time.time()
        
        # Check if it's time to cast skill (after frequency wait)
        if current_time - skill_time >= skill_frequency:
            if skill_type == "Combat Skill" or skill_type == "战技":
                self.get_current_char().send_combat_key()
            elif skill_type == "Ultimate Skill" or skill_type == "终结技":
                self.get_current_char().send_ultimate_key()
            elif skill_type == "Geniemon Support" or skill_type == "魔灵支援":
                self.get_current_char().send_geniemon_key()
            
            skill_time = current_time
        
        return skill_time'''

def find_okdna_working_dir():
    """Find ok-dna working directory"""
    script_dir = Path(__file__).parent.absolute()
    current = script_dir
    
    # Search up to 10 levels
    for _ in range(10):
        config_path = current / "src" / "config.py"
        if config_path.exists():
            has_main = (current / "main.py").exists()
            has_ok = (current / "ok").exists()
            has_mod = (current / "mod").is_dir()
            
            if has_main or (has_ok and has_mod):
                return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    
    # Try common paths
    common_paths = [
        Path.home() / "AppData" / "Local" / "ok-dna" / "data" / "apps" / "ok-dna" / "working",
        Path("C:/ok-dna/working"),
        Path("D:/ok-dna/working"),
        Path("E:/ok-dna/working"),
    ]
    
    for path in common_paths:
        if (path / "src" / "config.py").exists():
            return path
    
    return None

def add_skill_config_to_init(content):
    """Add skill config options to __init__ method"""
    lines = content.split('\n')
    new_lines = []
    in_init = False
    in_default_config = False
    in_config_type = False
    in_config_description = False
    bracket_count = 0
    brace_count = 0
    added_config = False
    added_config_type = False
    added_config_description = False
    
    for i, line in enumerate(lines):
        # Detect __init__ method
        if 'def __init__' in line:
            in_init = True
            new_lines.append(line)
            continue
        
        if in_init:
            # Detect default_config.update({
            if 'default_config.update({' in line or 'self.default_config.update({' in line:
                in_default_config = True
                brace_count = line.count('{') - line.count('}')
                new_lines.append(line)
                continue
            
            # Detect config_type[' or self.config_type['
            if ('config_type[' in line or 'self.config_type[' in line) and not in_config_type:
                in_config_type = True
                new_lines.append(line)
                continue
            
            # Detect config_description.update({
            if 'config_description.update({' in line or 'self.config_description.update({' in line:
                in_config_description = True
                brace_count = line.count('{') - line.count('}')
                new_lines.append(line)
                continue
            
            # Handle default_config block
            if in_default_config:
                brace_count += line.count('{') - line.count('}')
                new_lines.append(line)
                
                # Check if we're closing the default_config dict
                if brace_count <= 0 and '})' in line:
                    # Add skill config before closing
                    if not added_config:
                        indent = len(line) - len(line.lstrip())
                        for key, value in SKILL_CONFIG.items():
                            if isinstance(value, str):
                                new_lines.append(f"{' ' * indent}    '{key}': \"{value}\",")
                            else:
                                new_lines.append(f"{' ' * indent}    '{key}': {value},")
                        added_config = True
                    in_default_config = False
                continue
            
            # Handle config_type block
            if in_config_type:
                # Look for end of config_type assignments (next method or class)
                if line.strip().startswith('def ') or line.strip().startswith('class '):
                    # Add config_type before this line
                    if not added_config_type:
                        indent = len(line) - len(line.lstrip())
                        for key, value in SKILL_CONFIG_TYPE.items():
                            new_lines.append(f"{' ' * indent}        self.config_type['{key}'] = {repr(value)}")
                        added_config_type = True
                    in_config_type = False
                    new_lines.append(line)
                    continue
                
                # Check if we're in a method that's not config_type related
                if line.strip() and not ('config_type' in line or line.strip().startswith('#') or line.strip() == ''):
                    # Might be end of config_type section
                    if not added_config_type:
                        indent = len(line) - len(line.lstrip())
                        for key, value in SKILL_CONFIG_TYPE.items():
                            new_lines.append(f"{' ' * indent}        self.config_type['{key}'] = {repr(value)}")
                        added_config_type = True
                    in_config_type = False
                
                new_lines.append(line)
                continue
            
            # Handle config_description block
            if in_config_description:
                brace_count += line.count('{') - line.count('}')
                new_lines.append(line)
                
                # Check if we're closing the config_description dict
                if brace_count <= 0 and '})' in line:
                    # Add skill config descriptions before closing
                    if not added_config_description:
                        indent = len(line) - len(line.lstrip())
                        for key, value in SKILL_CONFIG_DESCRIPTION.items():
                            new_lines.append(f"{' ' * indent}    '{key}': '{value}',")
                        added_config_description = True
                    in_config_description = False
                continue
            
            # Check if we've left __init__ method
            if line.strip().startswith('def ') and not line.strip().startswith('def __init__'):
                in_init = False
                in_default_config = False
                in_config_type = False
                in_config_description = False
                # Make sure we added everything
                if not added_config or not added_config_type or not added_config_description:
                    # Try to add at end of __init__ before this method
                    indent = len(line) - len(line.lstrip())
                    if not added_config:
                        new_lines.append(f"{' ' * indent}        # Add skill config options")
                        new_lines.append(f"{' ' * indent}        self.default_config.update({{")
                        for key, value in SKILL_CONFIG.items():
                            if isinstance(value, str):
                                new_lines.append(f"{' ' * indent}            '{key}': \"{value}\",")
                            else:
                                new_lines.append(f"{' ' * indent}            '{key}': {value},")
                        new_lines.append(f"{' ' * indent}        }})")
                        added_config = True
                    if not added_config_type:
                        for key, value in SKILL_CONFIG_TYPE.items():
                            new_lines.append(f"{' ' * indent}        self.config_type['{key}'] = {repr(value)}")
                        added_config_type = True
                    if not added_config_description:
                        new_lines.append(f"{' ' * indent}        self.config_description.update({{")
                        for key, value in SKILL_CONFIG_DESCRIPTION.items():
                            new_lines.append(f"{' ' * indent}            '{key}': '{value}',")
                        new_lines.append(f"{' ' * indent}        }})")
                        added_config_description = True
                new_lines.append(line)
                continue
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def add_skill_methods(content):
    """Add use_skill and use_skill_2 methods if they don't exist"""
    # Check if methods already exist with advanced version
    if 'def use_skill(self, skill_time):' in content and 'Advanced skill casting' in content:
        # Already has the advanced version, check if use_skill_2 exists
        if 'def use_skill_2(self, skill_time):' in content:
            return content, False
        # Has use_skill but not use_skill_2, add it
        lines = content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if 'def use_skill(self, skill_time):' in line:
                # Find end of use_skill method
                j = i + 1
                indent = len(line) - len(line.lstrip())
                while j < len(lines):
                    if lines[j].strip().startswith('def ') or (lines[j].strip() and not lines[j].startswith(' ' * (indent + 4)) and not lines[j].startswith(' ' * indent + '    ')):
                        break
                    j += 1
                # Insert use_skill_2 after use_skill
                new_lines.append('')
                new_lines.append(USE_SKILL_2_METHOD)
                continue
        return '\n'.join(new_lines), True
    
    # Check if old use_skill exists and needs replacement
    old_use_skill_match = re.search(r'def use_skill\(self[^)]*\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
    has_old_use_skill = bool(old_use_skill_match)
    
    # Find where to insert methods (before last method or at end of class)
    lines = content.split('\n')
    new_lines = []
    insert_pos = -1
    
    if has_old_use_skill:
        # Replace old use_skill
        start_pos = old_use_skill_match.start()
        end_pos = old_use_skill_match.end()
        
        # Find the line numbers
        start_line = content[:start_pos].count('\n')
        end_line = content[:end_pos].count('\n')
        
        for i, line in enumerate(lines):
            if start_line <= i <= end_line:
                if i == start_line:
                    # Replace with new methods
                    new_lines.append(USE_SKILL_METHOD)
                    new_lines.append('')
                    new_lines.append(USE_SKILL_2_METHOD)
                # Skip old method lines
                continue
            new_lines.append(line)
        
        return '\n'.join(new_lines), True
    
    # No use_skill exists, find insertion point
    # Find the last method before class end
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        if line.strip().startswith('def ') and 'use_skill' not in line:
            insert_pos = i + 1
            break
    
    if insert_pos == -1:
        # No methods found, insert before class end
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() and not lines[i].strip().startswith('#'):
                insert_pos = i + 1
                break
    
    if insert_pos == -1:
        insert_pos = len(lines)
    
    # Build new content
    for i, line in enumerate(lines):
        if i == insert_pos:
            # Insert methods here
            new_lines.append('')
            new_lines.append(USE_SKILL_METHOD)
            new_lines.append('')
            new_lines.append(USE_SKILL_2_METHOD)
        new_lines.append(line)
    
    return '\n'.join(new_lines), True

def update_init_param(content):
    """Add skill-related variable initialization to init_param method"""
    if 'def init_param(self):' not in content:
        # Try to add init_param if it doesn't exist
        # Find do_run or run method to add init_param before it
        lines = content.split('\n')
        new_lines = []
        added = False
        
        for i, line in enumerate(lines):
            if not added and ('def do_run(self):' in line or 'def run(self):' in line):
                # Add init_param before this method
                indent = len(line) - len(line.lstrip())
                new_lines.append(f"{' ' * indent}    def init_param(self):")
                new_lines.append(f"{' ' * indent}        self.skill_time = 0")
                new_lines.append(f"{' ' * indent}        self.skill_time_2 = 0  # Second skill timer")
                new_lines.append(f"{' ' * indent}        self.skill_cast_count = 0  # Current cast count in cycle")
                new_lines.append(f"{' ' * indent}        self.click_spam_start_time = 0  # When click spam phase started")
                new_lines.append(f"{' ' * indent}        self.in_click_spam_phase = False  # Whether currently in click spam phase")
                new_lines.append('')
                added = True
            new_lines.append(line)
        
        if not added:
            # Add at end of class
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip() and not lines[i].strip().startswith('#'):
                    indent = len(lines[i]) - len(lines[i].lstrip())
                    new_lines.insert(i + 1, '')
                    new_lines.insert(i + 2, f"{' ' * indent}    def init_param(self):")
                    new_lines.insert(i + 3, f"{' ' * indent}        self.skill_time = 0")
                    new_lines.insert(i + 4, f"{' ' * indent}        self.skill_time_2 = 0  # Second skill timer")
                    new_lines.insert(i + 5, f"{' ' * indent}        self.skill_cast_count = 0  # Current cast count in cycle")
                    new_lines.insert(i + 6, f"{' ' * indent}        self.click_spam_start_time = 0  # When click spam phase started")
                    new_lines.insert(i + 7, f"{' ' * indent}        self.in_click_spam_phase = False  # Whether currently in click spam phase")
                    break
        
        content = '\n'.join(new_lines)
    
    # Update existing init_param to include skill variables
    lines = content.split('\n')
    new_lines = []
    in_init_param = False
    
    for i, line in enumerate(lines):
        if 'def init_param(self):' in line:
            in_init_param = True
            new_lines.append(line)
            continue
        
        if in_init_param:
            # Check if we've left the method
            if line.strip().startswith('def ') or (line.strip() and not (line.startswith(' ') or line.startswith('\t'))):
                # Add skill variables if not present
                recent_lines = '\n'.join(new_lines[-15:])
                if 'skill_time' not in recent_lines or ('skill_time_2' not in recent_lines and 'skill_cast_count' not in recent_lines):
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(f"{' ' * indent}        self.skill_time = 0")
                    new_lines.append(f"{' ' * indent}        self.skill_time_2 = 0  # Second skill timer")
                    new_lines.append(f"{' ' * indent}        self.skill_cast_count = 0  # Current cast count in cycle")
                    new_lines.append(f"{' ' * indent}        self.click_spam_start_time = 0  # When click spam phase started")
                    new_lines.append(f"{' ' * indent}        self.in_click_spam_phase = False  # Whether currently in click spam phase")
                in_init_param = False
            new_lines.append(line)
            continue
        
        new_lines.append(line)
    
    # Also check do_run/run for local variable initialization
    # If tasks use _skill_time as local variable, we don't need to add to init_param
    # But we should ensure use_skill_2 variable is initialized
    content = '\n'.join(new_lines)
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # Look for _skill_time initialization in do_run/run
        if '_skill_time = 0' in line or ('_skill_time =' in line and 'time.time()' not in line and 'self.' not in line):
            # Check if _skill_time_2 is initialized nearby
            has_skill_2_init = False
            for j in range(max(0, i-3), min(i+5, len(lines))):
                if '_skill_time_2' in lines[j] or ('skill_time_2' in lines[j] and 'self.' not in lines[j]):
                    has_skill_2_init = True
                    break
            
            if not has_skill_2_init:
                indent = len(line) - len(line.lstrip())
                new_lines.append(line)
                new_lines.append(f"{' ' * indent}_skill_time_2 = 0  # Second skill timer")
                continue
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def update_skill_calls(content):
    """Update existing use_skill calls and add use_skill_2 calls in combat loops"""
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # Look for use_skill calls (both self.skill_time and _skill_time patterns)
        if '= self.use_skill(' in line or '_skill_time = self.use_skill(' in line:
            new_lines.append(line)
            # Check if use_skill_2 is called on next few lines
            has_skill_2 = False
            for j in range(i + 1, min(i + 5, len(lines))):
                if 'use_skill_2' in lines[j]:
                    has_skill_2 = True
                    break
            
            if not has_skill_2:
                # Add use_skill_2 call after use_skill
                indent = len(line) - len(line.lstrip())
                
                # Determine variable name pattern
                if 'self.skill_time' in line:
                    skill_2_var = 'self.skill_time_2'
                elif '_skill_time' in line:
                    skill_2_var = '_skill_time_2'
                else:
                    skill_2_var = 'self.skill_time_2'
                
                new_lines.append(f"{' ' * indent}{skill_2_var} = self.use_skill_2({skill_2_var})")
            continue
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def ensure_time_import(content):
    """Ensure time module is imported"""
    if 'import time' in content:
        return content
    
    # Find import section
    lines = content.split('\n')
    new_lines = []
    added = False
    
    for i, line in enumerate(lines):
        if not added and ('from ok import' in line or 'import ' in line):
            # Check if time is imported in nearby lines
            if 'time' not in '\n'.join(lines[max(0, i-5):i+10]):
                # Add time import
                new_lines.append('import time')
                added = True
        new_lines.append(line)
    
    if not added:
        # Add at top after other imports
        for i, line in enumerate(lines):
            if line.strip().startswith('from ') or line.strip().startswith('import '):
                new_lines.append(line)
            else:
                new_lines.insert(i, 'import time')
                break
    
    return '\n'.join(new_lines)

def process_task_file(file_path):
    """Process a single task file to add skill options"""
    print(f"\n  Processing: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"    ✗ ERROR: Failed to read file: {e}")
        return False
    
    original_content = content
    
    # Step 1: Ensure time import
    content = ensure_time_import(content)
    
    # Step 2: Add skill config to __init__
    content = add_skill_config_to_init(content)
    
    # Step 3: Add skill methods
    content, methods_added = add_skill_methods(content)
    
    # Step 4: Update init_param
    content = update_init_param(content)
    
    # Step 5: Update skill calls
    content = update_skill_calls(content)
    
    # Only write if content changed
    if content != original_content:
        # Create backup
        backup_path = file_path.with_suffix('.py.backup')
        shutil.copy2(file_path, backup_path)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"    ✓ Successfully updated (backup saved to {backup_path.name})")
            return True
        except Exception as e:
            print(f"    ✗ ERROR: Failed to write file: {e}")
            # Restore backup
            shutil.copy2(backup_path, file_path)
            return False
    else:
        print(f"    ℹ No changes needed (already has skill options)")
        return True

def main():
    working_dir = find_okdna_working_dir()
    
    if working_dir is None:
        print("ERROR: Could not find ok-dna installation!")
        print("Please make sure ok-dna is installed and this script can find it.")
        return 1
    
    print(f"Found ok-dna at: {working_dir}")
    
    fullauto_dir = working_dir / "src" / "tasks" / "fullauto"
    
    if not fullauto_dir.exists():
        print(f"ERROR: {fullauto_dir} does not exist!")
        return 1
    
    print(f"\nScanning {fullauto_dir} for task files...")
    
    task_files = []
    for file_path in fullauto_dir.glob("*.py"):
        # Skip __init__ and tasks in SKIP_TASKS
        if file_path.name == "__init__.py":
            continue
        
        class_name = file_path.stem
        if class_name in SKIP_TASKS:
            print(f"  Skipping: {file_path.name} (fishing task or ImportTask)")
            continue
        
        task_files.append(file_path)
    
    if not task_files:
        print("  No task files found to process.")
        return 0
    
    print(f"\nFound {len(task_files)} task file(s) to process:")
    for tf in task_files:
        print(f"  - {tf.name}")
    
    print("\n" + "="*70)
    print("WARNING: This will modify task files in src/tasks/fullauto/")
    print("Backups will be created with .backup extension")
    print("="*70)
    
    response = input("\nContinue? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return 0
    
    success_count = 0
    for task_file in task_files:
        if process_task_file(task_file):
            success_count += 1
    
    print(f"\n{'='*70}")
    print(f"Completed: {success_count}/{len(task_files)} files updated successfully")
    print(f"{'='*70}")
    print("\nNext steps:")
    print("1. Review the changes in the task files")
    print("2. Test the tasks to ensure they work correctly")
    print("3. If something breaks, restore from .backup files")
    print("4. Delete .backup files once you're satisfied")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())

