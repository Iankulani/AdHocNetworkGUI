import math
import socket
import tkinter as tk
from tkinter import messagebox
import threading
import time

class AdHocNetwork:
    def __init__(self, device_id, x_pos, y_pos, z_pos, mobility_range):
        self.device_id = device_id
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.mobility_range = mobility_range  # maximum communication range of the device

    def move(self, dx, dy, dz):
        self.x_pos += dx
        self.y_pos += dy
        self.z_pos += dz
        print(f"Device {self.device_id} moved to ({self.x_pos}, {self.y_pos}, {self.z_pos})")

    def distance_to(self, other_device):
        # Calculate Euclidean distance between two devices (in 3D space)
        return math.sqrt((self.x_pos - other_device.x_pos) ** 2 + 
                         (self.y_pos - other_device.y_pos) ** 2 + 
                         (self.z_pos - other_device.z_pos) ** 2)

    def can_communicate(self, other_device):
        # Check if the devices are within communication range
        distance = self.distance_to(other_device)
        if distance <= self.mobility_range:
            return True, distance
        else:
            return False, distance

# Socket server to simulate real-time networking
def socket_server(device, server_socket):
    server_socket.bind(("localhost", 12345))
    server_socket.listen(1)
    print(f"Device {device.device_id} is waiting for incoming connections...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    client_socket.send(f"{device.device_id} is online.".encode())
    client_socket.close()

def socket_client(device, server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 12345))
    print(f"Device {device.device_id} connected to server.")
    message = client_socket.recv(1024).decode()
    print(f"Message from server: {message}")
    client_socket.close()

# GUI for the Ad Hoc Network Simulation
class AdHocNetworkGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ad Hoc Network Simulation")
        self.geometry("500x400")
        
        self.device = None
        self.other_device = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.create_widgets()

    def create_widgets(self):
        self.device_id_label = tk.Label(self, text="Enter Device ID:")
        self.device_id_label.pack()
        
        self.device_id_entry = tk.Entry(self)
        self.device_id_entry.pack()

        self.x_pos_label = tk.Label(self, text="Enter X Position:")
        self.x_pos_label.pack()
        
        self.x_pos_entry = tk.Entry(self)
        self.x_pos_entry.pack()

        self.y_pos_label = tk.Label(self, text="Enter Y Position:")
        self.y_pos_label.pack()
        
        self.y_pos_entry = tk.Entry(self)
        self.y_pos_entry.pack()

        self.z_pos_label = tk.Label(self, text="Enter Z Position:")
        self.z_pos_label.pack()
        
        self.z_pos_entry = tk.Entry(self)
        self.z_pos_entry.pack()

        self.range_label = tk.Label(self, text="Enter Communication Range:")
        self.range_label.pack()

        self.range_entry = tk.Entry(self)
        self.range_entry.pack()

        self.other_device_id_label = tk.Label(self, text="Enter Other Device ID:")
        self.other_device_id_label.pack()

        self.other_device_id_entry = tk.Entry(self)
        self.other_device_id_entry.pack()

        self.start_button = tk.Button(self, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        self.move_button = tk.Button(self, text="Move Device", command=self.move_device)
        self.move_button.pack()

        self.communication_status_label = tk.Label(self, text="Communication Status: N/A")
        self.communication_status_label.pack()

    def start_simulation(self):
        # Create device based on user input
        device_id = self.device_id_entry.get()
        x_pos = float(self.x_pos_entry.get())
        y_pos = float(self.y_pos_entry.get())
        z_pos = float(self.z_pos_entry.get())
        mobility_range = float(self.range_entry.get())
        
        self.device = AdHocNetwork(device_id, x_pos, y_pos, z_pos, mobility_range)
        
        other_device_id = self.other_device_id_entry.get()
        other_device_x = float(self.x_pos_entry.get()) + 10
        other_device_y = float(self.y_pos_entry.get()) + 10
        other_device_z = float(self.z_pos_entry.get()) + 10
        other_device_range = mobility_range
        
        self.other_device = AdHocNetwork(other_device_id, other_device_x, other_device_y, other_device_z, other_device_range)

        # Check initial communication
        can_communicate, distance = self.device.can_communicate(self.other_device)
        if can_communicate:
            self.communication_status_label.config(text=f"Devices can communicate. Distance: {distance:.2f} meters.")
        else:
            self.communication_status_label.config(text=f"Devices cannot communicate. Distance: {distance:.2f} meters.")
        
        # Start socket server in another thread
        server_thread = threading.Thread(target=socket_server, args=(self.device, self.server_socket))
        server_thread.daemon = True
        server_thread.start()

    def move_device(self):
        dx = float(self.x_pos_entry.get())
        dy = float(self.y_pos_entry.get())
        dz = float(self.z_pos_entry.get())
        self.device.move(dx, dy, dz)

        can_communicate, distance = self.device.can_communicate(self.other_device)
        if can_communicate:
            self.communication_status_label.config(text=f"After moving, devices can communicate. Distance: {distance:.2f} meters.")
        else:
            self.communication_status_label.config(text=f"After moving, devices cannot communicate. Distance: {distance:.2f} meters.")

if __name__ == "__main__":
    app = AdHocNetworkGUI()
    app.mainloop()
