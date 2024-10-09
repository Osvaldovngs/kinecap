from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Usuario simulado (usaremos un usuario ficticio por ahora)
users = {'test@example.com': {'password': 'password123'}}

# Clase de formulario de login usando Flask-WTF
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=50)])
    submit = SubmitField('Login')

# Clase User que hereda de UserMixin, necesaria para manejar usuarios con Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Cargar el usuario por su id (en este caso el email)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Verificar si el email existe en nuestro diccionario y la contraseña coincide
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            flash('Login exitoso.')
            return redirect(url_for('dashboard'))

        flash('Correo o contraseña incorrectos.')

    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Bienvenido {current_user.id} al dashboard.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

if __name__ == '__main__':
    app.run(debug=True)
