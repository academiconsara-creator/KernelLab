
def exibir_gantt(nome, timeline):
    print(f"\n{'=' * 65}")
    print(f"DIAGRAMA DE GANTT - {nome}")
    print("=" * 65)

    if not timeline:
        print("Nenhum intervalo de execução.")
        return

    # Une intervalos consecutivos do mesmo processo.
    intervalos = []

    for item in timeline:
        atual = item.copy()

        if (
            intervalos
            and intervalos[-1]["id"] == atual["id"]
            and intervalos[-1]["finish"] == atual["start"]
        ):
            intervalos[-1]["finish"] = atual["finish"]
        else:
            intervalos.append(atual)

    tempo_atual = intervalos[0]["start"]
    tempos = [tempo_atual]

    for item in intervalos:
        pid = item["id"]
        inicio = item["start"]
        fim = item["finish"]

        # Exibe eventuais intervalos ociosos.
        if inicio > tempo_atual:
            print(
                f"| OCIOSA ({tempo_atual}-{inicio}) ",
                end=""
            )
            tempos.append(inicio)

        print(f"| {pid} ({inicio}-{fim}) ", end="")

        tempos.append(fim)
        tempo_atual = fim

    print("|")
    print("Tempo:", " -> ".join(map(str, tempos)))
