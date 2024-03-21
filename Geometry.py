from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

class GeometryObject(ABC):
    @staticmethod
    @abstractmethod
    def FromDict(data: dict) -> 'GeometryObject':
        match data["type"]:
            case "Point":
                return Point.FromDict(data)
            case "LineString":
                return LineString.FromDict(data)
            case "Polygon":
                return Polygon.FromDict(data)
            case _:
                return Composite.FromDict(data)
        # Do the same for LineString, Polygon and Composite...


@dataclass
class Point(GeometryObject):
    x: float
    y: float

    def to_svg(self, classname: str) -> str:
        return ["circle", classname, f"cx={self.x}", f"cy={self.y}"]

    @staticmethod
    def FromDict(data: dict) -> 'Point':
        coordinates = data["coordinates"]
        return Point(coordinates[0], coordinates[1])

@dataclass
class LineString(GeometryObject):
    coordinates: List[Point]

    def to_svg(self, classname: str) -> str:
        fin = ["path", classname, "d"]
        sttr = "M "
        for i in self.coordinates:
            add = f"{i.x},{i.y} "
            sttr += add
        fin.append(sttr)
        return fin

    def bounding_box(self) -> Tuple[float, float, float, float]:
        bottom = 0
        top = 0
        left = 0
        right = 0
        for i in self.coordinates:
            if i.x > right:
                right = i.x
            elif i.x < left:
                left = i.x

            if i.y > top:
                top = i.y
            elif i.y < bottom:
                bottom = i.y
        return bottom, top, left, right

    @staticmethod
    def FromDict(data: dict) -> 'LineString':
        # coords = []
        # for (x,y) in data["coordinates"]:
        #     coords.append(Point(x,y))
        #
        coords = [Point(x,y) for x,y in data["coordinates"]]
        return LineString(coords)

@dataclass
class Polygon(GeometryObject):

    points: LineString

    def to_svg(self, classname: str) -> str:
        fin = ['polygon', classname, "points"]
        sttr = ''
        for i in self.points.coordinates:
            add = f"{i.x},{i.y} "
            sttr += add
        fin.append(sttr)
        return fin

    def bounding_box(self) -> Tuple[float, float, float, float]:
        return self.points.bounding_box()

    @staticmethod
    def FromDict(data: dict) -> 'Polygon':
        line_1 = LineString([Point(x, y) for x, y in data["coordinates"][0]])
        # line_2 = LineString([Point(x,y) for x,y in data["coordinates"][1]])
        return Polygon(line_1)

@dataclass
class Composite(GeometryObject):
    objects: List[GeometryObject]

    def to_svg(self, classname: str) -> str:
        ls = []
        for i in self.objects:
            ls.append(i.to_svg(classname))
        return ls

    def bounding_box(self) -> Tuple[float, float, float, float]:
        bottom = 0
        top = 0
        left = 0
        right = 0
        for i in self.objects:
            if isinstance(i, Point):
                if i.x > right:
                    right = i.x
                elif i.x < left:
                    left = i.x

                if i.y > top:
                    top = i.y
                elif i.y < bottom:
                    bottom = i.y
            elif isinstance(i, LineString) or isinstance(i, Polygon):
                b, t, l, r = i.bounding_box()
                if b < bottom:
                    bottom = b
                if t > top:
                    top = t
                if l < left:
                    left = l
                if r > right:
                    right = r
        return bottom, top, left, right

    @staticmethod
    def FromDict(data: dict) -> 'Composite':
        match data["type"]:
            case "MultiPoint":
                return Composite([Point(x, y) for x, y in data["coordinates"]])
            case "MultiLineString":
                return Composite([LineString([Point(x,y) for (x,y) in line]) for line in data["coordinates"]])
            case "MultiPolygon":
                return Composite(
                    [Polygon(LineString([Point(point[0], point[1]) for point in line[0]])) for line in data["coordinates"]])
            case "GeometryCollection":
                return Composite([GeometryObject.FromDict(i) for i in data["geometries"]])
    

