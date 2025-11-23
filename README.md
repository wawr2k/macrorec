# AutoFishMultiSpotTask - ok-dna Fishing Automation

An enhanced multi-spot fishing automation task for [ok-dna](https://github.com/BnanZ0/ok-duet-night-abyss), the automation framework for Duet Night Abyss. This task automatically rotates through multiple fishing spots (Purgatorio, Icelake, and Sewers) with intelligent navigation, real-time statistics tracking, and optimized fishing logic.

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

## Requirements

- [ok-dna](https://github.com/BnanZ0/ok-duet-night-abyss) installed and configured
- **Game resolution: 1920x1080 (REQUIRED)** - The task uses image recognition and all images were captured at 1920x1080 resolution. Using a different resolution may cause navigation failures.
- **Game client language: English (REQUIRED)** - All image assets are designed for the English client. The task will not work correctly with other language clients.
- Python 3.10+ (included with ok-dna)
- Windows OS

## Installation

### Method 1: Automatic Installation (Recommended)

1. Download the latest release from the GitHub Releases page
2. Extract the zip file to a temporary location
3. Copy files to your ok-dna installation:
   - Copy `AutoFishMultiSpotTask.py` to: `[your ok-dna folder]\src\tasks\fullauto\AutoFishMultiSpotTask.py`
   - Copy the `mod\fish\` folder to: `[your ok-dna folder]\mod\fish\`
   - If `assets\` folder is included, copy it to: `[your ok-dna folder]\assets\`
   - **Important**: If you already have an `assets\` folder, it will be backed up to `assets - original\` before replacement
4. Run `add_autofish_to_config.bat` to automatically add the task to `config.py`
   - The script will automatically find your ok-dna installation
   - Or manually add this line to `config.py`'s `onetime_tasks` list:
     ```python
     ["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],
     ```
5. Restart ok-dna and the task will appear in your task list

### Method 2: Manual Installation

1. Download the source files
2. Copy `src/tasks/fullauto/AutoFishMultiSpotTask.py` to your ok-dna `src/tasks/fullauto/` folder
3. Copy all PNG files from `mod/fish/` to your ok-dna `mod/fish/` folder
4. Edit `src/config.py` and add to the `onetime_tasks` list:
   ```python
   ["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],
   ```
5. Restart ok-dna

## Usage

1. Launch ok-dna
2. Select **"Auto Fish Multi Spot"** from the task list (under "Fully Automatic" group)
3. Configure your settings:
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

## Configuration Options

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
│       └── fullauto/
│           └── AutoFishMultiSpotTask.py    # Main task file
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

