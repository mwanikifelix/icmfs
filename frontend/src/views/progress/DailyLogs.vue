<template>
  <div class="progress-page">
    <div class="page-header">
      <div>
        <span class="page-tag green">PROGRESS · DAILY LOGS</span>
        <h1>Daily Logs</h1>
        <p class="page-sub">Site activity log entries submitted by site engineers and foremen</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary green" @click="showForm = true">+ Add Log Entry</button>
      </div>
    </div>

    <div class="stat-row">
      <div class="stat-card green">
        <div class="stat-val">{{ logs.length }}</div>
        <div class="stat-label">Total Entries Today</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-val">{{ totalWorkers }}</div>
        <div class="stat-label">Workers Logged</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ totalEquipment }}</div>
        <div class="stat-label">Equipment On-Site</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-val">{{ totalMaterials }}</div>
        <div class="stat-label">Material Deliveries</div>
      </div>
    </div>

    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search site, activity or submitted by..." />
      </div>
      <select v-model="filterSite" class="filter-select">
        <option value="">All Sites</option>
        <option v-for="s in siteOptions" :key="s">{{ s }}</option>
      </select>
      <input v-model="filterDate" type="date" class="filter-select" />
      <select v-model="filterWeather" class="filter-select">
        <option value="">All Weather</option>
        <option value="sunny">Sunny</option>
        <option value="cloudy">Cloudy</option>
        <option value="rainy">Rainy</option>
      </select>
    </div>

    <div class="log-list">
      <div class="log-card" v-for="log in filteredLogs" :key="log.id" @click="activeLog = log">
        <div class="log-header">
          <div style="display:flex;align-items:center;gap:10px">
            <div class="weather-icon">{{ weatherIcon(log.weather) }}</div>
            <div>
              <div class="cell-main" style="font-size:14px">{{ log.site }}</div>
              <div class="cell-sub">{{ log.date }} · Submitted by {{ log.submittedBy }}</div>
            </div>
          </div>
          <div style="display:flex;gap:8px;align-items:center">
            <span class="status-badge" :class="log.status">{{ log.status }}</span>
            <span class="log-ref mono">{{ log.ref }}</span>
          </div>
        </div>

        <div class="log-meta-grid">
          <div class="log-meta-item">
            <span class="meta-icon">👷</span>
            <div>
              <div class="meta-val">{{ log.workers }}</div>
              <div class="meta-lbl">Workers</div>
            </div>
          </div>
          <div class="log-meta-item">
            <span class="meta-icon">🚜</span>
            <div>
              <div class="meta-val">{{ log.equipment }}</div>
              <div class="meta-lbl">Equipment</div>
            </div>
          </div>
          <div class="log-meta-item">
            <span class="meta-icon">🧱</span>
            <div>
              <div class="meta-val">{{ log.materials }}</div>
              <div class="meta-lbl">Deliveries</div>
            </div>
          </div>
          <div class="log-meta-item">
            <span class="meta-icon">⏱️</span>
            <div>
              <div class="meta-val">{{ log.hoursWorked }}h</div>
              <div class="meta-lbl">Hours</div>
            </div>
          </div>
        </div>

        <div class="log-activities">
          <div class="activity-tag" v-for="a in log.activities" :key="a">{{ a }}</div>
        </div>

        <div v-if="log.issues" class="log-issue">
          <span>⚠️</span> {{ log.issues }}
        </div>
      </div>
    </div>

    <!-- Detail Drawer -->
    <div class="drawer-overlay" v-if="activeLog" @click.self="activeLog = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#22c55e;display:block;margin-bottom:4px">{{ activeLog.ref }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ activeLog.site }}</h2>
            <div class="cell-sub">{{ activeLog.date }}</div>
          </div>
          <button class="close-btn" @click="activeLog = null">✕</button>
        </div>
        <div class="drawer-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:18px">
            <div v-for="f in drawerFields" :key="f.label">
              <div class="cell-sub" style="text-transform:uppercase">{{ f.label }}</div>
              <div style="font-size:13px;color:#e8e4dc;margin-top:4px">{{ f.value }}</div>
            </div>
          </div>
          <div style="margin-bottom:14px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Activities Completed</div>
            <div style="display:flex;flex-wrap:wrap;gap:6px">
              <div class="activity-tag" v-for="a in activeLog.activities" :key="a">{{ a }}</div>
            </div>
          </div>
          <div v-if="activeLog.remarks" style="margin-bottom:14px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:6px">Remarks</div>
            <p style="font-size:13px;color:#9ca3af;line-height:1.6">{{ activeLog.remarks }}</p>
          </div>
          <div v-if="activeLog.issues" class="log-issue">
            <span>⚠️</span> {{ activeLog.issues }}
          </div>
        </div>
      </div>
    </div>

    <!-- Add Log Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>📋 Add Daily Log Entry</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Site *</label>
              <select v-model="form.site">
                <option value="">Select site...</option>
                <option v-for="s in siteOptions" :key="s">{{ s }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Date *</label>
              <input type="date" v-model="form.date" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Workers on Site</label>
              <input type="number" v-model="form.workers" placeholder="0" />
            </div>
            <div class="form-group">
              <label>Equipment On-Site</label>
              <input type="number" v-model="form.equipment" placeholder="0" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Hours Worked</label>
              <input type="number" v-model="form.hoursWorked" placeholder="0" />
            </div>
            <div class="form-group">
              <label>Weather</label>
              <select v-model="form.weather">
                <option value="sunny">☀️ Sunny</option>
                <option value="cloudy">⛅ Cloudy</option>
                <option value="rainy">🌧️ Rainy</option>
              </select>
            </div>
          </div>
          <div class="form-group full">
            <label>Activities Completed</label>
            <textarea v-model="form.activities" rows="2" placeholder="e.g. Roofing, Plastering, Plumbing rough-in..."></textarea>
          </div>
          <div class="form-group full">
            <label>Issues / Remarks</label>
            <textarea v-model="form.issues" rows="2" placeholder="Any issues or observations..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary green" @click="submitLog">Submit Log</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const search = ref('')
const filterSite = ref('')
const filterDate = ref('')
const filterWeather = ref('')
const showForm = ref(false)
const activeLog = ref(null)
const siteOptions = ['Nairobi Housing — Phase 1', 'Mombasa Port Road', 'Kisumu Commercial Complex', 'Nakuru Ring Road']
const form = ref({ site: '', date: '', workers: '', equipment: '', hoursWorked: '', weather: 'sunny', activities: '', issues: '' })

const logs = ref([
  { id: 1, ref: 'LOG-2025-0218-01', site: 'Nairobi Housing — Phase 1',  date: '2025-02-18', submittedBy: 'Eng. Kariuki', workers: 45, equipment: 6, materials: 3, hoursWorked: 9, weather: 'sunny',  activities: ['Roof Truss Installation', 'Plastering Floor 4', 'Window Frame Fixing'], issues: null, remarks: 'Good progress on truss installation. Completed 80% of Block A roofing.', status: 'completed' },
  { id: 2, ref: 'LOG-2025-0218-02', site: 'Mombasa Port Road',          date: '2025-02-18', submittedBy: 'Eng. Oduya',   workers: 32, equipment: 8, materials: 5, hoursWorked: 8, weather: 'cloudy', activities: ['Base Course Compaction', 'Material Delivery — Ballast', 'Survey Work'], issues: 'Equipment breakdown: Roller CM-004 out of service from 2pm', remarks: 'Ballast delivery delayed by 2 hrs due to traffic.', status: 'in-progress' },
  { id: 3, ref: 'LOG-2025-0218-03', site: 'Kisumu Commercial Complex',  date: '2025-02-18', submittedBy: 'Eng. Achieng', workers: 28, equipment: 4, materials: 2, hoursWorked: 8, weather: 'sunny',  activities: ['Column Casting — Grids E-H', 'Formwork Removal Floor 2', 'Rebar Fixing Floor 3'], issues: null, remarks: 'Concrete mix ratios verified and within spec.', status: 'completed' },
  { id: 4, ref: 'LOG-2025-0217-01', site: 'Nakuru Ring Road',           date: '2025-02-17', submittedBy: 'Eng. Mwangi',  workers: 18, equipment: 5, materials: 4, hoursWorked: 7, weather: 'rainy',  activities: ['Road Markings Section B3', 'Guardrail Installation', 'Drainage Clearing'], issues: 'Work suspended 1.5hrs due to heavy rain at 14:00', remarks: 'Weather impacted productivity. Will compensate Saturday.', status: 'completed' },
])

const filteredLogs = computed(() => logs.value.filter(l =>
  (!search.value || l.site.toLowerCase().includes(search.value.toLowerCase()) || l.submittedBy.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterSite.value || l.site === filterSite.value)
  && (!filterDate.value || l.date === filterDate.value)
  && (!filterWeather.value || l.weather === filterWeather.value)
))

const totalWorkers   = computed(() => logs.value.filter(l => l.date === '2025-02-18').reduce((a, b) => a + b.workers, 0))
const totalEquipment = computed(() => logs.value.filter(l => l.date === '2025-02-18').reduce((a, b) => a + b.equipment, 0))
const totalMaterials = computed(() => logs.value.filter(l => l.date === '2025-02-18').reduce((a, b) => a + b.materials, 0))

const drawerFields = computed(() => activeLog.value ? [
  { label: 'Submitted By', value: activeLog.value.submittedBy },
  { label: 'Weather',      value: weatherLabel(activeLog.value.weather) },
  { label: 'Workers',      value: activeLog.value.workers },
  { label: 'Equipment',    value: activeLog.value.equipment },
  { label: 'Hours Worked', value: activeLog.value.hoursWorked + 'h' },
  { label: 'Deliveries',   value: activeLog.value.materials },
] : [])

function weatherIcon(w)  { return w === 'sunny' ? '☀️' : w === 'rainy' ? '🌧️' : '⛅' }
function weatherLabel(w) { return w === 'sunny' ? '☀️ Sunny' : w === 'rainy' ? '🌧️ Rainy' : '⛅ Cloudy' }

function submitLog() {
  logs.value.unshift({
    id: Date.now(), ref: `LOG-${form.value.date}-0${logs.value.length + 1}`,
    ...form.value, workers: Number(form.value.workers), equipment: Number(form.value.equipment),
    materials: 0, hoursWorked: Number(form.value.hoursWorked),
    activities: form.value.activities.split(',').map(a => a.trim()),
    submittedBy: 'Current User', status: 'in-progress'
  })
  showForm.value = false
  form.value = { site: '', date: '', workers: '', equipment: '', hoursWorked: '', weather: 'sunny', activities: '', issues: '' }
}
</script>

<style scoped>
@import '/src/assets/progress.css';
.log-list { display: flex; flex-direction: column; gap: 12px; }
.log-card { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 18px 20px; cursor: pointer; transition: border-color 0.2s; }
.log-card:hover { border-color: #22c55e; }
.log-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }
.weather-icon { width: 38px; height: 38px; background: #0d0f14; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.log-ref { font-size: 10px; color: #22c55e; }
.log-meta-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 12px; padding: 12px; background: #0d0f14; border-radius: 8px; }
.log-meta-item { display: flex; align-items: center; gap: 8px; }
.meta-icon { font-size: 18px; }
.meta-val  { font-size: 16px; font-weight: 800; color: #fff; }
.meta-lbl  { font-size: 10px; color: #4b5563; text-transform: uppercase; font-family: 'DM Mono', monospace; }
.log-activities { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.activity-tag { font-size: 11px; font-family: 'DM Mono', monospace; padding: 3px 10px; border-radius: 4px; background: #1e2230; color: #9ca3af; }
.log-issue { font-size: 12px; color: #f59e0b; background: #1f1a08; border: 1px solid #92400e; border-radius: 6px; padding: 8px 12px; display: flex; gap: 8px; align-items: flex-start; }
</style>