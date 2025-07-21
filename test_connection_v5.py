#!/usr/bin/env python3
"""
Script de teste para verificar conexão com OBS WebSocket v5
"""

import requests
import base64
import json

def test_obs_connection_v5(host="192.168.102.26", port=4455, password="123456"):
    """Testa conexão com OBS WebSocket v5"""
    
    print(f"Testando conexão com OBS WebSocket v5 em {host}:{port}")
    print(f"Senha configurada: {'Sim' if password else 'Não'}")
    print("-" * 50)
    
    # Configurar headers com autenticação se necessário
    headers = {
        'Content-Type': 'application/json'
    }
    
    if password:
        auth = base64.b64encode(f":{password}".encode()).decode()
        headers['Authorization'] = f'Basic {auth}'
    
    try:
        # Teste 1: Status básico (sem versão específica)
        print("1. Testando endpoint de status...")
        url = f"http://{host}:{port}/api/status"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("✓ Status OK - OBS está respondendo")
            try:
                data = response.json()
                print(f"   Resposta: {data}")
            except:
                print(f"   Resposta: {response.text}")
        else:
            print(f"✗ Erro no status (Status: {response.status_code})")
            print(f"   Resposta: {response.text}")
            
        # Teste 2: Tentar diferentes endpoints
        print("\n2. Testando diferentes endpoints...")
        
        endpoints = [
            "/api/status",
            "/api/v1/status", 
            "/api/v2/status",
            "/api/obs/status",
            "/status",
            "/"
        ]
        
        for endpoint in endpoints:
            url = f"http://{host}:{port}{endpoint}"
            try:
                response = requests.get(url, headers=headers, timeout=3)
                print(f"   {endpoint}: {response.status_code}")
                if response.status_code == 200:
                    print(f"   ✓ {endpoint} funcionou!")
                    break
            except:
                print(f"   {endpoint}: Erro de conexão")
                
        # Teste 3: Tentar POST para verificar se é WebSocket
        print("\n3. Testando se é WebSocket...")
        try:
            import websocket
            ws_url = f"ws://{host}:{port}"
            print(f"   Tentando conectar via WebSocket: {ws_url}")
            
            # Teste simples de WebSocket
            ws = websocket.create_connection(ws_url, timeout=5)
            print("   ✓ WebSocket conectado!")
            ws.close()
            
        except ImportError:
            print("   ✗ websocket-client não instalado")
        except Exception as e:
            print(f"   ✗ Erro WebSocket: {e}")
            
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

def test_simple_http(host="192.168.102.26", port=4455):
    """Teste simples de HTTP"""
    print(f"\nTeste simples HTTP em {host}:{port}")
    print("-" * 30)
    
    try:
        url = f"http://{host}:{port}/"
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Conteúdo: {response.text[:200]}...")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    print("OBS WebSocket v5 Connection Tester")
    print("=" * 50)
    
    # Testar com configurações da imagem
    test_obs_connection_v5("192.168.102.26", 4455, "123456")
    
    # Teste simples HTTP
    test_simple_http("192.168.102.26", 4455)
    
    print("\n" + "=" * 50)
    print("Teste concluído!")
    print("=" * 50) 