from flask import render_template, redirect, url_for, flash,request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import login, cadastro , form_editar_perfil, form_post, form_editarpost
from comunidadeimpressionadora.models import Usuarios, Post
from flask_login import login_user, logout_user, current_user,login_required
import secrets
import os
from PIL import Image

@app.route('/')
def home():
    data=Post.query.order_by(Post.data_criacao.desc()).all()
    usuario= Usuarios.query.all()
    return render_template('home.html', usuario=usuario, datas=data)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/lista-usuarios')
@login_required
def usuarios():
    lista_usuario= Usuarios.query.all()
    return render_template('usuarios.html', lista_usuario= lista_usuario)

@app.route('/login-cadastro', methods = ['GET', 'POST'])
def cad_login():
    logar= login()
    criarconta= cadastro()

    if logar.validate_on_submit() and 'botao_entrar' in request.form:
        usuario= Usuarios.query.filter_by(email= logar.email.data).first()
        if usuario  and bcrypt.check_password_hash(usuario.senha, logar.senha.data):
            login_user(usuario, remember=logar.lembrar_dados.data)
            flash(f'Login bem sucedido ','alert-success')
            par_next= request.args.get('nest')
            if par_next :
                return redirect(par_next)
            else:
                return  redirect(url_for('home'))
        else:
            flash('Falha ao fazer login E-mail ou Senha invalido', 'alert-danger')
    if criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript= bcrypt.generate_password_hash(criarconta.senha.data)
        usuario= Usuarios( username=criarconta.username.data, email= criarconta.e_mail.data, senha=senha_cript)
        #o trcho criarconta.exemplo.data serve para pegar os dados nos campos de formulario
        database.session.add(usuario)
        database.session.commit()
        flash(f' Cadastro realizado com sucesso para { criarconta.e_mail.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template("cad_login.html", logar= logar, criarconta=criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('sessão encerrada','alert-success')
    return redirect(url_for('home'))

@app.route('/Perfil', )
@login_required
def perfil():
    foto_perfil= url_for('static', filename=f'fotoperfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil )

@app.route('/posts/criar', methods = ['GET','POST'] )
@login_required
def criar_post():
    form = form_post()
    if form.validate_on_submit():
        post= Post(titulo=form.titulo.data, corpo=form.corpo.data, id_usuario=current_user.id)

        database.session.add(post)
        database.session.commit()
        flash('Pst atualizado 👌🏼', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    #add codigo no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao= os.path.splitext(imagem.filename) #slpitext serve para separa o nome da extensão da imagem
    nome_arquivo= nome + codigo + extensao
    caminho_completo= os.path.join(app.root_path, 'static/fotoperfil' , nome_arquivo)

    # Abrir a imagem
    imagem_aberta = Image.open(imagem)

    # Garantir que a imagem seja quadrada (cortar)
    largura, altura = imagem_aberta.size
    lado_menor = min(largura, altura)
    esquerda = (largura - lado_menor) // 2
    topo = (altura - lado_menor) // 2
    direita = esquerda + lado_menor
    inferior = topo + lado_menor

    # Recortar a imagem
    imagem_cortada = imagem_aberta.crop((esquerda, topo, direita, inferior))

    # Reduzir o tamanho da imagem (opcional)
    tamanho = (300, 300)  # Defina o tamanho desejado
    imagem_cortada.thumbnail(tamanho)

    #  modelo antigo
    # # reduzir imagem
    # tamanho= (400,400)
    # imagen_reduzia= Image.open(imagem)
    # imagen_reduzia.thumbnail(tamanho)

    #salvar imagem
    #imagen_reduzia.save(caminho_completo)
    imagem_cortada.save(caminho_completo)
    return nome_arquivo
def atualizar_cursos(formulario):
    lista_de_cursos= []
    for campo in formulario: #capo sãoas variaveis que estão dentro da classe form_editar_perfil
        if 'curso_' in campo.name:
            if campo.data:
                lista_de_cursos.append(campo.label.text)# campo.label reorna em forma de objeto o .txt transforma em texto
    return ';'.join(lista_de_cursos)# join junta os cursos e separa com ;

@app.route('/Perfil/editarperfil', methods= ['GET', 'POST'])
@login_required
def editar_perfil():
    formulario= form_editar_perfil()
    if formulario.validate_on_submit():
        current_user.email= formulario.email.data
        current_user.username= formulario.username.data
        if formulario.fotoperfil.data:
            nome_imagem= salvar_imagem(formulario.fotoperfil.data)
            current_user.foto_perfil= nome_imagem
        current_user.cursos= atualizar_cursos(formulario)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')

        return redirect(url_for('perfil'))

    elif request.method == 'GET':
        formulario.email.data= current_user.email
        formulario.username.data= current_user.username

    foto_perfil = url_for('static', filename=f'fotoperfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil= foto_perfil, form= formulario)

@app.route('/post/<id_post>', methods=['GET', 'POST'])
@login_required
def exibir_post(id_post):
    post = Post.query.get(id_post)
    if current_user == post.autor:
        form= form_editarpost()
        if  request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo= form.titulo.data
            post.corpo= form.corpo.data
    else:
        form= None
    return render_template('post.html', post=post, form= form)

@app.route('/post/<id_post>/excluir', methods=['GET', 'POST'])
@login_required
def excluirpost(id_post):
    post= Post.query.get(id_post)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        return redirect(url_for('home'))
    else:
        abort(403)