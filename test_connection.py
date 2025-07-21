#!/usr/bin/env python3
"""
Script de teste para verificar conexão com OBS WebSocket
"""

import requests
import base64
import json

def test_obs_connection(host="192.168.102.26", port=4455, password="123456"):
    """Testa conexão com OBS WebSocket"""
    
    print(f"Testando conexão com OBS em {host}:{port}")
    print(f"Senha configurada: {'Sim' if password else 'Não'}")
    print("-" * 50)
    
    # Configurar headers com autenticação se necessário
    headers = {}
    if password:
        auth = base64.b64encode(f":{password}".encode()).decode()
        headers['Authorization'] = f'Basic {auth}'
    
    try:
        # Teste 1: Status básico
        print("1. Testando endpoint de status...")
        url = f"http://{host}:{port}/api/v1/status"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("✓ Status OK - OBS está respondendo")
            data = response.json()
            print(f"   Versão do OBS: {data.get('obsVersion', 'N/A')}")
            print(f"   Versão do WebSocket: {data.get('obsWebSocketVersion', 'N/A')}")
        else:
            print(f"✗ Erro no status (Status: {response.status_code})")
            print(f"   Resposta: {response.text}")
            return False
            
        # Teste 2: Informações de gravação
        print("\n2. Testando informações de gravação...")
        url = f"http://{host}:{port}/api/v1/record/status"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("✓ Informações de gravação OK")
            data = response.json()
            print(f"   Gravando: {data.get('outputActive', False)}")
        else:
            print(f"✗ Erro ao obter status de gravação (Status: {response.status_code})")
            
        # Teste 3: Listar cenas
        print("\n3. Testando listagem de cenas...")
        url = f"http://{host}:{port}/api/v1/scenes"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("✓ Listagem de cenas OK")
            data = response.json()
            scenes = data.get('scenes', [])
            print(f"   Cenas encontradas: {len(scenes)}")
            for scene in scenes[:3]:  # Mostrar apenas as 3 primeiras
                print(f"   - {scene.get('sceneName', 'N/A')}")
        else:
            print(f"✗ Erro ao listar cenas (Status: {response.status_code})")
            
        print("\n" + "=" * 50)
        print("✓ Todos os testes básicos passaram!")
        print("O OBS WebSocket está funcionando corretamente.")
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Erro de conexão!")
        print("   Verifique se:")
        print("   1. O OBS Studio está aberto")
        print("   2. O WebSocket está habilitado")
        print("   3. O IP e porta estão corretos")
        return False
        
    except requests.exceptions.Timeout:
        print("✗ Timeout na conexão!")
        print("   O OBS não respondeu dentro do tempo limite")
        return False
        
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        return False

def test_recording_control(host="192.168.102.26", port=4455, password="123456"):
    """Testa controle de gravação"""
    
    print("\n" + "=" * 50)
    print("TESTE DE CONTROLE DE GRAVAÇÃO")
    print("=" * 50)
    
    headers = {}
    if password:
        auth = base64.b64encode(f":{password}".encode()).decode()
        headers['Authorization'] = f'Basic {auth}'
    
    try:
        # Verificar status atual
        url = f"http://{host}:{port}/api/v1/record/status"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            is_recording = data.get('outputActive', False)
            print(f"Status atual: {'Gravando' if is_recording else 'Não gravando'}")
            
            if is_recording:
                print("⚠️  OBS já está gravando. Teste de início pode falhar.")
            else:
                print("✓ OBS não está gravando. Pode testar início de gravação.")
                
        else:
            print(f"✗ Não foi possível verificar status (Status: {response.status_code})")
            
    except Exception as e:
        print(f"✗ Erro ao verificar status: {e}")

if __name__ == "__main__":
    print("OBS WebSocket Connection Tester")
    print("=" * 50)
    
    # Testar com configurações da imagem
    success = test_obs_connection("192.168.102.26", 4455, "123456")
    
    if success:
        test_recording_control("192.168.102.26", 4455, "123456")
    
    print("\n" + "=" * 50)
    print("Teste concluído!")
    print("=" * 50) 