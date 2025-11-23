#!/usr/bin/env python3
"""
Package all Choaga mod files for distribution.
Includes AutoFishMultiSpotTask, mod files, assets, and installation scripts.
"""

import os
import shutil
import zipfile
import tempfile
from pathlib import Path

def find_okdna_working_dir():
    """Try to find the ok-dna working directory"""
    # Method 1: Search up from script location to find working directory
    script_dir = Path(__file__).parent.absolute()
    current = script_dir
    
    # Search up to 10 levels to find working directory
    # Working directory should have src/config.py directly
    # We need to go up from mod/backup/Choaga to the actual working directory
    # The working directory should have main.py or ok/ folder at root level
    candidates = []
    for _ in range(10):
        config_path = current / "src" / "config.py"
        if config_path.exists():
            # Verify this is the working directory by checking it has the expected structure
            # Working directory should have main.py or ok/ folder at root
            has_main = (current / "main.py").exists()
            has_ok = (current / "ok").exists()
            has_mod = (current / "mod").is_dir()
            
            # The actual working directory should have main.py or ok/ folder
            # mod/backup might have src/config.py but not main.py
            if has_main or (has_ok and has_mod):
                candidates.append(current)
        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent
    
    # Return the candidate closest to root (the actual working directory)
    if candidates:
        # Sort by path depth (shortest path = closest to root = working directory)
        candidates.sort(key=lambda p: len(str(p)))
        return candidates[0]
    
    # Method 2: Search common ok-dna installation locations
    common_paths = [
        Path.home() / "AppData" / "Local" / "ok-dna" / "data" / "apps" / "ok-dna" / "working",
        Path("C:/ok-dna/working"),
        Path("D:/ok-dna/working"),
        Path("E:/ok-dna/working"),
    ]
    
    for path in common_paths:
        config_path = path / "src" / "config.py"
        if config_path.exists():
            return path
    
    return None

def main():
    # Find the ok-dna working directory
    working_dir = find_okdna_working_dir()
    
    if working_dir is None:
        print("ERROR: Could not find ok-dna working directory!")
        print("Please make sure ok-dna is installed and this script can find it.")
        return 1
    
    print(f"Found ok-dna working directory: {working_dir}\n")
    
    print("=== Choaga Mods Distribution Package Creator ===\n")
    
    # Package name
    package_name = "Choaga_Mods_Package"
    zip_name = f"{package_name}.zip"
    zip_path = working_dir / zip_name
    
    # Remove old zip if exists
    if zip_path.exists():
        zip_path.unlink()
        print(f"Removed old package: {zip_name}")
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    print(f"Created temp directory: {temp_dir}\n")
    
    try:
        # 1. Copy AutoFishMultiSpotTask.py
        print("[1/6] Copying AutoFishMultiSpotTask.py...")
        task_source = working_dir / "src/tasks/fullauto/AutoFishMultiSpotTask.py"
        if task_source.exists():
            task_dest = Path(temp_dir) / "src/tasks/fullauto"
            task_dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(task_source, task_dest)
            print("  ✓ Copied AutoFishMultiSpotTask.py")
        else:
            raise FileNotFoundError(f"ERROR: {task_source} not found!")
        
        # 2. Copy mod/fish/ folder with all images
        print("\n[2/6] Copying mod/fish/ folder...")
        mod_fish_source = working_dir / "mod/fish"
        if mod_fish_source.exists():
            mod_fish_dest = Path(temp_dir) / "mod/fish"
            mod_fish_dest.mkdir(parents=True, exist_ok=True)
            
            # Copy all PNG files
            image_files = list(mod_fish_source.glob("*.png"))
            if image_files:
                for img_file in image_files:
                    shutil.copy2(img_file, mod_fish_dest)
                print(f"  ✓ Copied {len(image_files)} PNG files from mod/fish/")
            else:
                print("  ⚠ WARNING: No PNG files found in mod/fish/")
        else:
            raise FileNotFoundError(f"ERROR: {mod_fish_source} not found!")
        
        # 3. Copy assets folder (if it exists)
        print("\n[3/6] Copying assets folder...")
        assets_source = working_dir / "assets"
        if assets_source.exists():
            assets_dest = Path(temp_dir) / "assets"
            assets_dest.mkdir(parents=True, exist_ok=True)
            
            # Copy result.json if it exists
            result_json = assets_source / "result.json"
            if result_json.exists():
                shutil.copy2(result_json, assets_dest)
                print("  ✓ Copied assets/result.json")
            
            # Copy images folder if it exists
            images_source = assets_source / "images"
            if images_source.exists():
                images_dest = assets_dest / "images"
                shutil.copytree(images_source, images_dest, dirs_exist_ok=True)
                print("  ✓ Copied assets/images/ folder")
        else:
            print("  ⚠ WARNING: assets folder not found (optional)")
        
        # 4. Copy installation scripts (from backup folder)
        print("\n[4/6] Copying installation scripts...")
        script_dir = Path(__file__).parent
        scripts = ["add_autofish_to_config.bat", "add_autofish_to_config.py"]
        for script in scripts:
            script_path = script_dir / script
            if script_path.exists():
                shutil.copy2(script_path, temp_dir)
                print(f"  ✓ Copied {script}")
            else:
                print(f"  ⚠ WARNING: {script} not found")
        
        # 5. Copy README/DISTRIBUTE file
        print("\n[5/6] Copying README...")
        readme_files = ["DISTRIBUTE_AutoFishMultiSpotTask.txt", "README.md"]
        readme_copied = False
        for readme in readme_files:
            readme_path = working_dir / readme
            if readme_path.exists():
                shutil.copy2(readme_path, temp_dir)
                print(f"  ✓ Copied {readme}")
                readme_copied = True
                break
        if not readme_copied:
            print("  ⚠ WARNING: No README file found")
        
        # 6. Create installation instructions
        print("\n[6/6] Creating installation instructions...")
        install_instructions = """INSTALLATION INSTRUCTIONS
=========================

1. Extract this zip file to a temporary location

2. Copy files to your ok-dna installation:
   
   a) Copy AutoFishMultiSpotTask.py to:
      [your ok-dna folder]\\src\\tasks\\fullauto\\AutoFishMultiSpotTask.py
   
   b) Copy the mod\\fish\\ folder to:
      [your ok-dna folder]\\mod\\fish\\
      (Make sure all PNG files are copied)
   
   c) If assets folder exists, copy it to:
      [your ok-dna folder]\\assets\\
      (This is optional - only if assets were included)

3. Run add_autofish_to_config.bat to automatically add the task to config.py
   OR manually add this line to config.py's 'onetime_tasks' list:
   ["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],

4. Restart ok-dna and the task will appear in your task list

NOTES:
- The add_autofish_to_config.bat script will automatically find your ok-dna installation
- Make sure your game resolution is set to 1920x1080 for best results
- All image files in mod/fish/ are required for the task to work properly

"""
        
        install_path = Path(temp_dir) / "INSTALL.txt"
        install_path.write_text(install_instructions, encoding='utf-8')
        print("  ✓ Created INSTALL.txt")
        
        # Create zip from temp directory
        print("\nCreating zip package...")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✓ Package created: {zip_name}")
        
        # Show package contents
        print("\nPackage contents:")
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            for name in sorted(zipf.namelist()):
                print(f"  {name}")
        
        print("\n=== Package creation complete! ===")
        print(f"Package location: {zip_path.absolute()}")
        return 0
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return 1
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print("\nCleaned up temp directory")

if __name__ == "__main__":
    exit(main())

