import stream_controller
import time
from utils.file_utils import load_yaml
from rich import print

CONFIG = load_yaml('config.yaml')
remote = stream_controller.StreamController(CONFIG)

if __name__ == "__main__":
    print("[bold yellow]=== OBS Video Switcher ===[/bold yellow]")
    
    # Load program schedule
    queue = load_yaml("program schedules/program_schedule.yaml")
    
    if queue is None:
        print("[bold red][ERROR] Program schedule could not be loaded.[/bold red]")
        exit(1)

    for index, item in enumerate(queue):
        print(f"{index + 1}. {item['title']} ({item['length']}s)")
    
    # Connect to OBS
    remote.connect_obs()
    
    try:
        remote.main_loop(queue)
    except KeyboardInterrupt:
        print("\n[bold red][STATUS] User stopped the switcher[/bold red]")
    finally:
        if remote.obs:
            remote.disconnect()