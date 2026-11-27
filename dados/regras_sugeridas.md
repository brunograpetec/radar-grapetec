# Regras sugeridas (aprendidas das consultorias)

Observações tiradas das consultorias que contradizem ou não estão em regras_bruno.md. São sugestões: o Bruno decide se viram regra. O código do site NÃO foi alterado.

## 16/11/2026 (lote das consultorias 208 a 247)

### Processador e plataforma
- Perfil FPS/competitivo com orçamento alto (R$ 9,5 a 13 mil) muitas vezes vai de Ryzen 7 7700 sem X3D, e o dinheiro vai pra RX 9070 / 9070 XT. O algoritmo manda X3D pra FPS. (238, 240, 243, 216)
- Competitivo com ~R$ 8 mil: AM5 com 6 núcleos (7500F) e a economia vai pra placa de vídeo. (218)
- AM4 aparece em faixas mais altas que o esperado quando é pra encaixar uma placa forte ou 32GB: 5700X + RTX 5070 em ~R$ 6,7 a 8,4 mil; AM4 + GPU de 16GB + 32GB em ~R$ 7,5 a 9 mil; AM4 com ~R$ 7 mil quando o cliente não quer upgrade tão cedo. (213, 222, 228, 231, 227)
- Entre AM4 (~R$ 7,4 mil) e AM5 (~R$ 9,4 mil) com a mesma placa de vídeo, prefere AM5 se o orçamento comportar, pela longevidade. (217)
- Orçamento curto (~R$ 5,5 mil) com outros gastos: APU AM4 (5600GT) + B550 Wi-Fi em vez de AM5 série G. (225)
- Ryzen 9 de 16 núcleos só entra como opção pra produtividade, nunca por FPS. (228)

### Refrigeração
- Water cooler 360mm aparece com processadores que não estão na lista dos "que esquentam": 5700X, 7700, 9700X e até 7500F, por oferta barata, estética ou preferência do cliente. (247, 243, 228, 224, 219, 218, 217, 214, 213, 212, 209)

### Memória
- Com DDR5 cara, mantém 16GB (2x8GB) mesmo em PCs AM5 de R$ 9 a 11 mil (com RX 9070 / RTX 5070) e deixa 32GB pra depois. A regra atual põe 32GB a partir de ~R$ 7,5 mil. (217, 224, 226)
- Mas acima de ~R$ 10 mil ele também indica 32GB DDR5 6000 como opção principal: a faixa varia conforme o preço da DDR5. (212)
- Placa de vídeo mais forte vem antes de 32GB; 32GB só se o orçamento máximo permitir. (240)
- Uso com máquinas virtuais ou trabalho/multitarefa pesado: 32GB (2x16GB) é prioridade, mesmo em orçamento curto. (235, 237)
- Uma montagem AM5 de ~R$ 9 mil saiu com um único pente de 8GB DDR5, o que contradiz a regra de dual channel. Vale conferir se foi intencional. (236)

### Fonte, SSD e gabinete
- Fonte 850W Gold "pra upgrade" já em PCs AM4 de ~R$ 6 mil; 650W Gold num AM4 de ~R$ 7 mil; 750W Gold com RX 9070 / 9070 XT. (247, 241, 238, 209, 222)
- Fonte Bronze (650 a 750W) aceita em orçamento apertado, até com RTX 5070. (225)
- SSD de 500GB num PC de ~R$ 8 mil quando a DDR5 aperta, ou quando o orçamento inclui monitor e periféricos. A regra atual pede 1TB a partir de ~R$ 5,5 mil. (218, 208)
- Gabinete aquário baratinho (~R$ 280) em PCs acima de R$ 7 mil, o que contradiz a regra de gabinete decente acima de R$ 7 mil. (230, 231)
- Build com vídeo integrado pensando em placa futura usou gabinete barato, não mid tower caprichado. (223)

