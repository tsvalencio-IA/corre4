const viewer = document.getElementById('viewer');
const parts = {
  cabedal: ['Cabedal','Parte superior vermelha com volume de malha, abertura, língua, cadarços e logo CORRE na lateral.'],
  entressola: ['Entressola','Camada intermediária alta e curva, responsável pela sensação visual de amortecimento e resposta.'],
  solado: ['Solado','Base vermelho escuro com travas e ranhuras para representar a borracha de contato.'],
  contraforte: ['Contraforte','Região traseira com volume de calcanhar, puxador e etiqueta vertical.'],
  placa: ['Placa / apoio','Estrutura de apoio representada pela geometria da entressola e da base, sem prometer placa rígida real.']
};
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const [t,p] = parts[btn.dataset.part];
    document.getElementById('partTitle').textContent = t;
    document.getElementById('partText').textContent = p;
  });
});
document.querySelectorAll('.thumb').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.thumb').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    if (viewer && btn.dataset.orbit) viewer.cameraOrbit = btn.dataset.orbit;
  });
});
const arBtn = document.getElementById('arBtn');
if (arBtn) arBtn.addEventListener('click', () => viewer && viewer.activateAR && viewer.activateAR());
const resetBtn = document.getElementById('resetBtn');
if (resetBtn) resetBtn.addEventListener('click', () => {
  if (viewer) {
    viewer.cameraOrbit = '35deg 68deg 0.72m';
    viewer.fieldOfView = '34deg';
  }
});
