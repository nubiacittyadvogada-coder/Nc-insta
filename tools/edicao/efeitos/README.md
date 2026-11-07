# Efeitos com profundidade (05/11/2026)

Base de todos: máscara da pessoa (recorte_fundo.py). A página HTML tem duas camadas, renderizadas separadamente com `render_camadas.js <html> bg|fg <pasta> <quadros>`:
- `bg`: tudo que fica ATRÁS da pessoa (título de capa, palavra gigante, notas de trás, celular, cartões da órbita no lado de trás, parede de vídeos, papel).
- `fg`: tudo que fica NA FRENTE (moldura, notas da frente, cartões da frente, checklist, cabeçalho, rótulo numerado, legenda, CTA).

Composição ffmpeg: vídeo base → camada bg → (vídeo "uma tomada, vários visuais" na janela dele) → pessoa recortada (vídeo base com a máscara como alfa, dilatada 2x e gblur 2) → (recorte de papel: pessoa a 86% com contorno branco = máscara dilatada 14x) → camada fg.

Efeitos prontos em vitrine-efeitos.html: 01 capa de revista (título atrás da cabeça), 02 texto atrás, 03 parede de notas/manchetes, 04 mockup do app, 05 órbita, 06 uma tomada vários visuais, 07 recorte de papel, 08 checklist, 09 parede de vídeos.
Regra de uso no Instagram de criminalista: no máximo 1 ou 2 efeitos por vídeo (capa de revista na abertura de série, parede de manchetes reais em react). Os lúdicos (órbita, recorte, rabisco) ficam para o TikTok do sistema e para anúncio do produto.
Funciona melhor com a pessoa do peito para cima, a um braço de distância, fundo liso.

Módulos novos (07/11/2026): ver CATALOGO-MODULOS.md (prompt, passos, painel, lousa, fluxo, objeto, cta, conversa).
