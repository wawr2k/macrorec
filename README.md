# Choaga's Complete Automation Mod Pack

A comprehensive collection of automation enhancements for ok-dna, including advanced skill options, multi-spot fishing, and skill speed technology.

## What's Included

This mod pack contains THREE major features:

1. **Advanced Skill Options** - Complex skill rotations with multi-cast and click spam
2. **Multi-Spot Fishing** - Automated fishing across multiple locations with character switching
3. **Skill Speed Tech** - Trigger task for enhanced combat performance

## Compatibility Note

✅ **This mod is fully compatible with the Mouse Jitter AFK Bypass mod!**

If you want BOTH features:
1. Install the Mouse Jitter mod first (from `../mousejitter/`)
2. Then run this Choaga mod scripts to add features

The mods work together seamlessly since they both extend `CommissionsTask`.

---

# Feature 1: Advanced Skill Options

Adds advanced skill casting options to ok-dna tasks, allowing you to automate complex skill rotations.

## Advanced Skill 1 Options:
- **Use Skill 1**: Choose which skill to use (Combat Skill, Ultimate Skill, or Geniemon Support)
- **Skill 1 Cast Count**: Cast the skill multiple times in a row
- **Skill 1 Click Spam Type**: Spam left/right clicks after casting
- **Skill 1 Click Spam Duration**: How long to spam clicks (seconds)
- **Skill 1 Release Frequency**: Cooldown between skill cycles (seconds)

## Simple Skill 2 Options:
- **Use Skill 2**: Choose which skill to use
- **Skill 2 Release Frequency**: Cooldown between casts (seconds)

## Installation

### Automatic (Recommended):

1. Double-click `add_skill_options_to_tasks.bat`
2. Confirm the ok-dna installation path
3. Review which files will be modified
4. Type 'y' to proceed

The script will:
- Automatically find your ok-dna installation
- Create `.backup` files of all modified tasks
- Add skill options to all fullauto tasks (except fishing tasks)
- Show progress for each file

## What Gets Modified

