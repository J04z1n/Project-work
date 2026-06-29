"""
O que esse módulo faz?
-Implementa o modelo médio não linear.
-Implementa o modelo linearizado.
-Simula degraus de 1%, 2,5% e 5% em torno de u_bar = 0.5.
-Comparar v_C do modelo não linear com v_bar_C + Delta v_C do linear.
-Calcular RMSE e erro máximo para discutir a validade da linearização.

Dependências: (instale professora Michela, pode ser necessário instalar outras bibliotecas como Scipy e SYMPY se ainda não tiver)
    pip install numpy scipy matplotlib
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# infromaç~~oes dos modelos
SID = 568274
ES = 24.0                 # V
ALPHA = 0.01              # A^-2
U_BAR = 0.50              # duty cycle nominal (adimensional)

rng = np.random.default_rng(SID)
DELTA = float(rng.standard_normal())
L0 = 6e-3 * (1.0 + DELTA)       # H
C_CAP = 1e-3 * (1.0 + DELTA)    # F
R_LOAD = 100.0 * (1.0 + DELTA)  # ohm

# Ponto de equilíbrio definido na linearizção
V_BAR = ES / (1.0 - U_BAR)
I_BAR = ES / (R_LOAD * (1.0 - U_BAR) ** 2)
X_BAR = np.array([I_BAR, V_BAR], dtype=float)

# Matrizes numéricas do modelo linearizado em variáveis de desvio.
# Delta_x_dot = A Delta_x + B Delta_u
# Delta_y = C_OUT Delta_x + D Delta_u
BETA = 1.0 + ALPHA * I_BAR**2
A = np.array(
    [
        [0.0, -BETA * (1.0 - U_BAR) / L0],
        [(1.0 - U_BAR) / C_CAP, -1.0 / (R_LOAD * C_CAP)],
    ],
    dtype=float,
)
B = np.array(
    [
        [BETA * V_BAR / L0],
        [-I_BAR / C_CAP],
    ],
    dtype=float,
)
C_OUT = np.array([[0.0, 1.0]], dtype=float)
D = np.array([[0.0]], dtype=float)

# Degraus relativos a u_bar: 1%, 2,5% e 5%.
# Essa faixa mantém o conversor próximo do ponto de operação e evita
# usar o caso de 10%, que pode levar o modelo médio a uma corrente negativa.
PERCENTUAIS = (1.0, 2.5, 5.0)
T_INICIO = 0.05            # s
T_FINAL = 1.50             # s
N_PONTOS = 6000
PASTA_SAIDA = Path("resultados")


@dataclass
class Resultado:
    percentual: float
    delta_u: float
    rmse_v: float
    erro_max_v: float
    v_final_nl: float
    v_final_lin: float
    i_min_nl: float
    i_max_nl: float

# Modelos do sistema
def duty_absoluto(t: float, delta_u: float) -> float:
    """Duty cycle absoluto aplicado ao modelo não linear.

    Antes do degrau: u(t) = u_bar.
    Após o degrau : u(t) = u_bar + Delta_u.
    """
    u = U_BAR + (delta_u if t >= T_INICIO else 0.0)
    return float(np.clip(u, 0.0, 1.0))


def modelo_nao_linear(t: float, x: np.ndarray, delta_u: float) -> np.ndarray:
    """Modelo médio não linear: x_dot = f(x, u)."""
    i_l, v_c = x
    u = duty_absoluto(t, delta_u)

    inverso_l = (1.0 + ALPHA * i_l**2) / L0
    di_l = inverso_l * (ES - (1.0 - u) * v_c)
    dv_c = ((1.0 - u) * i_l - v_c / R_LOAD) / C_CAP

    return np.array([di_l, dv_c], dtype=float)


def modelo_linearizado(t: float, delta_x: np.ndarray, delta_u: float) -> np.ndarray:
    """Modelo linearizado em variáveis de desvio: Delta_x_dot=A Delta_x+B Delta_u."""
    entrada = delta_u if t >= T_INICIO else 0.0
    return A @ delta_x + B[:, 0] * entrada

# Simulação e comparação
def simular_caso(percentual: float, tempo: np.ndarray) -> tuple[Resultado, dict[str, np.ndarray]]:
    """Simula um degrau percentual relativo a u_bar nos dois modelos."""
    delta_u = U_BAR * percentual / 100.0

    if not 0.0 <= U_BAR + delta_u <= 1.0:
        raise ValueError("O degrau escolhido torna o duty cycle fisicamente inválido.")

    # Não linear: estados e entrada são valores absolutos.
    sol_nl = solve_ivp(
        fun=lambda t, x: modelo_nao_linear(t, x, delta_u),
        t_span=(float(tempo[0]), float(tempo[-1])),
        y0=X_BAR,
        t_eval=tempo,
        rtol=1e-8,
        atol=1e-10,
        max_step=2e-4,
    )
    if not sol_nl.success:
        raise RuntimeError(f"Falha na simulação não linear: {sol_nl.message}")

    # Linear: estados, entrada e saída são desvios do equilíbrio.
    sol_lin = solve_ivp(
        fun=lambda t, dx: modelo_linearizado(t, dx, delta_u),
        t_span=(float(tempo[0]), float(tempo[-1])),
        y0=np.zeros(2),
        t_eval=tempo,
        rtol=1e-9,
        atol=1e-11,
        max_step=2e-4,
    )
    if not sol_lin.success:
        raise RuntimeError(f"Falha na simulação linear: {sol_lin.message}")

    v_nl = sol_nl.y[1]
    delta_y_lin = (C_OUT @ sol_lin.y).reshape(-1)

    # Ponto essencial: reconstrói a tensão absoluta do modelo linearizado.
    v_lin = V_BAR + delta_y_lin

    erro = v_nl - v_lin
    resultado = Resultado(
        percentual=percentual,
        delta_u=delta_u,
        rmse_v=float(np.sqrt(np.mean(erro**2))),
        erro_max_v=float(np.max(np.abs(erro))),
        v_final_nl=float(v_nl[-1]),
        v_final_lin=float(v_lin[-1]),
        i_min_nl=float(np.min(sol_nl.y[0])),
        i_max_nl=float(np.max(sol_nl.y[0])),
    )

    dados = {
        "tempo": tempo,
        "v_nao_linear": v_nl,
        "v_linear": v_lin,
        "i_nao_linear": sol_nl.y[0],
        "duty": np.array([duty_absoluto(t, delta_u) for t in tempo]),
    }
    return resultado, dados


def salvar_grafico(resultado: Resultado, dados: dict[str, np.ndarray], pasta: Path) -> None:
    """Gera um gráfico profissional para um caso de degrau."""
    pasta.mkdir(parents=True, exist_ok=True)
    tempo = dados["tempo"]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(tempo, dados["v_nao_linear"], linewidth=2, label="Modelo não linear")
    ax.plot(tempo, dados["v_linear"], "--", linewidth=2, label="Modelo linearizado")
    ax.axvline(T_INICIO, linestyle=":", linewidth=1.5, label="Início do degrau")
    ax.set_title(
        f"Comparação em malha aberta — degrau de {resultado.percentual:g}% em $\\bar{{u}}$ "
        f"($\\Delta u={resultado.delta_u:.3f}$)"
    )
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Tensão de saída $v_C$ (V)")
    ax.grid(True, alpha=0.35)
    ax.legend()
    fig.tight_layout()

    rotulo = f"{resultado.percentual:g}".replace(".", "p")
    nome = f"comparacao_aberta_{rotulo}pct.png"
    fig.savefig(pasta / nome, dpi=220)
    plt.close(fig)


def imprimir_dados_base() -> None:
    print("=" * 72)
    print("SIMULAÇÕES | CONVERSOR BOOST")
    print("=" * 72)
    print(f"SID                         = {SID}")
    print(f"delta                       = {DELTA:.10f}")
    print(f"L0                          = {L0:.9f} H")
    print(f"C                           = {C_CAP:.9f} F")
    print(f"R                           = {R_LOAD:.9f} ohm")
    print(f"u_bar                       = {U_BAR:.6f}")
    print(f"x_bar = [iL_bar, vC_bar]^T  = [{I_BAR:.9f} A, {V_BAR:.6f} V]^T")
    print("\nA =")
    print(A)
    print("B =")
    print(B)
    print("C =", C_OUT)
    print("D =", D)


def main() -> None:
    imprimir_dados_base()
    tempo = np.linspace(0.0, T_FINAL, N_PONTOS)

    print("\nRESULTADOS DA COMPARAÇÃO LINEAR × NÃO LINEAR")
    print("-" * 72)
    resultados: list[Resultado] = []

    for percentual in PERCENTUAIS:
        resultado, dados = simular_caso(percentual, tempo)
        salvar_grafico(resultado, dados, PASTA_SAIDA)
        resultados.append(resultado)

        print(
            f"Degrau de {resultado.percentual:>4.1f}% | "
            f"Delta_u = {resultado.delta_u:.5f} | "
            f"RMSE = {resultado.rmse_v:.6f} V | "
            f"Erro máximo = {resultado.erro_max_v:.6f} V"
        )
        print(
            f"  vC final: não linear = {resultado.v_final_nl:.6f} V | "
            f"linear = {resultado.v_final_lin:.6f} V | "
            f"faixa de iL não linear = [{resultado.i_min_nl:.6f}, {resultado.i_max_nl:.6f}] A"
        )

    print("\nArquivos gerados em:", PASTA_SAIDA.resolve())
    print("\nInterpretação sugerida:")
    print("- Quanto menores RMSE e erro máximo, melhor é a aproximação linear.")
    print("- A faixa de validade deve ser discutida a partir do crescimento do erro")
    print("  à medida que a amplitude do degrau aumenta.")


if __name__ == "__main__":
    main()
