# Catálogo de módulos (07/11/2026)

É a "biblioteca pronta" da Núbia: cada módulo é um bloco reutilizável. Para usar num vídeo, basta escrever uma linha no fx.js dele.
Arquivos: `modulos.js` (os módulos), `fx_engine.html` (motor, já carrega os módulos), `exemplos/fx-demo-modulos.js` (vídeo de demonstração com todos).
Render e composição: iguais aos efeitos antigos (`render_camadas.js` camada fg, depois `fx_comp.py`). Para prévia rápida sem máscara: sobrepor fxfg direto no corte.
Tempos sempre na linha do corte (antes do 1,1x). Identidade: creme, rosé, vinho, fundo escuro, Bodoni + Archivo + Caveat (lousa).

| Módulo | Para que serve | Linha mínima |
|---|---|---|
| `prompt` | caixa de comando sendo digitada (série Criei com IA) | `{type:'prompt',t0,t1,label:'CRIEI COM IA',text:'...',at}` |
| `passos` | lista 1-2-3 que acende e ganha check | `{type:'passos',t0,t1,k:'...',items:[{txt,at}]}` |
| `painel` | metade de cima vira quadro com título e ícone; ela continua embaixo | `{type:'painel',t0,t1,k,ttl,icon:'martelo'}` |
| `lousa` | explicação escrita à mão, com sublinha, circula ou risca | `{type:'lousa',t0,t1,linhas:[{txt,at,marca:'sublinha'}]}` |
| `fluxo` | caminho do processo em caixas e setas; um nível pode dividir em 2 | `{type:'fluxo',t0,t1,k,nos:[{txt,sub,at},{lado:[{txt},{txt,hi:true}],at}]}` |
| `objeto` | ícone ou personagem entrando com mola e flutuando | `{type:'objeto',t0,t1,icon:'algema',x,y,size,label}` |
| `cta` | botão com cursor clicando | `{type:'cta',t0,t1,txt:'Comenta AULA',sub,clickAt}` |
| `conversa` | balões de mensagem entrando | `{type:'conversa',t0,t1,items:[{txt,lado:'e'/'d',at}]}` |
| `lei` | página de código com o trecho que importa sendo grifado | `{type:'lei',t0,t1,lei:'CÓDIGO PENAL',art:'Art. 147-A',txt:'... [[grifo]] ...',pena,marcaAt}` |
| `vertigem` | efeito vertigem (dolly zoom): ela fica igual e o fundo avança | evento `{type:'vertigem',t0,t1}` (só para o som) + `fx_comp.py --vertigem t0,t1,plate.png[,zoom]` |
| `assinatura` | selo "Citty sendo Citty" na ABERTURA (@nubiacitty, todo vídeo) | `{type:'assinatura',t0:TOQUE,t1:2.5,toqueAt:TOQUE}` |
| `som` | som avulso em qualquer ponto | `{type:'som',t0,som:'impacto'}` |

Ícones próprios (sem imagem de terceiros): algema, martelo, balanca, relogio, documento, celular, cadeado, alerta, grade, escudo, dinheiro, ia.
Para um objeto ou personagem novo: gerar imagem sóbria no Runway, remover o fundo, salvar PNG e usar `src:'img/arquivo.png'` no `objeto` ou no `painel`.

## REGRA DE OURO: nada tampa o rosto (Núbia, 07/11/2026)
Antes de renderizar a camada fg, SEMPRE: `python3 zona_segura.py mask.mp4 PASTA/safe.js` (mesma pasta do fx_engine.html e do fx.js).
O motor lê o rosto a cada 0,25 s e encaixa cada elemento acima do rosto (sobe e encolhe) ou abaixo dele; o painel encurta e, se não couber, desce.
Na conferência dos quadros, olhar o rosto durante cada efeito. Se algum elemento encostar no rosto, o vídeo NÃO sobe.
Se o elemento ficar pequeno demais para ler (rosto muito alto no quadro), troque por um módulo menor ou divida o texto em dois momentos.

## Regras de uso (decisão da Núbia: o diferencial vem da edição, sem copiar ninguém)
1. Um "momento de diferencial" por vídeo, no ponto mais importante da fala. No máximo 2 módulos grandes (painel, lousa, fluxo) por vídeo.
2. Escolha pelo conteúdo: explicação de processo = `fluxo`; conceito que o público confunde = `lousa`; lista de direitos ou passos = `passos`; série IA = `prompt`; número ou prazo = `counter` (antigo) ou `objeto` relógio.
3. Alternar entre vídeos: não repetir o mesmo módulo grande dois vídeos seguidos.
4. `conversa` sem print real autorizado sai SEMPRE com o selo SIMULAÇÃO (já é automático). Nunca inventar fala de cliente como se fosse real.
5. Conteúdo jurídico do quadro passa pela mesma checagem do roteiro (nada de promessa de resultado, nada de caso identificável).
6. Perfil pessoal: livre. NC: padrão rápido; no máximo 1 módulo (fluxo ou passos) quando a explicação pedir.

## Sons (07/11/2026)
Biblioteca própria em `sons/` (sintetizada por `sons/gerar_sons.py`, sem direitos de terceiros): whoosh, whoosh_curto, tensao, pop, pop_grave, bolha, clique, tecla0-3, check, giz, marcador, impacto, carimbo, pagina.
Cada módulo já tem o seu som automático (`sfx_cues.js`). Para ativar: `fx_comp.py ... --sfx fx.js` (volume em `--ganho-sfx`, padrão 0.32). `sfx:false` no evento tira o som; `sfx:'impacto'` troca.
Use `{type:'som',t0,som:'impacto'}` na palavra mais forte do vídeo (uma vez só).

## Lei na tela: regra
Texto SEMPRE copiado da fonte oficial (planalto.gov.br), conferido palavra por palavra. Grifar só o trecho que a fala explica. Pena só se a fala citar.

## Vertigem: como fazer
1. Tirar um quadro do corte no momento do efeito. 2. Runway (imagem): "a mesma sala, mesmo ângulo e luz, vazia, sem a pessoa" com o quadro como referência (cerca de 20 créditos). 3. Conferir o alinhamento lado a lado com o quadro. 4. `--vertigem t0,t1,plate.png,0.5` (negativo = fundo se afasta). Janela de 1,5 a 2,5 s, no momento da virada. No máximo 1 por vídeo. Precisa de câmera parada.

## Assinatura @nubiacitty: Instagram, TikTok e stories (briefing da Núbia, 07/11/2026)
ABERTURA: a mão coloca o objeto do vídeo na mesa com um toque seco (som `toque` no quadro do toque, evento `{type:'som',t0:TOQUE,som:'toque'}`), depois o rosto e a fala "Citty sendo Citty." seguida de um gancho curto. Na edição: módulo `assinatura` (selo "Citty sendo Citty") do toque até cerca de 2,5 s; legenda normal desde o primeiro segundo.
FECHAMENTO: conteúdo de opinião termina com "Tem base um trem desse?"; conteúdo de venda termina com a chamada de venda. Sem selo no fechamento.
Stories: "Citty sendo Citty" como texto na tela, e o objeto na mesa abre a sequência do dia.
Exceção proposta (aguardando a Núbia): crime real com vítima, luto ou violência abre só com o objeto e o gancho, sem a frase e sem o selo.
NC Advogados nunca usa. Se o bruto não tiver o gesto ou a frase, não invente: edite com o que veio e avise no retorno à equipe.
Legenda do post: 5 hashtags do tema, uma delas #cittysendocitty.