The script modifies all task files in `src/tasks/fullauto/` except:
- `AutoFishTask.py` (fishing tasks don't need skills)
- `AutoFishMultiSpotTask.py`
- `AutoFishChainTask.py`
- `ImportTask.py` (already has skill options)

## Example Skill Configurations:

**Basic Auto-Cast:**
- Use Skill 1: Combat Skill
- Skill 1 Cast Count: 1
- Skill 1 Release Frequency: 5.0

**Multi-Cast with Click Spam:**
- Use Skill 1: Ultimate Skill
- Skill 1 Cast Count: 3 (cast 3 times in a row)
- Skill 1 Click Spam Type: Left Click
- Skill 1 Click Spam Duration: 2.0 (spam for 2 seconds after casting)
- Skill 1 Release Frequency: 10.0 (wait 10 seconds before next cycle)

**Dual Skill Rotation:**
- Use Skill 1: Combat Skill
- Skill 1 Release Frequency: 5.0
- Use Skill 2: Geniemon Support
- Skill 2 Release Frequency: 8.0

---

# Feature 2: Multi-Spot Fishing (`AutoFishMultiSpotTask.py`)

Automated fishing system that cycles through multiple fishing spots and characters for maximum efficiency.

## Features

*   **Multi-Location Support**: Fish at 3 different spots (Sewers, Ice Lake, Purgatorio)
*   **Character Switching**: Automatically switches characters when inventory is full
*   **Smart Inventory Management**: Detects full inventory and switches spots/characters
*   **Configurable Rounds**: Set how many rounds to fish at each location
*   **Auto-Navigation**: Teleports between fishing spots automatically
*   **Fishing Supplies Management**: Automatically purchases fishing supplies when needed

## Installation

1. Copy `AutoFishMultiSpotTask.py` to `src/tasks/fullauto/`
2. Copy the entire `mod/fish/` folder (20 PNG files) to your ok-dna `mod/` directory
3. Copy `assets/result.json` and `assets/images/` (13 PNG files) to your ok-dna `assets/` directory
4. Restart ok-dna

## Required Files

**Task File:**
- `src/tasks/fullauto/AutoFishMultiSpotTask.py`

**Image Assets (mod/fish/):**
- armoury.png
- armourynotavailable.png
- combat.png
- covertmission.png
- deploy.png
- fish.png
- fishingsupplies.png
- fishingsupplies2.png
- Icelake.png
- inventory.png, inventory2.png, inventory3.png
- locatefishing.png
- nextchar.png
- nomorefish.png
- Purgatorio.png
- rod.png, rod2.png
- Sewers.png
- teleport.png

**Template Matching Assets (assets/):**
- `result.json` - Template matching configuration
- `images/0.png` through `images/12.png` - UI element templates

## Configuration

After installation, you'll see new options in the task:

- **Rounds**: Number of fishing rounds per location
- **Fishing Locations**: Choose which spots to fish (Sewers, Ice Lake, Purgatorio)
- **Character Switching**: Enable/disable automatic character switching
- **Fishing Supplies**: Auto-purchase when running low

## How It Works

1. **Starts at first fishing spot** (e.g., Sewers)
2. **Fishes until inventory full** or rounds complete
3. **Switches to next character** if inventory full
4. **Moves to next fishing spot** when all characters done
5. **Repeats cycle** until all locations and rounds complete

## Tips

- Make sure all fishing spots are unlocked on your characters
- Have fishing rods equipped on all characters
- Keep some currency for auto-purchasing fishing supplies
- Set realistic round counts to avoid running out of supplies

---

# Feature 3: Skill Speed Tech (`SkillSpeedTask.py`)

A trigger task that enhances combat performance through optimized skill timing.

## Features

*   **Automatic Skill Speed Optimization**: Adjusts skill timing for maximum DPS
*   **Combat Detection**: Only activates during combat
*   **Configurable Triggers**: Set when the skill speed boost activates
*   **Compatible with Other Tasks**: Works alongside other automation tasks

## Installation

1. Copy `SkillSpeedTask.py` to `src/tasks/trigger/`
2. Restart ok-dna
3. Enable in the Triggers tab

## Configuration

- **Activation Trigger**: Set conditions for when skill speed activates
- **Speed Multiplier**: Adjust the skill speed boost amount
- **Cooldown**: Set cooldown between activations

## How to Use

1. Go to the **Triggers** tab in ok-dna
2. Enable **Skill Speed Task**
3. Configure your preferred settings
4. Run any combat task - skill speed will activate automatically

---

# Feature 4: Auto-Fish Config Script

Automatically adds fishing configuration to your ok-dna setup.

## Installation

1. Double-click `add_autofish_to_config.bat`
2. Confirm the ok-dna installation path
3. Script will add fishing-related configurations

This script:
- Adds fishing task configurations
- Sets up default fishing parameters
- Configures fishing-related UI elements

---

# Combining Features

You can use any combination of these features:

## Recommended Setups:

**Maximum Automation:**
1. Install Mouse Jitter mod (AFK prevention)
2. Install Advanced Skill Options (combat automation)
3. Install Multi-Spot Fishing (fishing automation)
4. Enable Skill Speed Tech (combat enhancement)

**Fishing Focus:**
1. Install Multi-Spot Fishing
2. Run Auto-Fish Config script
3. Optionally add Mouse Jitter for AFK prevention

**Combat Focus:**
1. Install Advanced Skill Options
2. Enable Skill Speed Tech
3. Optionally add Mouse Jitter for AFK prevention

---

# Installation Order (Full Package)

If installing everything:

1. **First**: Mouse Jitter mod (if using)
   ```
   cd ../mousejitter
   INSTALL.bat
   ```

2. **Second**: Advanced Skill Options
   ```
   cd ../Choaga
   add_skill_options_to_tasks.bat
   ```

3. **Third**: Multi-Spot Fishing
   - Copy `AutoFishMultiSpotTask.py` to `src/tasks/fullauto/`
   - Copy `mod/fish/` folder
   - Copy `assets/` files

4. **Fourth**: Skill Speed Tech
   - Copy `SkillSpeedTask.py` to `src/tasks/trigger/`

5. **Fifth**: Auto-Fish Config (optional)
   ```
   add_autofish_to_config.bat
   ```

6. **Restart ok-dna**

---

# Troubleshooting

**Advanced Skills not working:**
- Check that "Use Skill 1" is not set to "Don't Use"
- Verify you're in combat (skills only cast during combat)
- Check the frequency isn't too high

**Multi-Spot Fishing stuck:**
- Verify all PNG files are in `mod/fish/` folder
- Check that fishing spots are unlocked
- Ensure characters have fishing rods equipped
- Verify `assets/result.json` and images are present

**Skill Speed not activating:**
- Make sure it's enabled in Triggers tab
- Check that you're in combat
- Verify trigger conditions are met

**Script can't find ok-dna:**
- Make sure ok-dna is installed in default location
- Manually specify path when prompted

**Want to undo changes:**
- Find `.backup` files in modified directories
- Remove `.backup` extension to restore
- Or reinstall ok-dna

---

# File Structure

After full installation, your ok-dna folder should have:

```
ok-dna/
├── src/
│   └── tasks/
│       ├── fullauto/
│       │   ├── AutoFishMultiSpotTask.py (NEW)
│       │   ├── [other tasks with skill options] (MODIFIED)
│       │   └── ...
│       └── trigger/
│           ├── SkillSpeedTask.py (NEW)
│           └── ...
├── mod/
│   └── fish/
│       └── [20 PNG files] (NEW)
└── assets/
    ├── result.json (UPDATED)
    └── images/
        └── [0.png through 12.png] (NEW)
```

---

# Credits

- Original mods by Choaga
- Multi-Spot Fishing system
- Skill Speed technology
- Advanced skill casting framework
- Compatible with Mouse Jitter mod by wawr2k
- Built for ok-dna by BnanZ0

---

# Support

For issues or questions:
- Check the main ok-dna Discord/QQ
- Review backup files to see what changed
- Test with simple configurations first
- Join the community for help

---

**Note**: These mods modify Python source files and add new assets. Always keep backups and test thoroughly!
