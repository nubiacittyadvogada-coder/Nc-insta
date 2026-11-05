# Prompt para o app de MKT: edição automática de vídeo falado

Cole tudo abaixo no projeto do app de MKT. Primeiro peça a análise do código atual e só depois a implementação. Tudo aqui foi testado em vídeos reais da Núbia Citty e do NC Advogados em 04/11/2026 e aprovado por ela depois de 5 rodadas de ajuste.

Implementação de referência (código que roda de verdade): repositório `nubiacittyadvogada-coder/Nc-insta`, ramo `central-nubia-citty`, pasta `tools/edicao/`:
- `setup.sh`: instala Whisper, o modelo de recorte e as dependências
- `recorte_fundo.py`: máscara da pessoa quadro a quadro
- `overlay_min.py`: camada de texto na Estética A (HTML animado)
- `referencia/01_cortes_e_legenda.py`: cortes, zoom e legenda palavra a palavra
- `referencia/02_render_texto.js`: transforma o HTML animado em quadros PNG transparentes
- `referencia/03_composicao_final.py`: cor, fundo desfocado, tela dividida, texto e velocidade
- `README.md`: histórico das decisões

---

## PROMPT

Você vai implementar no app a **edição automática de Reels falados**. A pessoa grava o vídeo bruto e envia, e o app devolve o vídeo editado para aprovação. Antes de escrever código, analise o que já existe no app: upload de vídeo, fila de tarefas, armazenamento, perfis de marca e usuários de teste. Depois me entregue um plano curto e só então implemente. Não quebre o que os usuários de teste já usam.

### 1. Princípio do produto
- **A equipe só grava e envia.** Ela não corta e não edita nada, e o vídeo pode chegar com contagem, erros e várias tentativas. Cortar é trabalho do app.
- **Autenticidade por cliente.** Fontes, cores de destaque, @, nome e cargo, séries e frases vêm do perfil de marca de cada cliente. Nunca use os dados ou o visual de um cliente em outro, nem os valores de exemplo deste documento como padrão de todo mundo.
- **Nada é publicado automaticamente.** O vídeo editado vai para "aprovar".

### 2. Envio do vídeo bruto (o que travou na vida real)
- Não comprima vídeo longo no navegador. A compressão leva o mesmo tempo do vídeo e para se a tela bloquear. Isso travou o envio de um arquivo de 517 MB em 1min36.
- Ofereça como caminho principal o **link do Google Drive** ("Qualquer pessoa com o link"). O Drive sobe em segundo plano. O servidor baixa com `https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t` e, se vier HTML, lê o `uuid` do formulário e repete com `&uuid=`.
- Envio direto só para vídeos curtos (até ~20 MB). Se usar compressão no aparelho, peça Wake Lock (`navigator.wakeLock.request('screen')`) e retome de onde parou.
- O formulário pede: **roteiro (card)**, **quem gravou** (lista da equipe com nome e cargo) e **observação** do que mudou na fala.
- Envio que parou no meio gera aviso automático para a equipe dizendo até onde chegou.

### 3. Pipeline de edição (no servidor, com ffmpeg)
Rode tudo em fila de tarefas no servidor (worker com ffmpeg, Python e Chromium headless). Ordem:

**3.1 Transcrição.** Whisper modelo `small`, idioma `pt`, `word_timestamps=True`. Guarde cada palavra com início e fim.

**3.2 Escolha das tomadas e cortes.**
- Compare a transcrição com o roteiro do card e, quando a fala foi repetida, fique com a **melhor tentativa** de cada frase. Corte contagem, conversa de bastidor, tropeços e pausas maiores que ~0,5s.
- Cuidado: o Whisper às vezes "engole" frases repetidas. Confira a energia do áudio nos trechos suspeitos.
- Comece o vídeo no **primeiro quadro com olhos abertos** antes da primeira palavra (use o silêncio inicial para isso).
- Se faltar parte do roteiro no bruto, avise o que falta em vez de inventar.
- Corrija na legenda os erros de transcrição óbvios (nome da pessoa, nome do escritório, siglas como INSS), sem mudar o que foi dito.

**3.3 Zoom de corte por frase.** Alterne o enquadramento a cada corte: 100%, 118%, 100%, 132%, centrado no rosto. O rosto é detectado no primeiro quadro, ou definido no perfil por tipo de cenário.

**3.4 Recorte da pessoa e fundo desfocado (look de cinema).**
- Máscara quadro a quadro com o modelo `selfie_multiclass_256x256.tflite` (MediaPipe), rodando pelo `ai-edge-litert`. O mediapipe completo exige libEGL e falha em servidor.
- Suavização temporal: `a = 0.55*atual + 0.45*anterior`.
- **Sem contorno claro em volta da pessoa:** dilate a máscara (7 passadas de `dilation`) e depois `gblur=sigma=4`. Fundo com `gblur=sigma=6`. Com sigma 9 aparece um halo, e a Núbia reprovou.
- Pessoa sentada à mesa: some uma máscara fixa da mesa (`blend=all_mode=lighten`) para a mesa não borrar.
- Aplique a máscara no vídeo **antes** dos zooms e corte a máscara com os mesmos zooms, senão ela desalinha.

