import json
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import obsws_python as obs
import os
from datetime import datetime

class CustomStyle:
    """Classe para gerenciar estilos personalizados."""
    
    # Cores
    BG_LIGHT = "#FFFFFF"  # Fundo branco
    BG_MEDIUM = "#F5F5F5"  # Fundo cinza muito claro
    BG_HOVER = "#E0E0E0"  # Cinza claro para hover
    FG_DARK = "#000000"   # Texto preto
    FG_MEDIUM = "#000000" # Texto preto
    ACCENT = "#2196F3"    # Azul
    ACCENT_DARK = "#1976D2"  # Azul escuro
    WARNING = "#FF9800"   # Laranja
    ERROR = "#F44336"     # Vermelho
    SUCCESS = "#4CAF50"   # Verde
    
    def __init__(self):
        self.style = ttk.Style()
        self.configure_styles()
    
    def configure_styles(self):
        """Configura os estilos personalizados."""
        # Configuração geral
        self.style.configure(".",
            background=self.BG_LIGHT,
            foreground=self.FG_DARK,
            font=("Segoe UI", 10)
        )
        
        # Notebook (abas)
        self.style.configure("TNotebook",
            background=self.BG_LIGHT,
            borderwidth=0
        )
        self.style.configure("TNotebook.Tab",
            background=self.BG_MEDIUM,
            foreground=self.FG_DARK,
            padding=[15, 8],
            font=("Segoe UI", 10, "bold")
        )
        self.style.map("TNotebook.Tab",
            background=[("selected", self.ACCENT), ("active", self.BG_HOVER)],
            foreground=[("selected", self.FG_DARK)]  # Texto preto mesmo quando selecionado
        )
        
        # Frame
        self.style.configure("TFrame",
            background=self.BG_LIGHT
        )
        
        # LabelFrame
        self.style.configure("TLabelframe",
            background=self.BG_LIGHT,
            foreground=self.FG_DARK
        )
        self.style.configure("TLabelframe.Label",
            background=self.BG_LIGHT,
            foreground=self.FG_DARK,
            font=("Segoe UI", 11, "bold")
        )
        
        # Label
        self.style.configure("TLabel",
            background=self.BG_LIGHT,
            foreground=self.FG_DARK,
            font=("Segoe UI", 10)
        )
        
        # Status Labels - Todos em preto
        self.style.configure("Status.TLabel",
            font=("Segoe UI", 10, "bold"),
            foreground=self.FG_DARK
        )
        self.style.configure("Connected.TLabel",
            foreground=self.FG_DARK,
            font=("Segoe UI", 10, "bold")
        )
        self.style.configure("Disconnected.TLabel",
            foreground=self.FG_DARK,
            font=("Segoe UI", 10, "bold")
        )
        self.style.configure("Recording.TLabel",
            foreground=self.FG_DARK,
            font=("Segoe UI", 10, "bold")
        )
        self.style.configure("Timer.TLabel",
            font=("Segoe UI", 24, "bold"),
            foreground=self.FG_DARK
        )
        
        # Entry
        self.style.configure("TEntry",
            fieldbackground=self.BG_LIGHT,
            foreground=self.FG_DARK,
            insertcolor=self.FG_DARK,
            borderwidth=1,
            relief="solid"
        )
        
        # Button - Texto preto em todos os estados
        self.style.configure("TButton",
            background=self.BG_MEDIUM,
            foreground=self.FG_DARK,
            padding=[15, 8],
            font=("Segoe UI", 10, "bold"),
            borderwidth=1
        )
        self.style.map("TButton",
            background=[("active", self.BG_HOVER), ("disabled", self.BG_MEDIUM)],
            foreground=[("disabled", self.FG_DARK)]
        )
        
        # Success Button
        self.style.configure("Success.TButton",
            background=self.BG_MEDIUM,
            foreground=self.FG_DARK
        )
        self.style.map("Success.TButton",
            background=[("active", self.BG_HOVER), ("disabled", self.BG_MEDIUM)],
            foreground=[("disabled", self.FG_DARK)]
        )
        
        # Warning Button
        self.style.configure("Warning.TButton",
            background=self.BG_MEDIUM,
            foreground=self.FG_DARK
        )
        self.style.map("Warning.TButton",
            background=[("active", self.BG_HOVER), ("disabled", self.BG_MEDIUM)],
            foreground=[("disabled", self.FG_DARK)]
        )
        
        # Error Button
        self.style.configure("Error.TButton",
            background=self.BG_MEDIUM,
            foreground=self.FG_DARK
        )
        self.style.map("Error.TButton",
            background=[("active", self.BG_HOVER), ("disabled", self.BG_MEDIUM)],
            foreground=[("disabled", self.FG_DARK)]
        )
        
        # Separator
        self.style.configure("TSeparator",
            background=self.BG_HOVER
        )

