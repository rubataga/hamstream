import json
import yaml
import stream_controller
import time
# from program_tools import program_schedule_builder

CONFIG = yaml.safe_load(open('config.yaml'))

remote = stream_controller.StreamController(CONFIG)

def load_json(file_name):
    """Load JSON file with error handling"""
    try:
        with open(file_name) as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {file_name}: {e}")
        exit(1)

def load_yaml(file_name):
    """Load YAML file with error handling"""
    try:
        with open(file_name) as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {file_name}: {e}")
        return None

if __name__ == "__main__":
    print("=== OBS Video Switcher ===")
    
    # Load environment and schedule
    
    schedule = load_yaml("program_schedules/program_schedule.yaml")
    
    # Extract video paths from schedule
    # video_paths = [item["video_path"] for item in schedule]
    # print(f"[DEBUG] Loaded video paths: {video_paths}")
    
    # Connect to OBS
    remote.connect_obs()
    
    try:
        for item in schedule:
            video_path = item['path']
            video_length = item['length']
            remote.switch_video(video_path)
            time.sleep(video_length)  # Wait for the duration of the video
    except KeyboardInterrupt:
        print("\n[STATUS] User stopped the switcher")
    finally:
        if remote.obs:
            remote.obs.disconnect()
            print("[STATUS] Disconnected from OBS")