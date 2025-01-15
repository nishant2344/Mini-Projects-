import socket

def scan_ports(ip, start_port, end_port):
    """
    Scans ports in the specified range for a given IP address.

    Args:
        ip (str): The IP address to scan.
        start_port (int): The starting port number.
        end_port (int): The ending port number.

    Returns:
        list: A list of open ports.
    """
    open_ports = []

    print(f"Scanning IP: {ip} from port {start_port} to {end_port}\n")

    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Set a timeout of 0.5 seconds for the connection attempt
            result = s.connect_ex((ip, port))
            if result == 0:  # Port is open
                open_ports.append(port)

    return open_ports

if __name__ == "__main__":
    print("Welcome to the Port Scanner Tool")

    ip = input("Enter the IP address to scan: ").strip()

    while True:
        try:
            start_port = int(input("Enter the starting port number: ").strip())
            end_port = int(input("Enter the ending port number: ").strip())

            if start_port > 0 and end_port > 0 and start_port <= end_port:
                break
            else:
                print("Invalid range. Please enter valid port numbers.")
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    open_ports = scan_ports(ip, start_port, end_port)

    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            print(f"- Port {port} is open")
    else:
        print("\nNo open ports found in the specified range.")
