
import json
from pathlib import Path

from memory import fifo, lru, optimal
from devices import exibir_dispositivos
from gantt import exibir_gantt

from schedulers import (
    fcfs,
    sjf,
    round_robin,
    priority_scheduling
)


def carregar_processos():
    caminho = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "processes.json"
    )

    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def exibir_resultados(nome, resultados, timeline):
    print(f"\n{'=' * 65}")
    print(f"ESCALONADOR: {nome}")
    print("=" * 65)

    print(
        f"{'PID':<6}{'Início':>8}{'Fim':>8}"
        f"{'Espera':>10}{'Retorno':>10}{'Resposta':>11}"
    )

    for p in resultados:
        print(
            f"{p['id']:<6}{p['start']:>8}"
            f"{p['finish']:>8}{p['waiting']:>10}"
            f"{p['turnaround']:>10}{p['response']:>11}"
        )

    total = len(resultados)

    if total == 0:
        print("Nenhum processo foi executado.")
        return

    # A ordem vem da timeline para incluir as execuções
    # repetidas do Round Robin.
    ordem_execucao = [
        intervalo["id"]
        for intervalo in timeline
        if intervalo["id"] != "OCIOSO"
    ]

    print("-" * 65)
    print(f"Sequência de execução: {' -> '.join(ordem_execucao)}")

    print(
        f"Espera média: "
        f"{sum(p['waiting'] for p in resultados) / total:.2f}"
    )

    print(
        f"Retorno médio: "
        f"{sum(p['turnaround'] for p in resultados) / total:.2f}"
    )

    print(
        f"Resposta média: "
        f"{sum(p['response'] for p in resultados) / total:.2f}"
    )


def exibir_metricas(metricas):
    print("\n--- Métricas complementares ---")
    print(
        f"Trocas de contexto: "
        f"{metricas['trocas_contexto']}"
    )

    atrasos = metricas["atrasos_excessivos"]

    if atrasos:
        print("Possíveis atrasos excessivos:")

        for processo in atrasos:
            print(
                f"  {processo['id']}: espera de "
                f"{processo['waiting']} "
                f"(limite: {processo['limite']})"
            )
    else:
        print("Nenhum atraso excessivo identificado.")


def testar_memoria():
    referencias = [
        1, 2, 3, 4, 1, 2, 5, 1, 2,
        3, 4, 5, 2, 1, 5, 3, 2
    ]

    capacidade = 4

    algoritmos = {
        "FIFO": fifo,
        "LRU": lru,
        "Optimal": optimal
    }

    print("\n" + "=" * 65)
    print("KERNELLAB - SIMULAÇÃO DE GERENCIAMENTO DE MEMÓRIA")
    print("=" * 65)
    print(f"Referências: {referencias}")
    print(f"Quadros de memória: {capacidade}")

    for nome, algoritmo in algoritmos.items():
        resultado = algoritmo(referencias, capacidade)

        print(f"\n--- Algoritmo {nome} ---")
        print(
            f"{'Página':<10}"
            f"{'Quadros de memória':<30}"
            f"{'Resultado':<15}"
        )

        for etapa in resultado["historico"]:
            memoria = str(etapa["memoria"])
            situacao = "FALTA" if etapa["falta"] else "ACERTO"

            print(
                f"{etapa['pagina']:<10}"
                f"{memoria:<30}"
                f"{situacao:<15}"
            )

        print(
            f"\nTotal de referências: "
            f"{resultado['total_referencias']}"
        )
        print(f"Faltas de página: {resultado['faltas']}")
        print(f"Acertos: {resultado['acertos']}")
        print(
            f"Taxa de faltas: "
            f"{resultado['taxa_faltas']:.2f}%"
        )

    print("\n" + "=" * 65)
    print("FIM DA SIMULAÇÃO DE MEMÓRIA")
    print("=" * 65)


def exibir_comparacao(resultados_escalonadores):
    print("\n" + "=" * 90)
    print("KERNELLAB - COMPARAÇÃO DOS ESCALONADORES")
    print("=" * 90)

    print(
        f"{'Algoritmo':<18}"
        f"{'Espera média':>15}"
        f"{'Retorno médio':>16}"
        f"{'Resposta média':>17}"
        f"{'Trocas contexto':>20}"
    )

    comparacao = []

    for nome, resultado in resultados_escalonadores.items():
        processos = resultado["resultados"]
        metricas = resultado["metricas"]
        total = len(processos)

        if total == 0:
            continue

        espera = sum(p["waiting"] for p in processos) / total
        retorno = sum(p["turnaround"] for p in processos) / total
        resposta = sum(p["response"] for p in processos) / total
        trocas = metricas["trocas_contexto"]

        comparacao.append({
            "nome": nome,
            "espera": espera,
            "retorno": retorno,
            "resposta": resposta,
            "trocas": trocas
        })

        print(
            f"{nome:<18}"
            f"{espera:>15.2f}"
            f"{retorno:>16.2f}"
            f"{resposta:>17.2f}"
            f"{trocas:>20}"
        )

    if comparacao:
        melhor_espera = min(comparacao, key=lambda x: x["espera"])
        melhor_resposta = min(comparacao, key=lambda x: x["resposta"])

        print("\n--- Análise automática ---")
        print(
            f"Menor espera média: {melhor_espera['nome']} "
            f"({melhor_espera['espera']:.2f})"
        )
        print(
            f"Menor resposta média: {melhor_resposta['nome']} "
            f"({melhor_resposta['resposta']:.2f})"
        )

        print(
            "\nObservação: menor tempo médio não significa "
            "necessariamente maior justiça. "
            "Considere também a distribuição das esperas."
        )


def main():
    processos = carregar_processos()

    escalonadores = {
        "FCFS": fcfs,
        "SJF": sjf,
        "Round Robin": round_robin,
        "Prioridade": priority_scheduling
    }

    
    resultados_escalonadores = {}

    for nome, algoritmo in escalonadores.items():
        resultado = algoritmo(processos)
        resultados_escalonadores[nome] = resultado

        exibir_resultados(
            nome,
            resultado["resultados"],
            resultado["timeline"]
        )

        exibir_gantt(nome, resultado["timeline"])
        exibir_metricas(resultado["metricas"])

    exibir_comparacao(resultados_escalonadores)

    testar_memoria()
    exibir_dispositivos(processos)



if __name__ == "__main__":
    main()
