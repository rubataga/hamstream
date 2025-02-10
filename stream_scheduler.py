import stream_controller
from utils.file_utils import load_yaml
from program_tiles.program_tile import ProgramTile
import program_tiles  # Ensure all tile classes are discovered and registered
from rich import print

CONFIG = load_yaml('config.yaml')
remote = stream_controller.StreamController(CONFIG)

if __name__ == "__main__":
    print("[bold yellow]=== OBS Video Switcher ===[/bold yellow]")
    
    # Load program schedule
    schedule = load_yaml("schedules/program_schedule.yaml")
    
    if schedule is None:
        print("[bold red][ERROR] Program schedule could not be loaded.[/bold red]")
        exit(1)

    queue = []
    for entry in schedule:
        tile_path = entry['tile_path']
        duration = entry['duration']
        # Dynamically create the tile from the YAML file
        program_tile = ProgramTile.from_yaml(tile_path)
        queue.append((program_tile, duration))
        print(f"{len(queue)}. {program_tile.title} ({duration}s)")

    remote.queue = queue
    # Connect to OBS
    remote.connect_obs()
    
    try:
        remote.main_loop(queue)
    except KeyboardInterrupt:
        print("\n[bold red][STATUS] User stopped the switcher[/bold red]")
    finally:
        remote.disconnect()