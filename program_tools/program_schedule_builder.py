import os
from program_tools.video_processor import get_video_length
from utils.file_utils import load_json, save_yaml

def build_default_program_schedule():
    tiles_to_program = load_json("./schedule.json")
    tile_paths = [tile["video_path"] for tile in tiles_to_program]
    print(f"[DEBUG] Loaded tile paths: {tile_paths}")
    build_program_schedule(tile_paths)

def build_program_schedule(tile_paths, output_file='./schedules/program_schedule.yaml'):
    """Build a program schedule from a list of tile paths and save it to a YAML file."""
    schedule = []
    
    for tile_path in tile_paths:
        tile_title = os.path.basename(tile_path)
        tile_initializer_path = f"./schedules/tile_initializers/{tile_title}.yaml"
        
        if not os.path.exists(tile_initializer_path):
            print(f"[ERROR] Tile initializer file does not exist: {tile_initializer_path}")
            continue
        
        video_length = get_video_length(tile_path)
        if video_length is None:
            print(f"[ERROR] Could not get length for tile: {tile_path}")
            continue
        
        schedule.append({
            'tile_path': tile_initializer_path,
            'duration': video_length
        })
    
    save_yaml(schedule, output_file)
    
    print(f"[SUCCESS] Program schedule saved to {output_file}")

if __name__ == "__main__":
    build_default_program_schedule()