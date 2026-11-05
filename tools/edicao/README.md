# Padrão de edição "cinema" (aprovado pela Núbia em 04/11/2026)

**Antes de editar numa sessão nova: rode `bash tools/edicao/setup.sh`** (instala Whisper e o recorte e baixa o modelo).

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

## Estética v2 (aprovada em 04/11/2026, perfil pessoal e NC)
- Legenda editorial: Archivo 700 em maiúsculas, 82px, letter-spacing -3px, a palavra falada em branco e as seguintes a 55%; expressão-chave em Bodoni itálico 600 dentro do grifo (vinho no pessoal; preto com texto bege no NC). Degradê escuro na metade de baixo.
- Listas (primeiro, segundo, terceiro): número grande em Bodoni itálico ("01") no topo, rótulo pequeno espaçado e título curto, com barra de progresso de 3 traços que acende a cada ponto.
- Imagens de apoio em tela dividida: pessoa em cima (960px), imagem embaixo (960px), linha fina na cor da marca entre as duas, etiqueta com a ação da cena, legenda na divisa.

## Ficha de nome (04/11/2026)
Nome sempre em UMA fonte só (Archivo 700, 58px), nunca misturando com itálico. Cargo embaixo em Archivo 600 espaçado (.28em). Cartão off-white com barra lateral na cor da marca (vinho no pessoal, preto no NC). Modelo: ficha-nome.html.

## Ajustes de 04/11/2026 (Núbia achou feio na v2, valem para tudo)
1. Sem contorno claro em volta da pessoa: máscara dilatada (dilation x7 + gblur 4) e fundo com gblur sigma 6, não 9.
2. Primeiro quadro com olhos abertos: começar o corte no primeiro quadro de olho aberto antes da primeira palavra (conferir o silêncio no áudio).
3. Gancho visível já no quadro 0, sem entrar com fade.
4. Sem legenda enquanto o gancho está na tela (texto repetido duas vezes fica amador).
5. Ficha de nome discreta: cartão escuro translúcido (#111 a 82%), nome 46px claro, cargo 19px bege, barra fina bege, sem sombra.
6. CTA final no estilo do gancho (caixa escura + itálico no grifo claro + @ pequeno embaixo), sobre a mesa/parte escura, e sem legenda ao mesmo tempo.
7. Grifo da palavra-chave sempre sólido; antes de ser falada, só o texto fica apagado.

## Estética enxuta v4 (04/11/2026, em teste: Núbia achou a v2/v3 com informação demais, grande e pesada)
Modelo: overlay_min.py (configs a, b, jr como exemplo). Regras:
1. Uma camada de texto por vez: gancho sozinho até 3s, ficha de nome depois (nunca sobre imagem de apoio), legenda some no gancho e no CTA.
2. Sem caixas nem tarjas. Texto branco com sombra suave; destaque só com Bodoni itálico na cor de acento (rosa claro #F0C3CC no pessoal, bege #E3D2C3 no NC).
3. Tamanhos: gancho 62px em frase normal (não maiúsculas), legenda Archivo 600 54px em frase normal, nome 40px, cargo 16px espaçado, número de lista 130px.
4. Linha divisória da tela dividida com 4px, etiqueta 18px sem fundo. Flash a 30%.
5. CTA em duas linhas (frase + itálico) e @ pequeno embaixo.

## PADRÃO OFICIAL: Estética A (aprovada pela Núbia em 04/11/2026, vale para pessoal e NC)
Gerar com `python3 overlay_min.py <config> A`. Substitui a Estética v2 e os ajustes anteriores de tipografia.
- Cada texto em UMA família só. Nunca misturar sem serifa pesada com itálico serifado na mesma frase.
- Títulos (gancho, CTA, nome, título de lista, frase da série): Bodoni Moda 400, com o itálico da MESMA família no destaque. Gancho 74px, CTA 62px, nome 46px.
- Legendas e etiquetas: Archivo 500 (legenda 48px em frase normal; etiquetas 15 a 18px em maiúsculas espaçadas).
- Sem caixas, tarjas ou grifos coloridos. Texto branco com sombra suave.
- Uma camada por vez: gancho sozinho até 3s, nome depois (nunca sobre imagem de apoio), sem legenda no gancho e no CTA.

## Cortes sem picotar a voz (05/11/2026, Núbia: "a voz do Daniel ficou cortada")
- Cada fala é UM trecho contínuo, do começo da primeira palavra ao fim da última. Nunca cortar nos intervalos entre palavras do Whisper: os tempos dele erram 0,2 a 0,5s e o corte come sílaba.
- Só sai silêncio real, medido pela energia do áudio: pausa maior que 0,6s, deixando 0,2s antes e depois.
- Cortar segmento por segmento (ffmpeg com -ss por trecho e concat). Um filter_complex único com muitos trims estoura a memória.
- Conferência: o Whisper costuma "engolir" o fim de frase em arquivo longo. Para checar, transcreva cada trecho separado; se a frase aparece inteira no trecho, ela está no vídeo.

## Assinatura com a logo do NC (05/11/2026, pedido da Núbia)
- TODO vídeo do NC Advogados termina com 1,8s de cartão escuro liso (#0F0D0C) e a logo completa branca entrando em fade, depois do CTA.
- Comando: `python3 tools/edicao/endcard.py editado.mp4 final.mp4`. Logos em `tools/edicao/marca/` (completa e monograma, brancas com transparência).
