from flask import Flask, request, jsonify
import subprocess
import os

if (os.getenv("KUBE_CONFIG") is None) or (os.getenv("API_TOKEN") is None):
    print("Please set the KUBE_CONFIG and API_TOKEN environment variables")
    exit(1)

kube_dir = os.path.expanduser("~/.kube")
if not os.path.exists(kube_dir):
    os.makedirs(kube_dir)

# Check if kubectl config is present
kube_config_path = os.path.join(kube_dir, "config")
if not os.path.exists(kube_config_path):
    # Load the Kubernetes configuration from environment variables
    with open(kube_config_path, "w") as f:
        f.write(os.getenv("KUBE_CONFIG"))

app = Flask(__name__)

# Authentication token (simple example)
API_TOKEN = os.getenv("API_TOKEN")

@app.route("/kubectl", methods=["POST"])
def execute_kubectl():
    # Authenticate request
    token = request.headers.get("Authorization")
    if not token or token.split("Bearer ")[-1] != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Extract and validate request data
    data = request.json
    deployments = data.get("deployment").split(",")

    if len(deployments) == 0:
        return jsonify({"error": "Missing 'deployment' field"}), 400

    # Run kubectl command
    for deployment in deployments:
        try:
            command = ["kubectl", "rollout", "restart", "deployment", deployment, "--namespace=laravel-applications"]
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Command failed", "details": e.stderr}), 500
    return jsonify({"message": "Command executed successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)