
from collections import defaultdict, deque
from threading import Lock, Thread
from time import sleep


# Matriz ilustrativa de permissões por processo e dispositivo.
MATRIZ_ACESSO = {
    "P1": {
        "rede": ["utilizar", "solicitar_exclusivo"],
        "audio": [],
        "disco": [],
        "log": ["gravar"],
    },
    "P2": {
        "rede": ["ler", "gravar", "utilizar", "solicitar_exclusivo"],
        "audio": [],
        "disco": [],
        "log": ["gravar"],
    },
    "P3": {
        "rede": [],
        "audio": [],
        "disco": ["ler", "gravar", "utilizar", "solicitar_exclusivo"],
        "log": ["ler", "gravar"],
    },
    "P4": {
        "rede": ["utilizar", "solicitar_exclusivo"],
        "audio": ["executar", "utilizar", "solicitar_exclusivo"],
        "disco": [],
        "log": ["gravar"],
    },
    "P5": {
        "rede": [],
        "audio": [],
        "disco": ["ler", "gravar", "utilizar", "solicitar_exclusivo"],
        "log": ["ler", "gravar"],
    },
    "P6": {
        "rede": ["ler", "gravar", "utilizar", "solicitar_exclusivo"],
        "audio": [],
        "disco": ["ler", "utilizar", "solicitar_exclusivo"],
        "log": ["ler", "gravar"],
    },
}


def simular_dispositivos(processos):
    filas = defaultdict(deque)

    for processo in sorted(processos, key=lambda p: p["arrival"]):
        for dispositivo in processo.get("devices", []):
            filas[dispositivo].append(processo["id"])

    return {
        dispositivo: list(fila)
        for dispositivo, fila in filas.items()
    }


def pode_acessar(pid, dispositivo, operacao):
    permissoes = MATRIZ_ACESSO.get(pid, {})
    operacoes = permissoes.get(dispositivo, [])
    return operacao in operacoes


def exibir_matriz_acesso():
    print("\n" + "=" * 65)
    print("MATRIZ DE CONTROLE DE ACESSO")
    print("=" * 65)

    for pid, dispositivos in MATRIZ_ACESSO.items():
        print(f"\nProcesso {pid}:")

        for dispositivo, operacoes in dispositivos.items():
            texto = ", ".join(operacoes) if operacoes else "sem permissão"
            print(f"  {dispositivo}: {texto}")


def simular_acesso_exclusivo(fila, dispositivo="rede"):
    print("\n" + "=" * 65)
    print("SIMULAÇÃO DE ACESSO EXCLUSIVO COM LOCK")
    print("=" * 65)

    # Um único Lock protege o dispositivo compartilhado.
    trava = Lock()

    def utilizar_dispositivo(pid):
        if not pode_acessar(pid, dispositivo, "utilizar"):
            print(
                f"{pid} não possui permissão para utilizar "
                f"{dispositivo}."
            )
            return

        print(f"{pid} solicitou acesso a {dispositivo}.")

        # Apenas uma thread pode possuir a trava por vez.
        with trava:
            print(f"{pid} adquiriu o dispositivo {dispositivo}.")
            print(f"{pid} está utilizando o recurso.")

            # Pequeno intervalo para tornar a utilização visível.
            sleep(0.1)

            print(f"{pid} liberou o dispositivo {dispositivo}.")

    threads = []

    for pid in fila:
        thread = Thread(target=utilizar_dispositivo, args=(pid,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Simulação concluída: todas as threads finalizaram.")


def exibir_dispositivos(processos):
    filas = simular_dispositivos(processos)

    print("\n" + "=" * 55)
    print("KERNELLAB - DISPOSITIVOS DE ENTRADA E SAÍDA")
    print("=" * 55)

    if not filas:
        print("Nenhuma solicitação de dispositivo encontrada.")
    else:
        for dispositivo, processos_fila in sorted(filas.items()):
            print(f"\nDispositivo: {dispositivo}")
            print(f"Solicitações: {len(processos_fila)}")
            print(f"Fila FIFO: {' -> '.join(processos_fila)}")

    exibir_matriz_acesso()

    # Preferimos a rede para demonstrar um recurso compartilhado.
    dispositivo = "rede"

    if dispositivo in filas:
        fila = filas[dispositivo]

        print(
            f"\nDispositivo selecionado para demonstração: "
            f"{dispositivo}"
        )

        simular_acesso_exclusivo(fila, dispositivo)
    else:
        print("\nNão há solicitações para o dispositivo de rede.")

