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
