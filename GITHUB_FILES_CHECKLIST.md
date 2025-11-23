# GitHub Upload Checklist - Complete File List

## 📋 Files to Upload to GitHub

### ✅ **Root Directory Files:**
1. **README.md**
   - Location: `mod\backup\Choaga\README.md`
   - Upload to: Repository root
   - **GitHub will automatically display this on your repository page**

2. **add_autofish_to_config.bat**
   - Location: `mod\backup\Choaga\add_autofish_to_config.bat`
   - Upload to: Repository root

3. **add_autofish_to_config.py**
   - Location: `mod\backup\Choaga\add_autofish_to_config.py`
   - Upload to: Repository root

---

### ✅ **Source Code Files:**

4. **AutoFishMultiSpotTask.py**
   - Location: `src\tasks\fullauto\AutoFishMultiSpotTask.py`
   - Upload to: `src/tasks/fullauto/AutoFishMultiSpotTask.py`
   - Full path: `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\src\tasks\fullauto\AutoFishMultiSpotTask.py`

5. **SkillSpeedTask.py**
   - Location: `src\tasks\trigger\SkillSpeedTask.py`
   - Upload to: `src/tasks/trigger/SkillSpeedTask.py`
   - Full path: `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\src\tasks\trigger\SkillSpeedTask.py`

---

### ✅ **Image Assets (mod/fish/ folder):**

6. **All PNG files from mod/fish/**
   - Location: You need to create `mod\fish\` folder structure
   - Upload to: `mod/fish/` (upload the entire `mod` folder, which contains `fish`)
   - **Note**: If you don't have a `mod\fish\` folder yet, create it and add all the PNG files listed below
   
   **Files to include (20 PNG files - you need to gather these):**
   - armoury.png
   - armourynotavailable.png
   - combat.png
   - covertmission.png
   - deploy.png
   - fish.png
   - fishingsupplies.png
   - fishingsupplies2.png
   - Icelake.png
   - inventory.png
   - inventory2.png
   - inventory3.png
   - locatefishing.png
   - nextchar.png
   - nomorefish.png
   - Purgatorio.png
   - rod.png
   - rod2.png
   - Sewers.png
   - teleport.png

---

### ✅ **Assets Folder:**

7. **assets/result.json**
   - Location: `assets\result.json`
   - Upload to: `assets/result.json`
   - Full path: `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\assets\result.json`

8. **assets/images/ folder**
   - Location: `assets\images\` folder
   - Upload to: `assets/images/`
   - Full path: `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\assets\images\`
   
   **Files to include (13 PNG files):**
   - 0.png
   - 1.png
   - 2.png
   - 3.png
   - 4.png
   - 5.png
   - 6.png
   - 7.png
   - 8.png
   - 9.png
   - 10.png
   - 11.png
   - 12.png

---

## 📁 Final Repository Structure

```
YourRepository/
├── README.md                                    ← Root
├── add_autofish_to_config.bat                  ← Root
├── add_autofish_to_config.py                    ← Root
├── src/
│   └── tasks/
│       ├── fullauto/
│       │   └── AutoFishMultiSpotTask.py        ← Task file
│       └── trigger/
│           └── SkillSpeedTask.py               ← Task file
├── mod/
│   └── fish/
│       ├── armoury.png
│       ├── armourynotavailable.png
│       ├── combat.png
│       ├── covertmission.png
│       ├── deploy.png
│       ├── fish.png
│       ├── fishingsupplies.png
│       ├── fishingsupplies2.png
│       ├── Icelake.png
│       ├── inventory.png
│       ├── inventory2.png
│       ├── inventory3.png
│       ├── locatefishing.png
│       ├── nextchar.png
│       ├── nomorefish.png
│       ├── Purgatorio.png
│       ├── rod.png
│       ├── rod2.png
│       ├── Sewers.png
│       └── teleport.png
└── assets/
    ├── result.json
    └── images/
        ├── 0.png
        ├── 1.png
        ├── 2.png
        ├── 3.png
        ├── 4.png
        ├── 5.png
        ├── 6.png
        ├── 7.png
        ├── 8.png
        ├── 9.png
        ├── 10.png
        ├── 11.png
        └── 12.png
```

---

## ✅ Quick Upload Checklist

- [ ] README.md (root)
- [ ] add_autofish_to_config.bat (root)
- [ ] add_autofish_to_config.py (root)
- [ ] src/tasks/fullauto/AutoFishMultiSpotTask.py
- [ ] src/tasks/trigger/SkillSpeedTask.py
- [ ] mod/fish/ (all 20 PNG files)
- [ ] assets/result.json
- [ ] assets/images/ (all 13 PNG files)

---

## 📝 Important Notes

1. **Use files from the `working` folder**, NOT the `repo` folder
2. **Upload the entire `mod` folder** (which contains `fish`), not just the `fish` folder
3. **README.md must be in the root** - GitHub will automatically display it
4. **All paths are relative to**: `C:\Users\PTA\AppData\Local\ok-dna\data\apps\ok-dna\working\`

---

## 🚀 Upload Methods

### Option 1: GitHub Web Interface
1. Create repository
2. Click "uploading an existing file"
3. Create folders and upload files according to the structure above

### Option 2: Git Command Line
```bash
git init
git add README.md
git add add_autofish_to_config.*
git add src/
git add mod/
git add assets/
git commit -m "Initial commit: Choaga's mod collection"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Option 3: GitHub Desktop
1. Create repository on GitHub
2. Clone it locally
3. Copy all files maintaining the folder structure
4. Commit and push

---

## 📊 File Count Summary

- **Python files**: 2 (AutoFishMultiSpotTask.py, SkillSpeedTask.py)
- **Script files**: 2 (add_autofish_to_config.bat, add_autofish_to_config.py)
- **Image files**: 33 total
  - mod/fish/: 20 PNG files
  - assets/images/: 13 PNG files
- **JSON files**: 1 (assets/result.json)
- **Documentation**: 1 (README.md)

**Total files to upload: 39 files**

