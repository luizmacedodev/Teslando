from database import criar_tabelas

from crud import (
    criar_usuario,
    listar_usuarios,
    excluir_usuario,
    criar_tarefa,
    listar_tarefas,
    atualizar_tarefa,
    excluir_tarefa
)


def mostrar_usuarios():
    usuarios = listar_usuarios()

    if not usuarios:
        print("\nNenhum usuário cadastrado.")
        return False

    print("\n========== USUÁRIOS ==========")

    for usuario in usuarios:
        print(
            f"ID: {usuario[0]} | "
            f"Nome: {usuario[1]} | "
            f"E-mail: {usuario[2]}"
        )

    return True


def mostrar_tarefas():
    tarefas = listar_tarefas()

    if not tarefas:
        print("\nNenhuma tarefa cadastrada.")
        return

    print("\n================ TAREFAS ================")

    for tarefa in tarefas:
        print(f"\nID: {tarefa[0]}")
        print(f"Título: {tarefa[1]}")
        print(f"Descrição: {tarefa[2]}")
        print(f"Criada em: {tarefa[3]}")

        if tarefa[4]:
            print(f"Concluída em: {tarefa[4]}")
        else:
            print("Status: Pendente")

        print(f"Usuário: {tarefa[5]}")


def menu():
    while True:
        print("\n")
        print("====================================")
        print("       SISTEMA DE GERENCIAMENTO")
        print("             DE TAREFAS")
        print("====================================")
        print("1 - Criar usuário")
        print("2 - Listar usuários")
        print("3 - Criar tarefa")
        print("4 - Listar tarefas")
        print("5 - Atualizar tarefa")
        print("6 - Excluir tarefa")
        print("7 - Excluir usuário")
        print("0 - Sair")
        print("====================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n========== CRIAR USUÁRIO ==========")

            nome = input("Nome: ")
            email = input("E-mail: ")

            if not nome or not email:
                print("\nNome e e-mail são obrigatórios.")
                continue

            usuario_id = criar_usuario(nome, email)

            if usuario_id:
                print("\nUsuário criado com sucesso!")
                print(f"ID do usuário: {usuario_id}")
            else:
                print("\nEste e-mail já está cadastrado.")

        elif opcao == "2":
            mostrar_usuarios()

        elif opcao == "3":
            print("\n========== CRIAR TAREFA ==========")

            if not mostrar_usuarios():
                print("\nCadastre um usuário antes de criar uma tarefa.")
                continue

            try:
                usuario_id = int(
                    input("\nDigite o ID do usuário: ")
                )
            except ValueError:
                print("\nDigite um ID válido.")
                continue

            titulo = input("Título da tarefa: ")
            descricao = input("Descrição da tarefa: ")

            if not titulo:
                print("\nO título é obrigatório.")
                continue

            resultado = criar_tarefa(
                titulo,
                descricao,
                usuario_id
            )

            if resultado:
                print("\nTarefa criada com sucesso!")
            else:
                print("\nUsuário não encontrado.")

        elif opcao == "4":
            mostrar_tarefas()

        elif opcao == "5":
            print("\n========== ATUALIZAR TAREFA ==========")

            tarefas = listar_tarefas()

            if not tarefas:
                print("\nNenhuma tarefa cadastrada.")
                continue

            mostrar_tarefas()

            try:
                id_tarefa = int(
                    input("\nDigite o ID da tarefa: ")
                )
            except ValueError:
                print("\nDigite um ID válido.")
                continue

            titulo = input("Novo título: ")
            descricao = input("Nova descrição: ")

            data_conclusao = input(
                "Data de conclusão "
                "(AAAA-MM-DD HH:MM:SS ou deixe vazio): "
            )

            if data_conclusao == "":
                data_conclusao = None

            resultado = atualizar_tarefa(
                id_tarefa,
                titulo,
                descricao,
                data_conclusao
            )

            if resultado:
                print("\nTarefa atualizada com sucesso!")
            else:
                print("\nTarefa não encontrada.")

        elif opcao == "6":
            print("\n========== EXCLUIR TAREFA ==========")

            if not listar_tarefas():
                print("\nNenhuma tarefa cadastrada.")
                continue

            mostrar_tarefas()

            try:
                id_tarefa = int(
                    input("\nDigite o ID da tarefa: ")
                )
            except ValueError:
                print("\nDigite um ID válido.")
                continue

            confirmacao = input(
                "Tem certeza que deseja excluir? (s/n): "
            )

            if confirmacao.lower() == "s":
                resultado = excluir_tarefa(id_tarefa)

                if resultado:
                    print("\nTarefa excluída com sucesso!")
                else:
                    print("\nTarefa não encontrada.")
            else:
                print("\nOperação cancelada.")

        elif opcao == "7":
            print("\n========== EXCLUIR USUÁRIO ==========")

            if not mostrar_usuarios():
                continue

            try:
                usuario_id = int(
                    input("\nDigite o ID do usuário: ")
                )
            except ValueError:
                print("\nDigite um ID válido.")
                continue

            confirmacao = input(
                "Atenção: todas as tarefas desse usuário "
                "também serão excluídas.\n"
                "Tem certeza? (s/n): "
            )

            if confirmacao.lower() == "s":
                resultado = excluir_usuario(usuario_id)

                if resultado:
                    print("\nUsuário excluído com sucesso!")
                    print(
                        "As tarefas desse usuário "
                        "também foram excluídas."
                    )
                else:
                    print("\nUsuário não encontrado.")
            else:
                print("\nOperação cancelada.")

        elif opcao == "0":
            print("\nPrograma encerrado.")
            break

        else:
            print("\nOpção inválida.")


if __name__ == "__main__":
    criar_tabelas()
    menu()