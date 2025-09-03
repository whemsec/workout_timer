import time
import threading
import winsound
import tkinter as tk
from tkinter import ttk
import sys

class WorkoutTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Timer - Multiple Workout Types")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        # Timer state
        self.is_running = False
        self.timer_thread = None
        self.countdown_value = 60
        self.workout_type = "box"  # Default workout type
        
        # Create UI elements
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title label
        title_label = ttk.Label(main_frame, text="Workout Timer", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Workout type selection
        workout_frame = ttk.Frame(main_frame)
        workout_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        workout_label = ttk.Label(workout_frame, text="Workout Type:", font=("Arial", 12))
        workout_label.grid(row=0, column=0, padx=(0, 10))
        
        self.workout_var = tk.StringVar(value="box")
        self.workout_combo = ttk.Combobox(workout_frame, textvariable=self.workout_var, 
                                         values=["box", "easy cardio", "intermediate cardio"], state="readonly", width=15)
        self.workout_combo.grid(row=0, column=1)
        self.workout_combo.bind("<<ComboboxSelected>>", self.on_workout_change)
        
        # Timer display
        self.timer_label = ttk.Label(main_frame, text="01:00", font=("Arial", 36, "bold"))
        self.timer_label.grid(row=2, column=0, columnspan=2, pady=(0, 30))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to start", font=("Arial", 12))
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(0, 30))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2)
        
        self.play_button = ttk.Button(button_frame, text="Start", command=self.toggle_timer, width=15)
        self.play_button.grid(row=0, column=0, padx=(0, 10))
        
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, width=15)
        self.reset_button.grid(row=0, column=1)
    
    def on_workout_change(self, event=None):
        """Handle workout type change"""
        self.workout_type = self.workout_var.get()
        if self.workout_type == "box":
            self.countdown_value = 60
        elif self.workout_type == "easy cardio":
            self.countdown_value = 30
        else:  # intermediate cardio
            self.countdown_value = 45
        self.update_timer_display()
        self.status_label.config(text=f"Selected: {self.workout_type}")
        
    def get_workout_duration(self):
        """Get the duration for the selected workout type"""
        if self.workout_type == "box":
            return 60
        elif self.workout_type == "easy cardio":
            return 30
        else:  # intermediate cardio
            return 45
    
    def get_workout_description(self):
        """Get the description for the selected workout type"""
        if self.workout_type == "box":
            return "Rest period"
        elif self.workout_type == "easy cardio":
            return "Cardio interval"
        else:  # intermediate cardio
            return "Intermediate Cardio"
        
    def play_sound(self):
        """Play a beep sound to signal the end of an interval"""
        try:
            # Play a beep sound (frequency: 800Hz, duration: 500ms)
            winsound.Beep(2000, 400)
            
        except:
            # Fallback if winsound fails
            print("\a")  # System bell sound
    
    def update_timer_display(self):
        """Update the timer display with current countdown value"""
        minutes = self.countdown_value // 60
        seconds = self.countdown_value % 60
        if minutes > 0:
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        else:
            self.timer_label.config(text=f"{seconds:02d}s")
    
    def countdown_timer(self):
        """Count down based on workout type and automatically restart"""
        while self.is_running:
            # Reset countdown for new interval
            self.countdown_value = self.get_workout_duration()
            self.update_timer_display()
            workout_desc = self.get_workout_description()
            self.status_label.config(text=f"{workout_desc} started")
            
            # Countdown loop
            while self.countdown_value > 0 and self.is_running:
                time.sleep(1)
                self.countdown_value -= 1
                self.update_timer_display()
                
                # Update status
                if self.countdown_value > 0:
                    self.status_label.config(text=f"{workout_desc}: {self.countdown_value} seconds remaining")
                else:
                    self.status_label.config(text=f"{workout_desc} complete!")
            
            # Play sound when interval is complete
            if self.is_running:
                self.play_sound()
                # self.status_label.config(text=f"{workout_desc} complete! Starting next interval in 2 seconds...")
                # time.sleep(2)  # Brief pause before next interval
    
    def toggle_timer(self):
        """Start or stop the timer"""
        if not self.is_running:
            # Start timer
            self.is_running = True
            self.play_button.config(text="Stop")
            self.status_label.config(text="Timer running...")
            
            # Start countdown in separate thread
            self.timer_thread = threading.Thread(target=self.countdown_timer, daemon=True)
            self.timer_thread.start()
        else:
            # Stop timer
            self.is_running = False
            self.play_button.config(text="Start")
            self.status_label.config(text="Timer stopped")
    
    def reset_timer(self):
        """Reset the timer to initial state"""
        self.is_running = False
        self.countdown_value = self.get_workout_duration()
        self.update_timer_display()
        self.play_button.config(text="Start")
        self.status_label.config(text="Ready to start")
    
    def on_closing(self):
        """Handle window closing"""
        self.is_running = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = WorkoutTimer(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
