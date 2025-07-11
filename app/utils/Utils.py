from concurrent.futures import ThreadPoolExecutor
import os, json, hashlib, shutil
from pathlib import Path
from tkinter import Tk, filedialog


class FileFolder:
    @staticmethod
    def getPathFolder():
        root = Tk()
        root.withdraw()  # Oculta a janela principal
        root.attributes('-topmost', True)  # Garante que apareça na frente
        caminho = filedialog.askdirectory(initialdir=str(Path.home() / "Downloads"))
        root.destroy()
        return caminho

    @staticmethod
    def getPathFile():
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        caminho = filedialog.askopenfilename(initialdir=str(Path.home() / "Downloads"))
        root.destroy()
        return caminho
    
class Persistence:
    def __init__(self):
        pass
    
    @staticmethod
    def validate():
        p = Persistence()

        if p.BaseSystem == "" or p.FolderKeys == "" or p.NameKey == "" or p.FileExecute == "" or p.FolderDebugs == "" or p.LocateFolderSystems == "":
            return False
        
        return True
    
    def __genericSave(self, dado, name):
        file = Persistence.__load()
        file[name] = dado
        Persistence.__save(file)
    
    def __genericLoad(self, name):
        file = Persistence.__load()
        # Usar .get() é mais seguro, pois retorna None se a chave não existir
        return file.get(name)

    @property
    def InternalDebug(self):
        return self.__genericLoad("internalDebug")
    
    @InternalDebug.setter
    def InternalDebug(self, valor):
        self.__genericSave(valor, "internalDebug")

    @property
    def LocateFolderSystems(self):
        return self.__genericLoad("locateFolderSystems")
    
    @LocateFolderSystems.setter
    def LocateFolderSystems(self, valor):
        self.__genericSave(valor, "locateFolderSystems")

    @property
    def FolderDebugs(self):
        return self.__genericLoad("folderDebugs")

    @FolderDebugs.setter
    def FolderDebugs(self, valor):
        self.__genericSave(valor, "folderDebugs")
    
    @property
    def BaseSystem(self):
        return self.__genericLoad("baseSystem")

    @BaseSystem.setter
    def BaseSystem(self, valor):
        self.__genericSave(valor, "baseSystem")
    
    @property
    def FolderKeys(self):
        return self.__genericLoad("folderKeys")

    @FolderKeys.setter
    def FolderKeys(self, valor):
        self.__genericSave(valor, "folderKeys")
    
    @property
    def NameKey(self):
        return self.__genericLoad("nameKey")

    @NameKey.setter
    def NameKey(self, valor):
        self.__genericSave(valor, "nameKey")
    
    @property
    def FileExecute(self):
        return self.__genericLoad("fileExecute")

    @FileExecute.setter
    def FileExecute(self, valor):
        self.__genericSave(valor, "fileExecute")
    
    @staticmethod
    def __save(dado):
        file_path = Persistence.__config()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dado, f, indent=4, ensure_ascii=False)
    
    @staticmethod
    def __load():
        file_path = Persistence.__config()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existe ou está corrompido, retorna a estrutura padrão
            return {"baseSystem": "", "folderKeys": "", "nameKey": "", "fileExecute": "", "folderDebugs": "", "locateFolderSystems": "", "internalDebug": "Debug"}
    
    @staticmethod  
    def __config():
        file_name = "automation.json"
        repository_path = Persistence.__repositoryComputer()
        full_path = os.path.join(repository_path, file_name)
        
        if not os.path.exists(full_path):
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump({"baseSystem": "", "folderKeys": "", "nameKey": "", "fileExecute": "", "folderDebugs": "", "locateFolderSystems": "", "internalDebug": "Debug"}, f, indent=4)

        return full_path
    
    @staticmethod
    def __repositoryComputer():
        try: 
            if os.name == 'nt':  # Windows
                repository = os.path.join(os.getenv('APPDATA'), 'automatetest')
                print("Windows")
            else:  # Unix (Linux, macOS)
                repository = os.path.join(os.path.expanduser('~'), '.config', 'automatetest')
            
            if not os.path.exists(repository): 
                os.makedirs(repository)
            return repository
        except Exception as e:
            print(f"ERRO CRÍTICO: Não foi possível criar o diretório de configuração. {e}")
            raise

