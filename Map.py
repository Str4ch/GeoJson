from abc import ABC
from Geometry import GeometryObject
from dataclasses import dataclass
import json
from typing import List, Tuple


@dataclass
class MapElement(ABC):
    geometry: GeometryObject
    stroke: str
    stroke_width: float
    fill: str
    marker: str
    filter: str
    z_order: str

    def cls_settings_for_svg(self):

        return [self.__class__.__name__, self.stroke, self.stroke_width, self.fill, self.marker, self.filter, self.z_order]

    def to_svg(self):
        # print(self.geometry.to_svg(self.__class__.__name__))
        return self.geometry.to_svg(self.__class__.__name__)

    def __str__(self) -> str:
        return self.to_svg()

    def bounding_box(self):
        return self.geometry.bounding_box()

    @staticmethod
    def FromDict(data: dict, settings: dict) -> 'MapElement':
        r_width = settings["roadWidth"]
        w_width = settings["wallThickness"]
        riv_width = 1
        if "riverWidth" in settings:
            riv_width = settings["riverWidth"]
        g = GeometryObject.FromDict(data)
        match data["id"]:
            case "roads":
                return Road(geometry=g, stroke="#FFF2C8", stroke_width=r_width, fill=None, marker=None, filter=None, z_order=1)#
            case "rivers":
                return River(geometry=g, stroke="#779988", stroke_width=riv_width, fill=None, marker=None, filter=None, z_order=0)#
            case "walls":
                return Wall(geometry=g, stroke="#606661", stroke_width=w_width, fill=None, marker="url(#wall)", filter=None, z_order=0)#
            case "planks":
                return Plank(geometry=g, stroke="#FFF2C8", stroke_width=1, fill=None, marker=None, filter=None, z_order=0)#
            case "buildings":
                return Building(geometry=g, stroke="#000000", stroke_width=1, fill="#D6A36E", marker=None, filter="url(#shadow)", z_order=0)#
            case "prisms":
                return Prism(geometry=g, stroke="#000000", stroke_width=1, fill=None, marker=None, filter=None, z_order=0)#
            case "squares":
                return Square(geometry=g, stroke="#000000", stroke_width=1, fill="#F2F2DA", marker=None, filter=None, z_order=0)#
            case "greens":
                return Green(geometry=g, stroke="#99AA77", stroke_width=1, fill="url(#green)", marker=None, filter=None, z_order=0)#
            case "fields":
                return Field(geometry=g, stroke="#99AA77", stroke_width=1, fill="url(#green)", marker=None, filter=None, z_order=0)#
            case "trees":
                return Tree(geometry=g, stroke="#000000", stroke_width=1, fill="#667755", marker=None, filter=None, z_order=0)#
            case "districts":
                return District(geometry=g, stroke="none", stroke_width=1, fill=None, marker=None, filter=None, z_order=0)#
            case "earth":
                return Earth(geometry=g, stroke="#000000", stroke_width=1, fill=None, marker=None, filter=None, z_order=0)#
            case "water":
                return Water(geometry=g, stroke="#000000", stroke_width=1, fill="#779988", marker=None, filter=None, z_order=0)#




class Road(MapElement):
    pass


class River(MapElement):
    pass


class Wall(MapElement):
    pass


class Plank(MapElement):
    pass


class Building(MapElement):
    pass


class Prism(MapElement):
    pass


class Square(MapElement):
    pass


class Green(MapElement):
    pass


class Field(MapElement):
    pass


class Tree(MapElement):
    pass


class District(MapElement):
    pass


class Earth(MapElement):
    pass


class Water(MapElement):
    pass


@dataclass
class Map:
    items: List[MapElement]

    def bounding_box(self) -> Tuple[float, float, float, float]:
        bottom = 0
        top = 0
        left = 0
        right = 0
        for i in self.items:
            if isinstance(i, District):
                b, t, l, r = i.bounding_box()
                if b < bottom:
                    bottom = b
                if t > top:
                    top = t
                if l < left:
                    left = l
                if r > right:
                    right = r
        return left, bottom, right, top

    def LoadFromGeoJson(filename: str) -> 'Map':
        items = []
        with open(filename, 'r') as f:
            data = json.load(f)
        for feature in data['features']:
            idd = feature['id']

            if idd == "values":
                settings = feature
            else:
                myobject = MapElement.FromDict(feature, settings)
                items.append(myobject)
        return Map(items)
