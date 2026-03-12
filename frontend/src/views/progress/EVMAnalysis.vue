<template>
  <div class="progress-page">
    <div class="page-header">
      <div>
        <span class="page-tag purple">PROGRESS · EVM ANALYSIS</span>
        <h1>EVM Analysis</h1>
        <p class="page-sub">Earned Value Management — cost and schedule performance across projects</p>
      </div>
      <div style="display:flex;gap:10px">
        <select v-model="selectedProject" class="filter-select">
          <option v-for="p in projectOptions" :key="p.id" :value="p.id">{{ p.name }}</option>
        </select>
        <button class="btn-export">📥 Export</button>
      </div>
    </div>

    <!-- EVM KPIs -->
    <div class="kpi-row">
      <div class="kpi" :class="currentProject.cpi >= 1 ? 'green' : 'danger'">
        <div class="kpi-top">
          <span>💰</span>
          <span class="mono" style="font-size:10px" :style="currentProject.cpi >= 1 ? 'color:#22c55e' : 'color:#ef4444'">
            {{ currentProject.cpi >= 1 ? 'Under Budget' : 'Over Budget' }}
          </span>
        </div>
        <div class="kpi-val">{{ currentProject.cpi.toFixed(2) }}</div>
        <div class="kpi-label">CPI — Cost Performance Index</div>
      </div>
      <div class="kpi" :class="currentProject.spi >= 1 ? 'green' : 'danger'">
        <div class="kpi-top">
          <span>📅</span>
          <span class="mono" style="font-size:10px" :style="currentProject.spi >= 1 ? 'color:#22c55e' : 'color:#ef4444'">
            {{ currentProject.spi >= 1 ? 'Ahead of Schedule' : 'Behind Schedule' }}
          </span>
        </div>
        <div class="kpi-val">{{ currentProject.spi.toFixed(2) }}</div>
        <div class="kpi-label">SPI — Schedule Performance Index</div>
      </div>
      <div class="kpi amber">
        <div class="kpi-top"><span>📊</span><span class="mono" style="font-size:10px;color:#f5a623">Planned Value</span></div>
        <div class="kpi-val">{{ formatKES(currentProject.pv) }}</div>
        <div class="kpi-label">PV — Planned Value</div>
      </div>
      <div class="kpi blue">
        <div class="kpi-top"><span>✅</span><span class="mono" style="font-size:10px;color:#3b82f6">Earned Value</span></div>
        <div class="kpi-val">{{ formatKES(currentProject.ev) }}</div>
        <div class="kpi-label">EV — Earned Value</div>
      </div>
      <div class="kpi purple">
        <div class="kpi-top"><span>💸</span><span class="mono" style="font-size:10px;color:#a855f7">Actual Cost</span></div>
        <div class="kpi-val">{{ formatKES(currentProject.ac) }}</div>
        <div class="kpi-label">AC — Actual Cost</div>
      </div>
    </div>

    <!-- Variance Row -->
    <div class="variance-row">
      <div class="var-card" :class="currentProject.cv >= 0 ? 'positive' : 'negative'">
        <div class="var-label">Cost Variance (CV)</div>
        <div class="var-val">{{ currentProject.cv >= 0 ? '+' : '' }}{{ formatKES(currentProject.cv) }}</div>
        <div class="var-sub">{{ currentProject.cv >= 0 ? 'EV > AC — Saving on budget' : 'EV < AC — Cost overrun' }}</div>
      </div>
      <div class="var-card" :class="currentProject.sv >= 0 ? 'positive' : 'negative'">
        <div class="var-label">Schedule Variance (SV)</div>
        <div class="var-val">{{ currentProject.sv >= 0 ? '+' : '' }}{{ formatKES(currentProject.sv) }}</div>
        <div class="var-sub">{{ currentProject.sv >= 0 ? 'EV > PV — Ahead of schedule' : 'EV < PV — Behind schedule' }}</div>
      </div>
      <div class="var-card neutral">
        <div class="var-label">EAC — Estimate at Completion</div>
        <div class="var-val">{{ formatKES(currentProject.eac) }}</div>
        <div class="var-sub">Budget at Completion: {{ formatKES(currentProject.bac) }}</div>
      </div>
      <div class="var-card neutral">
        <div class="var-label">ETC — Estimate to Complete</div>
        <div class="var-val">{{ formatKES(currentProject.etc) }}</div>
        <div class="var-sub">{{ Math.round((currentProject.ev / currentProject.bac) * 100) }}% of work complete</div>
      </div>
    </div>

    <!-- Work Package Table -->
    <div class="panel" style="margin-bottom:16px">
      <div class="panel-header"><h2>Work Package EVM Breakdown</h2></div>
      <div class="table-wrap" style="margin-bottom:0">
        <table class="data-table">
          <thead>
            <tr>
              <th>Work Package</th><th>BAC (KES)</th><th>PV (KES)</th><th>EV (KES)</th>
              <th>AC (KES)</th><th>CV</th><th>SV</th><th>CPI</th><th>SPI</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="wp in currentProject.workPackages" :key="wp.name" class="table-row">
              <td>
                <div class="cell-main">{{ wp.name }}</div>
                <div class="cell-sub">{{ wp.category }}</div>
              </td>
              <td class="mono" style="font-size:12px;color:#e8e4dc">{{ (wp.bac/1000).toFixed(0) }}K</td>
              <td class="mono" style="font-size:12px;color:#f5a623">{{ (wp.pv/1000).toFixed(0) }}K</td>
              <td class="mono" style="font-size:12px;color:#3b82f6">{{ (wp.ev/1000).toFixed(0) }}K</td>
              <td class="mono" style="font-size:12px;color:#a855f7">{{ (wp.ac/1000).toFixed(0) }}K</td>
              <td class="mono" :style="wp.ev - wp.ac >= 0 ? 'color:#22c55e;font-size:12px' : 'color:#ef4444;font-size:12px'">
                {{ wp.ev - wp.ac >= 0 ? '+' : '' }}{{ ((wp.ev - wp.ac)/1000).toFixed(0) }}K
              </td>
              <td class="mono" :style="wp.ev - wp.pv >= 0 ? 'color:#22c55e;font-size:12px' : 'color:#ef4444;font-size:12px'">
                {{ wp.ev - wp.pv >= 0 ? '+' : '' }}{{ ((wp.ev - wp.pv)/1000).toFixed(0) }}K
              </td>
              <td>
                <span class="evm-index" :class="(wp.ev/wp.ac) >= 1 ? 'good' : 'bad'">
                  {{ (wp.ev/wp.ac).toFixed(2) }}
                </span>
              </td>
              <td>
                <span class="evm-index" :class="(wp.ev/wp.pv) >= 1 ? 'good' : 'bad'">
                  {{ (wp.ev/wp.pv).toFixed(2) }}
                </span>
              </td>
              <td><span class="status-badge" :class="wp.status">{{ wp.status }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- S-Curve Chart (CSS-based) -->
    <div class="panel">
      <div class="panel-header"><h2>S-Curve — Cumulative Cost (KES '000)</h2></div>
      <div class="s-curve-wrap">
        <div class="s-curve-chart">
          <div class="curve-bars">
            <div class="curve-col" v-for="m in sCurve" :key="m.month">
              <div class="curve-bar-group">
                <div class="curve-bar pv-bar" :style="{ height: (m.pv / maxSCurve * 100) + '%' }" title="PV"></div>
                <div class="curve-bar ev-bar" :style="{ height: (m.ev / maxSCurve * 100) + '%' }" title="EV"></div>
                <div class="curve-bar ac-bar" :style="{ height: (m.ac / maxSCurve * 100) + '%' }" title="AC"></div>
              </div>
              <span class="mono" style="font-size:9px;color:#4b5563;margin-top:4px">{{ m.month }}</span>
            </div>
          </div>
          <div class="curve-legend">
            <span class="legend-item pv">■ PV (Planned)</span>
            <span class="legend-item ev">■ EV (Earned)</span>
            <span class="legend-item ac">■ AC (Actual)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const selectedProject = ref(1)
const projectOptions = [
  { id: 1, name: 'Nairobi Housing — Phase 1'  },
  { id: 2, name: 'Mombasa Port Road'           },
  { id: 3, name: 'Kisumu Commercial Complex'   },
  { id: 4, name: 'Nakuru Ring Road'            },
]

const projectData = ref([
  {
    id: 1, cpi: 0.96, spi: 0.88, pv: 28500000, ev: 25200000, ac: 26250000,
    cv: -1050000, sv: -3300000, bac: 45000000,
    eac: 46875000, etc: 20625000,
    workPackages: [
      { name: 'Substructure Works',   category: 'Structural', bac: 8000000, pv: 8000000, ev: 8000000, ac: 7800000, status: 'completed'   },
      { name: 'Superstructure Frame', category: 'Structural', bac: 12000000,pv: 10000000,ev: 8500000, ac: 9200000, status: 'in-progress' },
      { name: 'Roofing Works',        category: 'Structural', bac: 5000000, pv: 3500000, ev: 2800000, ac: 3100000, status: 'in-progress' },
      { name: 'Electrical Works',     category: 'MEP',        bac: 4500000, pv: 2000000, ev: 1800000, ac: 1750000, status: 'in-progress' },
      { name: 'Plumbing Works',       category: 'MEP',        bac: 3500000, pv: 1500000, ev: 1200000, ac: 1400000, status: 'in-progress' },
      { name: 'Finishing Works',      category: 'Finishing',  bac: 6000000, pv: 1000000, ev: 900000,  ac: 1000000, status: 'planned'     },
    ],
  },
  {
    id: 2, cpi: 1.08, spi: 0.72, pv: 18000000, ev: 13000000, ac: 12050000,
    cv: 950000, sv: -5000000, bac: 32000000,
    eac: 29629629, etc: 17579629,
    workPackages: [
      { name: 'Survey & Design',   category: 'Prelim',    bac: 2000000, pv: 2000000, ev: 2000000, ac: 1900000, status: 'completed'   },
      { name: 'Earthworks',        category: 'Civil',     bac: 6000000, pv: 6000000, ev: 4500000, ac: 4100000, status: 'in-progress' },
      { name: 'Sub-Base Course',   category: 'Civil',     bac: 8000000, pv: 6000000, ev: 4000000, ac: 3700000, status: 'in-progress' },
      { name: 'Base Course',       category: 'Civil',     bac: 8000000, pv: 3000000, ev: 2000000, ac: 1900000, status: 'in-progress' },
      { name: 'Tarmac & Wearing',  category: 'Civil',     bac: 6000000, pv: 1000000, ev: 500000,  ac: 450000,  status: 'planned'     },
      { name: 'Drainage & Kerbs',  category: 'Drainage',  bac: 2000000, pv: 0,       ev: 0,       ac: 0,       status: 'planned'     },
    ],
  },
])

const currentProject = computed(() => projectData.value.find(p => p.id === selectedProject.value) || projectData.value[0])

const sCurve = computed(() => [
  { month: 'Aug',  pv: 1200, ev: 800,  ac: 750  },
  { month: 'Sep',  pv: 3500, ev: 2800, ac: 2600 },
  { month: 'Oct',  pv: 6200, ev: 5100, ac: 5300 },
  { month: 'Nov',  pv: 9800, ev: 8200, ac: 8600 },
  { month: 'Dec',  pv: 14000,ev: 11500,ac: 11800},
  { month: 'Jan',  pv: 18500,ev: 16000,ac: 16500},
  { month: 'Feb',  pv: 24000,ev: 21000,ac: 22000},
  { month: 'Mar',  pv: 29000,ev: null, ac: null  },
  { month: 'Apr',  pv: 33500,ev: null, ac: null  },
  { month: 'May',  pv: 38000,ev: null, ac: null  },
  { month: 'Jun',  pv: 42000,ev: null, ac: null  },
  { month: 'Jul',  pv: 45000,ev: null, ac: null  },
].map(m => ({ ...m, ev: m.ev || 0, ac: m.ac || 0 })))

const maxSCurve = computed(() => Math.max(...sCurve.value.map(m => m.pv)))
const formatKES = (n) => n >= 1000000 ? `KES ${(n / 1000000).toFixed(2)}M` : `KES ${(n / 1000).toFixed(0)}K`
</script>

<style scoped>
@import '/src/assets/progress.css';
.kpi-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.kpi-val { font-size: 28px; font-weight: 800; color: #fff; }

.variance-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 18px; }
.var-card { background: #13161f; border: 1px solid #1e2230; border-radius: 10px; padding: 16px; }
.var-card.positive { border-left: 3px solid #22c55e; }
.var-card.negative { border-left: 3px solid #ef4444; }
.var-card.neutral  { border-left: 3px solid #a855f7; }
.var-label { font-size: 10px; font-family: 'DM Mono', monospace; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.var-val   { font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 4px; }
.var-sub   { font-size: 10px; color: #6b7280; }
.var-card.positive .var-val { color: #22c55e; }
.var-card.negative .var-val { color: #ef4444; }

.evm-index { font-family: 'DM Mono', monospace; font-size: 12px; font-weight: 700; padding: 2px 8px; border-radius: 4px; }
.evm-index.good { background: #0d2818; color: #22c55e; }
.evm-index.bad  { background: #200e0e; color: #ef4444; }

.s-curve-wrap { padding: 8px 0; }
.s-curve-chart { position: relative; }
.curve-bars { display: flex; align-items: flex-end; gap: 6px; height: 160px; padding-bottom: 20px; }
.curve-col  { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; }
.curve-bar-group { flex: 1; width: 100%; display: flex; align-items: flex-end; gap: 2px; }
.curve-bar { flex: 1; border-radius: 2px 2px 0 0; min-height: 2px; }
.pv-bar { background: #f5a623; opacity: 0.7; }
.ev-bar { background: #3b82f6; }
.ac-bar { background: #a855f7; }
.curve-legend { display: flex; gap: 16px; margin-top: 8px; justify-content: center; }
.legend-item { font-family: 'DM Mono', monospace; font-size: 11px; color: #6b7280; }
.legend-item.pv { color: #f5a623; }
.legend-item.ev { color: #3b82f6; }
.legend-item.ac { color: #a855f7; }
</style>