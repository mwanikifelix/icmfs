<template>
  <div class="progress-page">
    <div class="page-header">
      <div>
        <span class="page-tag blue">PROGRESS · DAILY REPORTS</span>
        <h1>Daily Reports</h1>
        <p class="page-sub">Compiled end-of-day reports submitted per project for management review</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export PDF</button>
        <button class="btn-primary blue" @click="showForm = true">+ New Report</button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.key" :class="['tab', activeTab === tab.key ? 'active' : '']" @click="activeTab = tab.key">
        {{ tab.label }} <span class="mono" style="font-size:10px;margin-left:4px;color:#4b5563">({{ tab.count }})</span>
      </button>
    </div>

    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search project or submitted by..." />
      </div>
      <select v-model="filterProject" class="filter-select">
        <option value="">All Projects</option>
        <option v-for="p in projectOptions" :key="p">{{ p }}</option>
      </select>
      <input v-model="filterDate" type="date" class="filter-select" />
    </div>

    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Report Ref</th><th>Project</th><th>Date</th><th>Submitted By</th>
            <th>Activities Summary</th><th>Workers</th><th>Progress</th><th>Status</th><th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in filteredReports" :key="r.id" class="table-row">
            <td class="cell-ref" style="color:#3b82f6">{{ r.ref }}</td>
            <td>
              <div class="cell-main">{{ r.project }}</div>
              <div class="cell-sub">{{ r.site }}</div>
            </td>
            <td class="cell-date">{{ r.date }}</td>
            <td>
              <div class="cell-main">{{ r.submittedBy }}</div>
              <div class="cell-sub">{{ r.role }}</div>
            </td>
            <td class="cell-muted" style="max-width:200px;font-size:11px">{{ r.summary }}</td>
            <td style="font-size:13px;font-weight:700;color:#fff;text-align:center">{{ r.workers }}</td>
            <td style="min-width:120px">
              <div class="prog-bar-wrap">
                <div class="prog-bar"><div class="prog-fill" :class="r.color" :style="{ width: r.progress + '%' }"></div></div>
                <span class="prog-pct">{{ r.progress }}%</span>
              </div>
            </td>
            <td><span class="status-badge" :class="r.status">{{ r.status }}</span></td>
            <td>
              <button class="btn-view" @click="activeReport = r">View</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail Drawer -->
    <div class="drawer-overlay" v-if="activeReport" @click.self="activeReport = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#3b82f6;display:block;margin-bottom:4px">{{ activeReport.ref }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ activeReport.project }}</h2>
            <div class="cell-sub">{{ activeReport.date }} · {{ activeReport.submittedBy }}</div>
          </div>
          <button class="close-btn" @click="activeReport = null">✕</button>
        </div>
        <div class="drawer-body">
          <!-- Progress -->
          <div style="margin-bottom:18px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Site Progress Today</div>
            <div class="prog-bar-wrap">
              <div class="prog-bar" style="height:10px"><div class="prog-fill" :class="activeReport.color" :style="{ width: activeReport.progress + '%' }"></div></div>
              <span style="font-family:'DM Mono',monospace;font-size:14px;font-weight:700;color:#fff">{{ activeReport.progress }}%</span>
            </div>
          </div>
          <!-- Details -->
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:18px">
            <div v-for="f in reportDrawerFields" :key="f.label">
              <div class="cell-sub" style="text-transform:uppercase">{{ f.label }}</div>
              <div style="font-size:13px;color:#e8e4dc;margin-top:4px">{{ f.value }}</div>
            </div>
          </div>
          <!-- Activities -->
          <div style="margin-bottom:14px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Work Done</div>
            <ul style="list-style:none;display:flex;flex-direction:column;gap:6px">
              <li v-for="a in activeReport.workDone" :key="a" style="font-size:12px;color:#9ca3af;padding:6px 10px;background:#0d0f14;border-radius:6px;border-left:2px solid #3b82f6">{{ a }}</li>
            </ul>
          </div>
          <!-- Issues -->
          <div v-if="activeReport.issues">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Issues Raised</div>
            <div style="background:#1f1008;border:1px solid #92400e;border-radius:8px;padding:10px 12px;font-size:12px;color:#f59e0b">⚠️ {{ activeReport.issues }}</div>
          </div>
          <!-- Next Day Plan -->
          <div style="margin-top:14px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Plan for Tomorrow</div>
            <p style="font-size:12px;color:#9ca3af;line-height:1.6">{{ activeReport.tomorrowPlan }}</p>
          </div>
          <div style="margin-top:20px;display:flex;gap:8px">
            <button class="btn-primary blue" style="flex:1;text-align:center" @click="activeReport = null">✓ Acknowledge</button>
            <button class="btn-ghost" style="flex:1;text-align:center" @click="activeReport = null">Add Comment</button>
          </div>
        </div>
      </div>
    </div>

    <!-- New Report Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>📝 New Daily Report</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Project *</label>
              <select v-model="form.project"><option value="">Select project...</option><option v-for="p in projectOptions" :key="p">{{ p }}</option></select>
            </div>
            <div class="form-group"><label>Date *</label><input type="date" v-model="form.date" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Workers on Site</label><input type="number" v-model="form.workers" placeholder="0" /></div>
            <div class="form-group"><label>Progress % Today</label><input type="number" v-model="form.progress" placeholder="0" min="0" max="100" /></div>
          </div>
          <div class="form-group full"><label>Work Done Today *</label>
            <textarea v-model="form.workDone" rows="3" placeholder="List activities completed today..."></textarea>
          </div>
          <div class="form-group full"><label>Issues / Challenges</label>
            <textarea v-model="form.issues" rows="2" placeholder="Any issues encountered..."></textarea>
          </div>
          <div class="form-group full"><label>Plan for Tomorrow</label>
            <textarea v-model="form.tomorrowPlan" rows="2" placeholder="What is planned for the next working day..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary blue" @click="submitReport">Submit Report</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const activeTab = ref('all')
