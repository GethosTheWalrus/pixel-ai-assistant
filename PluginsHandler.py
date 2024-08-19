from plugins import * # noqa


class PluginsHandler:
    modules = {}

    def __init__(self):
        self.register_plugins()

    def register_plugins(self) -> None:
        for module in globals():
            parts = module.split("Plugin")
            if (len(parts) == 2 and len(parts[0]) > 0 and parts[0] != "Pixel"):
                module_name = parts[0]
                constructor = globals()[module_name + "Plugin"]
                instance = constructor()
                self.modules[instance.wake_phrase] = instance

    def invoke_plugins_by_wake_word(self, voice_command) -> str:
        plugin = self.modules[voice_command]
        return plugin.response
