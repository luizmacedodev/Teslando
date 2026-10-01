import sqlite3
from datetime import datetime


def conectar():
    conexao = sqlite3.connect("tarefas.db")
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_usuario(nome, email):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, email)
            VALUES (?, ?)
        """, (nome, email))

        conexao.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None

    finally:
        conexao.close()


def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email
        FROM usuarios
        ORDER BY id
    """)

    usuarios = cursor.fetchall()
    conexao.close()

    return usuarios


def excluir_usuario(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = ?
    """, (usuario_id,))

    conexao.commit()
    resultado = cursor.rowcount

    conexao.close()

    return resultado


def criar_tarefa(titulo, descricao, usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO tarefas
            (titulo, descricao, data_criacao, usuario_id)
            VALUES (?, ?, ?, ?)
        """, (
            titulo,
            descricao,
            data_criacao,
            usuario_id
        ))

        conexao.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conexao.close()


def listar_tarefas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            tarefas.id,
            tarefas.titulo,
            tarefas.descricao,
            tarefas.data_criacao,
            tarefas.data_conclusao,
            usuarios.nome
        FROM tarefas
        INNER JOIN usuarios
        ON tarefas.usuario_id = usuarios.id
        ORDER BY tarefas.id
    """)

    tarefas = cursor.fetchall()
    conexao.close()

    return tarefas


def atualizar_tarefa(
    id_tarefa,
    titulo,
    descricao,
    data_conclusao
):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE tarefas
        SET
            titulo = ?,
            descricao = ?,
            data_conclusao = ?
        WHERE id = ?
    """, (
        titulo,
        descricao,
        data_conclusao,
        id_tarefa
    ))

    conexao.commit()
    resultado = cursor.rowcount

    conexao.close()

    return resultado


def excluir_tarefa(id_tarefa):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM tarefas
        WHERE id = ?
    """, (id_tarefa,))

    conexao.commit()
    resultado = cursor.rowcount

    conexao.close()

    return resultado