const search = ref('')
const filterProject = ref('')
const filterDate = ref('')
const showForm = ref(false)
const activeReport = ref(null)
const projectOptions = ['Nairobi Housing — Phase 1', 'Mombasa Port Road', 'Kisumu Commercial Complex', 'Nakuru Ring Road']
const form = ref({ project: '', date: '', workers: '', progress: '', workDone: '', issues: '', tomorrowPlan: '' })

const reports = ref([
  { id: 1, ref: 'RPT-2025-0218-01', project: 'Nairobi Housing — Phase 1',  site: 'Embakasi',  date: '2025-02-18', submittedBy: 'Eng. J. Kariuki',  role: 'Site Engineer',   summary: 'Roofing, plastering and window frames on Block A', workers: 45, progress: 68, color: 'green',  status: 'completed', workDone: ['Roof truss installation Block A (80% complete)', 'Plastering floor 4 complete', '12 window frames fixed'], issues: null, tomorrowPlan: 'Complete roof truss Block A, begin Block B framing' },
  { id: 2, ref: 'RPT-2025-0218-02', project: 'Mombasa Port Road',          site: 'Miritini',  date: '2025-02-18', submittedBy: 'Eng. D. Oduya',    role: 'Resident Engineer', summary: 'Base course compaction and material delivery', workers: 32, progress: 42, color: 'red',    status: 'in-progress', workDone: ['Base course compaction Ch.0+200 to Ch.0+450', 'Ballast delivery 12 lorry loads', 'Survey pegs set out Ch.0+500'], issues: 'Roller CM-004 broke down at 14:00 hrs', tomorrowPlan: 'Repair roller and continue compaction from Ch.0+450' },
  { id: 3, ref: 'RPT-2025-0218-03', project: 'Kisumu Commercial Complex',  site: 'Milimani', date: '2025-02-18', submittedBy: 'Eng. A. Achieng',  role: 'Site Engineer',   summary: 'Column casting grids E-H, formwork removal', workers: 28, progress: 55, color: 'amber',  status: 'completed', workDone: ['Column casting grids E, F, G, H floor 3', 'Formwork removal floor 2 complete', 'Rebar fixing started floor 3 slab'], issues: null, tomorrowPlan: 'Continue rebar fixing floor 3, pour slab concrete' },
  { id: 4, ref: 'RPT-2025-0217-01', project: 'Nakuru Ring Road',           site: 'Nakuru',   date: '2025-02-17', submittedBy: 'Eng. P. Mwangi',   role: 'Site Engineer',   summary: 'Road markings and guardrail installation', workers: 18, progress: 80, color: 'blue',   status: 'completed', workDone: ['Road markings Section B3 complete', 'Guardrail posts installed 250m', 'Drainage clearing km 4.2–4.8'], issues: 'Work suspended 1.5hrs heavy rain at 14:00', tomorrowPlan: 'Continue guardrail installation, begin signage erection' },
])

const tabs = computed(() => [
  { key: 'all',         label: 'All',         count: reports.value.length },
  { key: 'completed',   label: 'Completed',   count: reports.value.filter(r => r.status === 'completed').length },
  { key: 'in-progress', label: 'In Progress', count: reports.value.filter(r => r.status === 'in-progress').length },
])

const filteredReports = computed(() => reports.value.filter(r =>
  (activeTab.value === 'all' || r.status === activeTab.value)
  && (!search.value || r.project.toLowerCase().includes(search.value.toLowerCase()) || r.submittedBy.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterProject.value || r.project === filterProject.value)
  && (!filterDate.value || r.date === filterDate.value)
))

const reportDrawerFields = computed(() => activeReport.value ? [
  { label: 'Site',         value: activeReport.value.site        },
  { label: 'Submitted By', value: activeReport.value.submittedBy },
  { label: 'Role',         value: activeReport.value.role        },
  { label: 'Workers',      value: activeReport.value.workers     },
] : [])

function submitReport() {
  reports.value.unshift({ id: Date.now(), ref: `RPT-${form.value.date}-0${reports.value.length + 1}`, ...form.value, site: '', role: 'Site Engineer', submittedBy: 'Current User', color: 'blue', workers: Number(form.value.workers), progress: Number(form.value.progress), status: 'in-progress', workDone: form.value.workDone.split('\n').filter(Boolean) })
  showForm.value = false
  form.value = { project: '', date: '', workers: '', progress: '', workDone: '', issues: '', tomorrowPlan: '' }
}
</script>

<style scoped>
@import '/src/assets/progress.css';
.btn-view { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 4px 12px; border-radius: 5px; font-size: 11px; cursor: pointer; font-family: 'Syne', sans-serif; }
.btn-view:hover { border-color: #3b82f6; color: #3b82f6; }
</style>