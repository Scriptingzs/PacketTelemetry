#!/usr/bin/env python3
# File: json_client.py
import socket
import json
import time

def run_json_flood(target_ip: str, total_packets: int):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5.0)
    
    # 1. CONSTRUCT THE MULTI-TYPE COMPLEX TELEMETRY MATRIX
    telemetry_data = {
        "device_mac_id": "ESP32-BED-A1B2",
        "epoch_timestamp": int(time.time()),
        "bed_temperature_f": 98.64,
        "heating_elements_active": True,
        "respiration_waveform_samples": [120, -45, 302, -88, 115, -50, 290, -92] # Nested table array
    }
    
    # 2. SERIALIZE TO TEXT STRING BLOCK
    # This turns the data into raw text characters, adding heavy formatting bloat
    json_string = json.dumps(telemetry_data)
    payload_bytes = json_string.encode('utf-8')
    
    print(f"Target Destination Node  : {target_ip}:8080")
    print(f"Unoptimized Payload Size : {len(payload_bytes)} Bytes of Raw Text JSON")
    
    try:
        client_socket.connect((target_ip, 8080))
        start_clock = time.perf_counter()
        
        # Stream the full text JSON string over the persistent socket
        for _ in range(total_packets):
            client_socket.sendall(payload_bytes)
            response = client_socket.recv(1024)
            
        duration = time.perf_counter() - start_clock
        print(f"\nFlood Completed! Duration: {duration:.4f}s")
        
    except Exception as e:
        print(f"Network Connection Interrupted: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    while True:
        HOST_IP = "192.168.1.227" # Update with your ThinkPad's active IP
        BURST_VOLUME = 1000       # Run 1,000 rapid iterations to test baseline throughput
        run_json_flood(HOST_IP, BURST_VOLUME)
