"""
=============================================================
PROJETO DO CONTROLADOR
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo implementa o projeto do controlador
utilizando Root Locus.

São suportados:

    - Controlador P
    - Controlador PI
    - Controlador PD

Autor:
=============================================================
"""

import control as ct
import matplotlib.pyplot as plt

from utils import titulo


class Controlador:

    """
    Projeto do controlador da planta.
    """

    # =========================================================
    # Construtor
    # =========================================================

    def __init__(self, transferencia):

        self.G = transferencia.tf

        self.controlador = None

        self.malha_fechada = None

    # =========================================================
    # Controlador Proporcional
    # =========================================================

    def controlador_P(self, K):

        self.controlador = ct.tf([K], [1])

        return self.controlador

    # =========================================================
    # Controlador PI
    # =========================================================

    def controlador_PI(self, K, Ti):

        self.controlador = K * ct.tf(

            [Ti, 1],

            [Ti, 0]

        )

        return self.controlador

    # =========================================================
    # Controlador PD
    # =========================================================

    def controlador_PD(self, K, Td):

        self.controlador = K * ct.tf(

            [Td, 1],

            [1]

        )

        return self.controlador

    # =========================================================
    # Malha aberta
    # =========================================================

    def malha_aberta(self):

        return self.controlador * self.G

    # =========================================================
    # Malha fechada
    # =========================================================

    def fechar_malha(self):

        self.malha_fechada = ct.feedback(

            self.controlador * self.G,

            1

        )

        return self.malha_fechada

    # =========================================================
    # Root Locus
    # =========================================================
        
    def root_locus(self):

        titulo("Lugar das Raízes")

        plt.figure(figsize=(8,6))

        ct.root_locus(

            self.controlador * self.G,

            grid=True

        )

        plt.title("Root Locus")

        plt.xlabel("Parte Real")

        plt.ylabel("Parte Imaginária")

        plt.grid(True)

        plt.show()
        
    # =========================================================
    # Resposta ao degrau
    # =========================================================

    def resposta_degrau(self):

        if self.malha_fechada is None:

            self.fechar_malha()

        tempo, resposta = ct.step_response(

            self.malha_fechada

        )

        return tempo, resposta

    # =========================================================
    # Métricas
    # =========================================================

    def metricas(self):
    

        return {
        "RiseTime": "Não calculado",
        "SettlingTime": "Não calculado",
        "Overshoot": "Não calculado",
        "Peak": "Não calculado"
    }

    # =========================================================
    # Impressão
    # =========================================================

    def imprimir(self):

        titulo("Controlador")

        print()

        print(self.controlador)

        print()

        print("Sistema em Malha Fechada")

        print()

        print(self.malha_fechada)

        print()

        print("Métricas")

        print()

        info = self.metricas()

        for chave, valor in info.items():

            print(f"{chave:20} {valor}")