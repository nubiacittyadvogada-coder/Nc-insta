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
- ERRO REAL de 05/11 (áudio mudo no fim de cada trecho): nunca usar `-ss` duplo (antes e depois do -i) com `afade=...:st=`; o st conta no tempo original e emudece os últimos segundos. Use só `-ss INICIO -i bruto -t DURACAO`, ou `asetpts=PTS-STARTPTS` antes do afade.
- Conferência obrigatória do arquivo FINAL antes de subir: `ffmpeg -i final.mp4 -af silencedetect=n=-45dB:d=0.9 -f null -` (o único silêncio longo permitido é o cartão da logo) e transcrição do arquivo final inteiro, conferida contra o roteiro.

## Fim e começo de cada bloco (05/11/2026, Núbia: "cada final de bloco ela olhando pro lado, ou terminando o outro")
- O FIM de cada trecho é o fim real da voz da última palavra (energia do áudio caindo e ficando baixa por 0,12s), mais 0,06s. Nada de folga longa: logo depois de falar a pessoa olha para o lado, para o teleprompter, ou já começa a próxima tentativa.
- O COMEÇO é o começo real da voz da primeira palavra, menos 0,04s. Nunca pegar o fim da tentativa anterior.
- Os tempos do Whisper servem só para achar a palavra; o ponto do corte vem da energia do áudio.
- Conferência visual obrigatória: tirar quadro do começo e dos últimos 0,45s / 0,2s / 0,03s de cada trecho e olhar. Se a pessoa estiver olhando para fora da câmera, de olho fechado ou começando outra fala, puxar o corte para antes.

## Recursos visuais: decididos vídeo a vídeo (05/11/2026, Núbia: "não há regra fixa; não precisa sempre ter b-roll")
- NÃO existe cota nem fórmula: nem b-roll obrigatório, nem número fixo de animações. Para cada vídeo, leia o roteiro e pergunte em cada trecho: o que ajuda a pessoa a entender ou lembrar ESTA fala? A resposta pode ser uma animação atrás da pessoa, um gráfico, um número, uma imagem que explica, um zoom, ou nada (só a pessoa falando, quando a fala se sustenta sozinha).
- B-roll só quando a imagem explica a fala (ex.: capacete e luvas para "atividade insalubre"). Imagem genérica (livro, cadeira vazia) é proibida: tira força.
- Animação atrás da pessoa (camada entre o fundo desfocado e a pessoa recortada) é UMA das ferramentas. Exemplo no vídeo da Lívia: "LEI 15.240 · OUTUBRO DE 2025"; "amar" riscado e depois "cuidar · É DEVER"; "ausência + dano · PRECISA DOS DOIS". Modelo: `atras-da-pessoa.html` + `render_atras.js` (sobrepor os quadros no fundo desfocado ANTES do maskedmerge). O texto e o desenho de cada animação são criados para aquele vídeo, não copiados.
- Sempre que houver texto atrás: lado livre do quadro, medindo a máscara na janela inteira do evento; a palavra-chave nunca pode ficar escondida atrás da cabeça (se a pessoa se inclinar, ajuste o tempo ou a posição).
- Uma camada por vez: durante uma animação, some a legenda, a ficha e o número do ponto.
- Na mensagem de entrega, diga em uma linha quais recursos usou e por quê.

## Abertura de série e legenda desde o início (06/11/2026, pedido da Núbia)
- Vídeo de série abre com animação: "EPISÓDIO N" (Archivo, caixa alta, pequeno) e o nome da série em Bodoni com itálico, revelado com elegância nos primeiros 2,5 a 3s, depois some. Ela ocupa o lugar do título grande do gancho no topo (uma camada no topo por vez). Pode ficar atrás da pessoa se o topo estiver livre, sem a cabeça cobrir as palavras.
- LEGENDA DESDE O PRIMEIRO SEGUNDO, inclusive durante o gancho. (Substitui a regra antiga "sem legenda no gancho".) No CTA final a legenda continua opcional.

