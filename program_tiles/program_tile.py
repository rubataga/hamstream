from abc import ABC, abstractmethod
import yaml

class ProgramTile(ABC):
    _registry = {}

    def __init__(self, title, path):
        self.title = title
        self.path = path

    @abstractmethod
    def get_type(self):
        pass

    def save_to_yaml(self, file_path):
        data = {
            'tile_class': self.__class__.__name__,
            'title': self.title,
            'path': self.path,
        }
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)

    @classmethod
    def register_tile_class(cls, tile_class):
        cls._registry[tile_class.__name__] = tile_class

    @classmethod
    def from_yaml(cls, file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            tile_class_name = data.pop('tile_class')
            tile_class = cls._registry.get(tile_class_name)
            if tile_class is None:
                raise ValueError(f"Unknown ProgramTile type: {tile_class_name}")
            return tile_class(**data)