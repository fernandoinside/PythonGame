# Network Topology Dashboard

Este aplicativo é um dashboard de topologia de rede que permite escanear e visualizar dispositivos na rede local, exibindo informações detalhadas sobre cada dispositivo encontrado. A interface utiliza D3.js para criar um gráfico de topologia de rede semelhante ao Zenmap.

## Funcionalidades

- **Escaneamento de Rede:** Realiza escaneamentos iniciais para descobrir dispositivos na rede local.
- **Escaneamento Detalhado:** Executa comandos `nmap` detalhados para cada dispositivo encontrado.
- **Visualização de Topologia:** Exibe um gráfico de topologia de rede usando D3.js, com informações detalhadas sobre cada dispositivo.

## Tecnologias Utilizadas

- **Backend:**
  - Python
  - Flask
  - Subprocess (para execução de comandos `nmap`)

- **Frontend:**
  - HTML
  - CSS
  - JavaScript
  - D3.js (para visualização de topologia)
  - Jinja2 (para renderização de templates)

## Instalação

### Pré-requisitos

- Python 3.x
- Nmap

### Passos de Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/network-topology-dashboard.git
    cd network-topology-dashboard
    ```

2. Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv venv
    source venv/bin/activate   # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Execute o aplicativo:
    ```sh
    python app.py
    ```

5. Abra seu navegador e acesse `http://127.0.0.1:5000`.

## Uso

1. **Adicionar Alvo:**
   - Digite o endereço IP ou o intervalo de IP no campo "Target".
   - Selecione a ação desejada (e.g., `detailed_scan`).
   - Clique em "Add Target" para iniciar o escaneamento.

2. **Visualizar Resultados:**
   - Após o escaneamento, os resultados serão exibidos na tabela.
   - Clique no botão "View on Map" para visualizar a topologia da rede.

3. **Topologia de Rede:**
   - O gráfico de topologia exibirá os dispositivos encontrados em um layout circular, com linhas conectando cada dispositivo ao nó central (localhost).
   - Passe o mouse sobre os dispositivos para ver detalhes adicionais, como endereço MAC e portas abertas.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Seu Nome - [seu-email@example.com](mailto:seu-email@example.com)

Link do Projeto: [https://github.com/seu-usuario/network-topology-dashboard](https://github.com/seu-usuario/network-topology-dashboard)
