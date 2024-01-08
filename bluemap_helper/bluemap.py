import os

from pyhocon import ConfigFactory, HOCONConverter, ConfigTree
from bluemap_helper.poi_utils import *
from xpinyin import Pinyin
from minecraft_data_api import get_player_dimension

DIMENSIONS = {
    0: "overworld",
    1: "end",
    -1: "nether"
}


def read_config(config_file):
    config = ConfigFactory.parse_file(config_file)
    return config


def write_config(config, config_file):
    config = HOCONConverter.convert(config, "hocon")
    with open(config_file, "w+", encoding="utf-8") as file:
        file.write(config)


def insert_mark(area, marker_set, marker_config):
    path = os.path.join("server\\config\\bluemap\\maps", area + ".conf")
    config = read_config(path)
    if marker_set not in config["marker-sets"]:
        config["marker-sets"].put(gen_id(marker_set), get_marker_set(marker_set))
    config["marker-sets"][marker_set]["markers"].put(gen_id(marker_config["label"]), marker_config)
    write_config(config, path)


def gen_id(name):
    p = Pinyin()
    return p.get_pinyin(name).replace(" ", "-").lower()


def get_bluemap_dimensions(player):
    dimension = get_player_dimension(player)
    return DIMENSIONS[dimension]
