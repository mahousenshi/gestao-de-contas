# Gestão de Contas Simples

Uma aplicação leve e direta para o controle de finanças domésticas, focada no que realmente importa: saber o que foi agendado, o que foi pago.

## 🌟 O Mantra: Simplicidade e Flexibilidade

Este sistema foi desenhado para quem foge de planilhas complexas ou apps cheios de funções inúteis. O objetivo é cadastrar o mínimo de informações possíveis para ter o máximo de controle.

## ✨ Funcionalidades principais

* **Controle de Ciclo:** Gestão de status (Agendado vs. Pago), valores e observações pertinentes.

* **Automação de Recorrência:** Cadastre suas contas fixas uma única vez. Se o mês atual estiver vazio, o sistema permite importar todas as entradas recorrentes com um clique.

* **Relatórios Adaptáveis:** Visões rápidas por períodos:
    * 📅 **Anual:** Visão macro do ano.
    
    * 📅 **Mensal:** O detalhamento do seu custo de vida atual.
    * 📅 **Diário:** Para conferir vencimentos específicos.
    
* **Leveza Técnica:** Dependência única de Flask, utilizando SQLite como banco de dados para evitar configurações complexas de infraestrutura.

## 🚀 Instalação Rápida

1. **Clone o repositório e acesse a pasta:**

```bash
git clone https://github.com/mahousenshi/gestao-de-contas.git
cd gestao-de-contas
```

2. **Criar um virtual envoiriment:** (Opicional)

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar as dependências:**

```bash
pip install -r requirements.txt
```

4. **Rodar o servidor:**

```Bash
python contas.py
```

Acesse no navegador: http://127.0.0.1:5000

## 🚀 Instalação Produção

Para uma instalação com persistência a cada reinicio se recomenda usar o **gunicorn** como servidor de produção. A seguir um guia para instalação no Linux(Fedora):

1. **Adiconar um usuario** 

Este usario pode ser qualquer um, o ideal que seja um diferente do usario atual.

```Bash
sudo adduser flask_user
```

2. **Instalar o projeto**

Instale o projeto como dado acima e instale o **gunicorn**

```bash
pip install flask gunicorn
```

3. **Criar o daemon**

```Bash
sudo nano /etc/systemd/system/gestao-de-contas.service
```

Copiar no editor

```Ini
[Unit]
Description=Serviço Flask/Gunicorn para o Gestor de Contas
After=network.target

[Service]
User=flask_user
Group=flask_user

WorkingDirectory=/home/flask_user/gestao-de-contas
ExecStart=/home/flask_user/gestao-de-contas/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 contas:app

Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Iniciar o serviço**

```Bash
sudo systemctl daemon-reload
sudo systemctl enable gestao-de-contas.service
sudo systemctl start gestao-de-contas.service
sudo systemctl status gestao-de-contas.service
```

Acesse no navegador: http://127.0.0.1:5000

## 🛠️ Tecnologias Utilizadas

- Linguagem: Python

- Framework Web: Flask

- Banco de Dados: SQLite (Arquivo local)

## ⚠️ Aviso de Segurança e Privacidade

Este projeto foi desenvolvido para uso pessoal e local.

⚠️ Importante ⚠️: O sistema não possui camadas nativas de autenticação ou criptografia de dados. Tenha cautela ao inserir informações extremamente sensíveis e evite hospedar a aplicação em ambientes públicos ou servidores abertos sem implementar as devidas proteções.