### Placa de vídeo e uso
- Pra IA, LLM local, Blender e edição: prioriza NVIDIA (CUDA), mesmo com AMD mais barata. Já pra software de trabalho comum (CAD, IDE, fatiador 3D) não exige NVIDIA. (213, 214, 211, 233)
- RTX 5060 (x8) em B550 (PCIe 4.0) com 5700X: sem problema, a penalidade x8 só vale pra PCIe 3.0. (241)
- Cliente com monitor 4K e orçamento curto (~R$ 6 mil): monta pra Full HD com placa de 8GB e explica, em vez de forçar 4K. (247, 242)
- Placa de vídeo com preço subindo semana a semana é a primeira peça a comprar. (224)

### Orçamento
- Orçamento no cartão: fecha o total de referência ~10% abaixo do teto pra absorver o parcelamento. (241)
- Não precisa gastar o orçamento inteiro se o PC já atende; não inclui monitor novo se o atual já serve. (237, 235)
- Quando o PC ideal passa muito do orçamento: mostra assim mesmo e oferece uma alternativa (ex.: AM4 com a mesma placa forte) que respeita o teto. (243, 226)

### Observação sobre os dados
- O doc "234 - João Pedro Aguiar Dantas Oliveira" tem o texto da consultoria 233 (outro cliente). Foi marcado como lido, mas não entrou na contagem pra não contar duas vezes.

## 18/11/2026 (consultorias 168 a 207, 248 e 249)

### Plataforma AM4 x AM5
- AM4 com placa forte (RX 9070 / 9070 XT) mesmo em ~8 a 10 mil, principalmente com monitor Full HD, sem plano de upgrade ou foco em jogo de história. A diferença vai pra GPU ou fica pra um monitor QHD depois. (186, 190, 192, 195, 198)
- Cliente que já tem 32GB DDR4: fica no AM4 (5800X3D + B550) pra não reduzir a placa de vídeo pagando placa-mãe AM5 + DDR5. Em ~9 mil, mostra AM4 e AM5 lado a lado e o cliente escolhe. Nunca reduz a GPU pra caber AM5. (248, 249)
- AM5 aparece com mais firmeza a partir de ~11-12 mil, já com chipset B850 e 32GB DDR5 6000. Disse que 750-850W Gold já bastam ali, mesmo usando uma 1000W. (184, 188, 204, 206)
- AAA em QHD no AM5: prefere Ryzen 7 7700 ao 9700X e ao 7800X3D. X3D só quando há competitivo junto (9800X3D em ~12-13 mil). (184, 188, 193)
- Produtividade pesada (Docker, edição): Ryzen 9 5900XT no AM4, com B550 de VRM mais robusto e WC 360, em vez de migrar pra AM5. (177, 182)
- Compra em etapas: base AM5 (CPU + placa-mãe + 32GB) primeiro, depois GPU + fonte, SSD por último. (203)
- Estação de trabalho sem jogo (~7,5 mil): Ryzen 7 7700 com vídeo integrado, sem placa de vídeo, 32GB DDR5. (200)

### Upgrades
- Base AM4 boa (5600/5600X/5700X + B450/B550): mantém CPU e placa-mãe e troca só GPU (+ fonte, às vezes monitor). B450M com RX 9060 XT não tem perda perceptível. Sugere 5700X3D como próximo passo. (180, 185, 189, 205)
- Upgrade de trabalho com GPU boa já instalada: não mexe na placa de vídeo e põe tudo em plataforma, RAM e cooler. (178)

### Fonte
- Fonte de linha boa que o cliente já tem (600-650W) é reaproveitada mesmo com RTX 5070 ou RX 9060 XT. A Gold nova fica opcional e o SSD 1TB vem antes dela. Isso contradiz a regra de 850W pra upgrade. (185, 201, 202)
- AM4 de ~6-6,5 mil com 5060 / 9060 XT / 7600: 650W Gold ou 750W Bronze, não 850W. (169, 191, 194)
- RX 9070 XT com 750W Gold, inclusive em build de ~10 mil. (179)