## ERRO REAL: áudio fora de sincronia no premium (06/11/2026)

O `atempo=1.1` dentro do mesmo filter_complex do vídeo deixou o áudio até 3 s atrasado em todos os premium. O fx_comp.py agora renderiza o vídeo sem áudio, acelera o áudio à parte e junta com `-shortest`. Conferência obrigatória antes de entregar: duração do stream de vídeo e de áudio iguais (diferença menor que 0,15 s) e um quadro de legenda no meio e no fim batendo com a fala.

## Qual padrão usar (decisão da Núbia, 06/11/2026)

- **Perfil pessoal (@nubiacitty, Instagram e TikTok): PADRÃO PREMIUM** (seção abaixo).
- **NC Advogados: PADRÃO RÁPIDO NC.** Meta: pronto em 10 a 15 minutos depois de baixar o bruto. Nada de Runway, de motor de efeitos nem de fx_comp.
  1. Mesmos cortes de sempre (fala contínua, energia, +0,06 s no fim, -0,04 s no começo, um -ss por segmento, 1,1x).
  2. **Zoom e troca de enquadramento** para dar ritmo sem efeito pesado: alterne a cada fala entre plano aberto (escala 1,0) e plano fechado (escala 1,15 a 1,25, centrado no rosto pela máscara ou pelo terço superior). Dentro de uma fala longa, zoom lento de 1,0 para 1,08. Na palavra mais forte do bloco, punch-in seco de 1,0 para 1,2 por 0,4 s. Nunca cortar a cabeça nem o microfone de lapela.
  3. Gancho animado nos 3 primeiros segundos, ficha de nome e cargo (sem inventar área nem sobrenome), frase da série na tela quando dita.
  4. Legenda desde o primeiro segundo (overlay_min.py modo A), revisada palavra por palavra.
  5. No máximo 2 ou 3 palavras-chave animadas (etiqueta ou texto atrás), só nos conceitos centrais.
  6. Cor natural, fundo levemente desfocado. Logo no fim com endcard.py. Qualidade: CRF 18, até 8 Mbps, cor BT.709 (regra de 10/11/2026; o limite antigo de 20 MiB foi abolido porque borrava o vídeo).
  7. Mesma conferência final: quadros nos cortes e nos zooms, silencedetect, transcrição contra o roteiro.

## PADRÃO PREMIUM DE EDIÇÃO (06/11/2026, aprovado pela Núbia: "adorei")
Edição simples demais foi reprovada ("básica, sem imagens junto da fala, sem animação, sem diferencial"). A partir de agora todo vídeo usa o motor de efeitos:
- `efeitos/fx_engine.html` + um `fx.js` por vídeo (exemplos em `efeitos/exemplos/`). Tipos: `cover` (capa de revista atrás da cabeça), `img` (imagem da fala ATRÁS da pessoa, com zoom lento e flash na entrada), `text` (título atrás, com subtítulo que entra no tempo da fala), `strike` (palavra riscada e a correção), `comments` (comentários surgindo e sendo riscados), `compare` (quadro com ✓ marcando), `counter` (relógio/contador), `list` (lista numerada entrando item a item), `tag` (etiqueta).
- Render: `node efeitos/render_camadas.js fx.html bg|fg pasta N` e composição `python3 efeitos/fx_comp.py PASTA saida.mp4 [--paper a,b] [--clip arquivo,inicio,ycorte,duracao]` (recorte de papel e cena de referência em tela dividida).
- Ritmo: algo muda na tela a cada 3 a 5 segundos. Imagem junto da fala sempre que a fala descreve uma cena (geradas no Runway, sóbrias, sem rosto real, placa borrada). Palavra-chave animada no momento em que é dita.
- Legenda o vídeo inteiro (Estética A, overlay_min.py), elegância mantida: Bodoni + Archivo, sem emoji, uma coisa por vez no topo.
- Trechos sensíveis (violência, criança, caso real do escritório): sem efeito lúdico, só etiqueta discreta e texto sóbrio.
- Cena de novela/série: só se a Núbia autorizar (decisão dela sobre direito autoral), som mudo, crédito na tela.
- Gravação de CORPO INTEIRO (cabeça perto do topo): textos de destaque vão na camada da frente, na parte de baixo (top ~1460, abaixo da legenda), com `layer:'fg'` e `band:true` (faixa escura para ler sobre roupa clara). Medir a máscara antes: se a cabeça começa acima de y=400, não usar texto atrás no topo. Exemplo: `efeitos/exemplos/fx-261-corpo-inteiro.js`.

