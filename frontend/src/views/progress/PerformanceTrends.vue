<template>
  <div class="progress-page">
    <div class="page-header">
      <div>
        <span class="page-tag cyan">PROGRESS · PERFORMANCE TRENDS</span>
        <h1>Performance Trends</h1>
        <p class="page-sub">Labour productivity, schedule adherence and quality metrics over time</p>
      </div>
      <div style="display:flex;gap:10px">
        <select v-model="selectedPeriod" class="filter-select">
          <option value="3m">Last 3 Months</option>
          <option value="6m">Last 6 Months</option>
          <option value="1y">Last 12 Months</option>
        </select>
        <button class="btn-export">📥 Export</button>
      </div>
    </div>

    <!-- KPIs -->
    <div class="kpi-row">
      <div class="kpi cyan">
        <div class="kpi-top"><span>⚡</span><span class="mono" style="font-size:10px;color:#06b6d4">↑ 6% vs last month</span></div>
        <div class="kpi-val">82%</div>
        <div class="kpi-label">Labour Productivity</div>
      </div>
      <div class="kpi green">
        <div class="kpi-top"><span>📅</span><span class="mono" style="font-size:10px;color:#22c55e">Improved</span></div>
        <div class="kpi-val">74%</div>
        <div class="kpi-label">Schedule Adherence</div>
      </div>
      <div class="kpi amber">
        <div class="kpi-top"><span>🏗️</span><span class="mono" style="font-size:10px;color:#f5a623">Avg this week</span></div>
        <div class="kpi-val">118</div>
        <div class="kpi-label">Daily Workers (Avg)</div>
      </div>
      <div class="kpi blue">
        <div class="kpi-top"><span>🔧</span><span class="mono" style="font-size:10px;color:#3b82f6">↑ 3 units</span></div>
        <div class="kpi-val">23</div>
        <div class="kpi-label">Equipment Utilisation</div>
      </div>
      <div class="kpi danger">
        <div class="kpi-top"><span>🔴</span><span class="mono" style="font-size:10px;color:#ef4444">↓ 2 this week</span></div>
        <div class="kpi-val">4</div>
        <div class="kpi-label">Delays Recorded</div>
      </div>
    </div>

    <div class="trend-grid">
      <!-- Labour Productivity Chart -->
      <div class="panel">
        <div class="panel-header"><h2>Labour Productivity (%)</h2></div>
        <div class="bar-chart-area">
          <div class="bar-col" v-for="d in productivityTrend" :key="d.week">
            <div class="bar-container">
              <div class="bar-fill-trend" :class="d.val >= 80 ? 'good' : d.val >= 65 ? 'warn' : 'bad'" :style="{ height: d.val + '%' }"></div>
            </div>
            <span class="bar-lbl mono">{{ d.week }}</span>
            <span class="bar-val-lbl mono" :class="d.val >= 80 ? 'text-green' : d.val >= 65 ? 'text-amber' : 'text-red'">{{ d.val }}%</span>
          </div>
        </div>
      </div>

      <!-- Schedule Adherence -->
      <div class="panel">
        <div class="panel-header"><h2>Schedule Adherence (%)</h2></div>
        <div class="bar-chart-area">
          <div class="bar-col" v-for="d in scheduleTrend" :key="d.week">
            <div class="bar-container">
              <div class="bar-fill-trend blue" :style="{ height: d.val + '%' }"></div>
            </div>
            <span class="bar-lbl mono">{{ d.week }}</span>
            <span class="bar-val-lbl mono text-blue">{{ d.val }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Project-by-Project Trend Table -->
    <div class="panel" style="margin-top:16px;margin-bottom:16px">
      <div class="panel-header"><h2>Project Performance Comparison</h2></div>
      <div class="table-wrap" style="margin-bottom:0">
        <table class="data-table">
          <thead>
            <tr>
              <th>Project</th>
              <th>Progress %</th>
              <th>Productivity</th>
              <th>Schedule</th>
              <th>Quality Score</th>
              <th>Delays (days)</th>
              <th>Workers Avg</th>
              <th>Trend</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in projectPerformance" :key="p.id" class="table-row">
              <td>
                <div class="cell-main">{{ p.name }}</div>
                <div class="cell-sub">{{ p.county }}</div>
              </td>
              <td style="min-width:120px">
                <div class="prog-bar-wrap">
                  <div class="prog-bar"><div class="prog-fill" :class="p.color" :style="{ width: p.progress + '%' }"></div></div>
                  <span class="prog-pct">{{ p.progress }}%</span>
                </div>
              </td>
              <td>
                <span class="perf-badge" :class="p.productivity >= 80 ? 'good' : p.productivity >= 65 ? 'avg' : 'poor'">
                  {{ p.productivity }}%
                </span>
              </td>
              <td>
                <span class="perf-badge" :class="p.schedule >= 80 ? 'good' : p.schedule >= 65 ? 'avg' : 'poor'">
                  {{ p.schedule }}%
                </span>
              </td>
              <td>
                <span class="perf-badge" :class="p.quality >= 85 ? 'good' : p.quality >= 70 ? 'avg' : 'poor'">
                  {{ p.quality }}/100
                </span>
              </td>
              <td>
                <span :style="p.delays > 5 ? 'color:#ef4444;font-weight:700' : 'color:#9ca3af'" class="mono" style="font-size:12px">
                  {{ p.delays }} days
                </span>
              </td>
              <td style="font-size:13px;font-weight:700;color:#e8e4dc">{{ p.avgWorkers }}</td>
              <td>
                <span class="trend-arrow" :class="p.trend">{{ p.trend === 'up' ? '↑' : p.trend === 'down' ? '↓' : '→' }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Issue Heatmap -->
    <div class="panel">
      <div class="panel-header"><h2>Delay Causes — This Month</h2></div>
      <div class="heatmap-list">
        <div class="heatmap-item" v-for="cause in delayCauses" :key="cause.name">
          <div class="heat-left">
            <div class="heat-icon">{{ cause.icon }}</div>
            <div>
              <div class="cell-main">{{ cause.name }}</div>
              <div class="cell-sub">{{ cause.incidents }} incidents</div>
            </div>
          </div>
          <div class="heat-right">
            <div class="prog-bar-wrap" style="width:200px">
              <div class="prog-bar"><div class="prog-fill" :class="cause.color" :style="{ width: (cause.incidents / maxCause * 100) + '%' }"></div></div>
              <span class="prog-pct">{{ cause.days }} days lost</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const selectedPeriod = ref('6m')

const productivityTrend = ref([
  { week: 'W1', val: 72 }, { week: 'W2', val: 68 }, { week: 'W3', val: 75 },
  { week: 'W4', val: 71 }, { week: 'W5', val: 78 }, { week: 'W6', val: 82 },
  { week: 'W7', val: 79 }, { week: 'W8', val: 84 },
])
const scheduleTrend = ref([
  { week: 'W1', val: 65 }, { week: 'W2', val: 60 }, { week: 'W3', val: 68 },
  { week: 'W4', val: 72 }, { week: 'W5', val: 70 }, { week: 'W6', val: 74 },
  { week: 'W7', val: 76 }, { week: 'W8', val: 74 },
])

const projectPerformance = ref([
  { id: 1, name: 'Nairobi Housing — Phase 1', county: 'Nairobi',  progress: 68, productivity: 84, schedule: 72, quality: 88, delays: 8,  avgWorkers: 142, color: 'green',  trend: 'up'   },
  { id: 2, name: 'Mombasa Port Road',          county: 'Mombasa', progress: 42, productivity: 71, schedule: 58, quality: 82, delays: 18, avgWorkers: 98,  color: 'red',    trend: 'down' },
  { id: 3, name: 'Kisumu Commercial Complex',  county: 'Kisumu',  progress: 55, productivity: 78, schedule: 75, quality: 90, delays: 5,  avgWorkers: 76,  color: 'amber',  trend: 'up'   },
  { id: 4, name: 'Nakuru Ring Road',           county: 'Nakuru',  progress: 80, productivity: 91, schedule: 88, quality: 94, delays: 2,  avgWorkers: 54,  color: 'blue',   trend: 'up'   },
])

const delayCauses = ref([
  { icon: '🌧️', name: 'Adverse Weather',        incidents: 8,  days: 12, color: 'blue'   },
  { icon: '🚜', name: 'Equipment Breakdown',    incidents: 6,  days: 9,  color: 'amber'  },
  { icon: '📦', name: 'Material Delay',         incidents: 5,  days: 7,  color: 'purple' },
  { icon: '👷', name: 'Labour Shortage',        incidents: 4,  days: 6,  color: 'cyan'   },
  { icon: '📋', name: 'Design / Change Orders', incidents: 3,  days: 5,  color: 'red'    },
  { icon: '🏛️', name: 'Permit / Approval Delay',incidents: 2, days: 4,  color: 'warn'   },
])

const maxCause = computed(() => Math.max(...delayCauses.value.map(c => c.incidents)))
</script>

<style scoped>
@import '/src/assets/progress.css';
.kpi-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }

.trend-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.bar-chart-area { display: flex; align-items: flex-end; gap: 8px; height: 140px; padding-bottom: 22px; }
.bar-col { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; }
.bar-container { flex: 1; width: 100%; display: flex; align-items: flex-end; }
.bar-fill-trend { width: 100%; border-radius: 4px 4px 0 0; transition: height 0.6s ease; min-height: 4px; }
.bar-fill-trend.good { background: linear-gradient(to top, #22c55e, #22c55e55); }
.bar-fill-trend.warn { background: linear-gradient(to top, #f59e0b, #f59e0b55); }
.bar-fill-trend.bad  { background: linear-gradient(to top, #ef4444, #ef444455); }
.bar-fill-trend.blue { background: linear-gradient(to top, #3b82f6, #3b82f655); }
.bar-lbl     { font-size: 9px; color: #4b5563; margin-top: 4px; }
.bar-val-lbl { font-size: 9px; }
.text-green { color: #22c55e; }
.text-amber { color: #f59e0b; }
.text-red   { color: #ef4444; }
.text-blue  { color: #3b82f6; }

.perf-badge { font-family: 'DM Mono', monospace; font-size: 11px; padding: 3px 8px; border-radius: 4px; font-weight: 700; }
.perf-badge.good { background: #11a34b; color: #22c55e; }
.perf-badge.avg  { background: #c59d0a; color: #f59e0b; }
.perf-badge.poor { background: #1a2bc2; color: #ef4444; }

.trend-arrow { font-size: 16px; font-weight: 800; }
.trend-arrow.up   { color: #22c55e; }
.trend-arrow.down { color: #ef4444; }
.trend-arrow.flat { color: #6b7280; }

.heatmap-list { display: flex; flex-direction: column; gap: 12px; }
.heatmap-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; background: #0d0f14; border-radius: 8px; border: 1px solid #1a1e2a; }
.heat-left { display: flex; align-items: center; gap: 10px; }
.heat-icon { font-size: 20px; width: 36px; text-align: center; }
.heat-right { display: flex; align-items: center; }
</style>