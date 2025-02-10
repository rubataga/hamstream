from obswebsocket import obsws, requests
import time
from datetime import datetime
from rich import print

class StreamController:
    def __init__(self, config):
        self.config = config['OBS']
        self.obs = None
        self.current_index = 0

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

    def switch_tile(self, tile):
        """Switch the tile source with error handling"""
        tile_path = tile.path
        try:
            print(f"Switched to [bold purple]{tile.title}[/bold purple] at {datetime.now().strftime('%H:%M:%S')}")
            self.obs.call(requests.SetInputSettings(
                inputName=self.config["source_name"],
                inputSettings={"local_file": tile_path}
            ))
            self.obs.call(requests.TriggerMediaInputAction(
                inputName=self.config["source_name"],
                mediaAction="OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART"
            ))
            # self.obs.call(requests.SetMediaInputCursor(
            #     inputName=self.config["source_name"],
            #     mediaCursor=0
            # ))
        except Exception as e:
            print(f"[bold red][ERROR] Failed to switch tile: {e}[/bold red]")

    def main_loop(self, queue):
        """Main switching logic with user input"""
        print("\n[STATUS] Starting tile switcher")

        while self.current_index < len(queue):
            tile, duration = queue[self.current_index]
            self.switch_tile(tile)
            
            for _ in range(int(duration)):
                command = input("Enter command (skip/back/exit): ").strip().lower()
                if command == "skip":
                    break
                elif command == "back":
                    self.current_index = max(0, self.current_index - 1)
                    break
                elif command == "exit":
                    self.disconnect()
                    return
                time.sleep(1)

            if command != "back":
                self.current_index += 1

        print("[bold red][STATUS] Stream ended[/bold red]")

    def disconnect(self):
        """Sever OBS connection"""
        if self.obs:
            self.obs.disconnect()
            print("[bold red][STATUS] Disconnected from OBS[/bold red]")