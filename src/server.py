import subprocess
from flask import Flask, jsonify
import yaml
from flask_httpauth import HTTPTokenAuth
from waitress import serve


class TaskAPIServer:
    def __init__(self, config_file):
        self.app = Flask(__name__)
        self.config = self.load_config(config_file)
        self.auth_enabled = self.config.get("auth_enabled", False)

        if self.auth_enabled:
            self.auth = HTTPTokenAuth(scheme="Bearer")
            self.tokens = self.load_tokens(config_file)
            self.auth.verify_token(self.verify_token)

        self.configure_routes()

    def load_config(self, config_file):
        with open(config_file, "r") as f:
            return yaml.safe_load(f)

    def load_tokens(self, config_file):
        config = self.load_config(config_file)
        return {token: username for token, username in config.get("tokens", {}).items()}

    def verify_token(self, token):
        # Validate the token and return associated user or None
        return self.tokens.get(token)

    def configure_routes(self):
        for action in self.config.get("actions", []):
            route_name = action["name"].replace(" ", "_").lower()
            route_path = "/" + route_name

            # Define a closure to capture the command for each route
            def make_route_func(cmd):
                def route_func():
                    output = self.run_bash_command(cmd)
                    return jsonify({"output": output})

                return route_func

            route_func = make_route_func(action["cmd"])

            if self.auth_enabled:
                self.app.route(route_path, methods=["GET"], endpoint=route_name)(
                    self.auth.login_required(route_func)
                )
            else:
                self.app.route(route_path, methods=["GET"], endpoint=route_name)(route_func)

    def run(self):
        serve(
            self.app,
            host="0.0.0.0",
            port=self.config["port"],
        )

    def run_bash_command(self, command):
        try:
            result = subprocess.run(
                command, shell=True, check=True, text=True, capture_output=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e.stderr}"


if __name__ == "__main__":
    api = TaskAPIServer("/etc/task-api.yaml")
    api.run()
