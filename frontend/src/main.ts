import { Chart, CategoryScale, LinearScale, BarController, BarElement, Tooltip } from 'chart.js';

Chart.register(CategoryScale, LinearScale, BarController, BarElement, Tooltip);

interface Prato { prato: string; quantidade: number; receita: number }
interface Res { data: Prato[]; cache: string }

document.getElementById('app')!.innerHTML = `
  <div style="max-width:800px;margin:0 auto;padding:2rem;font-family:system-ui,sans-serif;color:#e2e8f0">
    <h1 style="font-size:1.5rem;margin-bottom:2rem">🍽️ Dashboard — Restaurante</h1>

    <section style="background:#1e293b;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem">
      <h2 style="font-size:1.1rem;margin-bottom:1rem">🏅 Top Pratos Mais Vendidos</h2>
      <canvas id="chart" height="250"></canvas>
      <p id="tag-top" style="font-size:.75rem;color:#94a3b8;margin-top:.5rem"></p>
    </section>

    <section style="background:#1e293b;border-radius:12px;padding:1.5rem">
      <h2 style="font-size:1.1rem;margin-bottom:1rem">🔥 Insight: Noites de Sexta-feira</h2>
      <div id="insight">Carregando...</div>
      <p id="tag-sexta" style="font-size:.75rem;color:#94a3b8;margin-top:.5rem"></p>
    </section>
  </div>
`;

async function init() {
  const [top, sexta]: Res[] = await Promise.all([
    fetch('/api/top-pratos').then(r => r.json()),
    fetch('/api/sexta-noite').then(r => r.json()),
  ]);

  // Gráfico de barras
  new Chart(document.getElementById('chart') as HTMLCanvasElement, {
    type: 'bar',
    data: {
      labels: top.data.map(d => d.prato),
      datasets: [{
        label: 'Unidades vendidas',
        data: top.data.map(d => d.quantidade),
        backgroundColor: ['#6366f1','#22d3ee','#f59e0b','#f43f5e','#10b981','#8b5cf6'],
        borderRadius: 6,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
        y: { ticks: { color: '#cbd5e1' } },
      },
    },
  });
  document.getElementById('tag-top')!.textContent = `Cache: ${top.cache}`;

  // Insight sexta à noite
  const campeao = sexta.data[0];
  const total = sexta.data.reduce((s, d) => s + d.quantidade, 0);
  document.getElementById('insight')!.innerHTML = `
    <div style="display:flex;align-items:center;gap:1rem;background:rgba(245,158,11,.1);padding:1rem;border-radius:8px;margin-bottom:1rem">
      <span style="font-size:2rem">🏆</span>
      <div>
        <strong style="color:#f59e0b;font-size:1.1rem">${campeao.prato}</strong>
        <p style="color:#94a3b8;font-size:.85rem">${campeao.quantidade} unidades · R$ ${campeao.receita.toFixed(2)}</p>
      </div>
    </div>
    ${sexta.data.map(d => {
      const pct = Math.round((d.quantidade / total) * 100);
      return `<div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.4rem">
        <span style="width:180px;font-size:.85rem;color:#94a3b8">${d.prato}</span>
        <div style="flex:1;height:8px;background:#334155;border-radius:4px;overflow:hidden">
          <div style="width:${pct}%;height:100%;background:linear-gradient(90deg,#6366f1,#f59e0b);border-radius:4px"></div>
        </div>
        <span style="font-size:.8rem;width:35px;text-align:right">${pct}%</span>
      </div>`;
    }).join('')}
  `;
  document.getElementById('tag-sexta')!.textContent = `Cache: ${sexta.cache}`;
}

init();
