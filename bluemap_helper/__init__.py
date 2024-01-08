import json
from json import JSONDecodeError

from mcdreforged.api.command import SimpleCommandBuilder, Integer, Text, GreedyText
from mcdreforged.command.builder.common import CommandContext
from mcdreforged.command.builder.nodes.arguments import QuotableText
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.command.command_source import CommandSource
from mcdreforged.plugin.server_interface import PluginServerInterface

from bluemap_helper.bluemap import read_config, insert_mark
from bluemap_helper.poi_utils import get_poi_marker, get_position


def on_load(server: PluginServerInterface, prev_module):
    server.register_command(
        Literal("!!bm").then(
            Literal("make").then(
                Literal("poi").then(
                    QuotableText("comment").runs(make_poi).then(
                        QuotableText("config").runs(
                            make_poi
                        )
                    )
                )
            )
        )
    )


def make_poi(source: CommandSource, context: CommandContext):
    config = {}
    if "config" in context:
        try:
            config = json.loads(context["config"])
        except JSONDecodeError:
            source.reply("Invalid JSON")
    try:
        insert_mark(context["comment"], "default", get_poi_marker("Test", get_position(32, 71, 105), config))
        source.get_server().execute("bluemap reload")
        source.reply("POI添加成功")
    except FileNotFoundError:
        source.reply("Invalid World: " + context["comment"])
