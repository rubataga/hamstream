from program_tiles.program_tile import ProgramTile, ProgramTileFactory

class VideoTile(ProgramTile):
    def __init__(self, title, path):
        super().__init__(title, path)

    def get_type(self):
        return "video"

# Register the VideoTile class with the ProgramTileFactory
ProgramTileFactory.register_tile_class(VideoTile)