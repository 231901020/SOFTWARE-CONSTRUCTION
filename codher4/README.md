# GenAI-Powered C2 Behavior Simulator for Blue Team Training

This project simulates C2 (Command & Control) behavior with AES encryption, steganography, real-time CPU monitoring, GenAI-driven anomaly detection, and packet sniffing. It's ideal for Blue Team cybersecurity exercises.

---

## 🚀 Features

- ✅ AES encryption/decryption of text
- ✅ LSB steganography for hiding messages in images
- ✅ Dynamic CPU usage graph updating every 2 seconds
- ✅ Real-time monitoring dashboard
- ✅ Packet sniffer with PCAP file analysis
- ✅ C2 traffic simulator using Scapy
- ✅ GenAI anomaly detection using OpenAI LLM
- ✅ Docker container ready
- ✅ Modern UI with navbar and modular pages

---

## 🧱 Stack

| Layer        | Tech                             |
|--------------|----------------------------------|
| Frontend     | HTML, CSS, JavaScript, Chart.js  |
| Backend      | Flask (Python)                   |
| AI/LLM       | OpenAI API (GPT)                 |
| Encryption   | AES (PyCryptodome)               |
| Steganography| Stegano (LSB method)             |
| Packet Sniffing | Scapy                        |
| Monitoring   | psutil + Chart.js                |
| Container    | Docker                           |

---

## 📂 How to Run

### 🔧 Step 1: Clone the Repo
```bash
git clone https://github.com/yourusername/genai-c2-simulator.git
cd genai-c2-simulator
