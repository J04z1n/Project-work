"""
=============================================================
LINEARIZAÇÃO DO MODELO NÃO LINEAR
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo realiza automaticamente a linearização do
modelo não linear através das matrizes Jacobianas.

O processo consiste em:

1) Obter o modelo simbólico;
2) Calcular as Jacobianas;
3) Substituir o ponto de equilíbrio;
4) Substituir os parâmetros físicos;
5) Gerar o modelo linear numérico.

Autor:
=============================================================
"""

import sympy as sp
import numpy as np

from utils import (
    titulo,
    mostrar_matriz
)

from modelo_nao_linear import ModeloNaoLinear
from equilibrio import Equilibrio


class Linearizacao:

    """
    Responsável pela linearização automática
    do modelo não linear.
    """

    # =========================================================
    # Construtor
    # =========================================================

    def __init__(self, modelo, equilibrio):

        self.modelo = modelo

        self.eq = equilibrio

        (
            self.x,
            self.u,
            self.f,
            self.g,
            self.simbolos

        ) = modelo.modelo_simbolico()

    # =========================================================
    # Jacobianas simbólicas
    # =========================================================

    def calcular_jacobianas(self):

        """
        Calcula simbolicamente
        A, B, C e D.
        """

        self.A = self.f.jacobian(self.x)

        self.B = self.f.jacobian(
            sp.Matrix([self.u])
        )

        self.C = self.g.jacobian(self.x)

        self.D = self.g.jacobian(
            sp.Matrix([self.u])
        )

        return (

            self.A,

            self.B,

            self.C,

            self.D

        )

    # =========================================================
    # Substituição do ponto de equilíbrio
    # =========================================================

    def substituir_equilibrio(self):

        """
        Substitui o ponto de operação.
        """

        s = self.simbolos

        substituicoes = {

            s["x1"]: self.eq.iL_eq,

            s["x2"]: self.eq.vC_eq,

            s["u"]: self.eq.u_eq,

            s["Es"]: self.modelo.param.Es,

            s["L0"]: self.modelo.param.L0,

            s["C"]: self.modelo.param.C,

            s["R"]: self.modelo.param.R,

            s["alpha"]: self.modelo.param.alpha

        }

        self.A_num = sp.N(
            self.A.subs(substituicoes)
        )

        self.B_num = sp.N(
            self.B.subs(substituicoes)
        )

        self.C_num = sp.N(
            self.C.subs(substituicoes)
        )

        self.D_num = sp.N(
            self.D.subs(substituicoes)
        )

    # =========================================================
    # Conversão NumPy
    # =========================================================

    def converter_numpy(self):

        """
        Converte as matrizes para NumPy.
        """

        self.A_np = np.array(
            self.A_num,
            dtype=float
        )

        self.B_np = np.array(
            self.B_num,
            dtype=float
        )

        self.C_np = np.array(
            self.C_num,
            dtype=float
        )

        self.D_np = np.array(
            self.D_num,
            dtype=float
        )

    # =========================================================
    # Processo completo
    # =========================================================

    def calcular(self):

        self.calcular_jacobianas()

        self.substituir_equilibrio()

        self.converter_numpy()

    # =========================================================
    # Impressão simbólica
    # =========================================================

    def imprimir_simbolico(self):

        titulo("Jacobianas Simbólicas")

        print()

        print("A =")

        sp.pprint(self.A)

        print()

        print("B =")

        sp.pprint(self.B)

        print()

        print("C =")

        sp.pprint(self.C)

        print()

        print("D =")

        sp.pprint(self.D)

    # =========================================================
    # Impressão numérica
    # =========================================================

    def imprimir_numerico(self):

        titulo("Modelo Linearizado")

        mostrar_matriz("A", self.A_np)

        mostrar_matriz("B", self.B_np)

        mostrar_matriz("C", self.C_np)

        mostrar_matriz("D", self.D_np)

    # =========================================================
    # Retorno das matrizes
    # =========================================================

    def matrizes(self):

        return (

            self.A_np,

            self.B_np,

            self.C_np,

            self.D_np

        )


# =============================================================
# Teste
# =============================================================

if __name__ == "__main__":

    from parametros import Parametros

    SID = 123456789

    parametros = Parametros(SID)

    modelo = ModeloNaoLinear(parametros)

    equilibrio = Equilibrio(parametros)

    equilibrio.calcular(0.40)

    linear = Linearizacao(

        modelo,

        equilibrio

    )

    linear.calcular()

    linear.imprimir_simbolico()

    linear.imprimir_numerico()