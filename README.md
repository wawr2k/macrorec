# Choaga's Advanced Skill Options Mod

This mod adds advanced skill casting options to ok-dna tasks, allowing you to automate complex skill rotations with multiple casts and click spam.

## Compatibility Note

✅ **This mod is fully compatible with the Mouse Jitter AFK Bypass mod!**

If you want BOTH features:
1. Install the Mouse Jitter mod first (from `../mousejitter/`)
2. Then run this Choaga mod script to add skill options

The mods work together seamlessly since they both extend `CommissionsTask`.

## Features

### Advanced Skill 1 Options:
- **Use Skill 1**: Choose which skill to use (Combat Skill, Ultimate Skill, or Geniemon Support)
- **Skill 1 Cast Count**: Cast the skill multiple times in a row
- **Skill 1 Click Spam Type**: Spam left/right clicks after casting
- **Skill 1 Click Spam Duration**: How long to spam clicks (seconds)
- **Skill 1 Release Frequency**: Cooldown between skill cycles (seconds)

### Simple Skill 2 Options:
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

### Manual:

If you prefer to manually add skill options, you can:
1. Copy the skill-related code from `ImportTask.py`
2. Add it to your desired task files
3. Follow the pattern shown in the script

## What Gets Modified

The script modifies all task files in `src/tasks/fullauto/` except:
- `AutoFishTask.py` (fishing tasks don't need skills)
- `AutoFishMultiSpotTask.py`
- `AutoFishChainTask.py`
- `ImportTask.py` (already has skill options)

For each task, it adds:
1. **Config options** in `__init__` method
2. **use_skill()** method - Advanced skill casting with multi-cast and click spam
3. **use_skill_2()** method - Simple second skill casting
4. **Skill variables** in `init_param()` method
5. **Skill calls** in combat loops

## How to Use

After installation:

1. Open ok-dna and select a fullauto task
2. In the task settings, you'll see new options:
   - **Use Skill 1**: Select your skill type
   - **Skill 1 Cast Count**: Set how many times to cast (default: 1)
   - **Skill 1 Click Spam Type**: Choose None/Left Click/Right Click
   - **Skill 1 Click Spam Duration**: Set spam duration in seconds
   - **Skill 1 Release Frequency**: Set cooldown (default: 5.0 seconds)
   - **Use Skill 2**: Select second skill (optional)
   - **Skill 2 Release Frequency**: Set cooldown for second skill

3. Configure your desired skill rotation
4. Start the task

### Example Configurations:

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

## Combining with Mouse Jitter Mod

If you want both advanced skills AND mouse jitter:

1. **First**, install Mouse Jitter mod:
   ```
   cd ../mousejitter
   INSTALL.bat
   ```

2. **Then**, add skill options:
   ```
   cd ../Choaga
   add_skill_options_to_tasks.bat
   ```

Both mods will work together! You'll have:
- ✅ Mouse jitter for AFK prevention
- ✅ Advanced skill casting options
- ✅ All in the same tasks

## Troubleshooting

**Script can't find ok-dna:**
- Make sure ok-dna is installed in the default location
- Or manually specify the path when prompted

**Backup files (.backup) everywhere:**
- These are safety backups
- Test the tasks first
- Delete .backup files once you're satisfied

**Skills not casting:**
- Check that "Use Skill 1" is not set to "Don't Use"
- Verify the skill frequency isn't too high
- Make sure you're in combat (skills only cast during combat)

**Want to undo changes:**
- Find the `.backup` files in `src/tasks/fullauto/`
- Remove `.backup` extension to restore original files
- Or reinstall ok-dna

## Files Included

- `add_skill_options_to_tasks.bat` - Windows batch installer
- `add_skill_options_to_tasks.py` - Python script that does the modification
- `ImportTask.py` - Reference implementation with all skill features
- `README.md` - This file

## Credits

- Original skill system by Choaga
- Compatible with Mouse Jitter
- Built for ok-dna by BnanZ0

## Support

For issues or questions:
- Check the main ok-dna Discord/QQ
- Review the backup files to see what changed
- Test with simple configurations first

---

**Note**: This mod modifies Python source files. Always keep backups and test thoroughly before using in production!

