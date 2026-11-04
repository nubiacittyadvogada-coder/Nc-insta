# Padrão de edição "cinema" (aprovado pela Núbia em 04/11/2026)

1. Recorte da pessoa (modelo selfie_multiclass_256x256 do MediaPipe, rodado com ai-edge-litert):
   `python3 recorte_fundo.py VIDEO INICIO DURACAO selfie_multiclass_256x256.tflite mascara.mp4`
   Modelo: https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite (não versionar).
2. Animações: `node render_overlay.js overlay-editorial.html PASTA_FRAMES "#fume"` (150 PNGs a 30 fps). Variante "#claro" para fundo escuro. Padrão: fumê.
3. Composição (ffmpeg):
   - Cor A: `format=rgb24,colorbalance=rs=0.015:bs=-0.02:rm=0.025:bm=-0.025:rh=0.01:bh=-0.01,eq=contrast=1.08:brightness=0.015:saturation=1.04,curves=all='0/0.035 0.5/0.51 1/0.975'`
   - Fundo: `gblur=sigma=11,eq=brightness=-0.03:saturation=0.85` e `maskedmerge` com a máscara (tudo em gbrp).
   - Acabamento: brilho leve (screen 8% de um gblur 24), `vignette=PI/4.6`, `noise=alls=5:allf=t`.
   - Cartão de vidro: recorte da área, `gblur=sigma=30`, máscara arredondada (raio 44), entra com fade e sobe 60 px.
4. Tipografia: Archivo 700 (palavra grande, letter-spacing -11px), Bodoni Moda itálico 400 sobreposto, Archivo 600 em maiúsculas espaçadas (.42em) como subtítulo. Entrada letra a letra saindo do desfoque.
5. Regras: nunca número, resultado ou depoimento que não seja real; texto fora do rosto (terço de cima ou de baixo).

## Biblioteca de modelos (biblioteca-modelos.html)
`node render_frames.js biblioteca-modelos.html PASTA_FRAMES QTD_FRAMES` (30 fps). Cada modelo tem uma janela de tempo em `setT(s)`; troque textos e tempos por vídeo.
1. Ficha da série: aba vinho "DIA 01 / 07", título com itálico Bodoni, linha do tempo de pontos e placar real.
2. Contador: etiqueta + número em Bodoni itálico contando, com grifo vinho passando por baixo.
3. Etiquetas numeradas 01, 02, 03 (fumê), entrando uma a uma no lado direito.
4. Tipografia empilhada: palavra em caixa preta / itálico / palavra em caixa preta, no terço de cima.
5. Ícone de app que salta com rótulo.
6. Faixa de veredito: barra vinho de ponta a ponta entrando da esquerda, "VEREDITO" e o texto datilografado em Bodoni itálico.
Falta: legenda palavra a palavra (depende de transcrição) e vídeo dentro do vídeo (depende de clipes extras).

## Identidade própria (decisão da Núbia, 04/11/2026)
Referências servem para medir qualidade, nunca para copiar. Proibido: carimbo inclinado verde e creme, fileira de miniaturas de episódios, cartão de número com linha de gráfico, palavra solta flutuando ao lado do rosto. Assinatura nossa: vinho #6B1E2E, off-white #F6F1EA, Bodoni itálico, linguagem de ficha, grifo e sentença.

## Versão NC Advogados (biblioteca-modelos-nc.html)
Mesmos movimentos, cores do NC: preto #111111, off-white #F3F1EE, bege #D8C4B6, apoio #E6DAD1. Modelos: ficha "NC ADVOGADOS" com nome e cargo do advogado (abertura obrigatória), ficha da série com aba "EP 01" e linha do tempo, contador com grifo bege, etiquetas claras numeradas, tipografia empilhada em caixas pretas, faixa preta "ATENÇÃO" com texto datilografado.
Advogado sentado à mesa: somar `mascara-mesa.png` à máscara (blend lighten) para manter a mesa nítida e evitar ruído do recorte.

## Absorvido das edições da Núbia (04/11/2026)
1. Legenda palavra a palavra em blocos de 1 a 3 palavras, no centro, na altura do peito, com degradê escuro embaixo para leitura. Mantemos o grifo vinho só nas palavras-chave.
2. Zoom de corte a cada 3 a 5 segundos (100%, 115%, 130%), alternando plano aberto e fechado, inclusive close extremo no gancho.
3. Gancho visual com objeto ou ação no primeiro segundo (ex.: o celular tocando).
4. Imagens de apoio ilustrando a frase (pessoa ao telefone em pânico, mãos digitando, audiência), de 1 a 2 segundos.
5. Transição por desfoque e flash branco curto. Fora: transição de grade ou glitch, que briga com a identidade premium.
Regras novas: nada de imagem de autoridade ou pessoa real identificável (ministros, juízes, sessões reais) nem banco de imagens sem licença; preferir imagens de apoio gravadas pela equipe (rotina da Karol) ou de banco com licença comercial. Sempre manter, mesmo com esse ritmo: texto do gancho no topo nos 3 primeiros segundos, ficha de nome e cargo, CTA final e @.

## Padrão atualizado 04/11/2026 (vale para o perfil pessoal e para o NC Advogados)
1. Transcrição com Whisper (modelo small, pt) para cortar repetições e tropeços palavra por palavra. Conferir trechos suspeitos ouvindo de novo: o Whisper às vezes "engole" frases repetidas.
2. Zoom de corte por frase (100%, 118%, 100%, 132%) e flash branco curto nas viradas (primeiro, segundo, terceiro).
3. Legenda limpa em blocos de 1 a 3 palavras, sem tarja, com grifo nas palavras-chave (vinho no pessoal, preto com texto bege no NC).
4. Imagens de apoio geradas no Runway (nano-banana-2, 9:16, 7 créditos cada), 1,5 s com zoom lento, no momento da fala. NC: imagens sóbrias, sem algemas, sangue, viatura em ação ou qualquer cena sensacionalista; nunca cliente, pessoa real ou lugar identificável.
5. Velocidade final 1,1x.
6. Gancho no topo nos 3 primeiros segundos, ficha de nome e cargo, CTA final e @.
