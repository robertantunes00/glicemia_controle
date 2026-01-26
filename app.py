from flask import Flask, render_template, redirect, url_for, flash
from forms import GlicemiaForm
import mysql.connector
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Configurações MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '192401',
    'database': 'dados2'
}

# Inicializa tabela caso não exista
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS glicemia (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data DATE UNIQUE,
        jejum INT,
        `2_horas_apos_cafe` INT,
        antes_do_almoco INT,
        `2_horas_apos_almoco` INT,
        antes_do_jantar INT,
        `2_horas_apos_jantar` INT,
        antes_de_dormir INT,
        `3_horas` INT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    form = GlicemiaForm()
    ultima_medicao = None

    # Busca última medição
    conn = mysql.connector.connect(**DB_CONFIG)
    c = conn.cursor()
    c.execute("SELECT * FROM glicemia ORDER BY data DESC LIMIT 1")
    ultima_medicao = c.fetchone()
    conn.close()

    if form.validate_on_submit():
        data = date.today().strftime("%Y-%m-%d")  # ignora horário
        periodo = form.periodo.data
        valor = form.valor.data

        conn = mysql.connector.connect(**DB_CONFIG)
        c = conn.cursor()
        c.execute("SELECT id FROM glicemia WHERE data = %s", (data,))
        registro = c.fetchone()

        if registro:
            # Atualiza coluna do período
            c.execute(f"UPDATE glicemia SET `{periodo}` = %s WHERE data = %s", (valor, data))
        else:
            # Insere novo registro
            c.execute(f"INSERT INTO glicemia (data, `{periodo}`) VALUES (%s, %s)", (data, valor))

        conn.commit()
        conn.close()
        flash("Medição registrada com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("index.html", form=form, ultima=ultima_medicao)
