# AutomateTest 🚀

AutomateTest é uma aplicação web desenvolvida em Flask para gerenciar e automatizar a execução de múltiplos ambientes de teste. A ferramenta permite criar cópias de um sistema base, aplicar configurações específicas como chaves de licença e builds de depuração, e executá-los de forma isolada e organizada.

## 🎯 Objetivo

O principal objetivo do AutomateTest é otimizar o fluxo de trabalho de desenvolvedores e QAs que precisam testar uma aplicação com diferentes configurações. Em vez de duplicar e configurar pastas manualmente, o AutomateTest oferece uma interface centralizada para:

* Criar novos ambientes de teste a partir de um modelo (Sistema Base).
* Gerenciar e associar diferentes chaves de licença a cada ambiente.
* Aplicar diferentes versões ou builds de depuração.
* Lançar a aplicação para teste com a configuração desejada com apenas um clique.

## ✨ Funcionalidades Principais

* **Interface Web Intuitiva**: Gerencie todos os seus ambientes de teste através de uma interface simples e amigável.
* **Criação de Sistemas**: Clone um "Sistema Base" pré-configurado para criar novos ambientes de teste rapidamente.
* **Gerenciamento de Chaves**: Adicione um repositório de chaves e associe uma chave específica a cada sistema de teste.
* **Gerenciamento de Debugs**: Associe diferentes builds ou versões de depuração a cada sistema.
* **Configuração Centralizada**: Configure todos os caminhos e arquivos necessários em uma única página de configuração.
* **Execução com Um Clique**: Inicie qualquer sistema configurado diretamente pela interface.

## 🛠️ Como Funciona

A aplicação opera com base em alguns conceitos-chave:

1.  **Sistema Base**: Uma pasta contendo a versão estável ou principal da sua aplicação. Este é o modelo que será copiado para criar novos sistemas de teste.
2.  **Sistemas**: Cópias do Sistema Base, localizadas em uma pasta designada. Cada sistema pode ter sua própria configuração.
3.  **Chaves**: Arquivos de licença (ou qualquer arquivo de chave) que podem ser associados a um sistema. A aplicação compara as chaves usando hash para evitar duplicatas.
4.  **Debugs**: Pastas contendo arquivos específicos de uma versão ou build de depuração que podem ser aplicadas a um sistema.

A lógica de backend, escrita em Python com Flask, manipula as operações de arquivos como copiar, mover e renomear para configurar os ambientes de teste conforme solicitado pelo usuário na interface. Os dados de configuração são salvos localmente em um arquivo `automation.json`.

## 🔧 Instalação e Execução

Para executar este projeto localmente, siga os passos abaixo.

**Pré-requisitos:**

* Python 3.x
* Pip

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/AutomateTest.git](https://github.com/seu-usuario/AutomateTest.git)
    cd AutomateTest
    ```

2.  **Instale as dependências:**
    Ainda que não haja um `requirements.txt` no projeto, a única dependência principal é o Flask.
    ```bash
    pip install Flask
    ```

3.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

4.  Acesse a aplicação no seu navegador em `http://127.0.0.1:5000`.

## ⚙️ Configuração Inicial

Ao acessar a aplicação pela primeira vez, você será redirecionado para a página de configurações (`/configure`) caso o arquivo de configuração não exista.

1.  Clique no botão **Configurations** na página inicial.
2.  Preencha os seguintes campos:
    * **Base System Folder**: A pasta do seu sistema principal.
    * **Folder of Keys**: A pasta onde você armazenará os arquivos de chave.
    * **Folder of Versions**: A pasta onde você armazenará as diferentes builds de depuração.
    * **Locate Folder of Systems**: A pasta onde o AutomateTest criará os sistemas de teste.
    * **Name Key**: O nome que o arquivo de chave receberá ao ser copiado para um sistema (ex: `license.key`).
    * **File of Execute**: O nome do arquivo executável do seu sistema (ex: `start.exe`).
3.  Clique em **Submit** para salvar.

## 🚀 Como Usar

* **Adicionar Chaves e Debugs**: Na página inicial, use os botões "Add Key" e "Add Debug" para popular seus repositórios.
* **Criar um Novo Sistema**: Clique em "New System", dê um nome e salve. Uma cópia do Sistema Base será criada.
* **Editar um Sistema**: Clique em "Edit" ao lado de um sistema para alterar seu nome, associar uma chave ou aplicar uma versão de debug.
* **Executar**: Clique em "Execute" para iniciar o sistema com as configurações aplicadas.

## 💻 Tecnologias Utilizadas

* **Backend**: Python, Flask
* **Frontend**: HTML, CSS, JavaScript
* **Utilitários**: O projeto utiliza a biblioteca `tkinter` para diálogos de seleção de arquivos e `hashlib` para a verificação de chaves.
