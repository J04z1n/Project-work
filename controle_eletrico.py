from pathlib import Path
import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from scipy import signal
from scipy.integrate import solve_ivp

# Dados apresentados anteriormente
Es = 24.0
alpha = 0.01
L0 = 0.0062444701116
Ccap = 0.0010407450186
R = 104.07450186
u_bar = 0.5
i_bar = Es / (R * (1 - u_bar) ** 2)
v_bar = Es / (1 - u_bar)

# G(s) = N(s)/D(s)
a1 = 886.303677486
b0 = 3724353.357999
d1 = 9.232329974
d0 = 38795.347479
num_G = np.array([-a1, b0])
den_G = np.array([1.0, d1, d0])
Gdc = b0 / d0

# PD filtrado (derivada na medição)
Kp = 0.10
Tlead = 0.002574638182228838
Tf = 0.0001287319091114419
Td = Tlead - Tf
r_amp = 2.4

out = Path("figuras")
out.mkdir(exist_ok=True)

def cl_denominator(K):
    return np.polyadd(
        np.polymul([Tf, 1.0], den_G),
        K * np.polymul([Tlead, 1.0], num_G)
    )

def cl_reference_numerator(K):
    return K * np.polymul([Tf, 1.0], num_G)

def root_locus_branches(k_values):
    roots0 = np.roots(cl_denominator(k_values[0]))
    previous = np.array(roots0, dtype=complex)
    branches = [[root] for root in previous]

    for K in k_values[1:]:
        roots_now = np.roots(cl_denominator(K))
        best_perm = min(
            itertools.permutations(roots_now),
            key=lambda perm: sum(abs(previous[i] - perm[i]) ** 2 for i in range(len(previous)))
        )
        current = np.array(best_perm, dtype=complex)
        for i, root in enumerate(current):
            branches[i].append(root)
        previous = current

    return [np.array(branch) for branch in branches]

def response_metrics(t, y, y_final):
    peak = float(np.max(y))
    overshoot = (peak - y_final) / y_final * 100.0

    idx10 = np.where(y >= 0.10 * y_final)[0]
    idx90 = np.where(y >= 0.90 * y_final)[0]
    tr = float(t[idx90[0]] - t[idx10[0]]) if len(idx10) and len(idx90) else np.nan

    out_band = np.where(np.abs(y - y_final) > 0.02 * abs(y_final))[0]
    ts = float(t[out_band[-1] + 1]) if len(out_band) and out_band[-1] + 1 < len(t) else np.nan

    return peak, overshoot, tr, ts

# Malha fechada linear
den_cl = cl_denominator(Kp)
num_cl = cl_reference_numerator(Kp)
poles_cl = np.roots(den_cl)
dominant = poles_cl[np.argmax(np.imag(poles_cl))]
zeta_cl = -dominant.real / abs(dominant)
ess = 1.0 / (1.0 + Kp * Gdc)

t_cl = np.linspace(0.0, 0.05, 100001)
sys_cl = signal.TransferFunction(r_amp * num_cl, den_cl)
t_cl, y_cl = signal.step(sys_cl, T=t_cl)
y_cl_final = r_amp * (Kp * Gdc) / (1.0 + Kp * Gdc)

# Malha aberta
delta_u_open = 0.025
t_open = np.linspace(0.0, 1.0, 150001)
sys_open = signal.TransferFunction(delta_u_open * num_G, den_G)
t_open, y_open = signal.step(sys_open, T=t_open)

# Modelo não linear em malha fechada
def nonlinear_closed_loop(t, x):
    iL, vC, z_derivative = x
    delta_v = vC - v_bar
    error = r_amp - delta_v

    delta_u = Kp * error - Kp * Td * z_derivative
    duty = np.clip(u_bar + delta_u, 0.0, 1.0)

    diL = ((1.0 + alpha * iL**2) / L0) * (Es - (1.0 - duty) * vC)
    dvC = ((1.0 - duty) * iL - vC / R) / Ccap
    dz = (dvC - z_derivative) / Tf
    return [diL, dvC, dz]

solution = solve_ivp(
    nonlinear_closed_loop,
    (0.0, 0.05),
    [i_bar, v_bar, 0.0],
    dense_output=True,
    max_step=2e-6,
    rtol=1e-9,
    atol=1e-11,
)

i_nl, v_nl, z_nl = solution.sol(t_cl)
y_nl = v_nl - v_bar
u_nl = np.clip(
    u_bar + Kp * (r_amp - y_nl) - Kp * Td * z_nl,
    0.0,
    1.0,
)

# Diagrama de blocos com derivada aplicada à medição
# Estrutura: proporcional no erro e derivada filtrada somente na saída medida.
fig, ax = plt.subplots(figsize=(14.5, 5.7))
ax.set_xlim(0, 16)
ax.set_ylim(0, 6.5)
ax.axis("off")

