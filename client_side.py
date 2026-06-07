# ============================================================
# ECE 3325 Project 1 - Weather Data Client
# Cleaned + Improved Version (Renamed Variables & Comments)
# ============================================================

import sys
import csv
import socket

# Source weather CSV
CSV_WEATHER_FILE = "Weather_data.csv"


def build_weather_packet(record):
    """
    Convert one CSV row into a standardized network packet.

    Custom Protocol Format:
        WX|StationID|Date|Temperature|Condition

    This function ensures:
    - Required fields exist
    - All values are stripped and cleaned
    - Returns None if row is invalid or incomplete
    """
    try:
        station_id = record[0].strip()
        date_info = record[1].strip()
        celsius_temp = record[3].strip()
        sky_condition = record[8].strip()
    except IndexError:
        return None  # Row missing needed columns

    if not station_id or not date_info or not celsius_temp:
        return None  # Skip blank/invalid rows

    return f"WX|{station_id}|{date_info}|{celsius_temp}|{sky_condition}"


def run_weather_client():
    """
    Main client execution:
    - Reads CSV
    - Encodes packets
    - Sends to server
    - Receives OK/ERR responses
    """
    if len(sys.argv) != 2:
        print("Usage: python3 client.py <server_ip>")
        return

    server_ip = sys.argv[1]
    print(f"Attempting to connect to server at {server_ip}...")

    # Create TCP connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 23456))
    print("Connection established.\n")

    # Load CSV data (skipping header)
    with open(CSV_WEATHER_FILE, newline="") as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)  # Skip the header row
        data_records = list(csv_reader)

    print("Weather CSV Loaded:")
    print(f"  Data rows found: {len(data_records)}")
    print(f"  First entry: {data_records[0]}\n")

    sent_count = 0
    skipped_count = 0

    # Send records to server
    for row in data_records:
        packet = build_weather_packet(row)

        if packet is None:
            skipped_count += 1
            continue

        client_socket.sendall((packet + "\n").encode())

        # Wait for server acknowledgment
        response = client_socket.recv(16).decode().strip()

        if response == "OK":
            sent_count += 1
        else:
            skipped_count += 1

    print("\n============== TRANSMISSION SUMMARY ==============")
    print(f"Successfully delivered: {sent_count}")
    print(f"Skipped or invalid   : {skipped_count}")
    print("===================================================\n")

    # Command loop
    while True:
        user_cmd = input("Client> ").strip()

        if user_cmd.upper() == "QUIT":
            print("Closing connection...")
            client_socket.close()
            print("Client terminated.")
            break
        else:
            print("Unknown command. Only 'QUIT' is supported.")
            

if __name__ == "__main__":
    run_weather_client()
