"""
=============================================================
FUNÇÃO DE TRANSFERÊNCIA DO CONVERSOR BOOST
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo converte o modelo linearizado em espaço de
estados para sua representação por função de transferência.

Autor:
=============================================================
"""

import control as ct

from utils import titulo

from linearizacao import Linearizacao


class FuncaoTransferencia:

    """
    Representação do sistema linear no domínio de Laplace.
    """

    # =========================================================
    # Construtor
    # =========================================================

    def __init__(self, linearizacao):

        self.linear = linearizacao

    # =========================================================
    # Modelo em espaço de estados
    # =========================================================

    def criar_estado(self):

        """
        Cria o objeto StateSpace.
        """

        self.ss = ct.ss(

            self.linear.A_np,

            self.linear.B_np,

            self.linear.C_np,

            self.linear.D_np

        )

        return self.ss

    # =========================================================
    # Função de transferência
    # =========================================================

    def criar_tf(self):

        """
        Converte StateSpace em Transfer Function.
        """

        if not hasattr(self, "ss"):

            self.criar_estado()

        self.tf = ct.ss2tf(self.ss)

        return self.tf

    # =========================================================
    # Ganho DC
    # =========================================================

    def ganho_dc(self):

        """
        Calcula o ganho DC.
        """

        if not hasattr(self, "tf"):

            self.criar_tf()

        return ct.dcgain(self.tf)

    # =========================================================
    # Polos
    # =========================================================

    def polos(self):

        """
        Retorna os polos da função de transferência.
        """

        if not hasattr(self, "tf"):

            self.criar_tf()

        return ct.poles(self.tf)

    # =========================================================
    # Zeros
    # =========================================================

    def zeros(self):

        """
        Retorna os zeros da função de transferência.
        """

        if not hasattr(self, "tf"):

            self.criar_tf()

        return ct.zeros(self.tf)

    # =========================================================
    # Impressão
    # =========================================================

    def imprimir(self):

        titulo("Função de Transferência")

        print()

        print(self.tf)

        print()

        print("Ganho DC")

        print(self.ganho_dc())

        print()

        print("Polos")

        print(self.polos())

        print()

        print("Zeros")

        print(self.zeros())

    # =========================================================
    # Retorno
    # =========================================================

    def sistema(self):

        return self.tf


# =============================================================
# Teste
# =============================================================

if __name__ == "__main__":

    from parametros import Parametros
    from modelo_nao_linear import ModeloNaoLinear
    from equilibrio import Equilibrio

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

    G = FuncaoTransferencia(linear)

    G.criar_estado()

    G.criar_tf()

    G.imprimir()