### Memória, SSD e cooler
- Mais casos de 16GB DDR5 (2x8) em AM5 de ~11-12,4 mil, inclusive com 9800X3D + RX 9070 XT, por causa do preço da DDR5. 32GB DDR5 6400 entrou só acima de ~15 mil (4K). (172, 176, 168)
- SSD de 500-512GB em PCs de ~6-6,5 mil, principalmente quando o orçamento inclui periféricos ou é pra live. (169, 170, 187, 196)
- Quando o SSD 1TB nacional está caro, manda acompanhar promoção de SSD PCIe 4.0 importado. (205, 207)
- Air cooler topo em vez de water cooler em AM5 de ~10 mil, quando o cliente quer PC silencioso e sem RGB. Usa WC 240 pelo baixo ruído. (194, 199)

### Placa de vídeo e uso
- NVIDIA também pra live, gravação e edição leve (encoder NVENC), não só pra IA e Blender: RTX 5060 em ~6-6,5 mil. Também quando o cliente prefere NVIDIA. (170, 191, 196)
- AAA em AM4 de ~6,5 mil: RX 9060 XT 16GB pela VRAM. (171)

### Orçamento e compra
- Com teto de ~14 mil no cartão, montou ~10,3 mil à vista (margem de ~25%, bem acima dos ~10% de costume). (199)
- Cliente que quer receber montado e testado: indicou a configuração pelo montador de uma loja grande em vez de peças avulsas. (187)
- Placa-mãe sem Wi-Fi + adaptador USB depois, pra caber no orçamento. (170)
- Periféricos no orçamento: se precisar cortar, corta primeiro headset/teclado, nunca o PC. (196)

### Observação sobre os dados
- O doc "197" tem o mesmo texto da consultoria 198 (outro cliente no título). Foi marcado como lido, mas não entrou na contagem.
- Na 190, a placa-mãe da lista (ASUS TUF B550M-Plus) não bate com a da tabela financeira (MSI B550M PRO-VDH WiFi).

## 20/11/2026 (consultorias 128 a 167)

### Plataforma AM4 x AM5 x Intel
- Ryzen 7 5700X + B550 é a base padrão entre ~6,2 e 8,9 mil (7 de 10 docs entre 158 e 167), com RX 9060 XT 16GB, RTX 5060 ou até RX 9070 XT. (158, 161-164, 166)
- Mostrou AM4 (5700X) x AM5 (9800X3D) com a mesma RX 9060 XT e recomendou o AM4: com a mesma GPU, o FPS não acompanha os ~3,5 mil a mais. (166)
- 5700X + RX 9070 XT + 16GB DDR4 em ~8,9 mil pra competitivo acima de 200 FPS, sem X3D e sem AM5. (158)
- Pra AAA, preferiu 5700X ao 7600X e RX 9060 XT 16GB à RTX 5060 8GB, pela VRAM. (161)
- Competitivo em AM5 de ~7-8,6 mil: Ryzen 5 7600 sem X3D + RX 9060 XT 16GB, com a economia indo pra GPU e RAM. (133, 134)
- Cliente com 32GB DDR4 e 12 mil foi pro AM5 mesmo assim (7800X3D + RX 9070 XT + 32GB DDR5) por ser competitivo em QHD 360Hz, vendendo a DDR4. Contraponto à regra de ficar no AM4 quando já tem 32GB DDR4. (154)
- Intel aparece como opção: i5-14600KF + B760 DDR4 com RX 9070 XT em ~10,6 mil; i7-14700KF + B760M DDR4 quando o cliente pede Intel + NVIDIA e já tem DDR4; em upgrade, rota Intel D4 lado a lado com AM5. O algoritmo não considera Intel. (141, 144, 150)
- Ryzen 7 7700X aparece como CPU principal em AM5 de 10 a 14 mil, sempre com WC 360, mas não existe em pcideal_data.json. (128, 131, 135, 140)
- PC sem placa de vídeo com orçamento curto (~3-3,8 mil): APU Ryzen 7 5700G + B550 + 2x8GB e fonte já pensando na GPU futura; se comprar a GPU agora, troca pro 5700X. Complementa a regra da 200. (139, 149)

