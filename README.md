# Choaga's Mod Collection - AutoFishMultiSpotTask & SkillSpeedTask

A collection of automation tasks for [ok-dna](https://github.com/BnanZ0/ok-duet-night-abyss), the automation framework for Duet Night Abyss. This package includes:

- **AutoFishMultiSpotTask**: An enhanced multi-spot fishing automation task that automatically rotates through multiple fishing spots (Purgatorio, Icelake, and Sewers) with intelligent navigation, real-time statistics tracking, and optimized fishing logic.

- **SkillSpeedTask**: A trigger task providing hotkey-activated combat speed techniques including Rhythm, Quick Skill Cancel, Rapid Fire, Skill Charge Combo, and character switching.

## Features

- 🎣 **Multi-Spot Fishing**: Automatically rotates through Purgatorio, Icelake, and Sewers fishing spots
- 🎯 **Image-Based Navigation**: Uses image recognition instead of hardcoded coordinates for better reliability
- 🗺️ **Map Recognition**: Automatically detects when maps load (Purgatorio and Icelake) to reduce waiting times
- ⚙️ **Configurable Spots**: Enable/disable individual fishing spots via config options
- 📊 **Real-Time Statistics**: Live updates of fish caught, chances used, and current phase
- 💾 **Persistent Stats**: All statistics remain visible after task completion or manual stop
- 🔄 **Auto-Return**: Automatically teleports back to Purgatorio and AFKs after all spots are done
- 🎨 **Optimized for Sewers**: Special handling for Sewers spot to avoid mob attacks
- 🔇 **Silent Operation**: Sound notifications disabled when switching spots (configurable)
- 📁 **Chaoga's Mod Tab**: Appears in the "Chaoga's mod" tab alongside other Choaga mods in ok-dna

## Related Tasks

This package includes tasks from the **Chaoga's mod** collection in ok-dna:

### Included in This Package:
- **Auto Fish Multi Spot** (Stable) - Automatically rotates through multiple fishing spots
- **Skill Speed** (Stable) - Speed techniques: Rhythm, Shoot Cancel, Rapid Fire, and more

### Other Tasks in Chaoga's Mod Collection:
- **Auto Fish Chain Task** (Beta) - Runs multi-spot fishing first, then runs expulsion or lv 70 credit
- **Secret Letter** (Beta) - Selects and clicks commission using OCR

**Note**: Auto Fish Chain Task and Secret Letter are currently in beta and not included in this package. AutoFishMultiSpotTask and SkillSpeedTask are stable and production-ready.

## Requirements

- [ok-dna](https://github.com/BnanZ0/ok-duet-night-abyss) installed and configured
- **Game resolution: 1920x1080 (REQUIRED)** - The task uses image recognition and all images were captured at 1920x1080 resolution. Using a different resolution may cause navigation failures.
- **Game client language: English (REQUIRED)** - All image assets are designed for the English client. The task will not work correctly with other language clients.
- Python 3.10+ (included with ok-dna)
- Windows OS

## Download

### Latest Release

Download the latest version as a zip file:

**[📦 Download Latest Release (ZIP)](https://github.com/wawr2k/macrorec/archive/refs/heads/main.zip)**

This will download the complete package including:
- AutoFishMultiSpotTask.py
- SkillSpeedTask.py
- All mod/fish/ image files
- Assets folder (English client assets)
- Installation scripts
- README.md

After downloading, extract the zip file and follow the installation instructions below.

## Installation

### Method 1: Automatic Installation (Recommended)

1. Download the latest release from the GitHub Releases page
2. Extract the zip file to a temporary location
3. **Important**: Copy files to your ok-dna **working** folder, not the repo folder:
   - **Working folder location**: `C:\Users\[YourUsername]\AppData\Local\ok-dna\data\apps\ok-dna\working\`
   - **Do NOT copy to the `repo` folder** - ok-dna runs from the `working` folder, not the repo folder
   - The installation script (`add_autofish_to_config.bat`) automatically uses the working folder
4. Copy image and asset files to your ok-dna working installation:
   - Copy the `mod\fish\` folder to: `[ok-dna working folder]\mod\fish\`
   - If `assets\` folder is included, copy it to: `[ok-dna working folder]\assets\`
   - **Important**: If you already have an `assets\` folder, it will be backed up to `assets - original\` before replacement
   - **Note**: Python files (AutoFishMultiSpotTask.py and SkillSpeedTask.py) are handled automatically by the installation script in Step 5
5. Run `add_autofish_to_config.bat` to automatically install the Python files and update config:
   - **Automatically finds** your ok-dna **working** directory (NOT the repo folder)
   - **Automatically copies** Python files from the extracted package to the correct folders in the **working** directory:
     - `AutoFishMultiSpotTask.py` → `[working folder]\src\tasks\fullauto\AutoFishMultiSpotTask.py`
     - `SkillSpeedTask.py` → `[working folder]\src\tasks\trigger\SkillSpeedTask.py`
   - **Automatically adds** tasks to `config.py` in the **working** folder:
     - Adds `AutoFishMultiSpotTask` to `onetime_tasks` list
     - Adds `SkillSpeedTask` to `trigger_tasks` list
   - **Important**: The script ONLY works with the **working** folder (`ok-dna\data\apps\ok-dna\working`), NOT the repo folder
   - The script will automatically find your ok-dna installation
   - **Note**: Make sure the extracted package files (Python files) are accessible - the script looks for them in the same directory or extracted package structure
   - Or manually add these lines to `config.py` in the **working** folder (NOT repo folder):
     - In `onetime_tasks` list: `["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],`
     - In `trigger_tasks` list: `["src.tasks.trigger.SkillSpeedTask", "SkillSpeedTask"],`
6. Restart ok-dna and the tasks will appear in your task list

### Method 2: Manual Installation

1. Download the source files
2. **Important**: Copy files to your ok-dna **working** folder:
   - Working folder: `C:\Users\[YourUsername]\AppData\Local\ok-dna\data\apps\ok-dna\working\`
   - Do NOT use the `repo` folder - use the `working` folder
3. Copy `src/tasks/fullauto/AutoFishMultiSpotTask.py` to your ok-dna working `src/tasks/fullauto/` folder
4. Copy `src/tasks/trigger/SkillSpeedTask.py` to your ok-dna working `src/tasks/trigger/` folder
5. Copy the entire `mod\fish\` folder (not just the PNG files) to your ok-dna working `mod\` folder
   - This maintains the proper folder structure: `mod\fish\*.png`
6. If `assets\` folder is included, copy it to your ok-dna working folder
7. **Important**: Edit `src/config.py` in the **working** folder (NOT the repo folder) and add:
   - To `onetime_tasks` list: `["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],`
   - To `trigger_tasks` list: `["src.tasks.trigger.SkillSpeedTask", "SkillSpeedTask"],`
8. Restart ok-dna

## Usage

1. Launch ok-dna
2. Navigate to the **"Chaoga's mod"** tab in the sidebar
3. Select a task from the list:
   - **"Auto Fish Multi Spot"** - For automated fishing across multiple spots
   - **"Skill Speed"** - For combat speed techniques (trigger task, uses hotkeys)

### Auto Fish Multi Spot

1. Select **"Auto Fish Multi Spot"** from the task list
2. Configure your settings:
   - **Max Rounds Per Spot**: Number of fish to catch per spot (0 = unlimited)
   - **Enable Purgatorio/Icelake/Sewers**: Checkboxes to enable/disable each spot
   - **END_WAIT_SPACE**: Wait time after catching a fish (default: 0.5 seconds)
   - **MAX_START_SEC/MAX_FIGHT_SEC/MAX_END_SEC**: Timeouts for each fishing phase
4. Click **Start** to begin fishing
5. Monitor the real-time statistics:
   - **Total Fish Caught**: Total across all spots
   - **Fish Caught (Current Spot)**: Fish caught at the current spot
   - **Rounds Completed**: Number of fishing rounds completed
   - **Chance Used (Bigger Fish)**: Number of special chances used
   - **Current Phase**: Current fishing phase (Start/Fight/End)
   - **Status**: Current task status

### Skill Speed

**Skill Speed** is a trigger task that provides hotkey-activated combat speed techniques. It runs in the background and activates when you press the configured hotkeys.

#### How to Use:

1. Navigate to the **"Chaoga's mod"** tab in the sidebar
2. Find **"Skill Speed"** in the task list
3. **Enable the task** (toggle switch) - The task must be enabled to listen for hotkeys
4. Configure your hotkeys and technique settings (see Configuration Options below)
5. **The task runs automatically** - No need to click "Start". Just press your configured hotkeys during gameplay

#### Available Techniques:

1. **Rapid Fire Cancel** (Default: F6)
   - **What it does**: Holds Right Click and rapidly spams Ctrl
   - **Use case**: Rapid fire attacks
   - **Config options**:
     - Hotkey (default: F6)
     - Interval between Ctrl presses (default: 0.1 seconds)
     - Duration to hold right click (default: 1.0 seconds)

2. **Rhythm Technique** (Default: F7)
   - **What it does**: Executes E (skill) → Hold Left Click (charge) → Right Click (shoot)
   - **Use case**: Rhythm combo for optimal damage
   - **Config options**:
     - Hotkey (default: F7)
     - Skill delay (default: 0.05 seconds)
     - Charge duration (default: 0.1 seconds)
     - Shoot delay (default: 0.05 seconds)

3. **Quick Skill Cancel** (Default: F8)
   - **What it does**: Executes E (skill) → Right Click immediately
   - **Use case**: Quick skill cancel for faster combos
   - **Config options**:
     - Hotkey (default: F8)
     - Delay between skill and cancel (default: 0.05 seconds)

4. **Skill Charge Combo** (Default: F9)
   - **What it does**: Executes Skill → Charge → Skill combo
   - **Use case**: Extended combo sequences
   - **Config options**:
     - Hotkey (default: F9)
     - Delay between actions (default: 0.1 seconds)

5. **Change Char** (Default: F10)
   - **What it does**: Changes character to refresh Boxie and **instantly refresh Geniemon cooldown**
   - **Use case**: Quick character switching and Geniemon cooldown reset
   - **Important**: Character switching instantly refreshes the Geniemon cooldown, allowing you to use Geniemon abilities more frequently
   - **Config options**:
     - Hotkey (default: F10)

#### Important Notes:

- **Trigger Task**: Skill Speed is a trigger task, not a one-time task. It stays enabled and listens for hotkeys.
- **Hotkeys**: Default hotkeys are F6-F10 to avoid conflicts with game controls (F1-F5 are used in-game)
- **Game Window Focus**: Hotkeys only work when the game window is in focus
- **Enable/Disable**: Use the toggle switch to enable/disable the task. When disabled, hotkeys won't work.
- **Individual Technique Control**: Each technique can be individually enabled/disabled in the config
- **Custom Hotkeys**: You can change any hotkey to your preferred key in the task configuration

## Configuration Options

### Auto Fish Multi Spot

| Option | Description | Default |
|--------|-------------|---------|
| Max Rounds Per Spot | Number of fish to catch per spot (0 = unlimited) | 0 |
| Enable Purgatorio | Enable/disable Purgatorio fishing spot | True |
| Enable Icelake | Enable/disable Icelake fishing spot | True |
| Enable Sewers | Enable/disable Sewers fishing spot | True |
| END_WAIT_SPACE | Wait time after catching a fish (seconds) | 0.5 |
| MAX_START_SEC | Start phase timeout (seconds) | 20.0 |
| MAX_FIGHT_SEC | Fighting phase timeout (seconds) | 60.0 |
| MAX_END_SEC | End phase timeout (seconds) | 20.0 |
| No Fish Timeout | Time to wait for "no more fish" detection (seconds) | 30.0 |
| PNG Check Timeout | Time to wait for PNG image before W key (seconds) | 10.0 |

### Skill Speed

| Option | Description | Default |
|--------|-------------|---------|
| Enable Rapid Fire Cancel | Enable/disable rapid fire technique | True |
| Rapid Fire Cancel Hotkey | Hotkey to activate rapid fire | F6 |
| Rapid Fire Cancel Interval | Interval between Ctrl presses (seconds) | 0.1 |
| Rapid Fire Cancel Duration | How long to hold right click (seconds) | 1.0 |
| Enable Rhythm | Enable/disable Rhythm technique | True |
| Rhythm Hotkey | Hotkey to activate Rhythm | F7 |
| Rhythm Skill Delay | Delay after skill before charge (seconds) | 0.05 |
| Rhythm Charge Duration | How long to hold charge attack (seconds) | 0.1 |
| Rhythm Shoot Delay | Delay before shooting (seconds) | 0.05 |
| Enable Quick Skill Cancel | Enable/disable quick skill cancel | True |
| Quick Skill Cancel Hotkey | Hotkey to activate quick skill cancel | F8 |
| Quick Skill Cancel Delay | Delay between skill and cancel (seconds) | 0.05 |
| Enable Skill Charge Combo | Enable/disable skill charge combo | True |
| Skill Charge Combo Hotkey | Hotkey to activate skill charge combo | F9 |
| Skill Charge Combo Delay | Delay between actions (seconds) | 0.1 |
| Enable Change Char | Enable/disable change character (instantly refreshes Geniemon cooldown) | True |
| Change Char Hotkey | Hotkey to change character | F10 |

## How It Works

1. **Navigation**: Uses image recognition to navigate through menus:
   - Detects inventory, fishing supplies, rod, locate fishing, and teleport buttons
   - Waits for map images (Purgatorio.png, Icelake.png) to confirm map load
   
2. **Fishing Loop**: Integrated fishing logic handles:
   - **Start Phase**: Detects fishing bar and waits for bite
   - **Fight Phase**: Controls fish movement using keyboard input
   - **End Phase**: Confirms fish caught and waits for next round
   
3. **Spot-Specific Behavior**:
   - **Purgatorio**: Standard navigation with map recognition
   - **Icelake**: Taps 'a' twice before holding 'W', with map recognition
   - **Sewers**: 5-second wait after teleport, then looks for fish.png and presses 'F' immediately

4. **Completion**: After all enabled spots are done, teleports back to Purgatorio and enters AFK mode

## File Structure

```
AutoFishMultiSpotTask/
├── src/
│   └── tasks/
│       ├── fullauto/
│       │   └── AutoFishMultiSpotTask.py    # Multi-spot fishing task
│       └── trigger/
│           └── SkillSpeedTask.py           # Skill speed techniques task
├── mod/
│   └── fish/
│       ├── fish.png                        # Fish detection image
│       ├── nomorefish.png                  # No more fish detection
│       ├── inventory.png                   # Inventory button
│       ├── fishingsupplies.png             # Fishing supplies button
│       ├── rod.png                         # Rod button
│       ├── locatefishing.png               # Locate fishing button
│       ├── teleport.png                    # Teleport button
│       ├── Purgatorio.png                  # Purgatorio map
│       ├── Icelake.png                     # Icelake map
│       └── ... (other navigation images)
├── assets/                                 # Image recognition assets (English client only)
│   ├── result.json                         # Feature detection data
│   └── images/                             # Template images
│       └── ... (numbered PNG files)
├── add_autofish_to_config.bat             # Auto-installation script
├── add_autofish_to_config.py              # Config updater script
└── README.md                               # This file
```

**Note**: When installing, if you already have an `assets/` folder in your ok-dna installation, it will be automatically backed up to `assets - original/` before the new assets are copied. The backup location is: `C:\Users\[YourUsername]\AppData\Local\ok-dna\data\apps\ok-dna\working\assets - original\`

## Important Notes

### Resolution and Language Requirements

⚠️ **CRITICAL REQUIREMENTS**:
- **Resolution**: The game MUST be running at **1920x1080 resolution**. The task uses image recognition and all template images were captured at this specific resolution. Using any other resolution will cause navigation to fail.
- **Language**: The game client MUST be set to **English language**. All image assets (inventory buttons, menus, etc.) are designed for the English client interface. Other languages will not work.

### Assets Backup

When installing the `assets/` folder:
- If you already have an `assets/` folder, it will be automatically backed up
- Backup location: `C:\Users\[YourUsername]\AppData\Local\ok-dna\data\apps\ok-dna\working\assets - original\`
- You can restore your original assets from this backup folder if needed

## Troubleshooting

### Task doesn't appear in ok-dna
- Make sure you added the task to `config.py`'s `onetime_tasks` list
- Restart ok-dna after making changes
- Check that `AutoFishMultiSpotTask.py` is in `src/tasks/fullauto/` folder

### Navigation fails / clicks wrong buttons
- **CRITICAL**: Ensure your game resolution is set to **1920x1080** - this is required, not optional
- **CRITICAL**: Make sure your game client is set to **English language** - the image assets are designed for English only
- Check that all PNG files are in `mod/fish/` folder
- Make sure the game window is visible and not minimized
- Verify that `assets/` folder was copied correctly (check for `assets - original/` backup folder)

### Fish count shows 0
- This was fixed in a recent update - make sure you have the latest version
- Statistics update in real-time as fish are caught

### Task stops unexpectedly
- Check the logs in ok-dna for error messages
- Ensure you have enough inventory space
- Verify fishing supplies are available

### Sewers gets attacked by mobs
- The script is optimized for Sewers with a 5-second wait and immediate 'F' press
- If issues persist, try disabling Sewers in config and only use other spots

## Advanced Usage

### Creating Distribution Packages

If you want to package this mod for distribution:

1. Navigate to `mod/backup/Choaga/` folder in your ok-dna installation
2. Run `package_choaga_mods.bat` or `package_choaga_mods.py`
3. This will create `Choaga_Mods_Package.zip` in the working directory with all necessary files

### Manual Config Editing

If the auto-installation script doesn't work, manually edit `src/config.py`:

```python
'onetime_tasks': [
    # ... other tasks ...
    ["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],
    # ... more tasks ...
],
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is provided as-is for personal use. Please refer to ok-dna's license for framework-related terms.

## Credits

- Built for [ok-dna](https://github.com/BnanZ0/ok-duet-night-abyss) by BnanZ0
- Fishing logic integrated from AutoFishTask
- Image-based navigation for improved reliability
- **English assets provided by Maverick** - The `assets/` folder (result.json and images/) was captured and optimized for the English client by Maverick

## Disclaimer

This software is for personal use only. Using automation tools may violate game terms of service and could result in account bans. Use at your own risk.

## Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review ok-dna's documentation
3. Open an issue on GitHub with:
   - ok-dna version
   - Game resolution
   - Error messages from logs
   - Steps to reproduce the issue

---

**Note**: This task requires ok-dna to function. Make sure you have ok-dna properly installed and configured before using this task.

