
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def handle_alert():
    data = request.get_json(silent=True) or {}

    for alert in data.get("alerts", []):
        if (
            alert.get("labels", {}).get("alertname") == "NginxDown"
            and alert.get("status") == "firing"
        ):
            result = subprocess.run(
                [
                    "ansible-playbook",
                    "/ansible/restart-nginx.yml"
                ],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                app.logger.error("Ansible failed: %s", result.stderr)
                return jsonify({"status": "recovery_failed"}), 500

            app.logger.info("NGINX recovery playbook completed")
            return jsonify({"status": "recovery_triggered"}), 200

    return jsonify({"status": "no_matching_alert"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)