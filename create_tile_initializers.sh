#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Run the tile_initializer_builder script
python -c "
import json
from program_tools.tile_initializer_builder import create_tile_initializers
from utils.file_utils import load_json

# Load the schedule.json file
schedule = load_json('schedule.json')

# Extract video paths
video_paths = [item['video_path'] for item in schedule]

# Create tile initializers
create_tile_initializers(video_paths)
"

# Deactivate the virtual environment
deactivate