### Upgrades
- APU AM4 (5600G) com GPU antiga boa: prefere vender a GPU e pegar uma de nova geração (RTX 5070) mantendo a APU por enquanto, aceitando gargalo no single player. (136)
- Quem já tem X3D AM4 + 32GB DDR4: fica no AM4 com B550 nova + RX 9070 XT + fonte 850W Gold. (160)
- Quem já tem plataforma topo (9800X3D + B850 + 32GB DDR5): troca só GPU, fonte, SSD, gabinete e WC. Quem tem GPU topo (RTX 4090): troca só a plataforma. (142, 143)

### Fonte
- Reaproveita fonte boa de 650W com RTX 5070 e até fonte de 500W com 5700X + RTX 5060. (136, 137, 151)
- Fonte Bronze de entrada (650-750W) em AM4 de ~6,5-8 mil com RTX 5060 e RX 9060 XT. (146, 156, 163, 164)
- 850W Gold com RX 9070 XT + 9800X3D (inclusive em upgrade só de GPU); 700W Gold com RX 9060 XT em AM5. (133, 143, 144, 145)

### Memória e SSD
- 16GB DDR5 (2x8) com 9800X3D (~8,3 mil), com Ryzen 7 7700 + RTX 5070 (~9 mil) e até em dev pesado com Docker/VMs e teto de 15 mil (saiu ~9 mil). Contradiz 32GB como prioridade pra VMs. (129, 137, 155)
- 32GB DDR5 6000-6400 em AM5 de ~12-14,7 mil com edição/trabalho ou longevidade, mesmo com DDR5 cara; também 32GB DDR5 em AM5 de ~8,6 mil competitivo. (130, 133, 140, 145, 165)
- 16GB DDR4 mesmo num PC Intel de ~10,6 mil com RX 9070 XT. (144)
- SSD 500GB como único SSD novo num PC de ~10,4 mil com RTX 5070 Ti; mantém SSD de 240GB do cliente só pro Windows. (135, 137)

### Refrigeração e estética
- Silêncio + uso de 10-12h/dia em AM5 de ~14,5 mil: WC 360 + fans extras, dizendo que é mais silencioso que air cooler topo. Contradiz 194/199. (165)
- WC 360 barato com 5700X e 5800X3D por custo-benefício e estética. (160, 161)
- i5-14600KF tratado como processador quente: WC 240mm+ (360 na 144). (141, 144)
- Evita GPU na vertical com riser (instabilidade) e tela secundária interna; prefere WC com tela LCD e fans reversas. (132)
- Redragon Wideload Pro é o gabinete padrão (6 de 10 docs entre 148 e 157, de ~6 a ~13 mil); quando vem sem fans, adiciona 6. (148-157)

### Placa de vídeo e uso
- Live não exige NVIDIA: com ~7 mil indicou RX 9060 XT 16GB usando o encoder da AMD. Relativiza a regra de NVENC pra live. (162, 166)
- IA local: VRAM máxima (RTX 5060 Ti 16GB) e 64GB de RAM; placa-mãe premium é dinheiro mal gasto. IA/edição como uso futuro puxa pra NVIDIA (RTX 5070). (128, 153)
- Com RX 9060 XT 16GB, recomenda monitor QHD 165-180Hz até pra competitivo; Full HD desperdiça a placa. (161, 167)
- Quando o cliente pede uma GPU cara específica (RTX 5070 Ti), mostra a RX 9070 XT ao lado como opção ~1,8 mil mais barata. (131)

### Orçamento e periféricos
- Passou ~10% do teto: mostra a recomendada como opção 1 e uma versão ajustada ao teto como opção 2, sugerindo vender peças antigas. (154)
- Monitor tratado à parte do orçamento da torre em alguns casos; com periféricos no orçamento, teclado baratinho e trocar monitor 27" por 24" antes de mexer no PC. (140, 163)
- Com previsão de alta de GPU, usa a sobra pra antecipar a compra da placa. (139)

