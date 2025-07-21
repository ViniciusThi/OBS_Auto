import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import subprocess
import os
import json
from datetime import datetime, timedelta
import requests

class OBSAutoRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("OBS Auto Recorder")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Configurações do OBS WebSocket
        self.obs_host = "localhost"
        self.obs_port = 4455
        self.obs_password = ""
        
        # Variáveis de controle
        self.recording_thread = None
        self.is_scheduled = False
        self.start_time = None
        self.stop_time = None
        
        # Carregar configurações salvas
        self.load_config()
        
        # Criar interface
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="OBS Auto Recorder", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Configurações do OBS
        config_frame = ttk.LabelFrame(main_frame, text="Configurações do OBS", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(config_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.host_entry = ttk.Entry(config_frame, width=15)
        self.host_entry.insert(0, self.obs_host)
        self.host_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(config_frame, text="Porta:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.port_entry = ttk.Entry(config_frame, width=10)
        self.port_entry.insert(0, str(self.obs_port))
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(config_frame, text="Senha:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.password_entry = ttk.Entry(config_frame, width=15, show="*")
        self.password_entry.insert(0, self.obs_password)
        self.password_entry.grid(row=0, column=5, sticky=tk.W)
        
        # Horários de gravação
        schedule_frame = ttk.LabelFrame(main_frame, text="Horários de Gravação", padding="10")
        schedule_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Hora de início
        ttk.Label(schedule_frame, text="Iniciar gravação às:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.start_hour = ttk.Spinbox(schedule_frame, from_=0, to=23, width=5)
        self.start_hour.set("09")
        self.start_hour.grid(row=0, column=1, padx=(5, 2))
        
        ttk.Label(schedule_frame, text=":").grid(row=0, column=2)
        self.start_minute = ttk.Spinbox(schedule_frame, from_=0, to=59, width=5)
        self.start_minute.set("00")
        self.start_minute.grid(row=0, column=3, padx=(2, 10))
        
        # Hora de parada
        ttk.Label(schedule_frame, text="Parar gravação às:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.stop_hour = ttk.Spinbox(schedule_frame, from_=0, to=23, width=5)
        self.stop_hour.set("18")
        self.stop_hour.grid(row=1, column=1, padx=(5, 2))
        
        ttk.Label(schedule_frame, text=":").grid(row=1, column=2)
        self.stop_minute = ttk.Spinbox(schedule_frame, from_=0, to=59, width=5)
        self.stop_minute.set("00")
        self.stop_minute.grid(row=1, column=3, padx=(2, 10))
        
        # Botões de controle
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        self.start_button = ttk.Button(button_frame, text="Iniciar Agendamento", 
                                      command=self.start_scheduling)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="Parar Agendamento", 
                                     command=self.stop_scheduling, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        self.test_button = ttk.Button(button_frame, text="Testar Conexão", 
                                     command=self.test_connection)
        self.test_button.grid(row=0, column=2)
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Aguardando...", 
                                     font=("Arial", 10))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.time_label = ttk.Label(status_frame, text="", font=("Arial", 9))
        self.time_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, height=6, width=60)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Atualizar horário
        self.update_time()
        
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def update_time(self):
        """Atualiza o horário atual"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Horário atual: {current_time}")
        self.root.after(1000, self.update_time)
        
    def load_config(self):
        """Carrega configurações salvas"""
        try:
            if os.path.exists("obs_config.json"):
                with open("obs_config.json", "r") as f:
                    config = json.load(f)
                    self.obs_host = config.get("host", "localhost")
                    self.obs_port = config.get("port", 4455)
                    self.obs_password = config.get("password", "")
        except Exception as e:
            self.log_message(f"Erro ao carregar configurações: {e}")
            
    def save_config(self):
        """Salva configurações"""
        try:
            config = {
                "host": self.host_entry.get(),
                "port": int(self.port_entry.get()),
                "password": self.password_entry.get()
            }
            with open("obs_config.json", "w") as f:
                json.dump(config, f)
        except Exception as e:
            self.log_message(f"Erro ao salvar configurações: {e}")
            
    def test_connection(self):
        """Testa conexão com o OBS"""
        self.save_config()
        self.log_message("Testando conexão com OBS...")
        
        try:
            # Verificar se o OBS está rodando
            response = requests.get(f"http://{self.host_entry.get()}:{self.port_entry.get()}/api/status")
            if response.status_code == 200:
                self.log_message("✓ Conexão com OBS estabelecida com sucesso!")
                messagebox.showinfo("Sucesso", "Conexão com OBS estabelecida!")
            else:
                self.log_message("✗ Falha na conexão com OBS")
                messagebox.showerror("Erro", "Falha na conexão com OBS")
        except Exception as e:
            self.log_message(f"✗ Erro na conexão: {e}")
            messagebox.showerror("Erro", f"Erro na conexão: {e}")
            
    def start_recording(self):
        """Inicia a gravação no OBS"""
        try:
            url = f"http://{self.host_entry.get()}:{self.port_entry.get()}/api/start-recording"
            response = requests.post(url)
            if response.status_code == 200:
                self.log_message("✓ Gravação iniciada com sucesso!")
                self.status_label.config(text="Gravando...", foreground="green")
            else:
                self.log_message("✗ Erro ao iniciar gravação")
        except Exception as e:
            self.log_message(f"✗ Erro ao iniciar gravação: {e}")
            
    def stop_recording(self):
        """Para a gravação no OBS"""
        try:
            url = f"http://{self.host_entry.get()}:{self.port_entry.get()}/api/stop-recording"
            response = requests.post(url)
            if response.status_code == 200:
                self.log_message("✓ Gravação parada com sucesso!")
                self.status_label.config(text="Aguardando...", foreground="black")
            else:
                self.log_message("✗ Erro ao parar gravação")
        except Exception as e:
            self.log_message(f"✗ Erro ao parar gravação: {e}")
            
    def start_scheduling(self):
        """Inicia o agendamento de gravação"""
        try:
            # Obter horários
            start_h = int(self.start_hour.get())
            start_m = int(self.start_minute.get())
            stop_h = int(self.stop_hour.get())
            stop_m = int(self.stop_minute.get())
            
            # Validar horários
            if not (0 <= start_h <= 23 and 0 <= start_m <= 59 and 
                   0 <= stop_h <= 23 and 0 <= stop_m <= 59):
                messagebox.showerror("Erro", "Horários inválidos!")
                return
                
            # Calcular horários de hoje
            now = datetime.now()
            self.start_time = now.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
            self.stop_time = now.replace(hour=stop_h, minute=stop_m, second=0, microsecond=0)
            
            # Se o horário de início já passou, agendar para amanhã
            if self.start_time <= now:
                self.start_time += timedelta(days=1)
                self.stop_time += timedelta(days=1)
                
            # Se o horário de parada é menor que o de início, parada é no dia seguinte
            if self.stop_time <= self.start_time:
                self.stop_time += timedelta(days=1)
                
            self.is_scheduled = True
            self.recording_thread = threading.Thread(target=self.scheduling_loop, daemon=True)
            self.recording_thread.start()
            
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            self.log_message(f"Agendamento iniciado - Início: {self.start_time.strftime('%H:%M')}, "
                           f"Parada: {self.stop_time.strftime('%H:%M')}")
            self.status_label.config(text="Agendamento ativo", foreground="blue")
            
        except Exception as e:
            self.log_message(f"Erro ao iniciar agendamento: {e}")
            messagebox.showerror("Erro", f"Erro ao iniciar agendamento: {e}")
            
    def stop_scheduling(self):
        """Para o agendamento de gravação"""
        self.is_scheduled = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Aguardando...", foreground="black")
        self.log_message("Agendamento parado")
        
    def scheduling_loop(self):
        """Loop principal do agendamento"""
        while self.is_scheduled:
            now = datetime.now()
            
            # Verificar se é hora de iniciar
            if now >= self.start_time:
                self.log_message("Hora de iniciar gravação!")
                self.start_recording()
                self.start_time += timedelta(days=1)  # Agendar para amanhã
                
            # Verificar se é hora de parar
            if now >= self.stop_time:
                self.log_message("Hora de parar gravação!")
                self.stop_recording()
                self.stop_time += timedelta(days=1)  # Agendar para amanhã
                
            time.sleep(1)  # Verificar a cada segundo

def main():
    root = tk.Tk()
    app = OBSAutoRecorder(root)
    root.mainloop()

if __name__ == "__main__":
    main() 