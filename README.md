# MEI FINANCE

## Sobre o Projeto

O MEI FINANCE é uma aplicação web desenvolvida com Streamlit para auxiliar na organização financeira de pequenos negócios e profissionais autônomos. O sistema permite o controle de clientes, geração de relatórios de faturamento e lucro, além do gerenciamento de entradas, saídas e gastos fixos.

A aplicação é totalmente containerizada utilizando Docker e Docker Compose, facilitando a implantação e o ambiente de desenvolvimento.

## Funcionalidades
- Dashboard com métricas e gráficos financeiros
- Cadastro, edição e exclusão de clientes
- Geração de relatórios mensais, anuais e por cliente
- Controle de entradas, saídas e despesas fixas
- Interface web responsiva e intuitiva

## Estrutura do Projeto
```
ss-contab-docker/
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── streamlit_app.py
│   ├── pages/
│   │   ├── home.py
│   │   ├── dashboard.py
│   │   ├── relatorio.py
│   │   ├── financeiro.py
│   │   └── clientes.py
│   └── .streamlit/
│       └── config.toml
├── docker-compose.yml
└── README.md
```

## Como Executar

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/ss-contab-docker.git
   cd ss-contab-docker
   ```

2. Construa e inicie os containers:
   ```sh
   docker compose up --build
   ```

3. Acesse a aplicação no navegador:
   - http://localhost:8501

## Requisitos
- Docker
- Docker Compose

## Personalização de Tema
O tema da aplicação pode ser ajustado no arquivo `app/.streamlit/config.toml`.

## Licença
Este projeto está licenciado sob os termos da licença MIT.