### Observação sobre os dados
- 138 é um doc vazio; 153 é análise de PC já comprado (só a troca sugerida entrou); 148 e 132 só tinham complementos sobre base que o cliente já tinha.
- Na 133 o nome do cliente no corpo é diferente do título (possível doc trocado); foi contada normalmente.
- Muitas peças indicadas não têm modelo no site (Kalkan 650/750W, CM MWE Gold 850 V3, TUF B850M-Plus, B850 Eagle, Thermaltake LA360, Dahua C910, Kootion X16 Plus, Mancer CV500L) e ficaram fora da contagem.

## 23/11/2026 (consultorias 90 a 127 + doc sem número "Fabio Sobrinho de Freitas")

### Processador e plataforma
- AM5 domina já a partir de ~R$ 4-6 mil: Ryzen 5 7600 + B650 aparece em ~R$ 5-7 mil (95, 97, 106, 109, 116), e até em ~R$ 4-5 mil sem placa de vídeo dedicada, com Ryzen 5 8600G pra uso leve (94). AM4 (5700X + B550) ficou restrito a ~R$ 4-5,7 mil ou quando reaproveita DDR4 do cliente (96, 105, 110, 114, 115).
- Foco FPS com R$ 8-10 mil muitas vezes vai de Ryzen 5 7600/7600X (sem X3D) e põe o dinheiro na RTX 5070 (117, 119, 125, 126); mostra o 7600X como "opção 2" mais barata do 7800X3D com o resto igual (121). Contradiz X3D pra FPS.
- ~R$ 14 mil pra QHD/4K: Ryzen 7 7700 (sem X3D) + RTX 5070 Ti (doc sem número).
- Quando o cliente já tem GPU forte (RX 7900 XT, RX 9060 XT), monta só a base AM5 e não gasta o orçamento todo (102, 111).
- Com sobra de orçamento sem GPU, prioriza 7800X3D + WC 360 e deixa a placa de vídeo pra depois (122) ou bota GPU de entrada (RTX 5060) com o X3D (123).
- PC de escritório/PDV (~R$ 2 mil): APU AM4 5600GT + A520, 16GB num pente só, fonte 400W. (113)

### Memória
- 32GB DDR5 6000 virou padrão a partir de ~R$ 6-7 mil (97, 98, 106, 109, 120, 125, 126), inclusive em ~R$ 4-5 mil sem GPU (94) e em upgrade de ~R$ 3,2 mil (91). Ainda há 16GB DDR5 (2x8) em ~R$ 7 mil (112, 116).

### Fonte e refrigeração
- Fonte 750W Gold (ATX 3.1) quase sempre, mesmo com GPU de consumo baixo e orçamento de ~R$ 4 mil (110, 114, 116); 850W Gold com RTX 5060 (112) e RTX 5070 (125, 126). Exceções: 500W Bronze com 7600 + RTX 5060 (97), 600W White com 5700X + RTX 5060 (96).
- 9800X3D com air cooler de 120mm (AK400) em ~R$ 10 mil (103), mas WC 360 com o 7800X3D/9800X3D em outros (100, 107, 108, 121, 122, 123).

### Placa de vídeo e uso
- Edição de vídeo com orçamento curto: prefere NVIDIA (RTX 5060) por CUDA (96); produção musical sem GPU dedicada usa 8600G (94).
- Entre GPU melhor e periféricos/mesa/cadeira, recomenda cortar os acessórios e subir pra RTX 5070 (119).
- Build Intel (i5-14600K + B760 + RX 9070 XT) só a pedido do cliente ou quando ele já tem o processador (99, 124).

### Observação sobre os dados
- 92 e o rascunho "108 (INCOMPLETO)" estão vazios; contados como lidos, sem peças. O doc sem número "Fabio Sobrinho de Freitas" (~R$ 14 mil) é diferente da 115 (mesmo nome, ~R$ 4 mil) e foi contado à parte.
- O conector do Drive devolveu o texto truncado no fim de vários docs; peças e frases vieram das partes lidas.
- Muitas peças sem modelo no site: Kalkan Delta 360, Gamemax GX-750, XPG Lancer DDR5 2x16GB CL30, Corsair RM750x Shift, CM MWE Gold 850 V3, TUF B850M-Plus, B650M Aorus Elite, Adata Legend 710, Patriot P300, Husky DDR5, Mancer CV500L.


