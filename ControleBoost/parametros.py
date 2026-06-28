"""
=============================================================
PARÂMETROS DO CONVERSOR BOOST
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo gera todos os parâmetros físicos utilizados
durante o projeto.

Os parâmetros L0, C e R são calculados a partir do maior
SID do grupo, conforme especificado no enunciado.

Autor:
=============================================================
"""

import numpy as np

from utils import (
    titulo,
    mostrar,
    verificar_positivo
)


class Parametros:
    """
    Classe responsável por armazenar todos os parâmetros
    físicos do sistema.
    """

    # ---------------------------------------------------------
    # Construtor
    # ---------------------------------------------------------

    def __init__(self, sid):

        self.sid = int(sid)

        # Constantes fornecidas pelo enunciado

        self.Es = 24.0          # V
        self.alpha = 0.01       # A^-2

        # Geração dos parâmetros

        self.gerar_parametros()

        # Validação

        self.validar()

    # ---------------------------------------------------------
    # Geração dos parâmetros
    # ---------------------------------------------------------

    def gerar_parametros(self):
        """
        Gera os parâmetros pseudoaleatórios do sistema.
        """

        np.random.seed(self.sid)

        delta = np.random.randn()

        self.delta = delta

        # Conversão para unidades SI

        self.L0 = 6e-3 * (1 + delta)

        self.C = 1e-3 * (1 + delta)

        self.R = 100 * (1 + delta)

    # ---------------------------------------------------------
    # Validação
    # ---------------------------------------------------------

    def validar(self):
        """
        Garante que os parâmetros físicos sejam válidos.
        """

        verificar_positivo("Indutância L0", self.L0)

        verificar_positivo("Capacitância C", self.C)

        verificar_positivo("Resistência R", self.R)

    # ---------------------------------------------------------
    # Impressão
    # ---------------------------------------------------------

    def imprimir(self):

        titulo("Parâmetros do Sistema")

        mostrar("Maior SID", self.sid)

        mostrar("Delta", round(self.delta, 6))

        print()

        mostrar("Tensão de entrada Es", self.Es, "V")

        mostrar("Coeficiente α", self.alpha, "A⁻²")

        print()

        mostrar("Indutância L0", self.L0, "H")

        mostrar("Capacitância C", self.C, "F")

        mostrar("Resistência R", self.R, "Ω")

    # ---------------------------------------------------------
    # Conversão para dicionário
    # ---------------------------------------------------------

    def dicionario(self):
        """
        Retorna todos os parâmetros em formato de dicionário.
        """

        return {

            "sid": self.sid,

            "delta": self.delta,

            "L0": self.L0,

            "C": self.C,

            "R": self.R,

            "Es": self.Es,

            "alpha": self.alpha

        }


# =============================================================
# Execução direta
# =============================================================

if __name__ == "__main__":

    SID = 123456789

    parametros = Parametros(SID)

    parametros.imprimir()