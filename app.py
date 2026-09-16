from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
) 
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

#configurações SQLite
app.config['SECRET_KEY'] = "m4rc05"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///usuarios.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configuração SQLAlchemy
db = SQLAlchemy(app)

#Configuração do login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Faça login para acessar esta página."

#==================================#
#             MODELS               #
#==================================#
class Usuario(UserMixin, db.Model):
    matricula = db.Column(db.Integer, primary_key=True)

@login_manager.user_loader
def carregar_usuario(user_id):
    return db.session.get(Usuario, int(user_id))

#==================================#
#              LOGIN               #
#==================================#
@app.route('/')
def inicio():
    return redirect('/accounts/login/?next=/')

@app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next', '/')
    if request.method == 'POST':
        matricula = request.form['matricula']

        novo_usuario = Usuario(
            matricula = matricula,
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('video'))

    return render_template('index.html')

#==================================#
#        CRIAÇÃO DO BANCO          #
#==================================#
with app.app_context():
    db.create_all()

#==================================#
#            EXECUÇÃO              #
#==================================#
if __name__ == "__main__":
    app.run(debug=True)