"""
=============================================================
PONTO DE EQUILÍBRIO DO CONVERSOR BOOST
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo calcula o ponto de operação (equilíbrio)
do modelo não linear.

No ponto de equilíbrio:

    x_dot = 0

O resultado será utilizado posteriormente na
linearização por Jacobianas.

Autor:
=============================================================
"""

from parametros import Parametros
from modelo_nao_linear import ModeloNaoLinear
from utils import titulo, mostrar


class Equilibrio:

    """
    Calcula o ponto de equilíbrio do conversor Boost.
    """

    # ---------------------------------------------------------
    # Construtor
    # ---------------------------------------------------------

    def __init__(self, parametros):

        self.param = parametros

    # ---------------------------------------------------------
    # Cálculo do equilíbrio
    # ---------------------------------------------------------

    def calcular(self, duty):

        """
        Calcula o vetor de equilíbrio.

        Entrada
        -------
        duty : float

            Duty-cycle nominal.
        """

        if duty <= 0 or duty >= 1:

            raise ValueError(
                "O duty-cycle deve estar entre 0 e 1."
            )

        Es = self.param.Es
        R = self.param.R

        vC_eq = Es / (1 - duty)

        iL_eq = Es / (
            R * (1 - duty) ** 2
        )

        self.u_eq = duty

        self.iL_eq = iL_eq

        self.vC_eq = vC_eq

        return [iL_eq, vC_eq]

    # ---------------------------------------------------------
    # Vetor de estados
    # ---------------------------------------------------------

    def vetor_estado(self):

        return [

            self.iL_eq,

            self.vC_eq

        ]

    # ---------------------------------------------------------
    # Impressão
    # ---------------------------------------------------------

    def imprimir(self):

        titulo("Ponto de Equilíbrio")

        mostrar("Duty-cycle", self.u_eq)

        print()

        mostrar(
            "Corrente no indutor",
            self.iL_eq,
            "A"
        )

        mostrar(
            "Tensão no capacitor",
            self.vC_eq,
            "V"
        )

    # ---------------------------------------------------------
    # Verificação física
    # ---------------------------------------------------------

    def verificar(self):

        """
        Verifica se o ponto encontrado é fisicamente
        plausível.
        """

        erros = []

        if self.iL_eq <= 0:

            erros.append(
                "Corrente negativa."
            )

        if self.vC_eq <= 0:

            erros.append(
                "Tensão negativa."
            )

        if not (0 < self.u_eq < 1):

            erros.append(
                "Duty-cycle inválido."
            )

        if len(erros) == 0:

            return True

        print()

        print("Problemas encontrados:")

        for erro in erros:

            print(" -", erro)

        return False

    # ---------------------------------------------------------
    # Resumo
    # ---------------------------------------------------------

    def resumo(self):

        titulo("Resumo")

        print()

        print("Ponto de operação:")

        print()

        print("iL =", self.iL_eq)

        print("vC =", self.vC_eq)

        print("u  =", self.u_eq)


# =============================================================
# Teste do módulo
# =============================================================

if __name__ == "__main__":

    SID = 123456789

    parametros = Parametros(SID)

    equilibrio = Equilibrio(parametros)

    equilibrio.calcular(0.40)

    equilibrio.imprimir()

    equilibrio.verificar()