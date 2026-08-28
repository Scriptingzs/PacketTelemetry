#!/usr/bin/env python3
# File: json_server.py
import socket
import json

def run_json_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(100)
    print("Server Active: Listening for Unoptimized Complex JSON Strings...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            
            # Read the incoming string characters out of the network buffer
            raw_text_bytes = client_socket.recv(4096)
            
            if raw_text_bytes:
                try:
                    # 3. PARSE THE TEXT STRING BACK INTO AN OBJECT IN MEMORY
                    json_string = raw_text_bytes.decode('utf-8')
                    parsed_payload = json.loads(json_string)
                    
                    # Extract variables to confirm accurate data reassembly
                    print(f"\n[INGRESS LOG] Device: {parsed_payload['device_mac_id']}")
                    print(f"Metrics: Temp: {parsed_payload['bed_temperature_f']} | Active: {parsed_payload['heating_elements_active']}")
                    print(f"Nested Data Table: {parsed_payload['respiration_waveform_samples']}")
                    
                    client_socket.sendall(b"ACK_JSON_TEXT")
                except Exception as parse_error:
                    print(f"Parsing Failure: {parse_error}")
                    
            client_socket.close()
    except KeyboardInterrupt:
        print("\nShutting down server node cleanly.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_json_server()
