#sender? but i barely even know her!
import socket
import json
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_movement(x, y, z):
    movement = [x, y, z]
    message = json.dumps(movement).encode()
    sock.sendto(message, (UDP_IP, UDP_PORT))
    print(f"Sent movement: {movement}")


while True:
    command = input("Enter direction (up/down/left/right) or 'quit' to exit: ").lower()

    if command == 'quit':
        break
    elif command == 'up':
        send_movement(0, 0, 0.1)
    elif command == 'down':
        send_movement(0, 0, -0.1)
    elif command == 'left':
        send_movement(-0.1, 0, 0)
    elif command == 'right':
        send_movement(0.1, 0, 0)
    else:
        print("Invalid command. Please use up, down, left, or right.")

    time.sleep(0.1)  # Small delay to prevent flooding

print("Sender closed.")
sock.close()