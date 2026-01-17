let inicio = null;

document.getElementById("startTimer").onclick = () => {
  inicio = performance.now();
};

document.getElementById("stopTimer").onclick = () => {
  if (!inicio) return;

  const fim = performance.now();
  const segundos = ((fim - inicio) / 1000).toFixed(2);
  document.getElementById("tempoMontagem").value = segundos;
  inicio = null;
};

document.getElementById("smtForm").addEventListener("submit", async e => {
  e.preventDefault();

  const tempo = document.getElementById("tempoMontagem").value;
  const blank = document.getElementById("blankSMT").value;

  const fd = new FormData();
  fd.append("tempo_montagem", tempo);
  fd.append("blank", blank);

  const r = await fetch("/api/smt/calcular_meta", { method:"POST", body: fd });
  const data = await r.json();

  document.getElementById("resultadoSMT").innerHTML =
    `Meta Hora SMT: <strong>${data.meta_hora}</strong>`;
});

document.getElementById("smtInversoForm").addEventListener("submit", async e => {
  e.preventDefault();

  const fd = new FormData();
  fd.append("meta_hora", document.getElementById("metaHoraInv").value);
  fd.append("blank", document.getElementById("blankInv").value);

  const r = await fetch("/api/smt/calcular_tempo", { method:"POST", body: fd });
  const data = await r.json();

  document.getElementById("resultadoInverso").innerHTML =
    `Tempo de montagem considerado: <strong>${data.tempo_montagem}s</strong>`;
});

