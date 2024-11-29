from flask_wtf import  FlaskForm
from wtforms import StringField, SubmitField , PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from comunidadeimpressionadora.models import Usuarios
from comunidadeimpressionadora import bcrypt
from flask_login import current_user
#boolean field serve para memorizar email e senha


class cadastro(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired()])
    e_mail = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_e_mail(self, e_mail):
        usuario = Usuarios.query.filter_by(email=e_mail.data).first()
        if usuario:
            raise ValidationError("Já existe uma conta com este e-mail")

    def validate_senha(self, senha):
        usuarios = Usuarios.query.all()  # Obter todos os usuários
        senha_criptografada = bcrypt.generate_password_hash(senha.data).decode('utf-8')
        for usuario in usuarios:
            # Verificar se a senha coincide com alguma já armazenada
            if bcrypt.check_password_hash(usuario.senha, senha.data):
                raise ValidationError("Senha existente, tente novamente com outra senha")
class login( FlaskForm):
    email= StringField( 'E-mail',validators=[DataRequired(), Email()])
    senha= PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar_dados= BooleanField('Lembrar dados de acesso?')
    botao_entrar= SubmitField(' Fazer Login')

class form_editar_perfil (FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    fotoperfil= FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_excel= BooleanField('Excel ')
    curso_vba= BooleanField('Vba')
    curso_powebi= BooleanField("Powerbi")
    curso_pyhton= BooleanField('Python')
    curso_ppt= BooleanField('PPT')
    curso_sql= BooleanField('Sql')
    botao_submit_editarperfil= SubmitField('confirmar edição')

    def validate_email(self, email):
        #caso o usuario queira muerdar apenas username é este codigo não pode gerar conflito con seu proprio email que ja existe
        if current_user.email != email.data:
            usuario = Usuarios.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("Já existe uma conta com este e-mail, cadstre um novo E-mail")

class form_post(FlaskForm):
    titulo=StringField('Legenda', validators=[DataRequired(), Length(2,100)])
    corpo= TextAreaField('Novo Post', validators=[DataRequired()])
    botao_submit_post= SubmitField('🫡')

class form_editarpost(FlaskForm):
    titulo=StringField('Legenda', validators=[DataRequired(), Length(2,100)])
    corpo= TextAreaField('Editar Post', validators=[DataRequired()])
    botao_submit_post= SubmitField('🫡')