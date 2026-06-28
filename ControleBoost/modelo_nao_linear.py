"""
=============================================================
MODELO NÃO LINEAR DO CONVERSOR BOOST
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo implementa o modelo médio não linear do
conversor Boost em espaço de estados.

O objetivo deste arquivo é representar exclusivamente
a dinâmica física do sistema.

Modelo:

x1 = corrente no indutor (iL)
x2 = tensão no capacitor (vC)

Entrada:
u = duty-cycle PWM

Saída:
y = tensão do capacitor

Autor:
=============================================================
"""

import numpy as np
import sympy as sp

from parametros import Parametros
from utils import (
    titulo,
    mostrar
)


class ModeloNaoLinear:
    """
    Modelo médio não linear do conversor Boost.
    """

    # =========================================================
    # Construtor
    # =========================================================

    def __init__(self, parametros):

        self.param = parametros

    # =========================================================
    # Indutância não linear
    # =========================================================

    def indutancia(self, iL):
        """
        Calcula a indutância em função da corrente.

        L(iL) = L0 / (1 + alpha*iL²)
        """

        return self.param.L0 / (
            1 + self.param.alpha * iL**2
        )

    # =========================================================
    # Inverso da indutância
    # =========================================================

    def inverso_indutancia(self, iL):
        """
        Retorna 1/L(iL).

        Essa forma aparece diretamente na equação de estados.
        """

        return (
            1 + self.param.alpha * iL**2
        ) / self.param.L0
    # =========================================================
    # Modelo simbólico
    # =========================================================

    def modelo_simbolico(self):
        """
        Constrói simbolicamente o modelo não linear.

        Retorna
        -------
        x : vetor de estados

        u : entrada

        f : vetor de funções de estado

        g : função de saída

        símbolos : dicionário contendo todos os símbolos.
        """

        # -----------------------------------------------------
        # Variáveis de estado
        # -----------------------------------------------------

        x1, x2 = sp.symbols(
            "x1 x2",
            real=True
        )

        # -----------------------------------------------------
        # Entrada
        # -----------------------------------------------------

        u = sp.symbols(
            "u",
            real=True
        )

        # -----------------------------------------------------
        # Parâmetros físicos
        # -----------------------------------------------------

        Es, L0, C, R, alpha = sp.symbols(
            "Es L0 C R alpha",
            positive=True,
            real=True
        )

        # -----------------------------------------------------
        # Indutância
        # -----------------------------------------------------

        L = L0 / (1 + alpha*x1**2)

        # -----------------------------------------------------
        # Equações diferenciais
        # -----------------------------------------------------

        f1 = (1/L) * (
            Es -
            (1-u)*x2
        )

        f2 = (
            (1-u)*x1 -
            x2/R
        ) / C

        # -----------------------------------------------------
        # Vetores
        # -----------------------------------------------------

        x = sp.Matrix([x1, x2])

        f = sp.Matrix([f1, f2])

        g = sp.Matrix([x2])

        simbolos = {

            "x1": x1,
            "x2": x2,

            "u": u,

            "Es": Es,

            "L0": L0,

            "C": C,

            "R": R,

            "alpha": alpha

        }

        return x, u, f, g, simbolos
    
        # =========================================================
    # Substituição numérica
    # =========================================================

    def substituir_parametros(self, expressao):
        """
        Substitui os parâmetros físicos pelos valores
        armazenados na classe Parametros.
        """

        x, u, f, g, s = self.modelo_simbolico()

        return expressao.subs({

            s["Es"]: self.param.Es,

            s["L0"]: self.param.L0,

            s["C"]: self.param.C,

            s["R"]: self.param.R,

            s["alpha"]: self.param.alpha

        })
        
            # =========================================================
    # Impressão do modelo simbólico
    # =========================================================

    def imprimir_modelo_simbolico(self):

        titulo("Modelo Simbólico")

        x, u, f, g, s = self.modelo_simbolico()

        print()

        print("f(x,u) =")

        sp.pprint(f)

        print()

        print("g(x,u) =")

        sp.pprint(g)
    # =========================================================
    # Equações diferenciais
    # =========================================================

    def derivadas(self, t, estado, u):
        """
        Calcula as derivadas do sistema.

        Parâmetros
        ----------
        t : float

            Tempo (necessário para solve_ivp).

        estado : list

            [iL, vC]

        u : float

            Duty-cycle.
        """

        iL, vC = estado

        L_inv = self.inverso_indutancia(iL)

        diL = L_inv * (
            self.param.Es -
            (1 - u) * vC
        )

        dvC = (
            (1 - u) * iL
            - vC / self.param.R
        ) / self.param.C

        return np.array([diL, dvC])

    # =========================================================
    # Saída do sistema
    # =========================================================

    def saida(self, estado):
        """
        Saída medida.

        y = vC
        """

        return estado[1]

    # =========================================================
    # Vetor de estados
    # =========================================================

    def f(self, estado, u):
        """
        Interface matemática:

            x_dot = f(x,u)
        """

        return self.derivadas(0, estado, u)

    # =========================================================
    # Equação de saída
    # =========================================================

    def g(self, estado, u):
        """
        Interface matemática:

            y = g(x,u)
        """

        return self.saida(estado)

    # =========================================================
    # Impressão das informações
    # =========================================================

    def imprimir(self):

        titulo("Modelo Não Linear")

        mostrar(
            "Estados",
            "[iL, vC]"
        )

        mostrar(
            "Entrada",
            "Duty Cycle (u)"
        )

        mostrar(
            "Saída",
            "vC"
        )

    # =========================================================
    # Resumo
    # =========================================================

    def resumo(self):

        print()

        print("Equações implementadas:")

        print()

        print("diL/dt = (1/L(iL)) * (Es - (1-u)vC)")

        print()

        print("dvC/dt = ((1-u)iL - vC/R)/C")

        print()

        print("L(iL) = L0/(1 + alpha*iL²)")


# =============================================================
# Teste do módulo
# =============================================================

if __name__ == "__main__":

    SID = 123456789

    parametros = Parametros(SID)

    modelo = ModeloNaoLinear(parametros)

    modelo.imprimir()

    estado = [2.0, 30.0]

    u = 0.40

    derivadas = modelo.f(estado, u)

    titulo("Teste")

    mostrar("diL/dt", derivadas[0], "A/s")

    mostrar("dvC/dt", derivadas[1], "V/s")