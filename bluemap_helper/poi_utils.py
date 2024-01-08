"""
example-marker-set: {
  label: "Example Marker Set"
  toggleable: true
  default-hidden: false
  sorting: 0
  markers: {
    # markers go here ...
  }
}
"""
from pyhocon import ConfigTree


def get_marker_set(set_name):
    co = ConfigTree()
    co.put("label", set_name)
    co.put("toggleable", True)
    co.put("default-hidden", False)
    co.put("sorting", 0)
    co.put("markers", {})
    return co


"""
example-poi-marker: {
    type: "poi"
    position: { x: 1, y: 64, z: -23 }
    label: "Example POI Marker"
    
    # Optional:
    detail: "This is a <b>POI</b> marker"
    icon: "assets/poi.svg"
    anchor: { x: 25, y: 45 }
    sorting: 0
    listed: true
    classes: [
        "my-custom-class"
    ]
    min-distance: 10
    max-distance: 10000000
}
"""


def get_poi_marker(poi_name, position, config):
    co = ConfigTree()
    co.put("type", "poi")
    co.put("position", position)
    co.put("label", poi_name)
    co.put("detail", "This is a poi generated in mcdr plgin")
    co.put("icon", "assets/poi.svg")
    co.put("anchor", get_position(25, 45))
    co.put("min-distance", 10)
    co.put("max-distance", 1000000000)
    return co


def get_position(x=None, y=None, z=None):
    co = ConfigTree()
    x and co.put("x", x)
    y and co.put("y", y)
    z and co.put("z", z)
