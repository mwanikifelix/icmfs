<template>
  <div class="safety-dashboard">
    <!-- Header -->
    <div class="dash-header">
      <div class="header-left">
        <span class="header-tag">ICMFS — SAFETY MODULE</span>
        <h1>Safety Dashboard</h1>
        <p class="header-sub">Real-time safety monitoring across all active construction sites</p>
      </div>
      <div class="header-right">
        <div class="site-selector">
          <select v-model="selectedSite">
            <option value="all">All Sites</option>
            <option v-for="site in sites" :key="site.id" :value="site.id">{{ site.name }}</option>
          </select>
        </div>
        <div class="live-badge">
          <span class="pulse-dot"></span> LIVE
        </div>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card" v-for="kpi in kpiCards" :key="kpi.label" :class="kpi.status">
        <div class="kpi-icon">{{ kpi.icon }}</div>
        <div class="kpi-body">
          <div class="kpi-value">{{ kpi.value }}</div>
          <div class="kpi-label">{{ kpi.label }}</div>
          <div class="kpi-trend" :class="kpi.trendDir">
            {{ kpi.trend }}
          </div>
        </div>
        <div class="kpi-bar">
          <div class="kpi-fill" :style="{ width: kpi.pct + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Middle row -->
    <div class="mid-row">
      <!-- Risk Heatmap by Site -->
      <div class="panel risk-heatmap">
        <div class="panel-header">
          <h2>Risk Level by Site</h2>
          <span class="panel-badge">AI Predicted</span>
        </div>
        <div class="heatmap-list">
          <div class="heatmap-row" v-for="site in siteRisks" :key="site.name">
            <div class="site-info">
              <span class="site-name">{{ site.name }}</span>
              <span class="site-loc">{{ site.location }}</span>
            </div>
            <div class="risk-bar-wrap">
              <div class="risk-bar" :class="site.level">
                <div class="risk-fill" :style="{ width: site.score + '%' }"></div>
              </div>
              <span class="risk-score">{{ site.score }}%</span>
            </div>
            <div class="risk-badge" :class="site.level">{{ site.level.toUpperCase() }}</div>
          </div>
        </div>
      </div>

      <!-- Recent Activity Feed -->
      <div class="panel activity-feed">
        <div class="panel-header">
          <h2>Recent Safety Events</h2>
          <button class="view-all-btn" @click="$router.push('/safety/incidents')">View All</button>
        </div>
        <div class="feed-list">
          <div class="feed-item" v-for="event in recentEvents" :key="event.id" :class="event.type">
            <div class="feed-icon">{{ event.icon }}</div>
            <div class="feed-body">
              <div class="feed-title">{{ event.title }}</div>
              <div class="feed-meta">{{ event.site }} · {{ event.time }}</div>
            </div>
            <div class="feed-type-badge" :class="event.type">{{ event.type }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom row -->
    <div class="bottom-row">
      <!-- Monthly Incident Trend -->
      <div class="panel chart-panel">
        <div class="panel-header">
          <h2>Incident Trend (6 Months)</h2>
        </div>
        <div class="bar-chart">
          <div class="chart-bars">
            <div class="chart-col" v-for="month in monthlyData" :key="month.label">
              <div class="bar-stack">
                <div class="bar-seg critical" :style="{ height: (month.critical / maxMonthly * 100) + '%' }" :title="`Critical: ${month.critical}`"></div>
                <div class="bar-seg high" :style="{ height: (month.high / maxMonthly * 100) + '%' }" :title="`High: ${month.high}`"></div>
                <div class="bar-seg medium" :style="{ height: (month.medium / maxMonthly * 100) + '%' }" :title="`Medium: ${month.medium}`"></div>
              </div>
              <span class="bar-label">{{ month.label }}</span>
            </div>
          </div>
          <div class="chart-legend">
            <span class="legend-item critical">■ Critical</span>
            <span class="legend-item high">■ High</span>
            <span class="legend-item medium">■ Medium</span>
          </div>
        </div>
      </div>

      <!-- Audit Compliance -->
      <div class="panel compliance-panel">
        <div class="panel-header">
          <h2>Audit Compliance</h2>
          <span class="panel-badge">This Month</span>
        </div>
        <div class="compliance-list">
          <div class="compliance-item" v-for="item in complianceData" :key="item.category">
            <div class="comp-label">{{ item.category }}</div>
            <div class="comp-track">
              <div class="comp-fill" :style="{ width: item.pct + '%' }" :class="item.status"></div>
            </div>
            <div class="comp-pct" :class="item.status">{{ item.pct }}%</div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="panel quick-actions">
        <div class="panel-header">
          <h2>Quick Actions</h2>
        </div>
        <div class="action-grid">
          <button class="action-btn" @click="$router.push('/safety/incidents/new')">
            <span class="action-icon">🚨</span>
            <span>Report Incident</span>
          </button>
          <button class="action-btn" @click="$router.push('/safety/audits/new')">
            <span class="action-icon">📋</span>
            <span>Schedule Audit</span>
          </button>
          <button class="action-btn" @click="$router.push('/safety/risks/new')">
            <span class="action-icon">⚠️</span>
            <span>Log Risk</span>
          </button>
          <button class="action-btn" @click="exportReport">
            <span class="action-icon">📊</span>
            <span>Export Report</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const selectedSite = ref('all')

const sites = ref([
  { id: 1, name: 'Nairobi Affordable Housing — Phase 1' },
  { id: 2, name: 'Mombasa Infrastructure Project' },
  { id: 3, name: 'Kisumu Commercial Complex' },
])

const kpiCards = ref([
  { label: 'Open Incidents', value: 7, icon: '🚨', status: 'danger', trend: '↑ 2 from last week', trendDir: 'up', pct: 35 },
  { label: 'Audits This Month', value: 12, icon: '📋', status: 'info', trend: '✓ 8 completed', trendDir: 'good', pct: 67 },
  { label: 'High Risk Items', value: 4, icon: '⚠️', status: 'warning', trend: '↓ 1 resolved', trendDir: 'down', pct: 40 },
  { label: 'Safety Score', value: '83%', icon: '🛡️', status: 'good', trend: '↑ 5% this month', trendDir: 'good', pct: 83 },
])

const siteRisks = ref([
  { name: 'Nairobi Housing — Phase 1', location: 'Nairobi', score: 72, level: 'high' },
  { name: 'Mombasa Infrastructure', location: 'Mombasa', score: 45, level: 'medium' },
  { name: 'Kisumu Commercial', location: 'Kisumu', score: 88, level: 'critical' },
  { name: 'Nakuru Road Project', location: 'Nakuru', score: 23, level: 'low' },
])

const recentEvents = ref([
  { id: 1, icon: '🚨', title: 'Scaffolding collapse near Block C', site: 'Nairobi Housing', time: '2h ago', type: 'incident' },
  { id: 2, icon: '✅', title: 'Fire safety audit completed', site: 'Mombasa Infra', time: '5h ago', type: 'audit' },
  { id: 3, icon: '⚠️', title: 'Electrical hazard flagged — Level 3', site: 'Kisumu Commercial', time: '1d ago', type: 'risk' },
  { id: 4, icon: '📋', title: 'PPE compliance inspection passed', site: 'Nakuru Road', time: '1d ago', type: 'audit' },
  { id: 5, icon: '🚨', title: 'Worker injury reported — minor', site: 'Nairobi Housing', time: '2d ago', type: 'incident' },
])

const monthlyData = ref([
  { label: 'SEP', critical: 3, high: 5, medium: 8 },
  { label: 'OCT', critical: 2, high: 7, medium: 6 },
  { label: 'NOV', critical: 5, high: 4, medium: 9 },
  { label: 'DEC', critical: 1, high: 3, medium: 5 },
  { label: 'JAN', critical: 4, high: 6, medium: 7 },
  { label: 'FEB', critical: 2, high: 4, medium: 6 },
])

const maxMonthly = computed(() => {
  return Math.max(...monthlyData.value.map(m => m.critical + m.high + m.medium))
})

const complianceData = ref([
  { category: 'PPE Usage', pct: 91, status: 'good' },
  { category: 'Fire Safety', pct: 75, status: 'warning' },
  { category: 'Electrical Safety', pct: 60, status: 'warning' },
  { category: 'First Aid Readiness', pct: 95, status: 'good' },
  { category: 'Emergency Exits', pct: 48, status: 'danger' },
])

function exportReport() {
  alert('Generating safety report PDF...')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.safety-dashboard {
  font-family: 'Syne', sans-serif;
  background: #0d0f14;
  color: #e8e4dc;
  min-height: 100vh;
  padding: 28px 32px;
}

/* HEADER */
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #1e2230;
}
.header-tag {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 2px;
  color: #f5a623;
  text-transform: uppercase;
  display: block;
  margin-bottom: 6px;
}
.dash-header h1 { font-size: 32px; font-weight: 800; color: #fff; }
.header-sub { font-size: 13px; color: #6b7280; margin-top: 4px; }
.header-right { display: flex; align-items: center; gap: 16px; }
.site-selector select {
  background: #161922;
  border: 1px solid #2a2f3e;
  color: #e8e4dc;
  padding: 8px 14px;
  border-radius: 6px;
  font-family: 'Syne', sans-serif;
  font-size: 13px;
  cursor: pointer;
}
.live-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #0d1f12;
  border: 1px solid #1a3d22;
  color: #4ade80;
  padding: 6px 12px;
  border-radius: 20px;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  letter-spacing: 1px;
}
.pulse-dot {
  width: 7px; height: 7px;
  background: #4ade80;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.3); }
}

/* KPI GRID */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.kpi-card {
  background: #13161f;
  border: 1px solid #1e2230;
  border-radius: 12px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #f5a623; }
.kpi-card.danger  { border-left: 3px solid #ef4444; }
.kpi-card.warning { border-left: 3px solid #f59e0b; }
.kpi-card.good    { border-left: 3px solid #22c55e; }
.kpi-card.info    { border-left: 3px solid #3b82f6; }
.kpi-icon { font-size: 24px; margin-bottom: 10px; }
.kpi-value { font-size: 36px; font-weight: 800; color: #fff; line-height: 1; }
.kpi-label { font-size: 12px; color: #6b7280; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-trend { font-size: 11px; margin-top: 6px; font-family: 'DM Mono', monospace; }
.kpi-trend.up   { color: #ef4444; }
.kpi-trend.down { color: #22c55e; }
.kpi-trend.good { color: #22c55e; }
.kpi-bar {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 3px;
  background: #1e2230;
}
.kpi-fill {
  height: 100%;
  background: #f5a623;
  border-radius: 0 2px 2px 0;
  transition: width 0.8s ease;
}

/* MID ROW */
.mid-row {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

/* PANEL BASE */
.panel {
  background: #13161f;
  border: 1px solid #1e2230;
  border-radius: 12px;
  padding: 20px;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}
.panel-header h2 { font-size: 15px; font-weight: 700; color: #fff; }
.panel-badge {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  background: #1a1f2e;
  color: #f5a623;
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 0.5px;
}
.view-all-btn {
  background: none;
  border: 1px solid #2a2f3e;
  color: #9ca3af;
  padding: 4px 10px;
  border-radius: 5px;
  font-size: 11px;
  cursor: pointer;
  font-family: 'Syne', sans-serif;
  transition: all 0.2s;
}
.view-all-btn:hover { border-color: #f5a623; color: #f5a623; }

/* RISK HEATMAP */
.heatmap-list { display: flex; flex-direction: column; gap: 12px; }
.heatmap-row { display: flex; align-items: center; gap: 12px; }
.site-info { flex: 0 0 180px; }
.site-name { display: block; font-size: 13px; color: #e8e4dc; font-weight: 600; }
.site-loc { font-size: 11px; color: #4b5563; font-family: 'DM Mono', monospace; }
.risk-bar-wrap { flex: 1; display: flex; align-items: center; gap: 8px; }
.risk-bar {
  flex: 1;
  height: 6px;
  background: #1e2230;
  border-radius: 3px;
  overflow: hidden;
}
.risk-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 1s ease;
}
.risk-bar.low    .risk-fill { background: #22c55e; }
.risk-bar.medium .risk-fill { background: #f59e0b; }
.risk-bar.high   .risk-fill { background: #ef4444; }
.risk-bar.critical .risk-fill { background: #dc2626; box-shadow: 0 0 8px #dc2626; }
.risk-score { font-family: 'DM Mono', monospace; font-size: 11px; color: #6b7280; width: 32px; }
.risk-badge {
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  font-weight: 500;
  padding: 2px 7px;
  border-radius: 3px;
  letter-spacing: 0.5px;
}
.risk-badge.low      { background: #0d2818; color: #22c55e; }
.risk-badge.medium   { background: #1f1a08; color: #f59e0b; }
.risk-badge.high     { background: #200e0e; color: #ef4444; }
.risk-badge.critical { background: #2a0808; color: #dc2626; }

/* ACTIVITY FEED */
.feed-list { display: flex; flex-direction: column; gap: 10px; }
.feed-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #0d0f14;
  border-radius: 8px;
  border: 1px solid #1a1e2a;
  transition: border-color 0.2s;
}
.feed-item:hover { border-color: #2a2f3e; }
.feed-icon { font-size: 18px; }
.feed-body { flex: 1; }
.feed-title { font-size: 12px; color: #d1d5db; font-weight: 600; }
.feed-meta { font-size: 10px; color: #4b5563; margin-top: 2px; font-family: 'DM Mono', monospace; }
.feed-type-badge {
  font-size: 9px;
  font-family: 'DM Mono', monospace;
  padding: 2px 7px;
  border-radius: 3px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.feed-type-badge.incident { background: #200e0e; color: #ef4444; }
.feed-type-badge.audit    { background: #0d1a2e; color: #3b82f6; }
.feed-type-badge.risk     { background: #1f1a08; color: #f59e0b; }

/* BOTTOM ROW */
.bottom-row {
  display: grid;
  grid-template-columns: 1.4fr 1fr 0.8fr;
  gap: 16px;
}

/* BAR CHART */
.bar-chart { padding-top: 8px; }
.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 120px;
  padding-bottom: 8px;
}
.chart-col { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; }
.bar-stack {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column-reverse;
  border-radius: 4px;
  overflow: hidden;
  gap: 1px;
}
.bar-seg { width: 100%; min-height: 2px; transition: height 0.8s ease; }
.bar-seg.critical { background: #dc2626; }
.bar-seg.high     { background: #f59e0b; }
.bar-seg.medium   { background: #3b82f6; }
.bar-label { font-family: 'DM Mono', monospace; font-size: 10px; color: #4b5563; margin-top: 6px; }
.chart-legend { display: flex; gap: 16px; margin-top: 12px; padding-top: 12px; border-top: 1px solid #1e2230; }
.legend-item { font-family: 'DM Mono', monospace; font-size: 11px; }
.legend-item.critical { color: #dc2626; }
.legend-item.high     { color: #f59e0b; }
.legend-item.medium   { color: #3b82f6; }

/* COMPLIANCE */
.compliance-list { display: flex; flex-direction: column; gap: 12px; }
.compliance-item { display: flex; align-items: center; gap: 10px; }
.comp-label { font-size: 12px; color: #9ca3af; flex: 0 0 160px; }
.comp-track { flex: 1; height: 6px; background: #1e2230; border-radius: 3px; overflow: hidden; }
.comp-fill { height: 100%; border-radius: 3px; transition: width 1s ease; }
.comp-fill.good    { background: #22c55e; }
.comp-fill.warning { background: #f59e0b; }
.comp-fill.danger  { background: #ef4444; }
.comp-pct { font-family: 'DM Mono', monospace; font-size: 11px; width: 36px; text-align: right; }
.comp-pct.good    { color: #22c55e; }
.comp-pct.warning { color: #f59e0b; }
.comp-pct.danger  { color: #ef4444; }

/* QUICK ACTIONS */
.action-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 10px;
  background: #0d0f14;
  border: 1px solid #1e2230;
  border-radius: 10px;
  color: #9ca3af;
  font-family: 'Syne', sans-serif;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}
.action-btn:hover { background: #161922; border-color: #f5a623; color: #f5a623; }
.action-icon { font-size: 22px; }

/* RESPONSIVE */
@media (max-width: 1200px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .mid-row, .bottom-row { grid-template-columns: 1fr; }
}
</style>