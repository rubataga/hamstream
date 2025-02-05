import os
from program_tools.video_processor import get_video_length
from program_tiles.video_tile import VideoTile

def create_tile_initializers(tile_paths, output_dir='./schedules/tile_initializers'):
    """Create tile initializer YAML files for a list of tile paths."""
    os.makedirs(output_dir, exist_ok=True)
    
    for tile_path in tile_paths:
        if not os.path.exists(tile_path):
            print(f"[ERROR] Tile file does not exist: {tile_path}")
            continue
        
        video_length = get_video_length(tile_path)
        if video_length is None:
            print(f"[ERROR] Could not get length for tile: {tile_path}")
            continue
        
        tile_title = os.path.basename(tile_path)
        video_tile = VideoTile(title=tile_title, path=tile_path)
        
        tile_file_path = os.path.join(output_dir, f"{tile_title}.yaml")
        video_tile.save_to_yaml(tile_file_path)
        
        print(f"[SUCCESS] Tile initializer saved to {tile_file_path}")