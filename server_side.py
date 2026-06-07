# ============================================================
# ECE 3325 Project 1 - Weather Data Server
# Cleaned + Improved Version (Renamed Variables & Comments)
# ============================================================

import socket

# CSV output file where processed packets are stored
OUTPUT_CSV = "output.csv"

# Create CSV header if first time running
try:
    with open(OUTPUT_CSV, "x") as f:
        f.write("StationID,Date,TempC,Condition\n")
except FileExistsError:
    pass  # File already exists, continue normally


def parse_weather_packet(raw_packet):
    """
    Parse a WX-format packet.

    Expected Format:
        WX|StationID|Date|Temperature|Condition
    
    Returns tuple if valid, otherwise None.
    """
    parts = raw_packet.split("|")

    if len(parts) != 5:
        return None
    if parts[0] != "WX":
        return None

    _, station_id, date_info, temperature, condition = parts
    return station_id, date_info, temperature, condition


def store_weather_entry(packet_text):
    """
    Validates a WX packet and writes it to output.csv.
    Returns True if the packet is valid and stored.
    """
    parsed = parse_weather_packet(packet_text)

    if parsed is None:
        return False

    station_id, date_info, temperature, condition = parsed

    with open(OUTPUT_CSV, "a") as f:
        f.write(f"{station_id},{date_info},{temperature},{condition}\n")

    return True


def launch_weather_server():
    """
    Runs a simple TCP weather-data server.
    - Listens for one client
    - Processes incoming newline-separated packets
    - Responds with OK or ERR
    """
    print("Weather Server Online (Port 23456)...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("", 23456))
        server_socket.listen(1)

        connection, address = server_socket.accept()
        print(f"Client connected from: {address}")

        with connection:
            buffer_data = ""

            while True:
                incoming = connection.recv(1024)
                if not incoming:
                    break  # Client disconnected

                buffer_data += incoming.decode()

                # Process each packet per newline
                while "\n" in buffer_data:
                    packet_line, buffer_data = buffer_data.split("\n", 1)
                    packet_line = packet_line.strip()

                    if not packet_line:
                        continue

                    success = store_weather_entry(packet_line)

                    if success:
                        connection.sendall(b"OK\n")
                    else:
                        connection.sendall(b"ERR\n")


if __name__ == "__main__":
    launch_weather_server()
