"""
=============================================================
PROJETO BOOST
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Classe principal responsável por integrar todos os
módulos do projeto.

Autor:
=============================================================
"""

import numpy as np

from parametros import Parametros
from modelo_nao_linear import ModeloNaoLinear
from equilibrio import Equilibrio
from linearizacao import Linearizacao
from transferencia import FuncaoTransferencia
from analise import AnaliseSistema
from controlador import Controlador
from simulacao import Simulador


class ProjetoBoost:

    """
    Classe principal do projeto.
    """

    # =========================================================
    # Construtor
    # =========================================================

    def __init__(

            self,

            sid,

            duty=0.40,

            ganho=1.0

    ):

        self.sid = sid

        self.duty = duty

        self.ganho = ganho

        self._construir()

    # =========================================================
    # Construção do projeto
    # =========================================================

    def _construir(self):

        self.parametros = Parametros(self.sid)

        self.modelo = ModeloNaoLinear(self.parametros)

        self.equilibrio = Equilibrio(self.parametros)

        self.equilibrio.calcular(self.duty)

        self.linearizacao = Linearizacao(

            self.modelo,

            self.equilibrio

        )

        self.linearizacao.calcular()

        self.transferencia = FuncaoTransferencia(

            self.linearizacao

        )

        self.transferencia.criar_estado()

        self.transferencia.criar_tf()

        self.analise = AnaliseSistema(

            self.transferencia

        )

        self.controlador = Controlador(

            self.transferencia

        )

        self.controlador.controlador_P(

            self.ganho

        )

        self.controlador.fechar_malha()

        self.simulador = Simulador(

            self.modelo,

            self.equilibrio,

            self.transferencia,

            self.controlador

        )

    # =========================================================
    # Executa todo o projeto
    # =========================================================

    def executar(self):

        self.parametros.imprimir()

        self.modelo.imprimir()

        self.equilibrio.imprimir()

        self.linearizacao.imprimir_numerico()

        self.transferencia.imprimir()

        self.analise.imprimir()

        self.controlador.imprimir()

        self.controlador.root_locus()

        tempo = np.linspace(

            0,

            0.2,

            1000

        )

        self.simulador.comparar(

            tempo,

            1.10,

            self.duty

        )

        self.simulador.comparar_fechado(

            tempo,

            1.10,

            self.duty

        )

    # =========================================================
    # Métodos individuais
    # =========================================================

    def mostrar_parametros(self):

        self.parametros.imprimir()

    def mostrar_modelo(self):

        self.modelo.imprimir()

    def mostrar_equilibrio(self):

        self.equilibrio.imprimir()

    def mostrar_linearizacao(self):

        self.linearizacao.imprimir_simbolico()

        self.linearizacao.imprimir_numerico()

    def mostrar_transferencia(self):

        self.transferencia.imprimir()

    def mostrar_analise(self):

        self.analise.imprimir()

    def mostrar_controlador(self):

        self.controlador.imprimir()

    def mostrar_root_locus(self):

        self.controlador.root_locus()

    def executar_simulacoes(self):

        tempo = np.linspace(

            0,

            0.2,

            1000

        )

        self.simulador.comparar(

            tempo,

            1.10,

            self.duty

        )

        self.simulador.comparar_fechado(

            tempo,

            1.10,

            self.duty

        )