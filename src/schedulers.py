
from collections import deque


def registrar_intervalo(timeline, pid, inicio, fim):
    """Registra um intervalo válido no diagrama de Gantt."""
    if fim > inicio:
        timeline.append({
            "id": pid,
            "start": inicio,
            "finish": fim
        })


def calcular_metricas(timeline, resultados, fator_espera=2):
    """
    Calcula trocas de contexto e identifica possíveis atrasos excessivos.

    Um atraso é considerado excessivo quando o tempo de espera
    supera duas vezes o tempo de execução do processo.
    Esse limite é uma heurística configurável, não uma definição
    universal de starvation (inanição).
    """
    trocas_contexto = 0
    processo_anterior = None

    for intervalo in timeline:
        pid = intervalo["id"]

        # Um período ocioso interrompe a sequência de execução.
        if pid == "OCIOSO":
            processo_anterior = None
            continue

        if (
            processo_anterior is not None
            and pid != processo_anterior
        ):
            trocas_contexto += 1

        processo_anterior = pid

    atrasos_excessivos = []

    for processo in resultados:
        limite = processo["burst"] * fator_espera

        if processo["waiting"] > limite:
            atrasos_excessivos.append({
                "id": processo["id"],
                "waiting": processo["waiting"],
                "limite": limite
            })

    return {
        "trocas_contexto": trocas_contexto,
        "atrasos_excessivos": atrasos_excessivos
    }



def finalizar_escalonamento(resultados, timeline):
    metricas = calcular_metricas(timeline, resultados)

    return {
        "resultados": resultados,
        "timeline": timeline,
        "metricas": metricas
    }


def fcfs(processos):
    """First Come, First Served: executa por ordem de chegada."""
    fila = sorted(processos, key=lambda p: p["arrival"])

    tempo_atual = 0
    resultados = []
    timeline = []

    for p in fila:
        chegada = p["arrival"]
        duracao = p["burst"]

        inicio = max(tempo_atual, chegada)

        if inicio > tempo_atual:
            registrar_intervalo(
                timeline, "OCIOSO", tempo_atual, inicio
            )

        fim = inicio + duracao

        resultados.append({
            "id": p["id"],
            "arrival": chegada,
            "burst": duracao,
            "start": inicio,
            "finish": fim,
            "waiting": inicio - chegada,
            "turnaround": fim - chegada,
            "response": inicio - chegada
        })

        registrar_intervalo(timeline, p["id"], inicio, fim)
        tempo_atual = fim

    return finalizar_escalonamento(resultados, timeline)


def sjf(processos):
    """Shortest Job First não preemptivo."""
    pendentes = sorted(
        processos, key=lambda p: p["arrival"]
    )

    tempo_atual = 0
    resultados = []
    timeline = []

    while pendentes:
        disponiveis = [
            p for p in pendentes
            if p["arrival"] <= tempo_atual
        ]

        if not disponiveis:
            chegada = pendentes[0]["arrival"]

            registrar_intervalo(
                timeline, "OCIOSO", tempo_atual, chegada
            )

            tempo_atual = chegada
            continue

        escolhido = min(
            disponiveis,
            key=lambda p: (p["burst"], p["arrival"])
        )

        chegada = escolhido["arrival"]
        inicio = tempo_atual
        fim = inicio + escolhido["burst"]

        resultados.append({
            "id": escolhido["id"],
            "arrival": chegada,
            "burst": escolhido["burst"],
            "start": inicio,
            "finish": fim,
            "waiting": inicio - chegada,
            "turnaround": fim - chegada,
            "response": inicio - chegada
        })

        registrar_intervalo(
            timeline, escolhido["id"], inicio, fim
        )

        tempo_atual = fim
        pendentes.remove(escolhido)

    return finalizar_escalonamento(resultados, timeline)


def round_robin(processos, quantum=3):
    """Round Robin preemptivo com quantum configurável."""
    if quantum <= 0:
        raise ValueError("O quantum deve ser maior que zero.")

    pendentes = sorted(
        processos, key=lambda p: p["arrival"]
    )

    fila = deque()
    restante = {
        p["id"]: p["burst"] for p in pendentes
    }
    primeira_execucao = {}
    resultados = []
    timeline = []

    tempo_atual = 0
    indice = 0

    while indice < len(pendentes) or fila:
        # Adiciona à fila os processos que já chegaram.
        while (
            indice < len(pendentes)
            and pendentes[indice]["arrival"] <= tempo_atual
        ):
            fila.append(pendentes[indice])
            indice += 1

        if not fila:
            proxima_chegada = pendentes[indice]["arrival"]

            registrar_intervalo(
                timeline,
                "OCIOSO",
                tempo_atual,
                proxima_chegada
            )

            tempo_atual = proxima_chegada
            continue

        p = fila.popleft()
        pid = p["id"]

        if pid not in primeira_execucao:
            primeira_execucao[pid] = tempo_atual

        inicio = tempo_atual
        duracao = min(quantum, restante[pid])

        tempo_atual += duracao
        restante[pid] -= duracao

        registrar_intervalo(
            timeline, pid, inicio, tempo_atual
        )

        # Processos que chegaram durante este intervalo
        # entram na fila antes de o processo atual retornar.
        while (
            indice < len(pendentes)
            and pendentes[indice]["arrival"] <= tempo_atual
        ):
            fila.append(pendentes[indice])
            indice += 1

        if restante[pid] > 0:
            fila.append(p)
        else:
            chegada = p["arrival"]
            fim = tempo_atual

            resultados.append({
                "id": pid,
                "arrival": chegada,
                "burst": p["burst"],
                "start": primeira_execucao[pid],
                "finish": fim,
                "waiting": fim - chegada - p["burst"],
                "turnaround": fim - chegada,
                "response": primeira_execucao[pid] - chegada
            })

    return finalizar_escalonamento(resultados, timeline)


def priority_scheduling(processos):
    """Escalonamento por prioridade, não preemptivo.

    Quanto menor o número da prioridade, maior sua importância.
    """
    pendentes = sorted(
        processos, key=lambda p: p["arrival"]
    )

    tempo_atual = 0
    resultados = []
    timeline = []

    while pendentes:
        disponiveis = [
            p for p in pendentes
            if p["arrival"] <= tempo_atual
        ]

        if not disponiveis:
            chegada = pendentes[0]["arrival"]

            registrar_intervalo(
                timeline, "OCIOSO", tempo_atual, chegada
            )

            tempo_atual = chegada
            continue

        escolhido = min(
            disponiveis,
            key=lambda p: (p["priority"], p["arrival"])
        )

        chegada = escolhido["arrival"]
        duracao = escolhido["burst"]
        inicio = tempo_atual
        fim = inicio + duracao

        resultados.append({
            "id": escolhido["id"],
            "arrival": chegada,
            "burst": duracao,
            "start": inicio,
            "finish": fim,
            "waiting": inicio - chegada,
            "turnaround": fim - chegada,
            "response": inicio - chegada
        })

        registrar_intervalo(
            timeline, escolhido["id"], inicio, fim
        )

        tempo_atual = fim
        pendentes.remove(escolhido)

    return finalizar_escalonamento(resultados, timeline)
