#!/usr/bin/env python3
# File: complex_server.py
import socket
import struct

def run_complex_binary_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(100)
    print("Server Active: Listening for 31-Byte Complex Binary Bitbuffers...")

    # Mirror the format blueprint exactly to parse the raw incoming bits
    decoder_format = ">14sIf?4h"
    EXPECTED_SIZE = struct.calcsize(decoder_format) # Evaluates to exactly 31 bytes

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            
            # Read exactly the 31-byte frame directly out of the network card buffer
            binary_data = client_socket.recv(EXPECTED_SIZE)
            
            if len(binary_data) == EXPECTED_SIZE:
                # 3. UNPACK THE BITSTREAM STRAIGHT BACK INTO VARIABLES
                unpacked_data = struct.unpack(decoder_format, binary_data)
                
                # Extract and clean individual attributes natively from the tuple
                device_mac = unpacked_data[0].decode('utf-8')
                timestamp = unpacked_data[1]
                bed_temp = unpacked_data[2]
                heating_active = unpacked_data[3]
                # Reconstruct our original nested tracking array layout
                respiration_waveform = list(unpacked_data[4:8])
                
                print("\n=== SYSTEM INGRESS VERIFICATION PASS ===")
                print(f"Device MAC Handle : {device_mac}")
                print(f"Epoch Timestamp   : {timestamp}")
                print(f"Core Thermal Float: {bed_temp:.2f}°F")
                print(f"Actuator Boolean  : {heating_active}")
                print(f"Nested Waveform   : {respiration_waveform}")
                
                client_socket.sendall(b"ACK_COMPLEX_COMPRESSION")
                
            client_socket.close()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_complex_binary_server()