class OBSController:
    def __init__(self, config_file='obs_config.json'):
        # Carregar configuração
        self.config = self.carregar_configuracao(config_file)
        self.client = None
        self.connected = False
        self.is_recording = False
        self.status_thread = None
        self.stop_thread = False
        print("OBSController inicializado")
    
    def carregar_configuracao(self, arquivo):
        """Carrega as configurações de conexão do arquivo JSON."""
        try:
            with open(arquivo, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configuração: {e}")
            return {"host": "localhost", "port": 4456, "password": ""}
    
    def salvar_configuracao(self, config, arquivo='obs_config.json'):
        """Salva as configurações no arquivo JSON."""
        try:
            with open(arquivo, 'w') as f:
                json.dump(config, f)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configuração: {e}")
            return False
    
    def conectar(self):
        """Conecta ao OBS via websocket."""
        if self.connected:
            print("Já está conectado")
            return True
            
        try:
            host = self.config.get("host", "localhost")
            port = self.config.get("port", 4456)
            password = self.config.get("password", "")
            
            print(f"Tentando conectar ao OBS em {host}:{port}")
            print(f"Usando senha: {'Sim' if password else 'Não'}")
            
            # Criar cliente OBS
            self.client = obs.ReqClient(host=host, port=port, password=password, timeout=3)
            
            # Verificar conexão obtendo a versão
            print("Verificando conexão...")
            version = self.client.get_version()
            print(f"Versão OBS: {version.obs_version}")
            print(f"Versão WebSocket: {version.obs_web_socket_version}")
            
            self.connected = True
            print("Conexão estabelecida com sucesso")
            
            # Iniciar thread de monitoramento
            self.stop_thread = False
            self.status_thread = threading.Thread(target=self.monitorar_status)
            self.status_thread.daemon = True
            self.status_thread.start()
            print("Thread de monitoramento iniciada")
            
            return True
        except Exception as e:
            print(f"Erro durante a conexão: {e}")
            self.client = None
            self.connected = False
            raise e
    
    def desconectar(self):
        """Desconecta do OBS."""
        if not self.connected:
            print("Já está desconectado")
            return
            
        try:
            print("Iniciando desconexão")
            self.stop_thread = True
            if self.status_thread:
                self.status_thread.join(timeout=1)
                print("Thread de monitoramento encerrada")
            
            if self.client:
                del self.client
                self.client = None
                print("Desconectado do OBS")
            self.connected = False
        except Exception as e:
            print(f"Erro ao desconectar: {e}")
            messagebox.showerror("Erro", f"Erro ao desconectar: {e}")
    
    def iniciar_gravacao(self):
        """Inicia a gravação no OBS."""
        if not self.connected and not self.conectar():
            return False
            
        try:
            print("Iniciando gravação...")
            self.client.start_record()
            self.is_recording = True
            print("Gravação iniciada com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao iniciar gravação: {e}")
            raise e
    
    def parar_gravacao(self):
        """Para a gravação no OBS."""
        if not self.connected:
            return False
            
        try:
            print("Parando gravação...")
            self.client.stop_record()
            self.is_recording = False
            print("Gravação parada com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao parar gravação: {e}")
            raise e
    
    def verificar_status(self):
        """Verifica se está gravando ou não."""
        if not self.connected or not self.client:
            return False
            
        try:
            status = self.client.get_record_status()
            novo_status = status.output_active
            
            if novo_status != self.is_recording:
                print(f"Status de gravação mudou para: {'Gravando' if novo_status else 'Parado'}")
                self.is_recording = novo_status
            
            return self.is_recording
        except Exception as e:
            print(f"Erro ao verificar status: {e}")
            return False
    
    def monitorar_status(self):
        """Thread para monitorar continuamente o status da gravação."""
        print("Iniciando monitoramento de status")
        ultima_verificacao = 0
        
        while not self.stop_thread:
            if self.connected and self.client:
                try:
                    # Reduz a frequência de verificação para cada 2 segundos
                    agora = time.time()
                    if agora - ultima_verificacao >= 2:
                        self.verificar_status()
                        ultima_verificacao = agora
                except Exception as e:
                    print(f"Erro no monitoramento: {e}")
                    self.connected = False
            time.sleep(0.5)  # Reduz o uso de CPU
        print("Monitoramento de status encerrado")

class OBSControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OBS Auto Recorder")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.configure(bg=CustomStyle.BG_LIGHT)  # Fundo branco
        
        # Aplicar estilo personalizado
        self.style = CustomStyle()
        
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        print("Iniciando interface gráfica")
        self.obs = OBSController()
        
        # Variáveis para controle de estado
        self.connecting = False
        self.recording = False
        self.timer_running = False
        self.timer_thread = None
        
        # Variáveis para o timer
        self.hora_inicio = tk.StringVar(value="00:00")
        self.hora_fim = tk.StringVar(value="00:00")
        self.tempo_restante = tk.StringVar(value="--:--")
        
        self.criar_widgets()
        self.atualizar_status()
        self.atualizar_relogio()
        print("Interface gráfica inicializada")
    
    def criar_widgets(self):
        # Barra superior com relógio
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.relogio_var = tk.StringVar()
        relogio_label = ttk.Label(top_frame, textvariable=self.relogio_var, style="Timer.TLabel")
        relogio_label.pack(side=tk.RIGHT)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Aba de Conexão
        self.aba_conexao = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_conexao, text="Conexão")
        self.criar_aba_conexao()
        
        # Aba de Gravação
        self.aba_gravacao = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_gravacao, text="Gravação")
        self.criar_aba_gravacao()
    
    def criar_aba_conexao(self):
        # Frame de status
        status_frame = ttk.LabelFrame(self.aba_conexao, text="Status", padding=15)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.connection_var = tk.StringVar(value="Desconectado")
        self.recording_var = tk.StringVar(value="Não está gravando")
        
        # Grid para alinhar os status
        status_frame.columnconfigure(1, weight=1)
        
        # Ícones de status (usando caracteres Unicode)
        connection_icon = ttk.Label(status_frame, text="🔌", font=("Segoe UI", 14))
        connection_icon.grid(row=0, column=0, padx=(0,10), pady=5)
        
        connection_label = ttk.Label(status_frame, text="Status da Conexão:", style="Status.TLabel")
        connection_label.grid(row=0, column=1, sticky="w", pady=5)
        
        self.connection_status = ttk.Label(status_frame, textvariable=self.connection_var, style="Disconnected.TLabel")
        self.connection_status.grid(row=0, column=2, padx=10, pady=5)
        
        recording_icon = ttk.Label(status_frame, text="⏺", font=("Segoe UI", 14), foreground=CustomStyle.ERROR)
        recording_icon.grid(row=1, column=0, padx=(0,10), pady=5)
        
        recording_label = ttk.Label(status_frame, text="Status da Gravação:", style="Status.TLabel")
        recording_label.grid(row=1, column=1, sticky="w", pady=5)
        
        self.recording_status = ttk.Label(status_frame, textvariable=self.recording_var, style="Status.TLabel")
        self.recording_status.grid(row=1, column=2, padx=10, pady=5)
        
        # Separador
        ttk.Separator(self.aba_conexao, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        
        # Frame de controles
        control_frame = ttk.LabelFrame(self.aba_conexao, text="Controles", padding=15)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.connect_button = ttk.Button(control_frame, text="Conectar ao OBS", command=self.conectar_thread, style="Success.TButton")
        self.connect_button.pack(fill=tk.X, padx=5, pady=5)
        
        self.disconnect_button = ttk.Button(control_frame, text="Desconectar", command=self.desconectar, style="Error.TButton", state=tk.DISABLED)
        self.disconnect_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame de configuração
        config_frame = ttk.LabelFrame(self.aba_conexao, text="Configuração", padding=15)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Grid para alinhar os campos
        config_frame.columnconfigure(1, weight=1)
        
        host_label = ttk.Label(config_frame, text="Host:")
        host_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.host_var = tk.StringVar(value=self.obs.config.get("host", "localhost"))
        host_entry = ttk.Entry(config_frame, textvariable=self.host_var)
        host_entry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        port_label = ttk.Label(config_frame, text="Porta:")
        port_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.port_var = tk.StringVar(value=str(self.obs.config.get("port", 4456)))
        port_entry = ttk.Entry(config_frame, textvariable=self.port_var)
        port_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        password_label = ttk.Label(config_frame, text="Senha:")
        password_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        self.password_var = tk.StringVar(value=self.obs.config.get("password", ""))
        password_entry = ttk.Entry(config_frame, textvariable=self.password_var, show="•")
        password_entry.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        save_button = ttk.Button(config_frame, text="Salvar Configuração", command=self.salvar_config)
        save_button.grid(row=3, column=0, columnspan=2, sticky="we", padx=5, pady=10)
    
    def criar_aba_gravacao(self):
        # Frame de controles manuais
        manual_frame = ttk.LabelFrame(self.aba_gravacao, text="Controle Manual", padding=15)
        manual_frame.pack(fill=tk.X, padx=10, pady=5)
        
        button_frame = ttk.Frame(manual_frame)
        button_frame.pack(fill=tk.X)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        self.start_button = ttk.Button(button_frame, text="▶ Iniciar Gravação", 
                                     command=self.iniciar_gravacao_thread,
                                     style="Success.TButton",
                                     state=tk.DISABLED)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.stop_button = ttk.Button(button_frame, text="⏹ Parar Gravação",
                                    command=self.parar_gravacao_thread,
                                    style="Error.TButton",
                                    state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Separador
        ttk.Separator(self.aba_gravacao, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        
        # Frame de timer
        timer_frame = ttk.LabelFrame(self.aba_gravacao, text="Timer de Gravação", padding=15)
        timer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Grid para organizar os campos do timer
        timer_frame.columnconfigure(1, weight=1)
        
        # Hora de início
        ttk.Label(timer_frame, text="🕒 Hora de Início:", style="Status.TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        hora_inicio_entry = ttk.Entry(timer_frame, textvariable=self.hora_inicio, width=10, justify="center")
        hora_inicio_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(timer_frame, text="(HH:MM)").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        
        # Hora de fim
        ttk.Label(timer_frame, text="🕒 Hora de Fim:", style="Status.TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        hora_fim_entry = ttk.Entry(timer_frame, textvariable=self.hora_fim, width=10, justify="center")
        hora_fim_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(timer_frame, text="(HH:MM)").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        
        # Separador
        ttk.Separator(timer_frame, orient='horizontal').grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=10)
        
        # Tempo restante com destaque
        ttk.Label(timer_frame, text="⏱ Tempo Restante:", style="Status.TLabel").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(timer_frame, textvariable=self.tempo_restante, style="Timer.TLabel").grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Botões do timer
        timer_buttons_frame = ttk.Frame(timer_frame)
        timer_buttons_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)
        timer_buttons_frame.columnconfigure(0, weight=1)
        timer_buttons_frame.columnconfigure(1, weight=1)
        
        self.timer_start_button = ttk.Button(timer_buttons_frame,
                                           text="▶ Ativar Timer",
                                           command=self.iniciar_timer,
                                           style="Success.TButton",
                                           state=tk.DISABLED)
        self.timer_start_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.timer_stop_button = ttk.Button(timer_buttons_frame,
                                          text="⏹ Parar Timer",
                                          command=self.parar_timer,
                                          style="Error.TButton",
                                          state=tk.DISABLED)
        self.timer_stop_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Indicador de timer ativo
        self.timer_status_var = tk.StringVar(value="Timer Desativado")
        self.timer_status_label = ttk.Label(timer_frame,
                                          textvariable=self.timer_status_var,
                                          style="Status.TLabel")
        self.timer_status_label.grid(row=5, column=0, columnspan=3, pady=10)
    
    def atualizar_relogio(self):
        """Atualiza o relógio digital."""
        agora = datetime.now()
        self.relogio_var.set(agora.strftime("%H:%M:%S"))
        self.root.after(1000, self.atualizar_relogio)
    
    def validar_hora(self, hora_str):
        """Valida o formato da hora HH:MM."""
        try:
            if len(hora_str) != 5:
                return False
            horas, minutos = hora_str.split(":")
            horas = int(horas)
            minutos = int(minutos)
            return 0 <= horas < 24 and 0 <= minutos < 60
        except:
            return False
    
    def iniciar_timer(self):
        """Inicia o timer de gravação."""
        if not self.validar_hora(self.hora_inicio.get()) or not self.validar_hora(self.hora_fim.get()):
            messagebox.showerror("Erro", "Formato de hora inválido. Use HH:MM (exemplo: 09:30)")
            return
        
        if self.timer_running:
            return
        
        self.timer_running = True
        self.timer_start_button.config(state=tk.DISABLED)
        self.timer_stop_button.config(state=tk.NORMAL)
        
        def timer_loop():
            while self.timer_running:
                agora = time.localtime()
                hora_atual = f"{agora.tm_hour:02d}:{agora.tm_min:02d}"
                
                # Verificar hora de início
                if hora_atual == self.hora_inicio.get() and not self.obs.is_recording:
                    print(f"Timer: Iniciando gravação em {hora_atual}")
                    self.iniciar_gravacao_thread()
                
                # Verificar hora de fim
                if hora_atual == self.hora_fim.get() and self.obs.is_recording:
                    print(f"Timer: Parando gravação em {hora_atual}")
                    self.parar_gravacao_thread()
                
                # Atualizar tempo restante
                if self.obs.is_recording:
                    hora_fim = time.strptime(self.hora_fim.get(), "%H:%M")
                    hora_fim = hora_fim.tm_hour * 60 + hora_fim.tm_min
                    hora_atual = agora.tm_hour * 60 + agora.tm_min
                    
                    if hora_fim < hora_atual:  # Se passar da meia-noite
                        hora_fim += 24 * 60
                    
                    minutos_restantes = hora_fim - hora_atual
                    horas = minutos_restantes // 60
                    minutos = minutos_restantes % 60
                    self.tempo_restante.set(f"{horas:02d}:{minutos:02d}")
                else:
                    self.tempo_restante.set("--:--")
                
                time.sleep(1)
        
        self.timer_thread = threading.Thread(target=timer_loop, daemon=True)
        self.timer_thread.start()
        print("Timer iniciado")
    
    def parar_timer(self):
        """Para o timer de gravação."""
        if not self.timer_running:
            return
        
        self.timer_running = False
        self.timer_start_button.config(state=tk.NORMAL)
        self.timer_stop_button.config(state=tk.DISABLED)
        self.tempo_restante.set("--:--")
        print("Timer parado")
    
    def salvar_config(self):
        """Salva as configurações do formulário."""
        try:
            host = self.host_var.get()
            port = int(self.port_var.get())
            password = self.password_var.get()
            
            config = {"host": host, "port": port, "password": password}
            if self.obs.salvar_configuracao(config):
                self.obs.config = config
                messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "A porta deve ser um número inteiro.")
    
    def conectar_thread(self):
        """Inicia uma thread para conectar ao OBS."""
        if self.connecting:
            print("Já está tentando conectar")
            return
            
        print("Iniciando processo de conexão")
        self.connecting = True
        self.connect_button.config(state=tk.DISABLED)
        
        def conectar():
            erro = None
            try:
                if self.obs.conectar():
                    print("Conexão bem-sucedida, atualizando UI")
                    self.root.after(0, self._atualizar_ui_conectado)
            except Exception as e:
                erro = str(e)
                print(f"Erro na conexão: {erro}")
                self.root.after(0, lambda: self._mostrar_erro_conexao(erro))
            finally:
                self.connecting = False
                if not self.obs.connected:
                    print("Conexão falhou, reabilitando botão")
                    self.root.after(0, lambda: self.connect_button.config(state=tk.NORMAL))
        
        threading.Thread(target=conectar, daemon=True).start()
        print("Thread de conexão iniciada")
    
    def _atualizar_ui_conectado(self):
        """Atualiza a UI após conexão bem-sucedida."""
        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.connection_var.set("Conectado")
        messagebox.showinfo("Sucesso", "Conectado ao OBS com sucesso!")
    
    def _mostrar_erro_conexao(self, erro):
        """Mostra mensagem de erro de conexão."""
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao OBS: {erro}")
    
    def desconectar(self):
        """Desconecta do OBS."""
        self.obs.desconectar()
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.connection_var.set("Desconectado")
        self.recording_var.set("Não está gravando")
    
    def iniciar_gravacao_thread(self):
        """Inicia uma thread para começar a gravação."""
        if self.recording:
            return
            
        print("Iniciando thread de gravação")
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        
        def iniciar():
            erro = None
            try:
                if self.obs.iniciar_gravacao():
                    print("Gravação iniciada, atualizando UI")
                    self.root.after(0, self._atualizar_ui_gravando)
            except Exception as e:
                erro = str(e)
                print(f"Erro ao iniciar gravação: {erro}")
                self.root.after(0, lambda: self._mostrar_erro_gravacao(erro))
            finally:
                if not self.obs.is_recording:
                    print("Gravação não iniciou, resetando estado")
                    self.recording = False
                    self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        
        threading.Thread(target=iniciar, daemon=True).start()
    
    def _atualizar_ui_gravando(self):
        """Atualiza a UI após iniciar gravação."""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.recording_var.set("Gravando")
        messagebox.showinfo("Sucesso", "Gravação iniciada com sucesso!")
    
    def _mostrar_erro_gravacao(self, erro):
        """Mostra mensagem de erro de gravação."""
        messagebox.showerror("Erro", f"Erro ao iniciar gravação: {erro}")
    
    def parar_gravacao_thread(self):
        """Inicia uma thread para parar a gravação."""
        if not self.obs.is_recording:
            print("Não está gravando, ignorando comando de parar")
            return
            
        print("Iniciando thread para parar gravação")
        self.stop_button.config(state=tk.DISABLED)
        
        def parar():
            erro = None
            try:
                if self.obs.parar_gravacao():
                    print("Gravação parada, atualizando UI")
                    self.recording = False
                    self.root.after(0, self._atualizar_ui_parado)
            except Exception as e:
                erro = str(e)
                print(f"Erro ao parar gravação: {erro}")
                self.root.after(0, lambda: self._mostrar_erro_parar(erro))
            finally:
                if self.obs.is_recording:
                    print("Gravação continua ativa, reabilitando botão de parar")
                    self.root.after(0, lambda: self.stop_button.config(state=tk.NORMAL))
        
        threading.Thread(target=parar, daemon=True).start()
    
    def _atualizar_ui_parado(self):
        """Atualiza a UI após parar gravação."""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.recording_var.set("Não está gravando")
        messagebox.showinfo("Sucesso", "Gravação parada com sucesso!")
    
    def _mostrar_erro_parar(self, erro):
        """Mostra mensagem de erro ao parar gravação."""
        messagebox.showerror("Erro", f"Erro ao parar gravação: {erro}")
    
    def atualizar_status(self):
        """Atualiza o status da interface com base no estado do OBS."""
        try:
            if self.obs.connected:
                self.connection_var.set("Conectado")
                self.connection_status.configure(style="Status.TLabel")  # Texto preto
                self.disconnect_button.config(state=tk.NORMAL)
                self.connect_button.config(state=tk.DISABLED)
                self.timer_start_button.config(state=tk.NORMAL)
                
                if self.obs.is_recording:
                    self.recording_var.set("Gravando")
                    self.recording_status.configure(style="Status.TLabel")  # Texto preto
                    self.start_button.config(state=tk.DISABLED)
                    self.stop_button.config(state=tk.NORMAL)
                    self.recording = True
                else:
                    self.recording_var.set("Não está gravando")
                    self.recording_status.configure(style="Status.TLabel")  # Texto preto
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.recording = False
            else:
                self.connection_var.set("Desconectado")
                self.connection_status.configure(style="Status.TLabel")  # Texto preto
                self.recording_var.set("Não está gravando")
                self.recording_status.configure(style="Status.TLabel")  # Texto preto
                self.connect_button.config(state=tk.NORMAL)
                self.disconnect_button.config(state=tk.DISABLED)
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                self.timer_start_button.config(state=tk.DISABLED)
                self.timer_stop_button.config(state=tk.DISABLED)
                self.recording = False
                self.parar_timer()
            
            # Atualizar status do timer
            if self.timer_running:
                self.timer_status_var.set("⏱ Timer Ativo")
                self.timer_status_label.configure(foreground=self.FG_DARK)  # Texto preto
            else:
                self.timer_status_var.set("⏱ Timer Desativado")
                self.timer_status_label.configure(foreground=self.FG_DARK)  # Texto preto
            
        except Exception as e:
            print(f"Erro ao atualizar status da interface: {e}")
        finally:
            self.root.after(1000, self.atualizar_status)

if __name__ == "__main__":
    root = tk.Tk()
    app = OBSControllerGUI(root)
    root.mainloop() 