from .program_tile import ProgramTileFactory

# Discover and register all tile classes in the program_tiles package
ProgramTileFactory.discover_tile_classes(__import__('program_tiles'))