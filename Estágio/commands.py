import os
import shutil
import shlex
from pathlib import Path

try:
    import readline
except ImportError:
    pass
 
diretorio_atual = Path.cwd().resolve()

def mostrar_comandos():
    print("\nComandos disponíveis:")
    for cmd in COMANDOS.keys():
        print(f"  {cmd}")

def comando_ls(args):
    if args: return print("Uso: ls")
    try:
        for item in diretorio_atual.iterdir():
            tipo = "[DIR]" if item.is_dir() else "     "
            print(f"{tipo} {item.name}")
    except PermissionError:
        print("Erro: você não tem permissão para acessar essa pasta.")

diretorio_anterior = Path.cwd().resolve()

def comando_cd(args):
    global diretorio_atual, diretorio_anterior
    
    if not args:
        novo_caminho = Path.home()
    
    elif args[0] == "-":
        novo_caminho = diretorio_anterior
        print(novo_caminho)
        
    else:
        novo_caminho = (diretorio_atual / args[0]).resolve()
    
    if not novo_caminho.exists():
        return print("Erro: diretório não encontrado.")
    if not novo_caminho.is_dir():
        return print("Erro: o caminho informado não é uma pasta.")
    
    diretorio_anterior = diretorio_atual
    diretorio_atual = novo_caminho

    
    diretorio_atual = novo_caminho

def comando_pwd(args):
    if args: return print("Uso: pwd")
    print(diretorio_atual)

def comando_cp(args):
    if len(args) != 2: return print("Uso: cp <origem> <destino>")
    origem = (diretorio_atual / args[0]).resolve()
    destino = (diretorio_atual / args[1]).resolve()
    
    try:
        if origem.is_dir():
            shutil.copytree(origem, destino)
        else:
            shutil.copy2(origem, destino)
        print("Copiado com sucesso.")
    except Exception as e:
        print(f"Erro na operação: {e}")

def comando_mv(args):
    if len(args) != 2: return print("Uso: mv <origem> <destino>")
    origem = (diretorio_atual / args[0]).resolve()
    destino = (diretorio_atual / args[1]).resolve()
    
    try:
        shutil.move(str(origem), str(destino))
        print("Movido com sucesso.")
    except Exception as e:
        print(f"Erro na operação: {e}")

def comando_rm(args):
    if len(args) != 1: return print("Uso: rm <arquivo/pasta>")
    caminho = (diretorio_atual / args[0]).resolve()
    
    if not caminho.exists():
        return print("Erro: arquivo ou pasta não encontrada.")
    
    print(f"Você está prestes a remover: {caminho}")
    if input("Tem certeza? [s/n]: ").lower() != "s":
        return print("Operação cancelada.")
        
    try:
        if caminho.is_dir():
            shutil.rmtree(caminho)
        else:
            caminho.unlink()
        print("Removido com sucesso.")
    except PermissionError:
        print("Erro: você não tem permissão para realizar essa operação.")

def comando_cat(args):
    if len(args) == 2 and args[0] == ">":
        caminho = (diretorio_atual / args[1]).resolve()
        
        if caminho.is_dir():
            return print("Erro: o destino não pode ser uma pasta.")
            
        print("✍️  Modo de escrita ativado. Digite o texto do arquivo.")
        print("💡 Digite [SAIR] em uma linha vazia para salvar e fechar.\n")
        
        linhas = []
        while True:
            try:
                linha = input()
                if linha.strip() == "[SAIR]":
                    break
                linhas.append(linha)
            except (KeyboardInterrupt, EOFError):
                break
        
        conteudo_final = "\n".join(linhas)
        try:
            caminho.write_text(conteudo_final, encoding="utf-8")
            print(f"\n💾 Arquivo '{caminho.name}' criado com sucesso!")
        except PermissionError:
            print("Erro: você não tem permissão para gravar neste local.")
        return

    if len(args) != 1: 
        return print("Uso:\n  Ler: cat <arquivo>\n  Criar: cat > <arquivo>")
        
    caminho = (diretorio_atual / args[0]).resolve()
    
    if not caminho.exists(): 
        return print("Erro: arquivo não encontrado.")
    if caminho.is_dir(): 
        return print("Erro: cat não pode ser usado em uma pasta.")
    
    try:
        print(caminho.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        print("Erro: esse arquivo não parece ser um arquivo de texto.")
    except PermissionError:
        print("Erro: você não tem permissão para ler esse arquivo.")


def comando_clear(args):
    if args: return print("Uso: clear")
    os.system("cls" if os.name == "nt" else "clear")

def comando_exit(args):
    if args: return print("Uso: exit")
    print("Encerrando a Python Shell...")
    return False

COMANDOS = {
    "ls": comando_ls, "cd": comando_cd, "pwd": comando_pwd,
    "cp": comando_cp, "mv": comando_mv, "rm": comando_rm,
    "cat": comando_cat, "clear": comando_clear, "exit": comando_exit
}

def executar_comando(entrada):
    try:
        partes = shlex.split(entrada)
    except ValueError:
        print("Erro: aspas não fechadas.")
        return True
        
    if not partes: return True
    
    cmd, args = partes[0], partes[1:]
    
    if cmd in COMANDOS:
        resultado = COMANDOS[cmd](args)
        # Se a função retornar False (caso do exit), encerra o programa
        return False if resultado is False else True
        
    print(f"Comando não encontrado: {cmd}")
    return True

# INÍCIO DA SHELL
print("========================")
print(" PYTHON SHELL")
print("========================")
mostrar_comandos()
print("\nDigite 'exit' para sair.")

while True:
    try:
        entrada = input(f"\n{diretorio_atual} $ ")
        if not executar_comando(entrada):
            break
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando...")
        break