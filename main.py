from app import app
import webbrowser
import threading
import socket

def find_available_port(start_port, max_attempts=10):
    """
    Tenta encontrar uma porta TCP disponível a partir de uma porta inicial.
    """
    for i in range(max_attempts):
        port = start_port + i
        try:
            # Tenta criar um socket e vinculá-lo à porta para verificar se está livre
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port # Retorna a porta se ela estiver livre
        except OSError:
            print(f"Porta {port} ocupada, tentando a próxima...")
    raise Exception(f"Não foi possível encontrar uma porta disponível após {max_attempts} tentativas a partir de {start_port}.")


if __name__ == '__main__':
    # Porta inicial que você deseja tentar
    initial_port = 5286

    # Encontra a primeira porta disponível a partir da inicial
    # Se initial_port estiver livre, ela será usada. Senão, tentará 5287, 5288, etc.
    try:
        actual_port = find_available_port(initial_port)
    except Exception as e:
        print(f"Erro crítico: {e}")
        exit() # Sai do programa se não encontrar uma porta

    # Constrói a URL usando a porta REAL encontrada
    url = f"http://127.0.0.1:{actual_port}"

    print(f"Iniciando o servidor Flask em: {url}")

    # Abre o navegador após um pequeno atraso para o servidor iniciar
    # Atraso um pouco maior aqui, pois a busca por porta pode consumir um tempo.
    threading.Timer(1, lambda: webbrowser.open(url)).start()

    # Inicia a aplicação Flask usando a porta REAL encontrada
    app.run(host='0.0.0.0', port=actual_port)