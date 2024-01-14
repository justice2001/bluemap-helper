import json
import re
from json import JSONDecodeError

from mcdreforged.api.command import SimpleCommandBuilder, Integer, Text, GreedyText
from mcdreforged.command.builder.common import CommandContext
from mcdreforged.command.builder.nodes.arguments import QuotableText
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.command.command_source import CommandSource, PlayerCommandSource
from mcdreforged.info_reactor.info import Info
from mcdreforged.minecraft.rtext.style import RColor
from mcdreforged.minecraft.rtext.text import RText, RTextList
from mcdreforged.plugin.server_interface import PluginServerInterface
from minecraft_data_api import get_player_info, get_player_dimension, get_server_player_list

from bluemap_helper.bluemap import read_config, insert_mark, get_bluemap_dimensions, get_marker_list, del_mark
from bluemap_helper.poi_utils import get_poi_marker, get_position
from bluemap_helper.utils import named_thread

PLAYER_COUNT: int = 0


def on_load(server: PluginServerInterface, prev_module):
    server.register_command(
        Literal("!!bm").then(
            Literal("make").then(
                Literal("poi").then(
                    QuotableText("comment").runs(make_poi)
                )
            )
        ).then(
            Literal("del").then(
                QuotableText("marker").runs(remove_marker)
                .then(
                    QuotableText("set").runs(remove_marker)
                    .then(
                        QuotableText("dimension").runs(remove_marker)
                    )
                )
            )
        ).then(
            Literal("list").runs(list_markers)
        )
    )
    server.execute("list")


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    global PLAYER_COUNT
    if not get_player_name(player).startswith("bot_"):
        PLAYER_COUNT += 1
    if PLAYER_COUNT - 1 == 0:
        server.say("发现玩家进入服务器，Bluemap渲染已暂停")
        server.execute("bluemap stop")


def on_player_left(server: PluginServerInterface, player: str):
    global PLAYER_COUNT
    if not get_player_name(player).startswith("bot_"):
        PLAYER_COUNT -= 1
    print(PLAYER_COUNT)
    if PLAYER_COUNT == 0:
        print("最后一个玩家已经退出，渲染继续")
        server.execute("bluemap start")


def on_info(server: PluginServerInterface, info: Info):
    global PLAYER_COUNT
    mat = re.match(r'There are ([0-9]*) of a max of ([0-9]*) players online: (.*)', info.content)
    if mat:
        players: list[str] = mat.group(3).split(",")
        for player in players:
            if not get_player_name(player).startswith("bot_"):
                PLAYER_COUNT += 1
        if PLAYER_COUNT > 0:
            server.execute("bluemap stop")
        else:
            server.execute("bluemap start")


def get_player_name(player: str):
    return player.strip().lower()


@named_thread
def make_poi(source: PlayerCommandSource, context: CommandContext):
    config = {}
    if not source.is_player:
        source.reply("该命令仅限玩家执行")
        return
    if "config" in context:
        try:
            config = json.loads(context["config"])
        except JSONDecodeError:
            source.reply("Invalid JSON")
    pos = get_player_info(source.player, "Pos")
    try:
        insert_mark(get_bluemap_dimensions(source.player), "default",
                    get_poi_marker(context["comment"], get_position(pos[0], pos[1], pos[2]), config))
        source.get_server().execute("bluemap reload")
        source.reply("POI添加成功")
    except FileNotFoundError:
        source.reply("Invalid World: " + context["comment"])


@named_thread
def remove_marker(source: PlayerCommandSource, context: CommandContext):
    if not source.is_player:
        marker_dimension = context.get("dimension", "overworld")
    else:
        marker_dimension = get_bluemap_dimensions(source.player)
    marker_set = context.get("set", "default")
    marker = context.get("marker")
    del_mark(marker_dimension, marker_set, marker)


@named_thread
def list_markers(source: PlayerCommandSource, context: CommandContext):
    sets = get_marker_list("overworld")
    source.reply(RText("================== Markers ================", color=RColor.gold))
    for i in sets:
        for j in i.markers:
            source.reply(j.get_rtext())
