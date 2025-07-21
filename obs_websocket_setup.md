# Configuração do OBS WebSocket

## Passo a Passo para Configurar o OBS WebSocket

### 1. Instalar o OBS WebSocket Plugin

#### Opção A: Instalação Automática (Recomendada)
1. Abra o OBS Studio
2. Vá em **Ferramentas** > **WebSocket Server Settings**
3. Se não aparecer esta opção, você precisa instalar o plugin

#### Opção B: Instalação Manual
1. Baixe o OBS WebSocket do site oficial: https://github.com/obsproject/obs-websocket
2. Ou use o instalador automático: https://github.com/obsproject/obs-websocket/releases
3. Execute o instalador e siga as instruções

### 2. Configurar o WebSocket Server

1. No OBS Studio, vá em **Ferramentas** > **WebSocket Server Settings**
2. Configure as seguintes opções:
   - **Enable WebSocket server**: ✅ Marque esta opção
   - **Server Port**: `4455` (padrão)
   - **Enable Authentication**: ❌ Desmarque (para facilitar o uso)
   - **Server Password**: Deixe vazio
   - **Enable Debug Logging**: ✅ Marque para debug
3. Clique em **OK**

### 3. Verificar a Instalação

1. No OBS Studio, vá em **Ferramentas** > **WebSocket Server Settings**
2. Você deve ver uma janela com as configurações
3. Se aparecer "Server is running", o WebSocket está funcionando

### 4. Testar a Conexão

1. Execute o programa OBS Auto Recorder
2. Clique em **"Testar Conexão"** (versão HTTP) ou **"Conectar ao OBS"** (versão WebSocket)
3. Se aparecer "Conexão estabelecida com sucesso", está tudo funcionando!

## Solução de Problemas

### Erro: "WebSocket Server Settings" não aparece
- O plugin não está instalado
- Reinstale o OBS WebSocket
- Reinicie o OBS Studio

### Erro: "Falha na conexão"
- Verifique se o OBS Studio está aberto
- Confirme se o WebSocket está habilitado
- Verifique se a porta 4455 está correta
- Tente reiniciar o OBS Studio

### Erro: "Porta já em uso"
- Altere a porta no WebSocket Server Settings
- Atualize a porta no programa também
- Reinicie o OBS Studio

### Erro: "Authentication failed"
- Desmarque "Enable Authentication" no WebSocket
- Ou configure a senha correta no programa

## Configurações Avançadas

### Usar Autenticação (Opcional)
Se quiser usar senha:
1. No WebSocket Server Settings, marque "Enable Authentication"
2. Digite uma senha
3. No programa, configure a mesma senha

### Alterar Porta (Opcional)
Se a porta 4455 estiver ocupada:
1. No WebSocket Server Settings, mude para outra porta (ex: 4456)
2. No programa, atualize a porta também

### Logs de Debug
Para ver logs detalhados:
1. Marque "Enable Debug Logging" no WebSocket
2. Os logs aparecerão no console do OBS Studio

## Compatibilidade

- **OBS Studio**: Versão 27.0 ou superior
- **OBS WebSocket**: Versão 5.0 ou superior
- **Sistema**: Windows 10/11, macOS, Linux

## Links Úteis

- [OBS WebSocket GitHub](https://github.com/obsproject/obs-websocket)
- [OBS Studio Download](https://obsproject.com/)
- [Documentação WebSocket](https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md) 