
from flask import Flask, request, jsonify
import subprocess
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/alert", methods=["POST"])
def handle_alert():
    data = request.get_json(silent=True) or {}
    app.logger.info("Received alert payload: %s", data)

    for alert in data.get("alerts", []):
        alert_name = alert.get("labels", {}).get("alertname")
        alert_status = alert.get("status")

        app.logger.info(
            "Alert received: name=%s status=%s",
            alert_name,
            alert_status
        )

        if alert_name == "NginxDown" and alert_status == "firing":
            try:
                result = subprocess.run(
                    [
                        "ansible-playbook",
                        "/ansible/restart-nginx.yml"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                app.logger.info("Ansible stdout:\n%s", result.stdout)
                app.logger.info("Ansible stderr:\n%s", result.stderr)

                if result.returncode != 0:
                    return jsonify({
                        "status": "recovery_failed"
                    }), 500

                return jsonify({
                    "status": "recovery_triggered"
                }), 200

            except Exception:
                app.logger.exception("Recovery execution failed")
                return jsonify({
                    "status": "recovery_failed"
                }), 500

    return jsonify({"status": "no_matching_alert"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
