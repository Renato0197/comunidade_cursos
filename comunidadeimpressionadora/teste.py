from comunidadeimpressionadora import app, database
with app.app_context():
    database.create_all()
# with app.app_context():
#     usuario1= Usuarios(username='renato', email='renato@gmail.com', senha='123456')
#     usuario2= Usuarios(username='bacurim', email='bacurim@gmail.com', senha='654321')
#     database.session.add(usuario1)
#     database.session.add(usuario2)
#     database.session.commit()
# with app.app_context():
#     meus_usuarios= Usuarios.query.all()
#     print(meus_usuarios)
#     primeirousuario= meus_usuarios[0]
#     print(primeirousuario.senha, primeirousuario.posts, primeirousuario.cursos)
#
# with app.app_context():
#     post= Post(titulo= 'ébojéé', corpo='gordo', id_usuario=2)
#     database.session.add(post)
#     database.session.commit()
# with app.app_context():
#     post= Post.query.all()
#     post1= post[0]
#     print(post1.corpo, post1.id_usuario, post1.autor.email) #autor é o valor atribuido a bakref da class Usuario que faz referencia ao usuario
# from comunidadeimpressionadora.models import Usuarios
# with app.app_context():
#     user= Usuarios.query.all()
#     user1= user[0]
#     print( user1.email)
# with app.app_context():
#     database.drop_all()