# Blocos do caminho direto
blocks = [
    (3.55, 4.05, 1.45, 0.95, r"$K_p$"),
    (7.25, 4.05, 1.85, 0.95, "Atuador\nideal"),
    (10.25, 4.05, 1.95, 0.95, r"$G(s)$"),
    # Blocos da medição e do caminho derivativo. A entrada do derivativo é a medida.
    (11.20, 1.90, 1.75, 0.80, r"$H(s)=1$"),
    (7.35, 0.60, 2.10, 0.95, r"$K_p\dfrac{T_d s}{T_f s+1}$"),
]
for x, y, w, h, label in blocks:
    ax.add_patch(Rectangle((x, y), w, h, fill=False, linewidth=1.5))
    ax.text(x + w/2, y + h/2, label, ha="center", va="center", fontsize=11)

# Somadores
sum1 = (2.45, 4.525)
sum2 = (6.35, 4.525)
for x, y in [sum1, sum2]:
    ax.add_patch(Circle((x, y), 0.28, fill=False, linewidth=1.5))
# Somador 1: r - y_m
ax.text(sum1[0], sum1[1] + 0.14, "+", ha="center", va="center", fontsize=13)
ax.text(sum1[0], sum1[1] - 0.14, "−", ha="center", va="center", fontsize=13)
# Somador 2: Kp e - termo derivativo
ax.text(sum2[0] - 0.12, sum2[1], "+", ha="center", va="center", fontsize=13)
ax.text(sum2[0] + 0.12, sum2[1] - 0.17, "−", ha="center", va="center", fontsize=13)

arrowprops = dict(arrowstyle="->", linewidth=1.4)
# Caminho direto
ax.annotate("", xy=(2.16, 4.525), xytext=(0.55, 4.525), arrowprops=arrowprops)
ax.annotate("", xy=(3.55, 4.525), xytext=(2.74, 4.525), arrowprops=arrowprops)
ax.annotate("", xy=(6.07, 4.525), xytext=(5.00, 4.525), arrowprops=arrowprops)
ax.annotate("", xy=(7.25, 4.525), xytext=(6.63, 4.525), arrowprops=arrowprops)
ax.annotate("", xy=(10.25, 4.525), xytext=(9.10, 4.525), arrowprops=arrowprops)
ax.annotate("", xy=(15.25, 4.525), xytext=(12.20, 4.525), arrowprops=arrowprops)

# Medição: saída da planta -> H(s) -> caminho de retorno para o primeiro somador.
# A seta vertical entra em H(s); a seta horizontal aponta para a esquerda, indicando a realimentação.
ax.annotate("", xy=(12.075, 2.70), xytext=(12.075, 4.525), arrowprops=arrowprops)
ax.annotate("", xy=(2.45, 2.30), xytext=(11.20, 2.30), arrowprops=arrowprops)
ax.annotate("", xy=(2.45, 4.245), xytext=(2.45, 2.30), arrowprops=arrowprops)

# Ramo derivativo: a entrada é a medida y_m e o sinal é subtraído no segundo somador.
# A seta entra pela direita do bloco derivativo; sua saída segue para o somador 2.
ax.annotate("", xy=(9.45, 1.075), xytext=(9.45, 2.30), arrowprops=arrowprops)
ax.annotate("", xy=(6.35, 1.075), xytext=(7.35, 1.075), arrowprops=arrowprops)
ax.annotate("", xy=(6.35, 4.245), xytext=(6.35, 1.075), arrowprops=arrowprops)

# Rótulos dos sinais
ax.text(0.55, 4.95, r"$r(t)=\Delta v_{\mathrm{ref}}(t)$ [V]", fontsize=10)
ax.text(2.93, 4.95, r"$e(t)$ [V]", fontsize=10)
ax.text(5.00, 4.95, r"$K_p e(t)$", fontsize=10)
ax.text(6.70, 4.95, r"$\Delta u(t)$", fontsize=10)
ax.text(9.15, 4.95, r"$u(t)=\bar u+\Delta u(t)$", fontsize=10)
ax.text(12.35, 4.95, r"$\Delta v_C(t)$ [V]", fontsize=10)
ax.text(9.55, 2.47, r"medida $\Delta v_C(t)$", fontsize=9, ha="center")
ax.text(7.85, 1.85, "ação derivativa\nna medição", fontsize=9, ha="center")
ax.set_title("Diagrama de Blocos da Malha Fechada com Derivada na Medição")
fig.savefig(out / "diagrama_malha_fechada.pdf", bbox_inches="tight")
fig.savefig(out / "diagrama_malha_fechada.png", dpi=240, bbox_inches="tight")
plt.close(fig)

