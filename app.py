from flask import Flask, render_template, request, url_for, redirect

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/MYFLASK'

db = SQLAlchemy(app)

class Funcionario(db.Model):
    __tablename__='funcionario'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

db.create_all()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        if nome and email:
            f = Funcionario(nome, email)
            db.session.add(f)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    funcionarios = Funcionario.query.all()
    return render_template("lista.html", funcionarios=funcionarios)

@app.route("/excluir/<int:id>")
def excluir(id):
    funcionario = Funcionario.query.filter_by(_id=id).first()

    db.session.delete(funcionario)
    db.session.commit()

    funcionarios = Funcionario.query.all()

    return render_template("lista.html", funcionarios=funcionarios)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    funcionario = Funcionario.query.filter_by(_id=id).first()

    if request.method == 'POST':
        nome = request.form.get("nome")
        email = request.form.get("email")

        if nome and email:
            funcionario.nome = nome
            funcionario.email = email

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("atualizar.html", funcionario=funcionario)


if __name__ == "__main__":
    app.run(debug=True)