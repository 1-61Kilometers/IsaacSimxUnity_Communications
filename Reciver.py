import omni.usd
import omni.kit.commands
import socket
import json
import asyncio
import carb

# UDP setup
UDP_IP = "10.0.0.238"  # Change this to the IP address of the machine running the UDP sender
UDP_PORT = 5005

# Get the current stage
stage = omni.usd.get_context().get_stage()

# Find the TargetCube object
target_cube_path = "/World/TargetCube"
target_cube = stage.GetPrimAtPath(target_cube_path)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

# Flag to control the loop
running = True

async def update_cube_position():
    global running
    while running:
        if target_cube:
            try:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                updated_values = json.loads(data.decode())
                
                new_position = (
                    updated_values[0],
                    updated_values[1],
                    updated_values[2]
                )
                
                new_rotation = (
                    updated_values[3],
                    updated_values[4],
                    updated_values[5]
                )
                
                # Move and rotate the cube
                omni.kit.commands.execute('TransformPrimSRT',
                                          path=target_cube_path,
                                          new_translation=new_position,
                                          new_rotation_euler=new_rotation
                                          )
                print(f"Moved cube to: {new_position}, Rotated to: {new_rotation}")
            except BlockingIOError:
                # No data available, continue the loop
                pass
        await asyncio.sleep(0.001)  # Small delay to prevent busy-waiting

# Function to stop the script
def stop_script():
    global running
    running = False
    sock.close()
    print("Script stopped.")

# Start the asyncio event loop
loop = asyncio.get_event_loop()
update_task = loop.create_task(update_cube_position())

print("Script is running. Move and rotate the cube using the UDP sender.")
print("To stop the script, call the stop_script() function.")