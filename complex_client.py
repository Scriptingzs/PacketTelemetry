#!/usr/bin/env python3
# File: complex_client.py
import socket
import struct
import time

def transmit_complex_bitbuffer(target_ip: str):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5.0)

    # 1. DEFINE COMPLEX MULTI-TYPE SOURCE DATA
    device_mac = b"ESP32-BED-A1B2"                  # 14-byte raw string
    timestamp = int(time.time())                    # 4-byte unsigned integer
    bed_temp = 98.64                                # 4-byte floating-point number
    heating_active = True                           # 1-byte boolean flag
    respiration_waveform = [120, -45, 302, -88, 115, -50, 290, -92]     # Nested Array:  points of 2-byte short integers

    # 2. ENCODE VARIABLE MATRIX TO HIGH-DENSITY BITSTREAM
    # Format String Details:
    # '>' = Big-Endian byte ordering
    # '14s' = 14-byte string, 'I' = 4-byte Int, 'f' = 4-byte Float, '?' = 1-byte Bool, '8h' = Eight 2-byte Shorts
    encoder_format = ">14sIf?8h"
    
    binary_payload = struct.pack(
        encoder_format,
        device_mac,
        timestamp,
        bed_temp,
        heating_active,
        respiration_waveform[0],
        respiration_waveform[1],
        respiration_waveform[2],
        respiration_waveform[3],
        respiration_waveform[4],
        respiration_waveform[5],
        respiration_waveform[6],
        respiration_waveform[7]
    )

    print(f"Target Destination Node  : {target_ip}:8080")
    print(f"Complex Binary Mass Allocation: {len(binary_payload)} Bytes")

    try:
        client_socket.connect((target_ip, 8080))
        start_clock = time.perf_counter()
        
        # Blast the unstyled binary array across the network card adapter
        client_socket.sendall(binary_payload)
        
        response = client_socket.recv(1024)
        duration = time.perf_counter() - start_clock
        print(f"Server Acknowledgment Pass: {response.decode('utf-8')} | Latency: {duration:.4f}s")
        
    except Exception as network_error:
        print(f"Connection Line Interrupted: {network_error}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    while True:
        # Update with your ThinkPad P50's active local IP address string
        HOST_IP = "192.168.1.227" 
        transmit_complex_bitbuffer(HOST_IP)
