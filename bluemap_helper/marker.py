from mcdreforged.minecraft.rtext.style import RColor
from mcdreforged.minecraft.rtext.text import RTextList, RText
from pyhocon import ConfigTree


class Position:
    x: int = 0
    y: int = 0
    z: int = 0

    def __init__(self, config: ConfigTree = None):
        if config:
            self.x = config.get("x")
            self.y = config.get("y")
            self.z = config.get("z")
        pass

    def __str__(self):
        return "{:.1f},{:.1f},{:.1f}".format(self.x, self.y, self.z)

    def get_rtext(self, color: RColor):
        return RText("[{:.1f}, {:.1f}, {:.1f}]".format(self.x, self.y, self.z), color=color)


class Marker:
    id: str = ""
    label: str = ""
    position: Position = Position()
    type: str = "poi"

    def __init__(self, config_id=None, config: ConfigTree = None):
        if config_id and config:
            self.id = config_id
            self.position = Position(config.get("position"))
            self.type = config.get("type")
            self.label = config.get("label")

    def __str__(self):
        return "[{}] {}({}) => {}".format(self.id, self.label, self.type, self.position)

    def get_rtext(self):
        return RTextList(
            RText("({}) {} ".format(self.id, self.label), color=RColor.dark_aqua),
            self.position.get_rtext(RColor.green),
            RText("[poi]", color=RColor.gold)
        )


class MarkerSet:
    label: str = ""
    id: str = ""
    markers: list[Marker] = []

    def __init__(self, config_id=None, config: ConfigTree = None):
        self.markers = []
        if config_id and config:
            self.id = config_id
            self.label = config.get("label")
            mks: ConfigTree = config.get("markers")
            for i in mks:
                self.markers.append(Marker(i, mks.get(i)))

    def __str__(self):
        markers = ""
        for i in self.markers:
            markers += "{}\n".format(i)
        return "[{}]{}:\n{}".format(self.id, self.label, markers)
