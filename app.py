from flask import Flask, render_template, redirect, url_for, flash
from forms import GlicemiaForm
import mysql.connector
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '192401',
    'database': 'medicaldata'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/", methods=["GET", "POST"])
def index():
    form = GlicemiaForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if form.validate_on_submit():
        hoje = date.today().strftime("%Y-%m-%d")
        periodo = form.periodo.data
        valor = form.valor.data

        # Lógica de Upsert: Se já existe registro hoje, atualiza. Se não, insere.
        cursor.execute("SELECT id FROM glicemia WHERE data = %s", (hoje,))
        if cursor.fetchone():
            cursor.execute(f"UPDATE glicemia SET `{periodo}` = %s WHERE data = %s", (valor, hoje))
        else:
            cursor.execute(f"INSERT INTO glicemia (data, `{periodo}`) VALUES (%s, %s)", (hoje, valor))
        
        conn.commit()
        flash("Registrado com sucesso!", "success")
        conn.close()
        return redirect(url_for("index"))

    # Busca a última linha inserida para mostrar o valor mais recente
    cursor.execute("SELECT * FROM glicemia ORDER BY data DESC LIMIT 1")
    ultima_linha = cursor.fetchone()
    
    # Extrai o último valor não nulo da linha encontrada
    valor_exibicao = "xxxx"
    if ultima_linha:
        # Colunas em ordem inversa de preferência para mostrar a "última" do dia
        colunas = ['3_horas', 'antes_de_dormir', '2_horas_apos_jantar', 'antes_do_jantar', 
                   '2_horas_apos_almoco', 'antes_do_almoco', '2_horas_apos_cafe', 'jejum']
        for col in colunas:
            if ultima_linha.get(col):
                valor_exibicao = ultima_linha[col]
                break

    conn.close()
    return render_template("index.html", form=form, valor_exibicao=valor_exibicao)

if __name__ == "__main__":
    # host='0.0.0.0' faz o Flask aceitar conexões de qualquer aparelho na rede
    app.run(debug=True, host='0.0.0.0', port=5000)
