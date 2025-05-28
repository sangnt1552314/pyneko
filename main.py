import platform
import tkinter as tk

class NekoApp:
    def __init__(self, root):
        self.root = root
        
        if platform.system() == 'Darwin':
            self.root.attributes('-transparent', True)
            self.root.lift()
        if platform.system() == 'Windows':
            self.root.attributes('-transparentcolor', 'white')
        
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)  # remove window borders
        self.root.geometry("50x50")
        self.label = tk.Label(root, bg="white")
        self.label.pack(fill=tk.BOTH, expand=True)

        # Replace with your ghost image
        self.image = tk.PhotoImage(file="./assets/photo/awake.png")
        self.label.config(image=self.image, bg="white")

        # Current position of the ghost
        self.current_x = 0
        self.current_y = 0

        self.update_position()

    def update_position(self):
        # Target position (near the cursor)
        target_x = self.root.winfo_pointerx() + 20
        target_y = self.root.winfo_pointery() + 20

        # Calculate the distance to move (move 10% of the way to the target)
        move_speed = 0.1
        dx = (target_x - self.current_x) * move_speed
        dy = (target_y - self.current_y) * move_speed

        # Update the current position
        self.current_x += dx
        self.current_y += dy

        # Position the window
        self.root.geometry(f"+{int(self.current_x)}+{int(self.current_y)}")

        # Update more frequently for smoother animation
        self.root.after(300, self.update_position)  # update every 30 ms

if __name__ == "__main__":
    root = tk.Tk()
    app = NekoApp(root)
    root.mainloop()
