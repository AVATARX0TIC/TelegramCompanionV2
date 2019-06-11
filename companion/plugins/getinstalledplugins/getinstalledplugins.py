from companion.pluginmanager import list_plugins, load_plugin_info
from companion.utils import CommandHandler


@CommandHandler(command="plugin", args=["plugin"], parse_mode="md")
async def get_plugin_info(event):
    """
        <b>param:</b> <code>plugin name</code>
        <b>return:</b> <i>Gets the info for a specific plugin</i>
    """
    plugin = event.args.plugin
    if not plugin:
        await event.edit("Give me a plugin name or use the `plugins` command to list all the available plugins!")
    else:
        info = await load_plugin_info(plugin)
        if info:
            plugin = plugin
            await event.edit("Plugin info for: " + plugin + ":" +
                             "\nName: " + info.get("main", "Not Available!") +
                             "\nAuthor: " + info.get("author", "Not Available!") +
                             "\nDescription: " + info.get("description", "Not Available!"))
        else:
            await event.edit("Plugin " + plugin + " isn't installed!")


@CommandHandler(command="listplugins", parse_mode="md")
async def get_installed_plugins(event):
    """
        <b>param:</b> <code>None</code>
        <b>return:</b> <i>Get a list with all the installed plugins</i>
    """
    await event.edit("Installed Plugins:\n" + list_plugins())
