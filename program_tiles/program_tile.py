from abc import ABC, abstractmethod
import yaml
import importlib
import pkgutil

class ProgramTile(ABC):
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
    def from_yaml(cls, file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return ProgramTileFactory.create_tile(data)

class ProgramTileFactory:
    _registry = {}

    @classmethod
    def register_tile_class(cls, tile_class):
        cls._registry[tile_class.__name__] = tile_class

    @classmethod
    def create_tile(cls, data):
        tile_class_name = data.pop('tile_class')
        tile_class = cls._registry.get(tile_class_name)
        if tile_class is None:
            raise ValueError(f"Unknown ProgramTile type: {tile_class_name}")
        return tile_class(**data)

    @classmethod
    def discover_tile_classes(cls, package):
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package.__name__}.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, ProgramTile) and attr is not ProgramTile:
                    cls.register_tile_class(attr)