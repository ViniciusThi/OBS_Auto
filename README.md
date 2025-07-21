# OBS Auto Recorder

Um programa em Python para automatizar o controle de gravação do OBS Studio com interface gráfica.

## Funcionalidades

- ✅ Interface gráfica intuitiva
- ✅ Agendamento de horários de início e parada de gravação
- ✅ Teste de conexão com OBS Studio
- ✅ Log de atividades em tempo real
- ✅ Salvamento automático de configurações
- ✅ Execução em segundo plano
- ✅ Agendamento diário automático

## Pré-requisitos

1. **Python 3.7 ou superior**
2. **OBS Studio** instalado e configurado
3. **OBS WebSocket** plugin instalado no OBS Studio

## Instalação

### 1. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 2. Configurar OBS WebSocket

1. Abra o OBS Studio
2. Vá em **Ferramentas** > **WebSocket Server Settings**
3. Configure:
   - **Server Port**: 4455 (padrão)
   - **Enable Authentication**: Desmarque (ou configure senha se desejar)
   - **Enable Debug Logging**: Marque para debug
4. Clique em **OK**

## Como usar

### 1. Executar o programa

```bash
python obs_auto_recorder.py
```

### 2. Configurar conexão

1. Na seção "Configurações do OBS":
   - **Host**: localhost (padrão)
   - **Porta**: 4455 (padrão)
   - **Senha**: deixe vazio se não configurou autenticação

2. Clique em **"Testar Conexão"** para verificar se está funcionando

### 3. Configurar horários

1. Na seção "Horários de Gravação":
   - **Iniciar gravação às**: Defina a hora de início (ex: 09:00)
   - **Parar gravação às**: Defina a hora de parada (ex: 18:00)

### 4. Iniciar agendamento

1. Clique em **"Iniciar Agendamento"**
2. O programa irá:
   - Agendar a gravação para o horário especificado
   - Se o horário já passou hoje, agendará para amanhã
   - Executar automaticamente todos os dias

### 5. Monitorar status

- **Status**: Mostra o estado atual do programa
- **Log**: Exibe todas as atividades e mensagens
- **Horário atual**: Atualizado em tempo real

## Funcionalidades Avançadas

### Agendamento Inteligente

- Se você definir início às 23:00 e parada às 06:00, o programa entenderá que a parada é no dia seguinte
- O agendamento se repete automaticamente todos os dias
- Se o horário de início já passou, agendará para o próximo dia

### Log de Atividades

- Todas as ações são registradas com timestamp
- Mensagens de sucesso (✓) e erro (✗) são claramente identificadas
- O log é salvo em tempo real e pode ser consultado a qualquer momento

### Configurações Persistentes

- As configurações de conexão são salvas automaticamente
- Na próxima execução, os valores serão carregados automaticamente

## Solução de Problemas

### Erro de Conexão

1. Verifique se o OBS Studio está aberto
2. Confirme se o WebSocket está habilitado
3. Verifique se a porta está correta (4455)
4. Teste a conexão usando o botão "Testar Conexão"

### Gravação não inicia/para

1. Verifique se o OBS Studio está em execução
2. Confirme se não há outra gravação em andamento
3. Verifique as configurações de saída do OBS
4. Consulte o log para mensagens de erro específicas

### Problemas de Horário

1. Verifique se o relógio do sistema está correto
2. Confirme se os horários estão no formato correto (HH:MM)
3. O programa usa o fuso horário local do sistema

## Estrutura de Arquivos

```
OBSauto/
├── obs_auto_recorder.py    # Programa principal
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
└── obs_config.json        # Configurações salvas (criado automaticamente)
```

## Tecnologias Utilizadas

- **Python 3.7+**: Linguagem principal
- **Tkinter**: Interface gráfica
- **Requests**: Comunicação HTTP com OBS WebSocket
- **Threading**: Execução em segundo plano
- **JSON**: Armazenamento de configurações

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades!

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT. 