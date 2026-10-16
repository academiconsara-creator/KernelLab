    
def fifo(referencias, capacidade):
    """Simula o algoritmo FIFO (First In, First Out)."""
    if capacidade <= 0:
        raise ValueError("A capacidade deve ser maior que zero.")

    memoria = []
    faltas = 0
    acertos = 0
    historico = []

    for pagina in referencias:
        falta = pagina not in memoria

        if falta:
            faltas += 1

            if len(memoria) >= capacidade:
                memoria.pop(0)

            memoria.append(pagina)
        else:
            acertos += 1

        historico.append({
            "pagina": pagina,
            "memoria": memoria.copy(),
            "falta": falta
        })

    total = len(referencias)
    taxa_faltas = (faltas / total * 100) if total > 0 else 0

    return {
        "faltas": faltas,
        "acertos": acertos,
        "total_referencias": total,
        "taxa_faltas": taxa_faltas,
        "historico": historico
    }


def lru(referencias, capacidade):
    """Simula o algoritmo LRU (Least Recently Used)."""
    if capacidade <= 0:
        raise ValueError("A capacidade deve ser maior que zero.")

    memoria = []
    faltas = 0
    acertos = 0
    historico = []

    for pagina in referencias:
        falta = pagina not in memoria

        if falta:
            faltas += 1

            if len(memoria) >= capacidade:
                memoria.pop(0)

            memoria.append(pagina)
        else:
            acertos += 1

            # Move a página utilizada para o final,
            # representando a página usada mais recentemente.
            memoria.remove(pagina)
            memoria.append(pagina)

        historico.append({
            "pagina": pagina,
            "memoria": memoria.copy(),
            "falta": falta
        })

    total = len(referencias)
    taxa_faltas = (faltas / total * 100) if total > 0 else 0

    return {
        "faltas": faltas,
        "acertos": acertos,
        "total_referencias": total,
        "taxa_faltas": taxa_faltas,
        "historico": historico
    }


def optimal(referencias, capacidade):
    """Simula o algoritmo Ótimo de substituição de páginas."""
    if capacidade <= 0:
        raise ValueError("A capacidade deve ser maior que zero.")

    memoria = []
    faltas = 0
    acertos = 0
    historico = []

    for indice, pagina in enumerate(referencias):
        falta = pagina not in memoria

        if falta:
            faltas += 1

            if len(memoria) >= capacidade:
                futuras = referencias[indice + 1:]
                distancias = []

                for armazenada in memoria:
                    if armazenada in futuras:
                        distancias.append(futuras.index(armazenada))
                    else:
                        # A página não será mais utilizada:
                        # é a melhor candidata para substituição.
                        distancias.append(float("inf"))

                posicao = distancias.index(max(distancias))
                memoria.pop(posicao)

            memoria.append(pagina)
        else:
            acertos += 1

        historico.append({
            "pagina": pagina,
            "memoria": memoria.copy(),
            "falta": falta
        })

    total = len(referencias)
    taxa_faltas = (faltas / total * 100) if total > 0 else 0

    return {
        "faltas": faltas,
        "acertos": acertos,
        "total_referencias": total,
        "taxa_faltas": taxa_faltas,
        "historico": historico
    }