# Root locus
k_grid = np.concatenate([np.linspace(0.0, 0.02, 350), np.linspace(0.02, 0.443, 900)])
branches = root_locus_branches(k_grid)
zeros_loop = np.roots(np.polymul([Tlead, 1.0], num_G))
poles_loop = np.roots(np.polymul([Tf, 1.0], den_G))

fig, ax = plt.subplots(figsize=(10, 6.2))
for branch in branches:
    ax.plot(branch.real, branch.imag, linewidth=1.2)

ax.scatter(poles_loop.real, poles_loop.imag, marker="x", s=115, linewidths=2, label="Polos de malha aberta")
ax.scatter(zeros_loop.real, zeros_loop.imag, marker="o", s=85, label="Zeros de malha aberta")
ax.scatter(poles_cl.real, poles_cl.imag, marker="*", s=150, label=rf"Polos escolhidos ($K={Kp:.2f}$)")

sigma = np.linspace(0.0, 5000.0, 200)
tan_theta = np.tan(np.arccos(0.707))
ax.plot(-sigma, sigma * tan_theta, linestyle="--", linewidth=1.0)
ax.plot(-sigma, -sigma * tan_theta, linestyle="--", linewidth=1.0)
ax.text(-2500, 2050, r"$\zeta=0{,}707$", fontsize=10)

ax.axhline(0, linewidth=0.8)
ax.axvline(0, linewidth=0.8)
ax.set_xlim(-9000, 5000)
ax.set_ylim(-3500, 3500)
ax.set_xlabel("Parte real [rad/s]")
ax.set_ylabel("Parte imaginária [rad/s]")
ax.set_title("Root Locus do Compensador PD Filtrado")
ax.grid(True)
ax.legend(loc="upper right")
fig.savefig(out / "root_locus_pd_filtrado.pdf", bbox_inches="tight")
fig.savefig(out / "root_locus_pd_filtrado.png", dpi=240, bbox_inches="tight")
plt.close(fig)

# Comparação aberta x fechada
_, y_cl_long = signal.step(sys_cl, T=t_open)

fig, ax = plt.subplots(figsize=(10, 5.8))
ax.plot(t_open, v_bar + y_open, label=r"Malha aberta: $\Delta u=0{,}025$")
ax.plot(t_open, v_bar + y_cl_long, label=r"Malha fechada linear: $r=2{,}4$ V")
ax.axhline(v_bar + r_amp, linestyle="--", label=r"Referência: $50{,}4$ V")
ax.set_xlabel("Tempo [s]")
ax.set_ylabel(r"Tensão de saída $v_C$ [V]")
ax.set_title("Comparação entre Malha Aberta e Malha Fechada")
ax.grid(True)
ax.legend()
fig.savefig(out / "comparacao_malha_aberta_fechada.pdf", bbox_inches="tight")
fig.savefig(out / "comparacao_malha_aberta_fechada.png", dpi=240, bbox_inches="tight")
plt.close(fig)

# Validação linear x não linear
fig, ax = plt.subplots(figsize=(10, 5.8))
ax.plot(t_cl, v_bar + y_cl, label="Modelo linear em malha fechada")
ax.plot(t_cl, v_nl, label="Modelo não linear em malha fechada")
ax.axhline(v_bar + r_amp, linestyle="--", label=r"Referência: $50{,}4$ V")
ax.set_xlabel("Tempo [s]")
ax.set_ylabel(r"Tensão de saída $v_C$ [V]")
ax.set_title("Validação do Controlador: Modelo Linear versus Não Linear")
ax.grid(True)
ax.legend()
fig.savefig(out / "validacao_linear_nao_linear.pdf", bbox_inches="tight")
fig.savefig(out / "validacao_linear_nao_linear.png", dpi=240, bbox_inches="tight")
plt.close(fig)

# Duty cycle
fig, ax = plt.subplots(figsize=(10, 5.8))
ax.plot(t_cl, u_nl, label=r"$u(t)$")
ax.axhline(0.0, linestyle="--", label="Limite inferior")
ax.axhline(1.0, linestyle="--", label="Limite superior")
ax.set_xlabel("Tempo [s]")
ax.set_ylabel("Duty cycle")
ax.set_title("Sinal de Controle no Modelo Não Linear")
ax.grid(True)
ax.legend()
fig.savefig(out / "duty_cycle_malha_fechada.pdf", bbox_inches="tight")
fig.savefig(out / "duty_cycle_malha_fechada.png", dpi=240, bbox_inches="tight")
plt.close(fig)

print("Polos de malha fechada:", poles_cl)
print("Amortecimento dominante:", zeta_cl)
print("Erro estacionário relativo:", ess)
print("Arquivos gerados em:", out.resolve())
