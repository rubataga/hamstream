from obswebsocket import obsws, requests
import time
from datetime import datetime
from rich import print

class StreamController:
    def __init__(self, config):
        self.config = config['OBS']
        self.obs = None
        self.skip = False
        # self.console = Console()

    def connect_obs(self):
        """Establish connection to OBS WebSocket with error handling"""
        try:
            self.obs = obsws(self.config['host'], self.config['port'], self.config['server_password'])
            self.obs.connect()
            print(f"[bold green][SUCCESS] Connected to OBS at {self.config['host']}:{self.config['port']}[/bold green]")
        except Exception as e:
            print(f"[bold red][ERROR] Connection failed: {e}[/bold red]")
            print("Check: 1) OBS is running 2) WebSocket enabled 3) Correct password/port")
            exit(1)

    def switch_video(self, video):
        """Switch the video source with error handling"""
        video_path = video['path']
        try:
            print(f"Switched to [bold purple]{video['title']}[/bold purple] at {datetime.now().strftime('%H:%M:%S')}")
            self.obs.call(requests.SetInputSettings(
                inputName=self.config["source_name"],
                inputSettings={"local_file": video_path}
            ))
        except Exception as e:
            print(f"[bold red][ERROR] Failed to switch video: {e}[/bold red]")

    def main_loop(self, queue):
        """Main switching logic with visual feedback"""
        print("\n[STATUS] Starting video switcher")

        for index, video in enumerate(queue):
            self.switch_video(video)
            
            if index == len(queue) - 1:
                task_description = "Ending stream in..."
            else:
                task_description = f"Switching to [bold purple]{queue[(index + 1) % len(queue)]['title']}[/bold purple] in..."
            print(f"{task_description} {video['length']}s")
            
            time.sleep(video['length'])

    def disconnect(self):
        """Sever OBS connection"""
        self.obs.disconnect()
        print("[bold red][STATUS] Disconnected from OBS[/bold red]")