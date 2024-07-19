from flask import Flask, jsonify
import yaml


class CharmAssistantAPIServer:
    def __init__(self, config_file):
        self.app = Flask(__name__)
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, "r") as f:
            return yaml.safe_load(f)

    def configure_routes(self):
        print(self.config)
        for action in self.config["actions"]:
            route_path = action["name"].replace(" ", "_").to_lower()
            route_func_name = action["func"]
            route_func = getattr(self, route_func_name)
            self.app.route(route_path, methods=["GET"])(route_func)

    def run(self):
        self.configure_routes()
        self.app.run(debug=True)

    def protected_route(self):
        return jsonify({"message": "Protected API is accessed"})

    def unprotected_route(self):
        return jsonify({"message": "Unprotected API is accessed"})


if __name__ == "__main__":
    api = CharmAssistantAPIServer("/etc/charm-assistant-api.yaml")
    api.run()