## 27/11/2026 (consultorias 250 a 252, 53 a 89 e 34-2)

### Processador e plataforma
- AM5 domina a partir de ~R$ 4,5 mil, inclusive quando a GPU fica pra depois: monta com processador com vídeo integrado (8600G, 8700G, 7600X) e explica que AM4 com 5700X não liga sem placa de vídeo (62, 80, 85, 252). Com foco em trabalho/IA (~R$ 6,5 mil), prefere 8700G + 32GB a uma GPU de entrada (252).
- AM4 (5700X + B550) só quando reaproveita DDR4/fonte do cliente ou quando a GPU nova não caberia no AM5: ~R$ 4 mil com RX 7600 (68-Lucas), ~R$ 5,2-5,7 mil (79), GPU forte já comprada (64, 65). Cliente com 5800X3D no AM4 não migra (251).
- Passa um pouco do orçamento pra entrar no AM5 em vez de AM4 com ~R$ 6,5 mil (72).
- X3D: entre 7800X3D e 9800X3D pega o que estiver mais barato (57, 58, 70); em 4K/60 não usa X3D e põe tudo na GPU (87). FPS competitivo com ~R$ 8 mil vai de 7600X + RTX 5060 Ti 16GB (56) — de novo sem X3D.
- Ryzen 7 7700/7700X (sem X3D) aparece bastante em ~R$ 6-12 mil (59, 60, 63, 69, 71, 78, 83, 84, 87). Em CPU de 8 núcleos sem cooler, evita o box e põe WC 360 barato (69).
- Uso profissional pesado (3D/Houdini, processamento): Ryzen 9 7950X, até 64GB de RAM, com GPU modesta ou sem GPU (86, 88). Sobe pra Ryzen 9/X670E só quando a diferença de preço é pequena (61).

### Memória
- 32GB DDR5 é padrão em praticamente tudo, inclusive ~R$ 4-5 mil sem GPU (80, 85). DDR5 6400 aparece muito, às vezes mais barata que 6000 (53, 56-60). 16GB só em AM4 com DDR4 (64, 68-Lucas, 79) e um AM5 apertado (62).

### Fonte e refrigeração
- Fonte 700W Gold mesmo com RTX 5070 / 5070 Ti (68-Dennis, 77); 800-850W Gold (PCIe 5.0/ATX 3.0) a partir de ~R$ 8 mil ou com GPU forte (58, 61, 63, 83, 87). 500W White só em PC sem GPU (80).
- Water cooler 360mm vira padrão a partir de ~R$ 4,6 mil, mesmo com Ryzen 5 7600X (56, 62); 240mm só em gabinete Mini ITX (63); 420mm em Ryzen 9 profissional (88).

### Placa de vídeo e uso
- Com sobra de orçamento, sobe primeiro a GPU (5060 Ti → 5070, 5070 Ti → 5080) e depois o SSD (56, 58). RTX 5090 considerada exagero pra jogos (58).
- Pra Full HD competitivo, prefere RX 9060 XT 16GB + monitor 240Hz em vez de RTX 5070 sem monitor (57).
- Render 3D (V-Ray/CUDA) → NVIDIA (89). Monitor: sugere Quad HD em vez de 4K pela longevidade (251, 65).

### Observação sobre os dados
- 55 veio vazio do Drive (contado como lido, sem peças). 76 é orçamento em euros só com lista de peças. 71 não tem preços. Vários docs vieram truncados no fim pelo conector.
- Peças frequentes sem modelo no site: Kalkan Asgard (gabinete), Ryzen 7 8700G, Ryzen 9 7950X/7900, B850M, X670E, B650I ITX, DDR5 6400 2x16, WC 420mm e 240mm, RX 7800 XT, RTX 5080.
