# Projeto de Geração de Relatórios Ad Hoc

Este projeto em Python permite a geração de relatórios ad hoc com base em filtros dinâmicos e múltiplas fontes de dados. A aplicação segue o padrão arquitetural de **Service Layer**, promovendo uma separação clara entre a lógica de negócios, persistência de dados e orquestração de operações.

---

## Estrutura do Projeto

- `repositories/` – Camada de acesso aos dados.
- `services/` – Camada de lógica de negócios.
- `controllers/` – Orquestração das chamadas e coordenação entre camadas.
- `models/` – Definição das entidades (se aplicável).
- `main.py` – Ponto de entrada da aplicação.

---

## Como iniciar o projeto

1. Clone este repositório na sua máquina local utilizando sua ferramenta Git preferida.
2. Abra o projeto em um editor de código (como VSCode ou PyCharm).
3. Crie e ative um ambiente virtual Python na raiz do projeto.
4. Instale as dependências listadas no arquivo `requirements.txt`.
5. Execute o arquivo `main.py` para iniciar a aplicação e gerar relatórios conforme desejado.

---

## Funcionalidades

- Geração de relatórios a partir de múltiplas tabelas.
- Filtros e agregações configuráveis em tempo de execução.
- Estrutura flexível para futuras integrações com bancos relacionais e APIs.

---

## Tecnologias utilizadas

- Python 3.x  
- SQLAlchemy (ou equivalente)  
- Arquitetura em camadas com separação entre repositório, serviço e controle  
- Aplicação orientada à composição de consultas personalizadas
