from djitellopy import Tello

def land_drone():
    # Initialize the Tello drone
    myDrone = Tello()

    # Connect to the drone
    myDrone.connect()

    # Print the battery level
    battery_level = myDrone.get_battery()
    print(f"Battery Level: {battery_level}%")

    # Send the land command
    print("Landing the drone...")
    myDrone.land()

    # Disconnect from the drone
    myDrone.end()
    print("Drone has landed and connection closed.")

if __name__ == "__main__":
    land_drone()