**3.5 Cor natural (nada de amarelo).** Use exatamente:
```
format=rgb24,colorbalance=rs=0.015:bs=-0.02:rm=0.025:bm=-0.025:rh=0.01:bh=-0.01,eq=contrast=1.08:brightness=0.015:saturation=1.04,curves=all='0/0.035 0.5/0.51 1/0.975',format=gbrp
```
Sem o `format=rgb24` no início o filtro não tem efeito. Fundo: `eq=brightness=-0.03:saturation=0.88` antes do desfoque. Final: `vignette=PI/4.8,noise=alls=4:allf=t`.

**3.6 Imagens de apoio em tela dividida (b-roll).** Veja a seção 4 para a origem das imagens.
- No máximo 3 por vídeo institucional e 4 por vídeo pessoal, cada uma por 1,6s, no momento exato da palavra-chave (pelo tempo da palavra no Whisper).
- Layout: pessoa em cima (1080x960, recorte do rosto), imagem embaixo (1080x960), linha fina de 4px na cor da marca na divisa e etiqueta pequena com a ação da cena ("TRABALHO RURAL", "NA DELEGACIA").
- Imagem parada vira vídeo com zoom lento: `scale=1080:1920,scale=1188:2112,zoompan=z='1+0.0012*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=48:s=1080x1920:fps=30`. Escolha o recorte vertical de cada imagem para o assunto principal ficar na metade visível.
- Durante a tela dividida, a legenda sobe para y=760 e o nome não aparece.

**3.7 Camada de texto (Estética A, seção 5).** Escreva uma página HTML com `setT(segundos)`, gere um PNG transparente por quadro (30 fps) com Playwright e sobreponha com `overlay`.

**3.8 Velocidade e exportação.** `setpts=PTS/1.1` e `atempo=1.1`, áudio com `loudnorm=I=-15:TP=-1.5:LRA=11`, H.264 com CRF 23 a 25, `+faststart`, 1080x1920, abaixo de 20 MiB.

**3.9 Conferência automática antes de entregar.** Extraia quadros nos pontos críticos (0s, gancho, cada tela dividida, cada número de lista, CTA) e confira texto cortado ou sobreposto, rosto coberto e legenda atravessando a divisa. Transcreva o áudio final para garantir que nenhuma repetição ficou.


### 3.1 Duas regras novas (05/11/2026)
- **Nunca picotar a voz.** Cada fala é um trecho contínuo; só sai silêncio real medido por energia (pausa maior que 0,6s, com 0,2s de folga de cada lado). Cortar nos intervalos de palavra do Whisper come sílabas, porque os tempos dele erram de 0,2 a 0,5s.
- **Assinatura da marca no fim.** Se o cliente subir a logo no perfil de marca, todo vídeo daquela marca termina com 1,8s de cartão liso na cor escura da marca e a logo entrando em fade, depois do CTA.

### 4. De onde vêm as imagens de apoio (b-roll)
Ordem de preferência, configurável por cliente:
1. **Imagens da própria equipe** (biblioteca do cliente: escritório, mãos digitando, rotina). São as mais autênticas.
2. **Banco de vídeo com licença comercial gratuita: Pexels API** (`https://api.pexels.com/videos/search?query=...&orientation=portrait`). A chave fica como segredo do servidor, nunca no navegador nem no código. Prefira vídeo real a imagem gerada.
3. **Imagem gerada por IA.** Hoje a Central da Núbia usa o **Runway**, modelo `nano-banana-2` (Gemini 3.1 Flash Image), proporção 9:16, 1K, a **7 créditos por imagem**, chamado pelo conector do Runway. No app, use a API oficial do provedor escolhido (Runway, Google Gemini Image ou outro) com chave de servidor e controle de gasto: limite por vídeo, limite mensal por cliente e parada quando o saldo estiver baixo (a Núbia usa "parar abaixo de 100 créditos").
   - Modelo de prompt: `Close-up of [assunto], soft natural light, shallow depth of field, documentary photography, muted natural colors, no face visible, cinematic, sober`
   - Exemplos que funcionaram: mãos calejadas segurando enxada na lavoura; certidões antigas sobre mesa de madeira (texto ilegível); celular tocando na mesa à noite; fachada genérica de delegacia à noite; martelo de juiz; mãos digitando no celular.

