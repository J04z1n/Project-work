# Resultados — Membro 3

## Parâmetros e ponto de operação

- SID: 568274
- `delta`: 0,0407450186
- \(L_0 = 0{,}006244470\,\text{H}\)
- \(C = 0{,}001040745\,\text{F}\)
- \(R = 104{,}074502\,\Omega\)
- \(\bar u = 0{,}5\)
- \(\bar i_L = 0{,}922416\,\text{A}\)
- \(\bar v_C = 48\,\text{V}\)

## Comparação entre os modelos

| Degrau relativo em \(\bar u\) | \(\Delta u\) | Duty após o degrau | RMSE | Erro máximo | Faixa de \(i_L\) no modelo não linear |
|---:|---:|---:|---:|---:|---:|
| 1% | 0,00500 | 0,50500 | 0,027002 V | 0,078589 V | 0,763404 a 1,133017 A |
| 2,5% | 0,01250 | 0,51250 | 0,154039 V | 0,476046 V | 0,520484 a 1,458521 A |
| 5% | 0,02500 | 0,52500 | 0,491357 V | 1,747249 V | 0,102241 a 2,029230 A |

## Conclusão sugerida

Para a perturbação de 1%, o modelo linearizado praticamente coincide com o modelo não linear. Em 2,5%, a diferença permanece pequena, mas já é perceptível. Para 5%, o erro aumenta de forma clara, embora ambos os modelos mantenham a mesma tendência dinâmica. Portanto, o modelo linearizado é mais confiável para pequenas perturbações em torno de \(\bar u=0{,}5\), como esperado de uma aproximação por Taylor de primeira ordem.

O caso de 10% foi removido dos gráficos principais porque pode levar a corrente do indutor a valores negativos no modelo médio, afastando a simulação de uma região fisicamente realista de operação.
