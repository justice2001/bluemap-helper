import json
from json import JSONDecodeError

from mcdreforged.api.command import SimpleCommandBuilder, Integer, Text, GreedyText
from mcdreforged.command.builder.common import CommandContext
from mcdreforged.command.builder.nodes.arguments import QuotableText
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.command.command_source import CommandSource, PlayerCommandSource
from mcdreforged.plugin.server_interface import PluginServerInterface
from minecraft_data_api import get_player_info, get_player_dimension, get_server_player_list

from bluemap_helper.bluemap import read_config, insert_mark, get_bluemap_dimensions
from bluemap_helper.poi_utils import get_poi_marker, get_position
from bluemap_helper.utils import named_thread


def on_load(server: PluginServerInterface, prev_module):
    server.register_command(
        Literal("!!bm").then(
            Literal("make").then(
                Literal("poi").then(
                    QuotableText("comment").runs(make_poi)
                )
            )
        )
    )


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
        insert_mark(get_bluemap_dimensions(source.player), "default", get_poi_marker(context["comment"], get_position(pos[0], pos[1], pos[2]), config))
        source.get_server().execute("bluemap reload")
        source.reply("POI添加成功")
    except FileNotFoundError:
        source.reply("Invalid World: " + context["comment"])
