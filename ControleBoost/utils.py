"""
=============================================================
UTILITÁRIOS DO PROJETO
-------------------------------------------------------------
Disciplina : Sistemas de Controle (TI0173)

Este módulo reúne funções auxiliares utilizadas em todo
o projeto. O objetivo é evitar repetição de código,
padronizar a saída no terminal e facilitar a leitura
dos resultados.

Nenhuma função deste arquivo depende diretamente do
modelo do conversor Boost.

Autor:
=============================================================
"""

import numpy as np


# ============================================================
# Impressão de títulos
# ============================================================

def titulo(texto):
    """
    Exibe um título padronizado no terminal.
    """

    print()
    print("=" * 60)
    print(texto.upper())
    print("=" * 60)


# ============================================================
# Impressão de subtítulos
# ============================================================

def subtitulo(texto):
    """
    Exibe um subtítulo padronizado.
    """

    print()
    print("-" * 60)
    print(texto)
    print("-" * 60)


# ============================================================
# Impressão organizada de valores
# ============================================================

def mostrar(nome, valor, unidade=""):
    """
    Exibe uma variável de forma organizada.

    Exemplo:
        mostrar("Capacitância", 0.002, "F")
    """

    if unidade:
        print(f"{nome:<30}: {valor} {unidade}")
    else:
        print(f"{nome:<30}: {valor}")


# ============================================================
# Impressão de matrizes
# ============================================================

def mostrar_matriz(nome, matriz):
    """
    Exibe uma matriz NumPy de forma organizada.
    """

    print()
    print(nome)
    print("-" * len(nome))
    print(np.array(matriz))


# ============================================================
# Verificação numérica
# ============================================================

def verificar_positivo(nome, valor):
    """
    Garante que um parâmetro físico seja positivo.
    """

    if valor <= 0:
        raise ValueError(
            f"{nome} deve ser positivo. Valor encontrado: {valor}"
        )


# ============================================================
# Impressão de separadores
# ============================================================

def linha():
    """
    Imprime uma linha horizontal.
    """

    print("-" * 60)