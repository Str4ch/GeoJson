from Map import Map
from typing import List
import chevron
from pathlib import Path
import sys


def render_map(map_path):
    mp = Map.LoadFromGeoJson(map_path)
    bb = mp.bounding_box()
    width = bb[2] - bb[0]
    height = bb[3] - bb[1]
    mm = (bb[0]-width*0.1, bb[1]-height*0.1, bb[2]+width*0.1, bb[3]+height*0.1)
    cls = []
    itm = []
    priority = []
    for i in mp.items:
        appender = i.to_svg()
        cls.append(i.cls_settings_for_svg())
        if appender:
            if i.z_order == 1:
                if isinstance(appender[0], List):
                    priority += appender
                else:
                    priority.append(appender)
            else:
                if isinstance(appender[0], List):
                    itm += appender
                else:
                    itm.append(appender)

    itm += priority
    data = {
        "bbox": {
            "x": mm[0],
            "y": mm[1],
            "width": mm[2] - mm[0],
            "height": mm[3] - mm[1]
        },
        "classes": cls,
        "items": itm
    }
    return chevron.render(open("map-template.svg", 'r'), data)



folder = sys.argv[1]
p = Path(folder)
filelists = [file for file in p.iterdir() if file.suffix == ".json"]
for file in filelists:
    f = open(str(file).replace(".json", ".svg"), "w")
    f.write(render_map(str(file)))
    f.close()