## Revisão de legenda obrigatória (06/11/2026, Núbia: "Ressocialização está errado")
O Whisper erra palavra jurídica e nome. Antes de renderizar, leia a legenda inteira (ov.json) como revisor e corrija com `fix`/`seq`. Erros já vistos: Restrocialização → Ressocialização; remissão → remição (pena); Enseja/ENCEJA → ENCCEJA; compreendo pena → cumprindo pena; e -mail → e-mail; sexta -feira → sexta-feira; aplaudi → aplaude; Donik/dono → Donny; "o índio" → "alguém"; nomes de série e personagens. Na dúvida sobre o que a pessoa disse, transcreva o trecho de novo com `initial_prompt` contendo o roteiro e ouça antes de escrever.

## Rosto livre e expressão boa nos cortes (07/11/2026, regra da Núbia)
ERRO REAL: no vídeo da Lívia (pensão) entrou um pedaço de 0,28 s sem palavra (estalo de boca) com ela de língua de fora, logo depois do gancho.
Regras:
1. Nenhum elemento tampa o rosto (efeitos/zona_segura.py + encaixe automático do motor; no padrão rápido NC, posicionar longe do rosto).
2. Pedaço de corte com menos de 0,5 s sai sempre (é ruído de boca ou respiração). O mk.py já faz isso.
3. FOLHA DE ROSTOS obrigatória antes de subir: `python3 folha_rostos.py final.mp4 segs.json folha.jpg` e OLHAR a imagem.
   Reprova: língua de fora, olho fechado no começo ou fim de trecho, boca torta, careta, rosto cortado.
   Correção: mover a borda 2 a 4 quadros para o quadro bom mais próximo dentro do silêncio; se a careta é no meio da fala, usar outra tentativa do bruto.
   O detector automático de expressão não é confiável (óculos e olhar para baixo enganam): a revisão é visual.
4. Escolher a tentativa de cada fala também pelo rosto, não só pelo áudio: entre duas tentativas boas, fica a de expressão mais natural.

## Vídeos de audiência e júri (09/11/2026, decisão da Núbia)
- Não desfocar rostos: só o réu, se aparecer. Policiais e demais presentes ficam como estão; o fundo pode ficar levemente desfocado.
- Estrutura: gancho forte primeiro (a frase mais forte do trecho, mesmo fora de ordem) e depois a explicação real. Alvo de 25 a 35 s.
- Sem "Citty sendo Citty" nem selo (caso real), sem nomes, sem detalhe do caso, sem veredito.

## Qualidade e cor do NC (10/11/2026)
- Cor sempre marcada como BT.709 (colorspace, primaries, trc, range tv) em todas as etapas; sem marcação o Instagram e o iPhone mostram a cor errada.
- Intermediários quase sem perda (CRF 10); só a etapa final comprime.
- Final com CRF 18 e teto de 8 Mbps (endcard.py). O limite antigo de 3,4 Mbps borrava a imagem.
- Bruto da equipe só pelo Google Drive, nunca pelo WhatsApp (o WhatsApp recomprime).
- 10/11/2026: o limite "arquivo final abaixo de 20 MiB" está ABOLIDO em todos os padrões (NC e pessoal). Ele forçava 1,2 a 3,4 Mbps e era a causa do vídeo ruim. Para caber na Central, vídeo publicado há mais de 7 dias sai da Central e fica no repositório (decisão da Núbia, 10/11).
