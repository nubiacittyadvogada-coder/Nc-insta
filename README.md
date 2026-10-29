# CENTRAL NÚBIA CITTY | CONTEÚDOS

Sistema de produção e inteligência de conteúdo do Instagram @nubiacitty.

**App (celular):** https://claude.ai/artifact/AHkcN3GHFYGsewtFnRVE5K (privado, abre com a conta do claude.ai)

## Pastas

| Pasta | O que guarda |
|---|---|
| `referencias/` | **Referências.** Como funciona a biblioteca visual e as etiquetas. As imagens ficam no app (Minha marca, Biblioteca de referências). |
| `modelos/` | **Modelos.** Motor de artes (`renderer.js`) com os 5 estilos visuais e as fontes da marca. O mesmo código roda no app e na produção automática. |
| `prontos-para-publicar/` | **Prontos para publicar.** Pacotes finais por data: artes PNG, vídeos, textos, legendas e .srt. |
| `central/` | Código do app publicado (painel Hoje, Gravar, Aprovar, Prontos, Calendário, Resultados, Vendas, Minha marca). |
| `conteudos/` | Conteúdos em formato de dados (entrada da produção automática). |
| `tools/` | Produção no servidor: `node tools/render.mjs <conteudos.json> <pasta>` gera PNG, textos e prévia MP4; `tools/montar-reel7.sh` monta o Reel de 7s com o vídeo gravado. |

`index.html` na raiz é a página de link da bio e não foi alterada.
