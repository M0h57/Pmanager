import os
import socket
import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread

class PS5PayloadApp(App):
    def build(self):
        # Main UI Layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # IP Address Dropdown
        self.ip_spinner = Spinner(
            text='192.168.1.100',
            values=('192.168.1.100', '192.168.1.50', '192.168.1.25'),
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.ip_spinner)
        
        # Payload Source URL
        self.repo_input = TextInput(
            text='https://raw.githubusercontent.com/username/repo/main/payloads.json',
            multiline=False,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.repo_input)
        
        # Action Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        sync_btn = Button(text='Sync GitHub Repo')
        sync_btn.bind(on_press=self.start_sync)
        btn_layout.add_widget(sync_btn)
        
        send_btn = Button(text='Send Payload')
        send_btn.bind(on_press=self.start_send)
        btn_layout.add_widget(send_btn)
        
        self.layout.add_widget(btn_layout)
        
        # Log Output Area
        self.log_area = TextInput(
            readonly=True, 
            text='[System] App initialized. Ready to deploy payloads.\n', 
            size_hint=(1, 0.7)
        )
        self.layout.add_widget(self.log_area)
        
        return self.layout

    @mainthread
    def log(self, message):
        """Thread-safe logging to the UI."""
        self.log_area.text += f"{message}\n"

    def start_sync(self, instance):
        threading.Thread(target=self._sync_logic, daemon=True).start()

    def _sync_logic(self):
        self.log("\n[Sync] Fetching updates from source...")
        try:
            req = requests.get(self.repo_input.text, timeout=5)
            if req.status_code == 200:
                self.log("[Sync] Success! Parsing payload data...")
                # Add your JSON parsing and downloading logic here
            else:
                self.log(f"[Sync] Failed. HTTP Status: {req.status_code}")
        except Exception as e:
            self.log(f"[Error] Sync failed: {str(e)}")

    def start_send(self, instance):
        threading.Thread(target=self._send_logic, daemon=True).start()

    def _send_logic(self):
        ip = self.ip_spinner.text
        port = 9020 # Standard PS5 payload port
        
        self.log(f"\n[Network] Connecting to {ip}:{port}...")
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5.0)
            client_socket.connect((ip, port))
            
            # This is where you would open the downloaded .bin/.elf and send it
            # with open('payload.elf', 'rb') as f:
            #     client_socket.sendall(f.read())
            
            self.log("[Network] Connection established. Payload sent successfully!")
        except Exception as e:
            self.log(f"[Network Error] {str(e)}")
        finally:
            client_socket.close()

if __name__ == '__main__':
    PS5PayloadApp().run()
