import subprocess
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
        for action in self.config["actions"]:
            route_name = action["name"].replace(" ", "_").lower()
            route_path = "/" + route_name

            # Define a closure to capture the command for each route
            def make_route_func(cmd):
                def route_func():
                    output = self.run_bash_command(cmd)
                    return jsonify({"output": output})

                return route_func

            # Create the route function with the specific command
            route_func = make_route_func(action["cmd"])

            # Add the route to the Flask app
            self.app.route(route_path, methods=["GET"], endpoint=route_name)(route_func)

    def run(self):
        self.configure_routes()
        self.app.run(debug=True)

    def protected_route(self):
        return jsonify({"message": "Protected API is accessed"})

    def unprotected_route(self):
        return jsonify({"message": "Unprotected API is accessed"})

    def run_bash_command(self, command):
        try:
            # Execute the command
            result = subprocess.run(
                command, shell=True, check=True, text=True, capture_output=True
            )

            # Return the output
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Handle errors in the called executable
            return f"An error occurred: {e.stderr}"


if __name__ == "__main__":
    api = CharmAssistantAPIServer("/etc/charm-assistant-api.yaml")
    api.run()
