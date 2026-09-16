import csv
import os
import smtplib
from email.message import EmailMessage

import requests


# ==========================================
# CONFIGURAÇÕES
# ==========================================

URL_API = "https://reqres.in/api/users"
ARQUIVO = "usuarios.csv"

CAMPOS = [
    "id",
    "email",
    "first_name",
    "last_name",
    "avatar"
]

def carregar_usuarios_locais():

    usuarios = []

    if not os.path.exists(ARQUIVO):
        return usuarios

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                linha["id"] = int(linha["id"])
                usuarios.append(linha)

        return usuarios

    except Exception as erro:
        print(f"Erro ao ler o arquivo salvo: {erro}")
        return []


def salvar_usuarios(usuarios):

    try:
        with open(
            ARQUIVO,
            "w",
            newline="",
            encoding="utf-8"
        ) as arquivo:

            escritor = csv.DictWriter(
                arquivo,
                fieldnames=CAMPOS
            )

            escritor.writeheader()

            for usuario in usuarios:
                escritor.writerow(usuario)

        return True

    except IOError as erro:
        print(f"Erro ao salvar dados no arquivo: {erro}")
        return False

def buscar_dados_api():

    usuarios_api = []
    pagina = 1

    while True:

        try:
            resposta = requests.get(
                URL_API,
                params={"page": pagina},
                timeout=10
            )

            resposta.raise_for_status()

            dados = resposta.json()

            usuarios_api.extend(
                dados.get("data", [])
            )

            total_paginas = dados.get(
                "total_pages",
                1
            )

            if pagina >= total_paginas:
                break

            pagina += 1

        except requests.exceptions.RequestException as erro:
            print(
                f"\n[Erro API] "
                f"Falha ao acessar a API: {erro}"
            )

            return []

    return usuarios_api

def enviar_email(destinatario):

    remetente = "klzluiz27@gmail.com"

    senha = os.getenv("EMAIL_SENHA")

    if not senha:
        print(
            "\n[ERRO] Senha de app não configurada."
        )
        print(
            "Configure a variável de ambiente EMAIL_SENHA."
        )
        return False

    mensagem = EmailMessage()

    mensagem["Subject"] = "Lista de Usuários"
    mensagem["From"] = remetente
    mensagem["To"] = destinatario

    mensagem.set_content(
        "Olá!\n\n"
        "Segue em anexo a lista de usuários "
        "atualizada.\n\n"
        "Atenciosamente."
    )

    try:

        with open(ARQUIVO, "rb") as arquivo:

            dados = arquivo.read()

            mensagem.add_attachment(
                dados,
                maintype="text",
                subtype="csv",
                filename=ARQUIVO
            )

    except IOError:
        print(
            "Erro: o arquivo CSV não foi encontrado "
            "ou está ilegível."
        )

        return False

    try:

        print(
            f"Conectando ao Gmail para enviar "
            f"para {destinatario}..."
        )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as servidor:

            servidor.login(
                remetente,
                senha
            )

            servidor.send_message(mensagem)

        print(
            "E-mail enviado com sucesso "
            "com o arquivo anexo!"
        )

        return True

    except Exception as erro:

        print(
            f"Falha no envio do e-mail: {erro}"
        )

        return False

def exibir_usuarios(usuarios):

    if not usuarios:

        print(
            "\n[Lista Vazia] "
            "Nenhum usuário cadastrado."
        )

        return

    print("\n" + "=" * 70)

    print(
        f"{'ID':<5} | "
        f"{'NOME':<20} | "
        f"E-MAIL"
    )

    print("=" * 70)

    for usuario in usuarios:

        nome_completo = (
            f"{usuario.get('first_name', '')} "
            f"{usuario.get('last_name', '')}"
        )

        print(
            f"{usuario.get('id'):<5} | "
            f"{nome_completo:<20} | "
            f"{usuario.get('email')}"
        )

    print("=" * 70)

def menu():

    usuarios = carregar_usuarios_locais()

    while True:

        print(
            f"\n--- GERENCIADOR "
            f"(Total: {len(usuarios)}) ---"
        )

        print("1. Listar usuários")
        print("2. Adicionar usuário")
        print("3. Remover usuário")
        print("4. Enviar arquivo por e-mail")
        print("5. Importar usuários da API ReqRes")
        print("6. Sair")

        opcao = input(
            "Escolha uma opção (1-6): "
        ).strip()

        if opcao == "1":

            exibir_usuarios(usuarios)

        elif opcao == "2":

            novo_id = (
                max(
                    [usuario["id"] for usuario in usuarios],
                    default=0
                ) + 1
            )

            primeiro_nome = input(
                "Primeiro Nome: "
            ).strip()

            ultimo_nome = input(
                "Sobrenome: "
            ).strip()

            email = input(
                "E-mail: "
            ).strip()

            novo_usuario = {
                "id": novo_id,
                "email": email,
                "first_name": primeiro_nome,
                "last_name": ultimo_nome,
                "avatar": ""
            }

            usuarios.append(novo_usuario)

            if salvar_usuarios(usuarios):

                print(
                    f"Usuário '{primeiro_nome}' "
                    f"salvo com sucesso!"
                )

        elif opcao == "3":

            exibir_usuarios(usuarios)

            if not usuarios:
                continue

            try:

                id_remover = int(
                    input(
                        "Digite o ID para remover: "
                    )
                )

                usuarios_filtrados = [
                    usuario
                    for usuario in usuarios
                    if usuario["id"] != id_remover
                ]

                if len(usuarios_filtrados) == len(usuarios):

                    print("ID não encontrado.")

                else:

                    usuarios = usuarios_filtrados

                    salvar_usuarios(usuarios)

                    print(
                        "Usuário removido e "
                        "arquivo atualizado!"
                    )

            except ValueError:

                print(
                    "Digite um número válido."
                )

        elif opcao == "4":

            exibir_usuarios(usuarios)

            if not usuarios:
                continue

            try:

                id_destino = int(
                    input(
                        "Digite o ID de quem "
                        "vai receber o e-mail: "
                    )
                )

                usuario_alvo = next(
                    (
                        usuario
                        for usuario in usuarios
                        if usuario["id"] == id_destino
                    ),
                    None
                )

                if usuario_alvo:

                    enviar_email(
                        usuario_alvo["email"]
                    )

                else:

                    print(
                        "Usuário não encontrado."
                    )

            except ValueError:

                print(
                    "Digite um número válido."
                )

        elif opcao == "5":

            print(
                "\nBuscando dados da API..."
            )

            dados_api = buscar_dados_api()

            if dados_api:

                ids_existentes = {
                    usuario["id"]
                    for usuario in usuarios
                }

                novos_usuarios = [
                    usuario
                    for usuario in dados_api
                    if usuario["id"] not in ids_existentes
                ]

                usuarios.extend(novos_usuarios)

                salvar_usuarios(usuarios)

                print(
                    f"{len(novos_usuarios)} "
                    f"novos usuários importados!"
                )

            else:

                print(
                    "Não foi possível "
                    "importar dados da API."
                )

        elif opcao == "6":

            print("Saindo...")
            break

        else:

            print(
                "Opção inválida."
            )

def main():
    menu()


if __name__ == "__main__":
    main()