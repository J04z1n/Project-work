# Membro 3 — Simulações linear × não linear

Este pacote contém **somente** a implementação e as simulações que cabem ao membro 3:

- modelo médio não linear do conversor boost;
- modelo linearizado numérico em variáveis de desvio;
- comparação em malha aberta para degraus de 1%, 2,5% e 5% em torno de `u_bar = 0.5`;
- geração de gráficos e cálculo de RMSE/erro máximo.

Ele **não** contém função de transferência, polos, zeros, Root Locus, projeto de controlador ou malha fechada, pois essas partes são dos membros 4 e 5.

## Instalação

```bash
python -m pip install -r requirements.txt
```

## Execução

```bash
python simulacoes_membro3.py
```

Os gráficos serão salvos em `resultados/`.

## Convenção importante

O modelo não linear usa valores absolutos:

```text
u(t) = u_bar + Delta_u(t)
x(0) = x_bar
```

O modelo linearizado usa variáveis de desvio:

```text
Delta_x(0) = 0
Delta_x_dot = A Delta_x + B Delta_u
Delta_y = C Delta_x + D Delta_u
```

Para a comparação correta com a tensão não linear, o código reconstrói a tensão absoluta linear:

```text
y_linear(t) = y_bar + Delta_y(t)
```

## Casos simulados

O código usa os seguintes degraus relativos ao ponto de operação \(\bar u=0{,}5\):

| Variação relativa | \(\Delta u\) | Duty cycle após o degrau |
|---:|---:|---:|
| 1% | 0,005 | 0,505 |
| 2,5% | 0,0125 | 0,5125 |
| 5% | 0,025 | 0,525 |

O caso de 10% foi removido dos gráficos principais porque afasta excessivamente o sistema do ponto de operação e pode tornar a corrente do indutor negativa no modelo médio.
