from companion import LOGGER
import os
import configparser


def get_plugins():
    config = configparser.ConfigParser()
    plugins = []
    for root, dirs, files in os.walk("companion/plugins/"):
        for dir in dirs:
            if not dir.endswith("__"):
                for file in os.listdir(root + dir):
                    if file.endswith(".plugin"):
                        config.read(root + dir + "/" + file)
                        plugins.append(
                            dir + "."
                            +
                            config.get(
                                "CORE",
                                "main"))
    return plugins
