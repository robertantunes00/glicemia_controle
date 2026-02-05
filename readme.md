# 📊 Sistema de Registro de Glicemia (Flask + MySQL)

Este projeto é uma aplicação web simples desenvolvida em **Flask** para registrar, atualizar e exibir medições de **glicemia diária**, utilizando **MySQL** como banco de dados.

O sistema foi pensado para permitir múltiplos registros ao longo do dia (jejum, pós-refeição, antes de dormir, etc.), mantendo **apenas uma linha por dia**, com atualização incremental dos valores.

---

## 🧩 Funcionalidades

* Registro de glicemia por **período do dia**
* Atualização automática do registro do dia (UPSERT lógico)
* Exibição do **último valor registrado**
* Validação de formulário com **Flask-WTF**
* Persistência de dados em **MySQL**

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Flask**
* **Flask-WTF**
* **MySQL**
* **mysql-connector-python**
* **HTML + Jinja2**

---

## 📂 Estrutura do Projeto

```text
project/
│
├── app.py                # Aplicação Flask principal
├── forms.py              # Definição do formulário de glicemia
├── templates/
│   └── index.html        # Interface principal
├── static/               # Arquivos estáticos (CSS, JS, ícones)
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação
```

---

## 🗄️ Estrutura do Banco de Dados

Tabela: `glicemia`

```sql
CREATE TABLE glicemia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL UNIQUE,
    jejum INT,
    `2_horas_apos_cafe` INT,
    antes_do_almoco INT,
    `2_horas_apos_almoco` INT,
    antes_do_jantar INT,
    `2_horas_apos_jantar` INT,
    antes_de_dormir INT,
    `3_horas` INT
);
```

> 🔑 A coluna `data` é única para garantir apenas **um registro por dia**.

---

## ▶️ Como Executar o Projeto

### 1️⃣ Clone o repositório

```bash
git clone <url-do-repositorio>
cd project
```

### 2️⃣ Crie um ambiente virtual (opcional, recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as variáveis de ambiente

```bash
export SECRET_KEY="sua_secret_key"
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="sua_senha"
export DB_NAME="medicaldata"
```

(No Windows, use `set` em vez de `export`.)

---

### 5️⃣ Execute a aplicação

```bash
python app.py
```

A aplicação ficará disponível em:

```
http://localhost:5000
```

---

## 👨‍💻 Autor

Projeto desenvolvido para fins educacionais e controle pessoal de saúde.

---

## 📄 Licença

Este projeto é de uso livre para fins educacionais e pessoais.
