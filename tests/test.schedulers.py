
import unittest

from src.schedulers import (
    fcfs,
    sjf,
    round_robin,
    priority_scheduling
)


class TestEscalonadores(unittest.TestCase):

    def setUp(self):
        self.processos = [
            {
                "id": "P1",
                "arrival": 0,
                "burst": 5,
                "priority": 2
            },
            {
                "id": "P2",
                "arrival": 1,
                "burst": 3,
                "priority": 1
            },
            {
                "id": "P3",
                "arrival": 2,
                "burst": 2,
                "priority": 3
            }
        ]

    def verificar_resultado(self, resultado):
        self.assertIn("resultados", resultado)
        self.assertIn("timeline", resultado)
        self.assertIn("metricas", resultado)

        resultados = resultado["resultados"]

        self.assertEqual(len(resultados), len(self.processos))

        for processo in resultados:
            self.assertGreater(processo["burst"], 0)
            self.assertGreater(
                processo["turnaround"], 0
            )
            self.assertGreaterEqual(
                processo["waiting"], 0
            )
            self.assertGreaterEqual(
                processo["response"], 0
            )

            # Retorno = espera + tempo de execução.
            self.assertEqual(
                processo["turnaround"],
                processo["waiting"] + processo["burst"]
            )

        self.assertGreaterEqual(
            resultado["metricas"]["trocas_contexto"], 0
        )

    def test_fcfs(self):
        self.verificar_resultado(fcfs(self.processos))

    def test_sjf(self):
        self.verificar_resultado(sjf(self.processos))

    def test_round_robin(self):
        self.verificar_resultado(
            round_robin(self.processos, quantum=3)
        )

    def test_prioridade(self):
        self.verificar_resultado(
            priority_scheduling(self.processos)
        )

    def test_quantum_invalido(self):
        with self.assertRaises(ValueError):
            round_robin(self.processos, quantum=0)


if __name__ == "__main__":
    unittest.main()
