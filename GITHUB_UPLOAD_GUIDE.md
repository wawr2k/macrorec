# GitHub Upload Guide

## README.md - Automatic Display

**GitHub automatically displays `README.md` if it's in the root of your repository.** You don't need to copy it anywhere special - just make sure it's named `README.md` (case-sensitive) and placed in the root directory of your repository.

## What to Upload to GitHub

### Recommended Repository Structure:

```
AutoFishMultiSpotTask/
├── README.md                                    # ← Goes in root (auto-displays)
├── src/
│   └── tasks/
│       └── fullauto/
│           └── AutoFishMultiSpotTask.py        # ← Main task file
├── mod/
│   └── fish/
│       ├── fish.png                            # ← All PNG images
│       ├── nomorefish.png
│       ├── inventory.png
│       ├── fishingsupplies.png
│       ├── fishingsupplies2.png
│       ├── rod.png
│       ├── rod2.png
│       ├── inventory2.png
│       ├── inventory3.png
│       ├── locatefishing.png
│       ├── teleport.png
│       ├── Purgatorio.png
│       ├── Icelake.png
│       └── ... (all other PNG files)
├── assets/                                      # ← Include this folder
│   ├── result.json
│   └── images/
│       ├── 0.png
│       ├── 1.png
│       └── ... (all numbered PNG files)
├── add_autofish_to_config.bat                  # ← Installation script
└── add_autofish_to_config.py                   # ← Installation script
```

### Files to Upload:

#### ✅ **MUST UPLOAD:**
1. **README.md** - Place in repository root (GitHub will auto-display it)
2. **src/tasks/fullauto/AutoFishMultiSpotTask.py** - The main task file
3. **mod/fish/** - All PNG image files (20 files total)
4. **assets/** - The entire assets folder (result.json + images folder)
5. **add_autofish_to_config.bat** - Installation helper
6. **add_autofish_to_config.py** - Installation helper

#### ⚠️ **OPTIONAL (for developers):**
- `package_choaga_mods.py` - Packaging script (useful for creating distribution packages)
- `package_choaga_mods.bat` - Packaging script wrapper
- `package_choaga_mods.ps1` - PowerShell packaging script (if you want to include it)

## Step-by-Step Upload Process

### Option 1: Using GitHub Web Interface

1. **Create a new repository** on GitHub
   - Name it something like `AutoFishMultiSpotTask` or `ok-dna-fishing-automation`
   - Make it Public or Private (your choice)
   - **Don't** initialize with README (you already have one)

2. **Upload files:**
   - Click "uploading an existing file"
   - Create the folder structure:
     - Create `src/tasks/fullauto/` folder, then upload `AutoFishMultiSpotTask.py`
     - Create `mod/fish/` folder, then upload all PNG files
     - Create `assets/` folder, then upload `result.json` and `images/` subfolder
   - Upload `README.md` to the root
   - Upload `add_autofish_to_config.bat` and `.py` to the root

3. **Commit** - GitHub will automatically display the README.md

### Option 2: Using Git Command Line

```bash
# Initialize repository
git init
git add README.md
git add src/tasks/fullauto/AutoFishMultiSpotTask.py
git add mod/fish/*.png
git add assets/
git add add_autofish_to_config.bat
git add add_autofish_to_config.py
git commit -m "Initial commit: AutoFishMultiSpotTask"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Option 3: Using GitHub Desktop

1. Create repository on GitHub
2. Clone it locally
3. Copy files into the cloned folder maintaining the structure above
4. Commit and push

## File Locations in Your System

To find the files to upload:

- **AutoFishMultiSpotTask.py**: 
  `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\src\tasks\fullauto\AutoFishMultiSpotTask.py`

- **mod/fish/ images**: 
  `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\mod\fish\*.png`

- **assets/ folder**: 
  `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\assets\`

- **README.md**: 
  `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\mod\backup\Choaga\README.md`

- **Installation scripts**: 
  `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\mod\backup\Choaga\add_autofish_to_config.*`

## Important Notes

1. **README.md auto-displays**: Just place it in the root directory, GitHub handles the rest
2. **Include assets folder**: Yes, upload the entire `assets/` folder - it's required for the task to work
3. **Include all images**: Upload all PNG files from `mod/fish/` - they're all needed
4. **File size**: If assets/images/ folder is very large, consider using Git LFS (Large File Storage) for binary files
5. **Releases**: After uploading, create a GitHub Release and attach the `Choaga_Mods_Package.zip` (created by package_choaga_mods.py) for easy distribution

## Quick Checklist

- [ ] README.md in repository root
- [ ] AutoFishMultiSpotTask.py in src/tasks/fullauto/
- [ ] All PNG files in mod/fish/
- [ ] assets/ folder with result.json and images/
- [ ] add_autofish_to_config.bat and .py in root
- [ ] Repository structure matches the guide above
- [ ] Test that README.md displays correctly on GitHub

## After Upload

1. Check that README.md displays correctly on your repository page
2. Create a GitHub Release with the distribution zip file
3. Update the README.md releases link if needed
4. Consider adding tags/topics to your repository (e.g., "ok-dna", "automation", "fishing", "duet-night-abyss")

