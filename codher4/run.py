import os
import random
from threading import Thread

import psutil

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

from modules.packet_sniffer import packet_logs, export_pcap, protocol_counts, start_sniffing
from modules.encryption import encrypt_text, decrypt_text
from modules.stegano_module import encode_message, decode_message
from modules.traffic_simulator import simulate_c2_traffic
from modules.ai_module import generate_analysis

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploaded/"
ENCODED_FOLDER = "static/encoded/"

# ====================== ROUTES ======================

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/packet-analyser")
def packet_analyser():
    return render_template("packet_analyser.html", packet_logs=packet_logs)

@app.route("/cpu-monitoring")
def cpu_monitoring():
    return render_template("cpu_monitoring.html")

@app.route("/download_pcap")
def download_pcap():
    export_pcap()  # Save to static/pcap/captured.pcap
    return send_file("static/pcap/captured.pcap", as_attachment=True)

@app.route("/aes", methods=["GET", "POST"])
def aes():
    result = ""
    if request.method == "POST":
        text = request.form['text']
        if 'encrypt' in request.form:
            result = encrypt_text(text)
        elif 'decrypt' in request.form:
            result = decrypt_text(text)
    return render_template("aes_encryption.html", result=result)

@app.route("/steganography", methods=["GET", "POST"])
def steganography():
    result = ""
    image_url = None
    if request.method == "POST":
        if 'hide' in request.form:
            msg = request.form['message']
            uploaded_file = request.files['image']
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                upload_path = os.path.join(UPLOAD_FOLDER, filename)
                uploaded_file.save(upload_path)

                output_path = os.path.join(ENCODED_FOLDER, f"encoded_{filename}")
                result = encode_message(upload_path, msg, output_path)
                image_url = output_path
        elif 'reveal' in request.form:
            uploaded_file = request.files['reveal_image']
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                uploaded_file.save(path)
                result = decode_message(path)

    return render_template("steganography.html", result=result, image_url=image_url)

@app.route("/realtime-monitoring")
def realtime_monitoring():
    return render_template("realtime_monitoring.html")

@app.route("/simulator")
def simulator():
    return render_template("simulator_menu.html")

@app.route("/analyser")
def analyser():
    ai_result = generate_analysis()
    return render_template("analyser.html", result=ai_result)

@app.route("/dynamic-graph")
def dynamic_graph():
    return render_template("dynamic_graph.html")

@app.route("/graph-data")
def graph_data():
    return jsonify(protocol_counts)

@app.route("/c2-apps")
def c2_apps():
    return render_template("c2_apps.html")

@app.route("/network_monitoring")
def network_monitoring():
    return render_template("network_monitoring.html")

@app.route("/network_monitoring_logs")
def network_monitoring_logs():
    sample_data = [
        "10.0.0.1 > 10.0.0.5: Normal traffic",
        "192.168.1.2 > 8.8.8.8: DNS lookup",
        "Suspicious spike detected at 10.0.0.4",
        "Port scanning activity flagged from 172.16.0.7"
    ]
    return "\n".join(random.sample(sample_data, k=3))

@app.route("/intrusion_detection")
def intrusion_detection():
    return render_template("intrusion_detection.html")

@app.route("/intrusion_detection_status")
def intrusion_detection_status():
    alerts = [
        "<span style='color:green;'>System Secure: No intrusion detected</span>",
        "<span style='color:red;'>Alert: Multiple failed login attempts</span>",
        "<span style='color:orange;'>Warning: Abnormal packet rate observed</span>"
    ]
    return random.choice(alerts)

@app.route("/attack_response", methods=["GET", "POST"])
def attack_response():
    result = ""
    if request.method == "POST" and 'simulate' in request.form:
        result = "🛡️ Simulated firewall block triggered and system isolated from suspect IPs."
    return render_template("attack_response.html", result=result)

# ====================== THREADS ======================

# Start sniffing and simulation in background
Thread(target=start_sniffing, daemon=True).start()
Thread(target=simulate_c2_traffic, daemon=True).start()

# ====================== START APP ======================

@app.route("/cpu-usage-data")
def cpu_usage_data():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            pinfo = proc.info
            if pinfo['cpu_percent'] > 1.0:  # Only show active ones
                processes.append({
                    "name": f"{pinfo['name']} (PID {pinfo['pid']})",
                    "cpu": pinfo['cpu_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return jsonify({
        "cpu": psutil.cpu_percent(interval=0.5),
        "processes": processes[:5]  # Limit top 5 processes
    })

@app.route("/genai-c2")
def genai_c2():
    return render_template("genai_c2.html")

@app.route("/genai/command-generator")
def command_generator():
    command = "simulate_traffic('beacon', 10)"  # Replace with LLM-generated logic
    return render_template("genai_app.html", title="Command Generator", content=command)

@app.route("/genai/log-analyzer")
def log_analyzer():
    logs = [
        "192.168.1.10 accessed /admin at 3AM",
        "Multiple failed SSH attempts from 203.0.113.50"
    ]
    analysis = "Suspicious activity detected in SSH and admin paths."  # Placeholder
    return render_template("genai_app.html", title="Log Analyzer", content=analysis)

@app.route("/genai/incident-advisor")
def incident_advisor():
    advice = "Recommend blocking IP 203.0.113.50 and initiating incident response."  # Placeholder
    return render_template("genai_app.html", title="Incident Response Advisor", content=advice)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