class Hash:
    @staticmethod
    def calculateHashFile(caminho_arquivo) -> str:
        if not os.path.exists(caminho_arquivo):
            raise Exception(f"O arquivo '{caminho_arquivo}' nao existe.")
        
        if not isinstance(caminho_arquivo, str):
            raise Exception("O argumento 'caminho_arquivo' deve ser uma string.")
        
        if os.path.isdir(caminho_arquivo):
            raise Exception("O argumento 'caminho_arquivo' deve ser um caminho para um arquivo.")
        
        with open(caminho_arquivo, 'rb') as f:
            conteudo = f.read()
        header = f"blob {len(conteudo)}\0".encode('utf-8')
        dados = header + conteudo
        return hashlib.sha1(dados).hexdigest()
    
    @staticmethod
    def print_json(dado):
        print(json.dumps(dado, indent=4, ensure_ascii=False))

class Command:
    @staticmethod
    def copy(pasta_origem, pasta_destino):
        print(f"Iniciando cópia recursiva de '{pasta_origem}' para '{pasta_destino}'...")
        
        if not os.path.exists(pasta_origem):
            raise Exception(f"O diretório de origem '{pasta_origem}' nao existe.")
        
        if not os.path.exists(pasta_destino):
            raise Exception(f"O diretório de destino '{pasta_destino}' nao existe.")
        
        if not os.path.isdir(pasta_origem):
            raise Exception(f"O argumento 'pasta_origem' deve ser um diretório.")
        
        if not os.path.isdir(pasta_destino):
            raise Exception(f"O argumento 'pasta_destino' deve ser um diretório.")

        os.makedirs(pasta_destino, exist_ok=True)

        for item in os.listdir(pasta_origem):
            caminho_origem_item = os.path.join(pasta_origem, item)
            caminho_destino_item = os.path.join(pasta_destino, item)

            if os.path.isdir(caminho_origem_item):
                print(f"  Copiando diretório: '{item}'")
                try:
                    shutil.copytree(caminho_origem_item, caminho_destino_item, dirs_exist_ok=True)
                except TypeError:
                    print(f"  Aviso: Sua versão do Python não suporta 'dirs_exist_ok'. Removendo '{item}' no destino antes de copiar.")
                    if os.path.exists(caminho_destino_item):
                        shutil.rmtree(caminho_destino_item)
                    shutil.copytree(caminho_origem_item, caminho_destino_item)
                except Exception as e:
                    print(f"  Erro ao copiar diretório '{item}': {e}")
            elif os.path.isfile(caminho_origem_item):
                try:
                    shutil.copy2(caminho_origem_item, caminho_destino_item)
                    print(f"  Copiado arquivo: '{item}'")
                except Exception as e:
                    print(f"  Erro ao copiar arquivo '{item}': {e}")
            else:
                print(f"  Ignorando item desconhecido (nem arquivo, nem diretório): '{item}'")

        print("Cópia recursiva concluída.")

    @staticmethod
    def move(pasta_origem, pasta_destino):
        print(f"Iniciando MOVER conteúdo de '{pasta_origem}' para '{pasta_destino}'...")
        
        if not os.path.exists(pasta_origem):
            raise Exception(f"O diretório de origem '{pasta_origem}' nao existe.")
        
        if not os.path.exists(pasta_destino):
            raise Exception(f"O diretório de destino '{pasta_destino}' nao existe.")
        
        if not os.path.isdir(pasta_origem):
            raise Exception(f"O argumento 'pasta_origem' deve ser um diretório.")
        
        if not os.path.isdir(pasta_destino):
            raise Exception(f"O argumento 'pasta_destino' deve ser um diretório.")

        if not os.path.isdir(pasta_origem):
            print(f"Erro: A pasta de destino '{pasta_origem}' não existe ou não é um diretório.")
            return

        os.makedirs(pasta_destino, exist_ok=True)

        for item in os.listdir(pasta_origem):
            caminho_origem_item = os.path.join(pasta_origem, item)
            caminho_destino_item = os.path.join(pasta_destino, item)

            try:
                if os.path.isdir(caminho_origem_item):
                    if os.path.exists(caminho_destino_item):
                        shutil.rmtree(caminho_destino_item) # Remove recursivamente o destino
                    shutil.move(caminho_origem_item, pasta_destino) # Move a subpasta para o destino
                    print(f"  Movido diretório e conteúdo: '{item}'")
                elif os.path.isfile(caminho_origem_item):
                    shutil.move(caminho_origem_item, pasta_destino) # Move o arquivo para o destino
                    print(f"  Movido arquivo: '{item}'")

            except shutil.Error as e:
                print(f"  Erro ao mover '{item}': {e}. Tentando sobrescrever/mesclar manualmente.")
                if os.path.isdir(caminho_origem_item):
                    pass # A lógica acima já tenta remover antes de mover.
                elif os.path.isfile(caminho_origem_item):
                    shutil.copy2(caminho_origem_item, caminho_destino_item)
                    os.remove(caminho_origem_item)
                    print(f"  Copiado e removido '{item}' manualmente.")
            except Exception as e:
                print(f"  Erro inesperado ao mover '{item}': {e}")

        try:
            shutil.rmtree(pasta_origem)
            print(f"\nPasta de origem '{pasta_origem}' apagada com sucesso.")
        except Exception as e:
            print(f"Erro ao apagar pasta de origem '{pasta_origem}': {e}")

        print("Operação de MOVER e APAGAR ORIGEM concluída.")
        return True
    
    @staticmethod
    def remove(pasta):
        if not os.path.exists(pasta):
            raise Exception(f"O diretório '{pasta}' nao existe.")
        shutil.rmtree(pasta)

    @staticmethod
    def removeFile(file):
        if not os.path.exists(file):
            raise Exception(f"O arquivo '{file}' nao existe.")
        
        if not os.path.isfile(file):
            raise Exception(f"O argumento 'file' deve ser um caminho para um arquivo.")
        
        os.remove(file)
    
    @staticmethod
    def copyFile(arquivo_origem, pasta_destino):
        """
        Copia um único arquivo para uma pasta de destino.
        Se o destino for um caminho de arquivo completo, ele o substituirá.
        """
        try:
            shutil.copy2(arquivo_origem, pasta_destino)
            print(f"Arquivo '{os.path.basename(arquivo_origem)}' copiado para '{pasta_destino}' com sucesso.")
            return True
        except Exception as e:
            raise Exception(f"Erro ao copiar o arquivo: {e}")

    @staticmethod
    def descompact(caminho_arquivo, caminho_destino):
        if not os.path.exists(caminho_destino):
            raise Exception(f"O diretório de destino '{caminho_destino}' não existe.")
        
        if not os.path.exists(caminho_arquivo):
            raise Exception(f"O arquivo '{caminho_destino}' não existe.")
        
        print(Command.validate_compact(caminho_arquivo))
        
        if not Command.validate_compact(caminho_arquivo):
            raise Exception(f"O arquivo '{caminho_arquivo}' não é um arquivo compactado.")
        
        
        shutil.unpack_archive(caminho_arquivo, caminho_destino)

    @staticmethod
    def mkdir(pasta):
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            
        return True
    
    @staticmethod     
    def listdir(pasta):
        return os.listdir(pasta)
    
    @staticmethod
    def validate_compact(caminho_do_arquivo):
        ASSINATURAS_COMPACTADAS = {
            "ZIP": b'PK\x03\x04',
            "RAR": b'Rar!\x1a\x07\x00',
            "7z": b"7z\xbc\xaf'\x1c",
            "GZIP": b'\x1f\x8b',
            "BZIP2": b'BZ'
        }

        try:
            if os.path.isdir(caminho_do_arquivo):
                raise Exception("O caminho que passou deve ser um arquivo compactado!")
            
            with open(caminho_do_arquivo, 'rb') as f:
                # Lê o número de bytes da assinatura mais longa para garantir a comparação
                max_len = max(len(s) for s in ASSINATURAS_COMPACTADAS.values())
                bytes_iniciais = f.read(max_len)
                
                for formato, assinatura in ASSINATURAS_COMPACTADAS.items():
                    if bytes_iniciais.startswith(assinatura):
                        print(f"O arquivo '{caminho_do_arquivo}' parece ser um formato '{formato}'.")
                        return formato # É um arquivo compactado
                
                print(f"O arquivo '{caminho_do_arquivo}' não corresponde a nenhum formato compactado conhecido.")
                return None # Não é um formato compactado conhecido
                
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado em '{caminho_do_arquivo}'")
            return None