**Regras de imagem (obrigatórias):**
- Nada de pessoa real identificável, cliente, autoridade (ministro, juiz), lugar identificável, placa ou fachada real.
- Nada sensacionalista (algemas, sangue, viatura em ação). No institucional, ainda mais sóbrio.
- Rosto só de costas ou fora de quadro.
- Crianças só de costas e de longe.
- Imagens geradas ficam no banco do cliente para reaproveitar e economizar créditos.

### 5. Estética A (padrão aprovado; valores configuráveis por marca)
- **Regra de ouro: cada texto em UMA família tipográfica só.** Nunca misturar uma sem serifa pesada em maiúsculas com itálico serifado na mesma frase. Foi o que a Núbia chamou de "não combina, não está sofisticado".
- **Títulos** (gancho, CTA, nome, título de lista, frase da série): serifa clássica regular (Bodoni Moda 400), com o destaque no **itálico da mesma família**. Gancho 74px, CTA 62px, nome 46px, número de lista em itálico 120px.
- **Legendas e etiquetas:** sem serifa leve (Archivo 500). Legenda 48px em frase normal (não MAIÚSCULAS), até 6 palavras por vez, quebra na pontuação. A palavra já falada fica em branco e as próximas a 62%. Etiquetas e cargo em 15 a 18px, maiúsculas, espaçamento .3em.
- **Sem caixas, tarjas, cartões ou grifos coloridos.** Texto branco com sombra suave (`0 2px 6px rgba(0,0,0,.35), 0 8px 30px rgba(0,0,0,.35)`) e degradê escuro leve só no rodapé.
- **Uma camada de texto por vez:**
  - 0 a 3s: só o gancho, já visível no quadro 0 (sem fade de entrada), no terço de cima;
  - depois, nome e cargo pequenos no canto inferior esquerdo por ~3s (nome em serifa, linha fina na cor da marca, cargo pequeno);
  - frase da série: em cima, pequena, sem coincidir com o nome;
  - CTA final em duas linhas (frase e destaque em itálico) com o @ pequeno embaixo, sem legenda ao mesmo tempo.
- **Listas** ("primeiro, segundo, terceiro"): número grande em itálico, rótulo pequeno espaçado e título curto no topo, barra de progresso de 3 traços finos e flash branco a 30% na virada.
- **Cores de destaque por marca:** no exemplo, rosa claro #F0C3CC e linha #8E2A3E no perfil pessoal; bege #E3D2C3 e linha #D8C4B6 no institucional. São só exemplos: cada cliente tem as suas.
- **Animações:** entrada com ease-out cúbico de 0,5s, subida de 14 a 18px e saída de 0,4s. Nada de pulos, giros ou emojis.
- **Identidade própria:** não copiar formatos de referências (selo verde inclinado, tira de miniaturas de episódio, cartão de número com linha de gráfico, palavra solta flutuando ao lado do rosto).

### 6. Estrutura de episódio de série (o roteiro já vem assim)
Gancho forte (0 a 3s), frase fixa da série (igual em todos os episódios), desenvolvimento que ensina algo e CTA. Se a pessoa não falou a frase da série, ela entra só como texto na tela e o app avisa para falar nas próximas gravações.

### 7. Regras jurídicas e de marca (advocacia)
- OAB (Provimento 205/2021): sem captação, sem promessa de resultado, sem preço de serviço jurídico, sem caso ou depoimento de cliente.
- Notícia de crime: "suspeito", sem nome e sem foto, com a fonte citada. Nunca acusar ou condenar suspeito, nunca minimizar violência.
- Nome e cargo exatamente como o cliente cadastrou. Não invente área de atuação (se a pessoa disser no vídeo uma área diferente do tema, avise).
- Música só da biblioteca da plataforma, adicionada na hora de postar.
- Nunca invente número, resultado ou depoimento.

### 8. Entrega ao usuário
- Vídeo editado no card com status "aprovar" e mensagem automática para a equipe dizendo o que foi feito (cortes, imagens usadas e de onde vieram) e o que conferir.
- Botão "pedir ajuste" com campo livre. O ajuste reaproveita transcrição, máscara e imagens já geradas, sem gastar créditos de novo.
- Registro de custo por vídeo (créditos de imagem e minutos de processamento).

### 9. Critérios de aceite
- Bruto de 70s com duas tentativas da mesma fala vira um vídeo de 40 a 50s sem nenhuma repetição (confirmado pela transcrição do resultado).
- Sem contorno claro em volta da pessoa e primeiro quadro de olhos abertos.
- Nenhum quadro com mais de uma camada de texto além da legenda. Nenhum texto atravessando a divisa da tela dividida.
- Só as duas famílias de fonte da marca, sem caixas.
- Arquivo abaixo de 20 MiB, 1080x1920, 30 fps, 1,1x.
- Funciona para dois clientes diferentes com marcas diferentes, sem nenhum vazamento de nome, cor, @ ou imagem de um para o outro.
