"""
=============================================================
SIMULAÇÃO DO SISTEMA
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo executa todas as simulações do projeto.

São suportadas:

    • Modelo linear
    • Modelo não linear
    • Malha aberta
    • Malha fechada
    • Comparações

Autor:
=============================================================
"""

import numpy as np
import matplotlib.pyplot as plt

import control as ct

from scipy.integrate import solve_ivp

from utils import titulo


class Simulador:

    """
    Laboratório de simulações do projeto.
    """

    # ---------------------------------------------------------
    # Construtor
    # ---------------------------------------------------------

    def __init__(

            self,

            modelo,

            equilibrio,

            transferencia,

            controlador=None

    ):

        self.modelo = modelo

        self.eq = equilibrio

        self.G = transferencia.tf

        self.controlador = controlador

    # ---------------------------------------------------------
    # Simulação Linear
    # ---------------------------------------------------------

    def simular_linear(

            self,

            tempo,

            amplitude

    ):

        T, y = ct.step_response(

            amplitude * self.G,

            T=tempo

        )

        return T, y

    # ---------------------------------------------------------
    # Simulação Não Linear
    # ---------------------------------------------------------

    def simular_nao_linear(

            self,

            tempo,

            duty

    ):

        estado0 = [

            self.eq.iL_eq,

            self.eq.vC_eq

        ]

        resposta = solve_ivp(

            lambda t, x:

                self.modelo.derivadas(

                    t,

                    x,

                    duty

                ),

            (

                tempo[0],

                tempo[-1]

            ),

            estado0,

            t_eval=tempo

        )

        return (

            resposta.t,

            resposta.y

        )

    # ---------------------------------------------------------
    # Malha Fechada
    # ---------------------------------------------------------

    def simular_fechado(

            self,

            tempo

    ):

        if self.controlador is None:

            raise ValueError(

                "Nenhum controlador informado."

            )

        sistema = self.controlador.malha_fechada

        T, y = ct.step_response(

            sistema,

            T=tempo

        )

        return T, y

    # ---------------------------------------------------------
    # Comparação
    # ---------------------------------------------------------

    def comparar(

            self,

            tempo,

            amplitude,

            duty

    ):

        t1, y1 = self.simular_linear(

            tempo,

            amplitude

        )

        t2, y2 = self.simular_nao_linear(

            tempo,

            duty

        )

        plt.figure(figsize=(10,6))

        plt.plot(

            t1,

            y1,

            label="Linear"

        )

        plt.plot(

            t2,

            y2[1],

            label="Não Linear"

        )

        plt.xlabel("Tempo (s)")

        plt.ylabel("Saída")

        plt.grid(True)

        plt.legend()

        plt.title(

            "Comparação dos Modelos"

        )

        plt.show()

    # ---------------------------------------------------------
    # Comparação Malha Fechada
    # ---------------------------------------------------------

    def comparar_fechado(

            self,

            tempo,

            amplitude,

            duty

    ):

        self.comparar(

            tempo,

            amplitude,

            duty

        )

        if self.controlador is None:

            return

        tf, yf = self.simular_fechado(

            tempo

        )

        plt.figure(figsize=(10,6))

        plt.plot(

            tf,

            yf,

            label="Malha Fechada"

        )

        plt.xlabel("Tempo (s)")

        plt.ylabel("Saída")

        plt.grid(True)

        plt.legend()

        plt.title(

            "Resposta em Malha Fechada"

        )

        plt.show()