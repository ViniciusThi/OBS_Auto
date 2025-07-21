# OBS Auto Recorder

Este programa permite controlar o OBS Studio remotamente via websocket para iniciar e parar gravações.

## Requisitos

- Python 3.6+
- OBS Studio instalado
- Plugin obs-websocket instalado no OBS

## Instalação

1. Instale o OBS Studio usando o instalador em `Executaveis/OBS-Studio-31.1.1-Windows-x64-Installer.exe`
2. Instale o plugin obs-websocket usando o instalador em `Executaveis/obs-websocket-4.9.1-compat-Qt6-Windows-Installer.exe`
3. Configure o plugin obs-websocket no OBS Studio:
   - Abra o OBS Studio
   - Vá para Ferramentas > WebSocket Server Settings
   - Ative o servidor websocket
   - Configure a porta (padrão 4455) 
   - Configure uma senha (usada no arquivo de configuração)

4. Instale as dependências do Python:
```
pip install -r requirements.txt
```

## Configuração

Edite o arquivo `obs_config.json` com os dados de conexão ao OBS:
```json
{
  "host": "localhost", 
  "port": 4455, 
  "password": "sua_senha"
}
```

- `host`: geralmente "localhost" se o OBS e o script estiverem no mesmo computador
- `port`: porta do websocket configurada no OBS (padrão 4455)
- `password`: senha configurada no plugin websocket

## Uso

### Versão de Linha de Comando

1. Inicie o OBS Studio
2. Execute o programa:
```
python obs_auto_recorder.py
```

3. Use o menu para:
   - Iniciar gravação
   - Parar gravação
   - Verificar status da gravação
   - Sair do programa

### Versão com Interface Gráfica

1. Inicie o OBS Studio
2. Execute o programa com interface gráfica:
```
python obs_auto_recorder_gui.py
```

3. Na interface gráfica você pode:
   - Conectar/desconectar do OBS
   - Iniciar/parar gravação
   - Ver o status da conexão e gravação em tempo real
   - Configurar as opções de conexão diretamente na interface

## Solução de problemas

- Verifique se o OBS está em execução
- Verifique se o plugin obs-websocket está instalado e configurado
- Verifique se as configurações no arquivo `obs_config.json` estão corretas 