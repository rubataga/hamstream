import json
import os
from dotenv import load_dotenv
from stream_controls import obs_controls

load_dotenv()

OBS_PASSWORD = os.getenv("OBS_PASSWORD")

def load_json(file_name):
    """Load JSON file with error handling"""
    try:
        with open(file_name) as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {file_name}: {e}")
        exit(1)

if __name__ == "__main__":
    print("=== OBS Video Switcher ===")
    
    # Load environment and schedule
    schedule = load_json("./schedule.json")
    
    # Extract video paths from schedule
    video_paths = [item["video_path"] for item in schedule]
    # print(f"[DEBUG] Loaded video paths: {video_paths}")
    
    # Connect to OBS
    obs_connection = obs_controls.connect_obs(OBS_PASSWORD)
    
    try:
        obs_controls.main_loop(obs_connection, video_paths)
    except KeyboardInterrupt:
        print("\n[STATUS] User stopped the switcher")
    finally:
        obs_connection.disconnect()
        print("[STATUS] Disconnected from OBS")