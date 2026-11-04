# Prompt para o app de MKT: radar diário de notícias e novidades por cliente

Cole no projeto do app de MKT. Peça primeiro a análise do código atual e só depois a implementação. Este radar foi construído para a Núbia Citty e o NC Advogados em 04/11/2026, depois de comparar com um radar feito no ChatGPT. Aqui ele está generalizado para qualquer cliente do app.

---

## PROMPT

Você vai implementar no app o **Radar diário**: todo dia, para cada cliente, o app pesquisa notícias e novidades das últimas 48h da área dele, confere nas fontes, ranqueia as pautas e entrega uma decisão pronta (o que gravar hoje e com qual roteiro). Antes de escrever código, analise o que já existe (perfis de marca, séries, produtos, conteúdos, filas e agendamentos) e me entregue um plano curto. Não quebre o que os usuários de teste já usam.

### 1. Princípios
- **Radar é decisão, não lista.** O usuário abre e sabe em 30 segundos o que gravar hoje e por quê.
- **Fonte primária ou não entra.** Só vai para o ranking o que foi publicado nas últimas 48h e teve a página aberta, com data confirmada. O que só apareceu em resumo de busca fica numa seção "não verificado" e nunca entra nos 2 vídeos do dia. Nunca invente decisão, número, data, tese ou viralização. Se não houver dado de viralização, diga isso.
- **Por cliente, sem vazamento.** Área de atuação, fontes, canais, séries, produtos, voz e regras vêm do perfil de cada cliente. Nunca use pauta, voz ou produto de um cliente no radar de outro.
- **Radar separado da criação de conteúdo.** É uma tarefa própria, que roda antes. Quando a pesquisa era só um passo dentro da rotina que também cria conteúdos e artes, ela saía rasa e velha.

### 2. Configuração por cliente (no perfil de marca)
- **Área e subtemas:** ex. criminal, previdenciário, trabalhista, família, empresarial; ou, fora do direito, saúde, estética, imobiliário etc.
- **Fontes por área.** Sugira uma lista padrão por área e deixe o cliente editar. Exemplos para advocacia:
  - Criminal: STJ, STF, CNJ, Planalto (leis sancionadas), Câmara e Senado (projetos em votação), Conjur, Migalhas, JOTA, grandes portais.
  - Previdenciário: INSS, Ministério da Previdência, STJ, TNU, Agência Brasil.
  - Trabalhista: TST, Ministério do Trabalho, Agência Brasil.
  - Família: STJ, IBDFAM, CNJ.
  - Advocacia e gestão: OAB Nacional e seccionais, CNJ.
  - Outros nichos: órgãos reguladores e veículos de referência do setor (ex. Anvisa e conselhos de classe).
- **Canais e objetivo de cada um:** ex. Instagram para autoridade e crescimento, TikTok para venda de produto, perfil institucional para informação.
- **Séries ativas, com a frase fixa de cada uma**, e o calendário de lançamentos (aulas, eventos).
- **Produtos e regras de oferta.** Ex. "público que chega pelo tema IA vai para a aula e o workshop, nunca para o Kit". O radar só liga pauta a produto quando a ligação é honesta.
- **Voz:** expressões típicas, regional, o que evitar.
- **Regras do setor:** para advocacia, OAB (Provimento 205/2021) e notícia de crime com "suspeito", sem nome e sem foto, citando a fonte; para saúde, as normas do conselho.
- **Horário de execução e canal de aviso** (push ou e-mail).

### 3. Pesquisa (no servidor, todo dia no horário do cliente)
1. Leia o contexto do cliente: perfil, séries, produtos, motivos de recusa recentes e radares dos últimos 7 dias, para não repetir pauta.
2. Abra as páginas de notícias de hoje e de ontem de cada fonte configurada (pelo menos 12 leituras ou buscas) e confirme a data de publicação na própria página. Busca na web serve para achar a pauta. A confirmação vem da página aberta.
3. **Rede:** o servidor precisa ter acesso de saída aos domínios das fontes. Se uma fonte não abrir, registre qual foi e marque as pautas dela como "não verificado". Nunca preencha com suposição. Hoje o radar da Núbia saiu todo "não verificado" porque a rede do ambiente bloqueava STJ, STF, CNJ e OAB. O app precisa mostrar esse alerta ao cliente.
4. Cache por fonte e por dia: clientes da mesma área reaproveitam a leitura das mesmas páginas, mas cada um recebe ângulo, voz e roteiro próprios.

