# OBS Auto Recorder

Um aplicativo para controlar o OBS Studio remotamente via websocket, permitindo iniciar e parar gravações automaticamente ou manualmente.

![OBS Auto Recorder](screenshot.png)

## Funcionalidades

- **Controle remoto do OBS Studio** via websocket
- **Interface gráfica intuitiva** com tema claro de alto contraste
- **Controle manual** para iniciar e parar gravações
- **Timer automático** para agendamento de gravações
- **Monitoramento em tempo real** do status de gravação
- **Configuração simples** de conexão com o OBS

## Requisitos

- OBS Studio (versão 28.0 ou superior recomendada)
- Plugin OBS Websocket instalado (incluído por padrão no OBS Studio 28+)
- Windows 10 ou 11

## Instalação

### Versão Executável

1. Baixe o arquivo `OBS_Auto_Recorder.exe`
2. Baixe o arquivo `obs_config.json` (ou crie um novo conforme instruções abaixo)
3. Coloque ambos os arquivos na mesma pasta
4. Execute o arquivo `OBS_Auto_Recorder.exe`

### Configuração do OBS Studio

1. Abra o OBS Studio
2. Vá para `Ferramentas > WebSocket Server Settings`
3. Marque a opção `Enable WebSocket server`
4. Anote a porta (padrão: 4455)
5. Se desejar, defina uma senha

### Configuração do OBS Auto Recorder

Edite o arquivo `obs_config.json`:

```json
{
  "host": "localhost", 
  "port": 4455, 
  "password": ""
}
```

- `host`: geralmente "localhost" para conexão local ou o endereço IP do computador com OBS
- `port`: porta configurada no OBS Websocket (normalmente 4455)
- `password`: senha do websocket (deixe em branco se não houver senha configurada)

## Como Usar

### Conexão

1. Inicie o OBS Studio
2. Abra o OBS Auto Recorder
3. Na aba "Conexão", clique em "Conectar ao OBS"
4. Verifique o status da conexão

### Gravação Manual

1. Vá para a aba "Gravação"
2. Clique em "Iniciar Gravação" para começar a gravar
3. Clique em "Parar Gravação" para finalizar

### Gravação Automática

1. Na aba "Gravação", configure a hora de início e fim (formato HH:MM)
2. Clique em "Ativar Timer"
3. O programa iniciará e parará a gravação nos horários definidos
4. Você pode acompanhar o tempo restante na interface

## Solução de Problemas

- **Não consegue conectar?**
  - Verifique se o OBS está em execução
  - Confirme se o plugin websocket está ativado
  - Verifique a porta e senha nas configurações

- **Gravação não inicia?**
  - Verifique se você está conectado ao OBS
  - Confirme se o OBS está configurado para gravar (pasta de saída, etc.)
  - Verifique se há espaço em disco suficiente

## Para Desenvolvedores

O projeto foi desenvolvido em Python usando:

- `tkinter` para a interface gráfica
- `obsws-python` para comunicação com o OBS Websocket
- Tema claro e de alto contraste para melhor legibilidade

## Licença

Este projeto está licenciado sob a licença MIT. 