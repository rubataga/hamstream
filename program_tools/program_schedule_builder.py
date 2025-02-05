import os
from program_tools.video_processor import get_video_length
from utils.file_utils import load_json, save_yaml

def build_default_program_schedule():
    videos_to_program = load_json("./schedule.json")
    video_paths = [item["video_path"] for item in videos_to_program]
    print(f"[DEBUG] Loaded video paths: {video_paths}")
    build_program_schedule(video_paths)

def build_program_schedule(video_paths, output_file='./program schedules/program_schedule.yaml'):
    """Build a program schedule from a list of video paths and save it to a YAML file."""
    schedule = []
    
    for video_path in video_paths:
        if not os.path.exists(video_path):
            print(f"[ERROR] Video file does not exist: {video_path}")
            continue
        
        video_length = get_video_length(video_path)
        if video_length is None:
            print(f"[ERROR] Could not get length for video: {video_path}")
            continue
        
        video_title = os.path.basename(video_path)
        schedule.append({
            'title': video_title,
            'path': video_path,
            'length': video_length,
        })
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    save_yaml(schedule, output_file)
    
    print(f"[SUCCESS] Program schedule saved to {output_file}")

if __name__ == "__main__":
    build_default_program_schedule()