### 4. Ranking
De 5 a 8 pautas, cada uma com notas de 1 a 5 em:
- **Debate:** quanto gera conversa;
- **Autoridade:** quanto reforça o cliente como especialista;
- **Crescimento:** potencial de alcance e compartilhamento;
- **Comercial:** ligação honesta com um produto do cliente, dizendo qual; nota 1 se não houver.

Ordene pela soma, com o peso definido pelo objetivo do canal.

### 5. Ficha de cada pauta
- Fonte, com data, hora e link.
- **O que aconteceu:** 3 linhas, só fatos confirmados.
- **O que NÃO significa:** o erro de leitura mais comum. É o que mais protege o cliente de falar bobagem.
- **Gancho:** até 15 palavras, provocativo, na voz do cliente.
- **Ângulo de opinião do cliente** (para advocacia criminal: defesa das garantias, sem acusar nem condenar suspeito e sem minimizar violência).
- **Valor prático:** o que o público aprende.
- **React:** link do vídeo ou comunicado oficial, ou "não localizei vídeo original".
- **Perfil e série** em que entra, público e etapa do funil (topo, meio, fundo).
- **Risco jurídico e regulatório**, com o que conferir antes de gravar.

### 6. Os 2 vídeos que eu gravaria hoje
- Um de **autoridade e crescimento** e um com o **melhor encaixe comercial ou institucional** (dizer qual e por quê).
- Para cada um: objetivo, duração (45 a 70s), texto de gancho na tela, roteiro completo e legenda curta com 5 hashtags.
- Estrutura do roteiro: gancho forte, frase fixa da série, desenvolvimento que ensina algo e CTA.
- O roteiro sai na voz do cliente: frases curtas, opinião firme e expressões dele, sem juridiquês.
- Proibido abrir com fórmula fria tipo "Uma decisão publicada ontem merece a atenção de quem...". Aula técnica não faz perfil crescer.
- Respeitar o calendário de lançamentos e as regras de oferta.
- Inclua um botão **"Transformar em conteúdo"** que cria o card do roteiro, já ligado à pauta, para gravação e para a edição automática (veja o prompt de edição).

### 7. Onde aparece no app
- Bloco **"Radar do dia"** no topo da aba Radar: "Gravar hoje: [pauta 1] · [pauta 2]" e o relatório completo recolhível.
- Cards das pautas com posição no ranking, gancho, "o que não significa", notas e fonte clicável, com os botões "Transformar em conteúdo" e "Descartar". O motivo do descarte alimenta o aprendizado.
- Alerta visível quando houver fonte que não abriu ou pauta não verificada.
- Notificação no horário com até 6 linhas: as 2 pautas com o gancho de cada uma, quantas entraram e quais fontes falharam.

### 8. Dados (por cliente)
Pauta: `data, tema, fonte, url, dataFonte, verificado (bool), tipo ("fato" só se confirmado), rank, notas {debate, autoridade, crescimento, comercial, produto}, oQueAconteceu, naoSignifica, gancho, anguloOpiniao, valorPratico, react, perfil, serie, publico, funil, riscos, origem "radar-diario", usado, descartado, motivoDescarte`.

Relatório do dia: `data, criadoEm, relatorio (Markdown), top2, fontesFalharam`.

### 9. Custos e limites
- Limite de buscas e leituras por cliente por dia. Cache compartilhado por fonte.
- Use o modelo mais capaz na escolha e no roteiro e um modelo mais barato na triagem das páginas.
- Registre o custo por radar.

### 10. Critérios de aceite
- Nenhuma pauta do ranking sem página aberta e data confirmada nas últimas 48h. Fonte bloqueada aparece como alerta, nunca como fato.
- Dois clientes de áreas diferentes recebem radares diferentes, sem nenhuma pauta, voz ou produto trocado.
- Os 2 roteiros seguem gancho, frase da série, ensino e CTA, na voz do cliente, sem oferta proibida pelas regras dele.
- O botão "Transformar em conteúdo" cria o card certo, e o descarte registra o motivo.
- O radar roda sozinho no horário e avisa o cliente.

---

Referência que roda hoje na Central da Núbia: a rotina "Radar diário Núbia Citty" (6h13) grava em `radar`, `nc_radar` e `settings/radarDia`. O bloco "Radar do dia" está na Central v36, arquivo `central/app.html`, funções `radarDiaBox`, `mdLite` e `radarCard`.
