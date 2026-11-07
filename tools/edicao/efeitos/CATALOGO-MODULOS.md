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

Ícones próprios (sem imagem de terceiros): algema, martelo, balanca, relogio, documento, celular, cadeado, alerta, grade, escudo, dinheiro, ia.
Para um objeto ou personagem novo: gerar imagem sóbria no Runway, remover o fundo, salvar PNG e usar `src:'img/arquivo.png'` no `objeto` ou no `painel`.

## Regras de uso (decisão da Núbia: o diferencial vem da edição, sem copiar ninguém)
1. Um "momento de diferencial" por vídeo, no ponto mais importante da fala. No máximo 2 módulos grandes (painel, lousa, fluxo) por vídeo.
2. Escolha pelo conteúdo: explicação de processo = `fluxo`; conceito que o público confunde = `lousa`; lista de direitos ou passos = `passos`; série IA = `prompt`; número ou prazo = `counter` (antigo) ou `objeto` relógio.
3. Alternar entre vídeos: não repetir o mesmo módulo grande dois vídeos seguidos.
4. `conversa` sem print real autorizado sai SEMPRE com o selo SIMULAÇÃO (já é automático). Nunca inventar fala de cliente como se fosse real.
5. Conteúdo jurídico do quadro passa pela mesma checagem do roteiro (nada de promessa de resultado, nada de caso identificável).
6. Perfil pessoal: livre. NC: padrão rápido; no máximo 1 módulo (fluxo ou passos) quando a explicação pedir.
