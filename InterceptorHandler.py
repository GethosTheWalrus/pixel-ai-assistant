from interceptors import * # noqa


class InterceptorHandler:
    modules = []

    def __init__(self):
        self.register_interceptors()

    def register_interceptors(self) -> None:
        for module in globals():
            parts = module.split("Interceptor")
            if (len(parts) == 2 and len(parts[0]) > 0 and parts[0] != "Pixel"):
                module_name = parts[0]
                constructor = globals()[module_name + "Interceptor"]
                instance = constructor()
                self.modules.append(instance)

    def evaluate_interceptors(self, voice_prompt) -> str:
        for module in self.modules:
            if module.is_matched(voice_prompt):
                return module.response
