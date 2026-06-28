"""
=============================================================
ANÁLISE DO SISTEMA DINÂMICO
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo realiza a análise dinâmica do sistema
linearizado.

São calculados:

- resposta ao degrau
- ganho DC
- polos
- zeros
- estabilidade
- controlabilidade
- observabilidade
- métricas transitórias

Autor:
=============================================================
"""

import numpy as np
import control as ct

from utils import titulo


class AnaliseSistema:

    """
    Classe responsável pela análise do sistema.
    """

    # ---------------------------------------------------------
    # Construtor
    # ---------------------------------------------------------

    def __init__(self, transferencia):

        self.G = transferencia

        self.tf = transferencia.tf

        self.ss = transferencia.ss

    # ---------------------------------------------------------
    # Resposta ao degrau
    # ---------------------------------------------------------

    def resposta_degrau(self):

        self.tempo, self.saida = ct.step_response(
            self.tf
        )

        return self.tempo, self.saida

    # ---------------------------------------------------------
    # Ganho DC
    # ---------------------------------------------------------

    def ganho_dc(self):

        return ct.dcgain(self.tf)

    # ---------------------------------------------------------
    # Polos
    # ---------------------------------------------------------

    def polos(self):

        return ct.poles(self.tf)

    # ---------------------------------------------------------
    # Zeros
    # ---------------------------------------------------------

    def zeros(self):

        return ct.zeros(self.tf)

    # ---------------------------------------------------------
    # Estabilidade BIBO
    # ---------------------------------------------------------

    def estavel(self):

        polos = self.polos()

        for polo in polos:

            if np.real(polo) >= 0:

                return False

        return True

    # ---------------------------------------------------------
    # Métricas transitórias
    # ---------------------------------------------------------

    def metricas(self):
    

        return {
        "RiseTime": "Não calculado",
        "SettlingTime": "Não calculado",
        "Overshoot": "Não calculado",
        "Peak": "Não calculado"
    }

    # ---------------------------------------------------------
    # Matriz de Controlabilidade
    # ---------------------------------------------------------

    def controlabilidade(self):

        A = self.ss.A

        B = self.ss.B

        Ctrb = ct.ctrb(A, B)

        posto = np.linalg.matrix_rank(Ctrb)

        return Ctrb, posto

    # ---------------------------------------------------------
    # Matriz de Observabilidade
    # ---------------------------------------------------------

    def observabilidade(self):

        A = self.ss.A

        C = self.ss.C

        Obs = ct.obsv(A, C)

        posto = np.linalg.matrix_rank(Obs)

        return Obs, posto

    # ---------------------------------------------------------
    # Impressão
    # ---------------------------------------------------------

    def imprimir(self):

        titulo("Análise do Sistema")

        print()

        print("Polos:")

        print(self.polos())

        print()

        print("Zeros:")

        print(self.zeros())

        print()

        print("Ganho DC:")

        print(self.ganho_dc())

        print()

        print("Sistema estável:")

        print(self.estavel())

        print()

        print("Métricas:")

        info = self.metricas()

        for chave, valor in info.items():

            print(f"{chave:20} {valor}")

        print()

        ctrb, posto = self.controlabilidade()

        print("Posto da Controlabilidade:", posto)

        obs, posto = self.observabilidade()

        print("Posto da Observabilidade:", posto)