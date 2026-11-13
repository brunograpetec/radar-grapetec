/**
 * PC Ideal · Grape Tec — recebe os dados anônimos do site e grava na planilha.
 * Como instalar (uma vez só):
 * 1. Crie uma Planilha Google nova chamada "PC Ideal - dados".
 * 2. Menu Extensões > Apps Script. Apague o que tiver e cole este arquivo inteiro. Salve.
 * 3. Botão "Implantar" > "Nova implantação" > tipo "App da Web".
 *    Executar como: Eu. Quem pode acessar: Qualquer pessoa. Implantar e autorizar.
 * 4. Copie a URL que termina em /exec e mande pro Claude.
 */
const ABAS = {
  montou: ['quando','vid','tela','origem','orcamento','itens','pagamento','parcelado','jogo','resolucao','hz','painel','plat_pedida','visual','internet',
           'plataforma','cpu','gpu','placa_mae','memoria','ssd','fonte','cooler','gabinete','monitor','perifericos','total_pc','total'],
  cliques: ['quando','vid','tela','origem','evento','peca','loja','cupom','total']
};

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    const aba = d.evento === 'montou' ? 'montou' : 'cliques';
    const sh = folha_(aba);
    sh.appendRow(ABAS[aba].map(k => d[k] === undefined ? '' : String(d[k]).slice(0, 200)));
  } catch (err) {}
  return ContentService.createTextOutput('ok');
}

function doGet() { return ContentService.createTextOutput('PC Ideal coleta ativa'); }

function folha_(nome) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(nome);
  if (!sh) { sh = ss.insertSheet(nome); sh.appendRow(ABAS[nome]); sh.setFrozenRows(1); }
  return sh;
}
