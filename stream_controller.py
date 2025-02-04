from obswebsocket import obsws, requests
from dotenv import load_dotenv
import time
from datetime import datetime

class StreamController:
    def __init__(self, config):
        self.config = config['OBS']
        self.obs = None

    def connect_obs(self):
        """Establish connection to OBS WebSocket with error handling"""
        print("[DEBUG] Attempting OBS connection...")
        try:
            self.obs = obsws(self.config['host'], self.config['port'], self.config['server_password'])
            self.obs.connect()
            print(f"[SUCCESS] Connected to OBS at {self.config['host']}:{self.config['port']}")
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            print("Check: 1) OBS is running 2) WebSocket enabled 3) Correct password/port")
            exit(1)

    def switch_video(self, video_path):
        """Switch the video source with error handling"""
        try:
            print(f"[ACTION] Switching to {video_path} at {datetime.now().strftime('%H:%M:%S')}")
            self.obs.call(requests.SetInputSettings(
                inputName=self.config["source_name"],
                inputSettings={"local_file": video_path}
            ))
        except Exception as e:
            print(f"[ERROR] Failed to switch video: {e}")

    def main_loop(self,video_paths):
        """Main switching logic with visual feedback"""
        SWITCH_INTERVAL = self.config['switch_interval']
        print("\n[STATUS] Starting video switcher")
        print(f"Cycle: {SWITCH_INTERVAL}s | Videos: {video_paths}\n")
        
        current_index = 0
        while True:
            # Get next video path
            video_path = video_paths[current_index]
            
            # Perform the switch
            self.switch_video(video_path)
            
            # Update index for next iteration
            current_index = (current_index + 1) % len(video_paths)
            
            # Wait for interval
            print(f"[SLEEP] Waiting {SWITCH_INTERVAL}s...\n")
            time.sleep(SWITCH_INTERVAL)

    def disconnect(self):
        """Sever OBS connection"""
        self.obs.disconnect()
        print("[DEBUG] Disconnected from OBS")