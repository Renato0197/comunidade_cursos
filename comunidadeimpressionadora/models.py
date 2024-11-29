from comunidadeimpressionadora import  database, logim_manege
from datetime import datetime
from flask_login import  UserMixin

@logim_manege.user_loader
def load_usuario(id_usuario):
    return Usuarios.query.get(int(id_usuario)) #o flas_login reconhe a Prymarykey da classe Usuaario como id_usuario que
    # recebe o valor de id da classe Usuario atraves de Usermixin
class Usuarios(database.Model, UserMixin):
    id= database.Column( database.Integer, primary_key= True)
    username= database.Column( database.String, nullable= False)
    email= database.Column( database.String, nullable=False, unique=True)
    senha= database.Column( database.String, nullable= False, unique=True)
    foto_perfil= database.Column( database.String, default='default.jpg')
    posts= database.relationship('Post', backref='autor' ,lazy=True)
    cursos= database.Column(database.String, nullable=False, default= 'Em andamento')

    def contarpost(self):
        return len(self.posts)
    def contarcursos(self):
        return len(self.cursos)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)
