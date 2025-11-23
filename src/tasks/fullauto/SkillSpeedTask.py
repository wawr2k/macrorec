from qfluentwidgets import FluentIcon
from ok import TriggerTask, Logger, og
from src.tasks.BaseListenerTask import BaseListenerTask
from src.tasks.BaseCombatTask import BaseCombatTask
from src.tasks.BaseDNATask import BaseDNATask
from pynput import mouse, keyboard
import time
import os
import cv2
import numpy as np
from pathlib import Path
from PIL import Image

logger = Logger.get_logger(__name__)


class SkillSpeedTask(BaseListenerTask, BaseCombatTask, BaseDNATask, TriggerTask):
    """Skill Speed Techniques for Duet Night Abyss"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Skill Speed"
        self.description = "Speed techniques: Rhythm, Shoot Cancel, and more"
        self.icon = FluentIcon.FLAG
        self.group_name = "Chaoga's mod"
        self.group_icon = FluentIcon.CAFE
        
        # Setup listener but remove activation key config (we use individual hotkeys)
        self.setup_listener_config()
        # Remove activation key configs since we don't use them
        self.default_config.pop('激活键', None)
        self.default_config.pop('键盘', None)
        self.config_type.pop('激活键', None)
        self.config_description.pop('激活键', None)
        
        # Default config for each technique
        # Using HTML in key names to style the labels (QLabel supports HTML)
        # Using F6-F10 to avoid conflicts with game controls (F1-F5 are used in-game)
        self.default_config.update({
            # Rapid Fire (Hold Right Click and spam Ctrl)
            'Enable Rapid Fire Cancel': True,
            '<span style="color: #3A7FCF;">Rapid Fire Cancel Hotkey</span>': 'f6',
            '<span style="color: #3A7FCF;">Rapid Fire Cancel Interval</span>': 0.1,
            '<span style="color: #3A7FCF;">Rapid Fire Cancel Duration</span>': 1.0,
            
            # Rhythm Technique (E -> Hold Left Click -> Right Click)
            'Enable Rhythm': True,
            '<span style="color: #3A7FCF;">Rhythm Hotkey</span>': 'f7',
            '<span style="color: #3A7FCF;">Rhythm Skill Delay</span>': 0.05,  # Delay after E before left click
            '<span style="color: #3A7FCF;">Rhythm Charge Duration</span>': 0.1,  # How long to hold left click
            '<span style="color: #3A7FCF;">Rhythm Shoot Delay</span>': 0.05,  # Delay before right click
            
            # Quick Skill Cancel (E -> Right Click immediately)
            'Enable Quick Skill Cancel': True,
            '<span style="color: #3A7FCF;">Quick Skill Cancel Hotkey</span>': 'f8',
            '<span style="color: #3A7FCF;">Quick Skill Cancel Delay</span>': 0.05,
            
            # Skill -> Charge -> Skill Combo
            'Enable Skill Charge Combo': True,
            '<span style="color: #3A7FCF;">Skill Charge Combo Hotkey</span>': 'f9',
            '<span style="color: #3A7FCF;">Skill Charge Combo Delay</span>': 0.1,
            
            # Change Char to refresh Boxie
            'Enable Change Char': True,
            '<span style="color: #3A7FCF;">Change Char Hotkey</span>': 'f10',
        })
        
        # Config descriptions with HTML formatting for better visibility
        self.config_description.update({
            'Enable Rapid Fire Cancel': '<b style="font-size: 18px; color: #4A9EFF; font-weight: bold;">RAPID FIRE</b><br>Hold Right Click and spam Ctrl',
            '<span style="color: #3A7FCF;">Rapid Fire Cancel Hotkey</span>': 'Hotkey to activate rapid fire',
            '<span style="color: #3A7FCF;">Rapid Fire Cancel Interval</span>': 'Interval between Ctrl presses (seconds)',
            '<span style="color: #3A7FCF;">Rapid Fire Cancel Duration</span>': 'How long to hold right click and spam (seconds)',
            
            'Enable Rhythm': '<b style="font-size: 18px; color: #4A9EFF; font-weight: bold;">RHYTHM</b><br>E -> Hold Left Click -> Right Click',
            '<span style="color: #3A7FCF;">Rhythm Hotkey</span>': 'Hotkey to activate Rhythm technique',
            '<span style="color: #3A7FCF;">Rhythm Skill Delay</span>': 'Delay after skill before charge attack (seconds)',
            '<span style="color: #3A7FCF;">Rhythm Charge Duration</span>': 'How long to hold charge attack (seconds)',
            '<span style="color: #3A7FCF;">Rhythm Shoot Delay</span>': 'Delay before shooting (seconds)',
            
            'Enable Quick Skill Cancel': '<b style="font-size: 18px; color: #4A9EFF; font-weight: bold;">QUICK SKILL CANCEL</b><br>E -> Right Click immediately',
            '<span style="color: #3A7FCF;">Quick Skill Cancel Hotkey</span>': 'Hotkey to activate quick skill cancel',
            '<span style="color: #3A7FCF;">Quick Skill Cancel Delay</span>': 'Delay between skill and cancel (seconds)',
            
            'Enable Skill Charge Combo': '<b style="font-size: 18px; color: #4A9EFF; font-weight: bold;">SKILL CHARGE COMBO</b><br>Skill -> Charge -> Skill combo',
            '<span style="color: #3A7FCF;">Skill Charge Combo Hotkey</span>': 'Hotkey to activate skill charge combo',
            '<span style="color: #3A7FCF;">Skill Charge Combo Delay</span>': 'Delay between actions (seconds)',
            
            'Enable Change Char': '<b style="font-size: 18px; color: #4A9EFF; font-weight: bold;">CHANGE CHAR</b><br>Change character to refresh Boxie',
            '<span style="color: #3A7FCF;">Change Char Hotkey</span>': 'Hotkey to change character',
        })
        
        # Hotkey config type - add keyboard options
        if '激活键' not in self.config_type:
            self.config_type['激活键'] = {'type': 'drop_down', 'options': ['x1', 'x2', '使用键盘']}
        
        # Hotkey fields will use default string input (LabelAndLineEdit)
        # No need to specify config_type for string values
        
        self.active_technique = None
        self.signal = False

    def disable(self):
        """Disable task and disconnect listener."""
        self.reset()
        self.try_disconnect_listener()
        return super().disable()

    def enable(self):
        """Enable task and connect listener."""
        self.reset()
        self.try_connect_listener()
        return super().enable()

    def reset(self):
        """Reset task state."""
        self.active_technique = None
        self.signal = False

    def run(self):
        """Main run loop - executes active technique when signal is received."""
        # For trigger tasks in onetime_tasks, return None to prevent TaskExecutor from executing
        # The task stays enabled for hotkey listening but won't be run by TaskExecutor loop
        if not (self.signal and self.active_technique):
            return None
        
        # Save technique and clear state immediately
        technique = self.active_technique
        self.signal = False
        self.active_technique = None
        
        try:
            if technique == 'rapid_fire_cancel':
                self._execute_rapid_fire_cancel()
            elif technique == 'rhythm':
                self._execute_rhythm()
            elif technique == 'quick_skill_cancel':
                self._execute_quick_skill_cancel()
            elif technique == 'skill_charge_combo':
                self._execute_skill_charge_combo()
            elif technique == 'change_char':
                self._execute_change_char()
        except Exception as e:
            logger.error(f"Error executing technique {technique}: {e}")
        
        # Return False to indicate this execution is done (but task stays enabled)
        return False

    def _execute_rhythm(self):
        """Rhythm technique: E -> Hold Left Click -> Right Click"""
        if not self.config.get('Enable Rhythm', True):
            return
        
        try:
            # Press E (skill) - use combat key directly
            combat_key = self.get_combat_key()
            self.send_key_down(combat_key)
            self.sleep(0.05)
            self.send_key_up(combat_key)
            self.sleep(self.config.get('<span style="color: #3A7FCF;">Rhythm Skill Delay</span>', 0.05))
            
            # Hold left click (charge attack)
            self.mouse_down(key='left')
            self.sleep(self.config.get('<span style="color: #3A7FCF;">Rhythm Charge Duration</span>', 0.1))
            self.mouse_up(key='left')
            
            # Right click (shoot)
            self.sleep(self.config.get('<span style="color: #3A7FCF;">Rhythm Shoot Delay</span>', 0.05))
            self.mouse_down(key='right')
            self.sleep(0.05)
            self.mouse_up(key='right')
            
            self.log_info("Rhythm technique executed")
        except Exception as e:
            logger.error(f"Error in _execute_rhythm: {e}")
            raise

    def _execute_quick_skill_cancel(self):
        """Quick skill cancel: E -> Right Click immediately"""
        if not self.config.get('Enable Quick Skill Cancel', True):
            return
        
        try:
            # Press E (skill) - use combat key directly
            combat_key = self.get_combat_key()
            self.send_key_down(combat_key)
            self.sleep(0.05)
            self.send_key_up(combat_key)
            self.sleep(self.config.get('<span style="color: #3A7FCF;">Quick Skill Cancel Delay</span>', 0.05))
            
            # Right click to cancel
            self.mouse_down(key='right')
            self.sleep(0.05)
            self.mouse_up(key='right')
            
            self.log_info("Quick skill cancel executed")
        except Exception as e:
            logger.error(f"Error in _execute_quick_skill_cancel: {e}")
            raise

    def _execute_skill_charge_combo(self):
        """Skill -> Charge -> Skill combo"""
        if not self.config.get('Enable Skill Charge Combo', True):
            return
        
        try:
            delay = self.config.get('<span style="color: #3A7FCF;">Skill Charge Combo Delay</span>', 0.1)
            combat_key = self.get_combat_key()
            
            # First skill
            self.send_key_down(combat_key)
            self.sleep(0.05)
            self.send_key_up(combat_key)
            self.sleep(delay)
            
            # Charge attack
            self.mouse_down(key='left')
            self.sleep(0.1)
            self.mouse_up(key='left')
            self.sleep(delay)
            
            # Second skill
            self.send_key_down(combat_key)
            self.sleep(0.05)
            self.send_key_up(combat_key)
            
            self.log_info("Skill charge combo executed")
        except Exception as e:
            logger.error(f"Error in _execute_skill_charge_combo: {e}")
            raise

    def _execute_rapid_fire_cancel(self):
        """Rapid fire: Hold Right Click and spam Ctrl"""
        if not self.config.get('Enable Rapid Fire Cancel', True):
            return
        
        try:
            interval = self.config.get('<span style="color: #3A7FCF;">Rapid Fire Cancel Interval</span>', 0.1)
            duration = self.config.get('<span style="color: #3A7FCF;">Rapid Fire Cancel Duration</span>', 1.0)  # How long to hold right click
            
            # Hold right click
            self.mouse_down(key='right')
            
            # Spam ctrl while holding right click
            start_time = time.time()
            while time.time() - start_time < duration:
                # Press and release ctrl
                self.send_key_down('lcontrol')
                self.sleep(0.02)
                self.send_key_up('lcontrol')
                self.sleep(interval)
            
            # Release right click
            self.mouse_up(key='right')
            
            self.log_info("Rapid fire executed")
        except Exception as e:
            logger.error(f"Error in _execute_rapid_fire_cancel: {e}")
            raise

    def _check_hotkey_match(self, key, hotkey_name):
        """Check if pressed key matches the configured hotkey."""
        if not self.config.get(f'Enable {hotkey_name}', True):
            return False
        
        # Use HTML-styled key name for config access
        html_key = f'<span style="color: #3A7FCF;">{hotkey_name} Hotkey</span>'
        configured_key = self.config.get(html_key, '').lower().strip()
        if not configured_key:
            logger.debug(f"Hotkey not configured for {hotkey_name}")
            return False
        
        # Use the normalize_hotkey method from BaseListenerTask
        try:
            expected_key = self.normalize_hotkey(configured_key)
            matched = self.key_equal(key, expected_key)
            if matched:
                logger.info(f"Hotkey matched: {hotkey_name} (configured: {configured_key})")
            return matched
        except Exception as e:
            logger.warning(f"Error checking hotkey match for {hotkey_name} (key: {configured_key}): {e}")
        
        return False

    def on_global_press(self, key):
        """Handle keyboard hotkey presses."""
        if self._executor.paused:
            return
        
        # Only activate if game window is in focus
        if not og.device_manager.hwnd_window.is_foreground():
            return
        
        # Allow new activation even if signal is set (will queue)
        # But don't allow if we're still processing the same technique
        if self.signal and self.active_technique:
            # Still processing, skip
            return
        
        # Check each technique's hotkey and set signal
        if self._check_hotkey_match(key, 'Rapid Fire Cancel'):
            self.active_technique = 'rapid_fire_cancel'
            self.signal = True
            self.log_info("Rapid fire activated")
        elif self._check_hotkey_match(key, 'Rhythm'):
            self.active_technique = 'rhythm'
            self.signal = True
            self.log_info("Rhythm technique activated")
        elif self._check_hotkey_match(key, 'Quick Skill Cancel'):
            self.active_technique = 'quick_skill_cancel'
            self.signal = True
            self.log_info("Quick skill cancel activated")
        elif self._check_hotkey_match(key, 'Skill Charge Combo'):
            self.active_technique = 'skill_charge_combo'
            self.signal = True
            self.log_info("Skill charge combo activated")
        elif self._check_hotkey_match(key, 'Change Char'):
            self.active_technique = 'change_char'
            self.signal = True
            self.log_info("Change char activated")

    def on_global_click(self, x, y, button, pressed):
        """Handle mouse button clicks (for mouse-based activation if needed)."""
        # Can be extended to support mouse button activation
        pass

    def find_image_template(self, template_img, threshold: float = 0.7):
        """Find template image in current frame using template matching"""
        if template_img is None:
            return None
        
        frame = self.frame
        if frame is None:
            return None
        
        # Convert frame to BGR if needed
        if len(frame.shape) == 3:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
        else:
            frame_gray = frame
            template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
        
        # Template matching
        result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            h, w = template_gray.shape[:2]
            x = max_loc[0] + w // 2
            y = max_loc[1] + h // 2
            return (x, y)
        
        return None
    
    def wait_for_png(self, png_path: str, timeout: float = 10.0):
        """Wait for PNG image to appear on screen using template matching"""
        logger.info(f"Waiting for PNG image: {png_path}")
        deadline = time.monotonic() + timeout
        
        # Load template image
        if not os.path.exists(png_path):
            logger.error(f"PNG file not found: {png_path}")
            return None
        
        try:
            pil_img = Image.open(png_path)
            img_array = np.array(pil_img)
            template = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        except Exception as e:
            logger.error(f"Failed to load PNG template {png_path}: {e}")
            return None
        
        while time.monotonic() < deadline:
            location = self.find_image_template(template, threshold=0.7)
            if location:
                image_name = Path(png_path).stem
                logger.info(f"Found PNG image: {image_name}")
                return location
            self.sleep(0.2)
            self.next_frame()
        
        image_name = Path(png_path).stem
        logger.warning(f"Timeout waiting for PNG image: {image_name}")
        return None

    def _execute_change_char(self):
        """Change character to refresh Boxie"""
        if not self.config.get('Enable Change Char', True):
            return
        
        try:
            # Move mouse to safe position to prevent interference
            if hasattr(self, 'move_mouse_to_safe_position'):
                self.move_mouse_to_safe_position(save_current_pos=False)
            
            mod_fish_folder = Path.cwd() / 'mod' / 'fish'
            armoury_path = mod_fish_folder / 'armoury.png'
            nextchar_path = mod_fish_folder / 'nextchar.png'
            deploy_path = mod_fish_folder / 'deploy.png'
            
            # Step 1: Press ESC
            logger.info("Pressing ESC to open menu")
            self.send_key("esc", down_time=0.1)
            self.sleep(1.0)
            self.next_frame()
            
            # Step 2: Look for armoury.png and click on it
            logger.info("Looking for armoury.png")
            armoury_location = self.wait_for_png(str(armoury_path), timeout=1.0)
            if not armoury_location:
                logger.error("armoury.png not found")
                return
            
            logger.info(f"Found armoury.png at {armoury_location}, clicking")
            self.click(armoury_location[0], armoury_location[1])
            self.sleep(1.0)
            self.next_frame()
            
            # Step 2.5: Check if armourynotavailable.png appears (armoury not available)
            armourynotavailable_path = mod_fish_folder / 'armourynotavailable.png'
            if armourynotavailable_path.exists():
                logger.info("Checking for armourynotavailable.png")
                notavailable_location = self.wait_for_png(str(armourynotavailable_path), timeout=0.5)
                if notavailable_location:
                    logger.warning("armourynotavailable.png detected - armoury not available, pressing ESC and aborting")
                    self.send_key("esc", down_time=0.1)
                    self.sleep(0.5)
                    return
            
            # Step 3: Wait for nextchar.png (with 1 second timeout check)
            logger.info("Waiting for nextchar.png")
            # Check if nextchar.png appears within 1 second
            nextchar_location = self.wait_for_png(str(nextchar_path), timeout=1.0)
            if not nextchar_location:
                logger.warning("nextchar.png not found within 1 second, pressing ESC and aborting")
                self.send_key("esc", down_time=0.1)
                self.sleep(0.5)
                return
            
            # Step 4: Press S key
            logger.info("Pressing S key")
            self.send_key("s", down_time=0.1)
            self.sleep(1.0)  # Wait longer for deploy button to appear
            self.next_frame()
            
            # Step 5: Click on deploy (if deploy.png exists, otherwise try to find deploy button)
            logger.info("Looking for deploy button")
            if deploy_path.exists():
                deploy_location = self.wait_for_png(str(deploy_path), timeout=5.0)
                if deploy_location:
                    logger.info(f"Found deploy at {deploy_location}, clicking")
                    # Wait a bit to ensure button is ready and clickable
                    self.sleep(0.5)
                    self.next_frame()
                    # Click with proper timing - use click method which handles positioning
                    self.click(deploy_location[0], deploy_location[1])
                    self.sleep(0.15)  # Small delay to ensure click is registered
                    # Click again to ensure it registers (sometimes first click just highlights)
                    self.click(deploy_location[0], deploy_location[1])
                    self.sleep(1.5)  # Wait longer to ensure click registers
                    self.next_frame()
                else:
                    logger.warning("deploy.png not found, trying to continue")
            else:
                # deploy.png doesn't exist, try to find deploy using OCR or continue
                logger.info("deploy.png not found in mod/fish folder, continuing")
                self.sleep(0.5)
            
            # Step 6: Press ESC
            logger.info("Pressing ESC")
            self.send_key("esc", down_time=0.1)
            self.sleep(1.0)
            self.next_frame()
            
            # Step 7: Wait for armoury.png again
            logger.info("Waiting for armoury.png again")
            armoury_location2 = self.wait_for_png(str(armoury_path), timeout=1.0)
            if armoury_location2:
                # Step 8: Press ESC again (don't click on armoury)
                logger.info("Found armoury.png, pressing ESC again")
                self.send_key("esc", down_time=0.1)
                self.sleep(0.5)
            else:
                logger.warning("armoury.png not found after deploy, but continuing")
            
            self.log_info("Change char completed")
        except Exception as e:
            logger.error(f"Error in _execute_change_char: {e}")
            raise

