import omni.usd
import omni.kit.commands
import socket
import json
import asyncio
import carb

# UDP setup
UDP_IP = "127.0.0.1"  # localhost
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
                updated_positions = json.loads(data.decode())

                current_position = target_cube.GetAttribute("xformOp:translate").Get()
                new_position = (
                    updated_positions[0],
                    updated_positions[1],
                    updated_positions[2]
                )

                # Move the cube
                omni.kit.commands.execute('TransformPrimSRT',
                                          path=target_cube_path,
                                          new_translation=new_position
                                          )
                print(f"Moved cube to: {new_position}")
            except BlockingIOError:
                # No data available, continue the loop
                pass
        await asyncio.sleep(0.01)  # Small delay to prevent busy-waiting


# Function to stop the script
def stop_script():
    global running
    running = False
    sock.close()
    print("Script stopped.")


# Start the asyncio event loop
loop = asyncio.get_event_loop()
update_task = loop.create_task(update_cube_position())

print("Script is running. Move the cube using the UDP sender.")
print("To stop the script, call the stop_script() function.")

# Optionally, you can set up a timer to stop the script after a certain duration
# import omni.kit.app
# app = omni.kit.app.get_app()
# app.create_task_and_add_to_queue(stop_script, delay_ms=60000)  # Stop after 60 seconds