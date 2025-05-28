import platform
import tkinter as tk
import math
import os
import configparser
from dataclasses import dataclass
import pygame  # For sound support

@dataclass
class Config:
    speed: int = 2
    scale: float = 2.0
    quiet: bool = False
    mouse_passthrough: bool = False

class NekoApp:
    def __init__(self, root):
        self.root = root
        self.config = self.load_config()
        
        # Initialize pygame for sound
        if not self.config.quiet:
            pygame.mixer.init()
            self.sounds = self.load_sounds()
        
        if platform.system() == 'Darwin':
            self.root.attributes('-transparent', True)
            self.root.lift()
        if platform.system() == 'Windows':
            self.root.attributes('-transparentcolor', 'white')

        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # Scale window size based on config
        base_size = 32
        window_size = int(base_size * self.config.scale)
        self.root.geometry(f"{window_size}x{window_size}")
        
        self.label = tk.Label(root, bg="white")
        self.label.pack(fill=tk.BOTH, expand=True)

        # Load all sprite images
        self.sprites = self.load_sprites()
        self.current_sprite = "awake"
        self.last_sprite = None
        
        # Animation state
        self.state = 0
        self.count = 0
        self.min_count = 8
        self.max_count = 16
        self.waiting = False
        
        # Position tracking
        self.current_x = self.root.winfo_screenwidth() // 2
        self.current_y = self.root.winfo_screenheight() // 2
        self.distance = 0
        
        # Bind left click to toggle waiting state
        self.root.bind('<Button-1>', self.toggle_waiting)
        
        self.update_position()

    def load_config(self):
        config = Config()
        parser = configparser.ConfigParser()
        
        if os.path.exists('neko.ini'):
            parser.read('neko.ini')
            if 'DEFAULT' in parser:
                config.speed = parser.getint('DEFAULT', 'speed', fallback=2)
                config.scale = parser.getfloat('DEFAULT', 'scale', fallback=2.0)
                config.quiet = parser.getboolean('DEFAULT', 'quiet', fallback=False)
                config.mouse_passthrough = parser.getboolean('DEFAULT', 'mousepassthrough', fallback=False)
        
        return config

    def load_sprites(self):
        sprites = {}
        sprite_names = ['awake', 'sleep', 'up1', 'up2', 'down1', 'down2', 
                       'left1', 'left2', 'right1', 'right2', 'upleft1', 'upleft2',
                       'upright1', 'upright2', 'downleft1', 'downleft2', 
                       'downright1', 'downright2']
        
        for name in sprite_names:
            try:
                sprites[name] = tk.PhotoImage(file=f"./assets/photo/{name}.png")
            except:
                # Fallback to awake.png if sprite doesn't exist
                sprites[name] = tk.PhotoImage(file="./assets/photo/awake.png")
        
        return sprites

    def load_sounds(self):
        sounds = {}
        sound_names = ['idle3', 'awake', 'sleep']
        
        for name in sound_names:
            try:
                sounds[name] = pygame.mixer.Sound(f"./assets/sounds/{name}.wav")
            except:
                print(f"Could not load sound: {name}")
        
        return sounds

    def play_sound(self, sound_name):
        if not self.config.quiet and sound_name in self.sounds:
            self.sounds[sound_name].play()

    def toggle_waiting(self, event):
        self.waiting = not self.waiting

    def update_position(self):
        if not self.waiting:
            # Get cursor position
            target_x = self.root.winfo_pointerx()
            target_y = self.root.winfo_pointery()

            # Calculate distance to cursor
            dx = target_x - self.current_x
            dy = target_y - self.current_y
            self.distance = abs(dx) + abs(dy)

            if self.distance > 32:  # Only move if far enough from cursor
                # Calculate angle to cursor
                angle = math.atan2(dy, dx)
                angle_deg = math.degrees(angle)
                if angle_deg < 0:
                    angle_deg += 360

                # Update position based on angle
                speed = self.config.speed
                self.current_x += int(math.cos(angle) * speed)
                self.current_y += int(math.sin(angle) * speed)

                # Update sprite based on movement direction
                self.update_movement_sprite(angle_deg)
            else:
                self.update_idle_state()

        # Keep within screen bounds
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.current_x = max(0, min(self.current_x, screen_width))
        self.current_y = max(0, min(self.current_y, screen_height))

        # Update window position
        self.root.geometry(f"+{int(self.current_x)}+{int(self.current_y)}")
        
        # Update sprite
        if self.current_sprite != self.last_sprite:
            sprite_key = self.current_sprite
            if sprite_key in self.sprites:
                self.label.config(image=self.sprites[sprite_key])
                self.last_sprite = self.current_sprite

        # Animation counter
        self.count += 1
        if self.count > self.max_count:
            self.count = 0
            if self.state > 0:
                self.state += 1
                if self.state == 13:
                    self.play_sound('sleep')

        # Schedule next update
        self.root.after(20, self.update_position)

    def update_movement_sprite(self, angle):
        # Convert angle to 8-directional sprite
        if self.state >= 13:
            self.play_sound('awake')
            self.state = 0
        
        frame = '1' if self.count < self.min_count else '2'
        
        if 247.5 <= angle <= 292.5:  # up
            self.current_sprite = f'up{frame}'
        elif 292.5 < angle <= 337.5:  # upright
            self.current_sprite = f'upright{frame}'
        elif angle <= 22.5 or angle > 337.5:  # right
            self.current_sprite = f'right{frame}'
        elif 22.5 < angle <= 67.5:  # downright
            self.current_sprite = f'downright{frame}'
        elif 67.5 < angle <= 112.5:  # down
            self.current_sprite = f'down{frame}'
        elif 112.5 < angle <= 157.5:  # downleft
            self.current_sprite = f'downleft{frame}'
        elif 157.5 < angle <= 202.5:  # left
            self.current_sprite = f'left{frame}'
        elif 202.5 < angle <= 247.5:  # upleft
            self.current_sprite = f'upleft{frame}'

    def update_idle_state(self):
        if self.state == 0:
            self.state = 1
        
        if 1 <= self.state <= 3:
            self.current_sprite = 'awake'
        elif 4 <= self.state <= 6:
            self.current_sprite = 'scratch1' if self.count < self.min_count else 'scratch2'
        elif 7 <= self.state <= 9:
            self.current_sprite = 'wash1' if self.count < self.min_count else 'wash2'
        elif 10 <= self.state <= 12:
            self.min_count = 32
            self.max_count = 64
            self.current_sprite = 'yawn'
            if self.state == 10 and self.count == self.min_count:
                self.play_sound('idle3')
        else:
            self.current_sprite = 'sleep'

if __name__ == "__main__":
    root = tk.Tk()
    app = NekoApp(root)
    root.mainloop()
