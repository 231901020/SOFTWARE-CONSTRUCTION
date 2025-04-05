from scapy.all import sniff, wrpcap, IP, TCP, UDP, ICMP, get_if_list
from datetime import datetime

packet_logs = []
packet_list = []
protocol_counts = {
    "TCP": 0,
    "UDP": 0,
    "ICMP": 0,
    "Other": 0
}

def packet_callback(packet):
    packet_list.append(packet)

    proto = "Other"
    if TCP in packet:
        proto = "TCP"
    elif UDP in packet:
        proto = "UDP"
    elif ICMP in packet:
        proto = "ICMP"

    protocol_counts[proto] += 1

    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        timestamp = datetime.now().strftime("%H:%M:%S")
        log = f"[{timestamp}] {proto} Packet: {src} -> {dst}"
        packet_logs.append(log)
        if len(packet_logs) > 100:
            packet_logs.pop(0)

def start_sniffing():
    print("🔍 Sniffing started...")
    sniff(prn=packet_callback, store=True, timeout=60, filter="ip")
    wrpcap("static/pcap/captured.pcap", packet_list)
    print("✅ Sniffing completed. PCAP saved.")

def export_pcap():
    wrpcap("static/pcap/captured.pcap", packet_list)
