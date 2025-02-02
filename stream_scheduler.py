import json
import time
import yaml
import os
from datetime import datetime
from obswebsocket import obsws, requests
from dotenv import load_dotenv

load_dotenv()

OBS_PASSWORD = os.getenv("OBS_PASSWORD")
print('[env debug]',OBS_PASSWORD)
# --------------------------
# Configuration Section
# --------------------------
# CONFIG = {
#     "host": "localhost",
#     "port": 4455,
#     "source_name": "VideoPlayer"  # Must match your OBS media source name
# }

with open('config.yaml', 'r') as file:
    CONFIG = yaml.safe_load(file)
    OBS_CONFIG = CONFIG['OBS']

print(CONFIG)

SWITCH_INTERVAL = 20  # Seconds between switches
# --------------------------

def load_json(file_name):
    """Load JSON file with error handling"""
    try:
        with open(file_name) as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {file_name}: {e}")
        exit(1)

def connect_obs(password):
    """Establish connection to OBS WebSocket with error handling"""
    print("[DEBUG] Attempting OBS connection...")
    print('config debug',OBS_CONFIG)
    print('host debug',OBS_CONFIG['host'])
    print('port debug',OBS_CONFIG['port'])
    try:
        obs = obsws(OBS_CONFIG['host'], 
                   OBS_CONFIG['port'], 
                   password)
        obs.connect()
        print(f"[SUCCESS] Connected to OBS at {OBS_CONFIG['host']}:{OBS_CONFIG['port']}")
        return obs
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        print("Check: 1) OBS is running 2) WebSocket enabled 3) Correct password/port")
        exit(1)

def switch_video(obs, video_path):
    """Switch the video source with error handling"""
    try:
        print(f"[ACTION] Switching to {video_path} at {datetime.now().strftime('%H:%M:%S')}")
        
        # Send command to OBS

        # response = obs.call(requests.GetInputSettings(
        #     inputName="VideoPlayer"
        # ))
        # print(f"[DEBUG] Source settings {response}")

        obs.call(requests.SetInputSettings(
            inputName=OBS_CONFIG["source_name"],
            inputSettings={"local_file": video_path}
        ))
        
        # # Verify update
        # response = obs.call(requests.GetSourceSettings(sourceName=CONFIG["source_name"]))
        # print(f"[DEBUG] Current source: {response.datain['sourceSettings']['local_file']}")
        
    except Exception as e:
        print(f"[ERROR] Failed to switch video: {e}")

def main_loop(obs, video_paths):
    """Main switching logic with visual feedback"""
    print("\n[STATUS] Starting video switcher")
    print(f"Cycle: {SWITCH_INTERVAL}s | Videos: {video_paths}\n")
    
    current_index = 0
    while True:
        # Get next video path
        video_path = video_paths[current_index]
        
        # Perform the switch
        switch_video(obs, video_path)
        
        # Update index for next iteration
        current_index = (current_index + 1) % len(video_paths)
        
        # Wait for interval
        print(f"[SLEEP] Waiting {SWITCH_INTERVAL}s...\n")
        time.sleep(SWITCH_INTERVAL)

if __name__ == "__main__":
    print("=== OBS Video Switcher ===")
    
    # Load environment and schedule
    schedule = load_json("./schedule.json")
    
    # Extract video paths from schedule
    video_paths = [item["video_path"] for item in schedule]
    print(f"[DEBUG] Loaded video paths: {video_paths}")
    
    # Connect to OBS
    obs_connection = connect_obs(OBS_PASSWORD)
    
    try:
        main_loop(obs_connection, video_paths)
    except KeyboardInterrupt:
        print("\n[STATUS] User stopped the switcher")
    finally:
        obs_connection.disconnect()
        print("[STATUS] Disconnected from OBS")