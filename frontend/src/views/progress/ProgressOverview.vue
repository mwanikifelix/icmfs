<template>
  <div class="progress-page">
    <div class="page-header">
      <div>
        <span class="page-tag amber">ICMFS · PROGRESS</span>
        <h1>Progress Overview</h1>
        <p class="page-sub">Real-time construction progress across all active projects and sites</p>
      </div>
      <div style="display:flex;gap:10px">
        <select v-model="selectedProject" class="filter-select">
          <option value="">All Projects</option>
          <option v-for="p in projects" :key="p.id">{{ p.name }}</option>
        </select>
        <button class="btn-primary amber" @click="showReport = true">📊 Generate Report</button>
      </div>
    </div>

    <!-- KPIs -->
    <div class="kpi-row">
      <div class="kpi amber">
        <div class="kpi-top"><span>🏗️</span><span class="mono" style="font-size:10px;color:#f5a623">{{ overallPct }}% overall</span></div>
        <div class="kpi-val">{{ activeProjects }}</div>
        <div class="kpi-label">Active Projects</div>
      </div>
      <div class="kpi green">
        <div class="kpi-top"><span>✅</span><span class="mono" style="font-size:10px;color:#22c55e">On schedule</span></div>
        <div class="kpi-val">{{ onTrackCount }}</div>
        <div class="kpi-label">On Track</div>
      </div>
      <div class="kpi danger">
        <div class="kpi-top"><span>⚠️</span><span class="mono" style="font-size:10px;color:#ef4444">Needs attention</span></div>
        <div class="kpi-val">{{ delayedCount }}</div>
        <div class="kpi-label">Delayed</div>
      </div>
      <div class="kpi blue">
        <div class="kpi-top"><span>👷</span><span class="mono" style="font-size:10px;color:#3b82f6">On-site today</span></div>
        <div class="kpi-val">{{ totalWorkers }}</div>
        <div class="kpi-label">Workers Deployed</div>
      </div>
      <div class="kpi purple">
        <div class="kpi-top"><span>📐</span><span class="mono" style="font-size:10px;color:#a855f7">This week</span></div>
        <div class="kpi-val">{{ tasksCompleted }}</div>
        <div class="kpi-label">Tasks Completed</div>
      </div>
    </div>

    <!-- Project Progress Cards -->
    <div class="section-title">Project Completion Status</div>
    <div class="project-grid">
      <div class="project-card" v-for="p in filteredProjects" :key="p.id" @click="activeProject = p">
        <div class="project-card-top">
          <div>
            <div class="cell-main" style="font-size:14px">{{ p.name }}</div>
            <div class="cell-sub">{{ p.site }} · {{ p.county }}</div>
          </div>
          <span class="status-badge" :class="p.status">{{ p.status }}</span>
        </div>
        <div class="prog-bar-wrap" style="margin:12px 0">
          <div class="prog-bar" style="height:8px">
            <div class="prog-fill" :class="p.color" :style="{ width: p.progress + '%' }"></div>
          </div>
          <span class="prog-pct">{{ p.progress }}%</span>
        </div>
        <div class="project-meta">
          <div class="meta-item"><span class="meta-label">Start</span><span class="meta-val mono">{{ p.startDate }}</span></div>
          <div class="meta-item"><span class="meta-label">End</span><span class="meta-val mono">{{ p.endDate }}</span></div>
          <div class="meta-item"><span class="meta-label">Budget Used</span><span class="meta-val">{{ p.budgetUsed }}%</span></div>
          <div class="meta-item"><span class="meta-label">Workers</span><span class="meta-val">{{ p.workers }}</span></div>
        </div>
        <div class="milestone-row">
          <div class="milestone" v-for="m in p.milestones" :key="m.name" :class="m.done ? 'done' : 'pending'">
            <span>{{ m.done ? '●' : '○' }}</span> {{ m.name }}
          </div>
        </div>
      </div>
    </div>

    <!-- Tasks Overview Table -->
    <div class="panel" style="margin-top:20px">
      <div class="panel-header">
        <h2>Current Task Breakdown</h2>
        <button class="btn-export">📥 Export</button>
      </div>
      <div class="table-wrap" style="margin-bottom:0">
        <table class="data-table">
          <thead>
            <tr>
              <th>Task</th><th>Project</th><th>Assigned To</th>
              <th>Progress</th><th>Due Date</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in tasks" :key="t.id" class="table-row">
              <td>
                <div class="cell-main">{{ t.name }}</div>
                <div class="cell-sub">{{ t.category }}</div>
              </td>
              <td class="cell-muted" style="font-size:11px">{{ t.project }}</td>
              <td>
                <div class="avatar-row">
                  <div class="mini-avatar" v-for="a in t.assignees" :key="a">{{ a }}</div>
                </div>
              </td>
              <td style="min-width:140px">
                <div class="prog-bar-wrap">
                  <div class="prog-bar"><div class="prog-fill" :class="t.color" :style="{ width: t.progress + '%' }"></div></div>
                  <span class="prog-pct">{{ t.progress }}%</span>
                </div>
              </td>
              <td class="cell-date">{{ t.dueDate }}</td>
              <td><span class="status-badge" :class="t.status">{{ t.status }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Detail Drawer -->
    <div class="drawer-overlay" v-if="activeProject" @click.self="activeProject = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="page-tag amber">PROJECT DETAIL</span>
            <h2 style="font-size:16px;font-weight:700">{{ activeProject.name }}</h2>
          </div>
          <button class="close-btn" @click="activeProject = null">✕</button>
        </div>
        <div class="drawer-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px">
            <div v-for="d in drawerFields" :key="d.label">
              <div class="cell-sub" style="text-transform:uppercase;letter-spacing:0.5px">{{ d.label }}</div>
              <div style="font-size:13px;color:#e8e4dc;margin-top:4px">{{ d.value }}</div>
            </div>
          </div>
          <div style="margin-bottom:16px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Overall Progress</div>
            <div class="prog-bar-wrap">
              <div class="prog-bar" style="height:10px"><div class="prog-fill" :class="activeProject.color" :style="{ width: activeProject.progress + '%' }"></div></div>
              <span class="prog-pct" style="font-size:14px;font-weight:700;color:#fff">{{ activeProject.progress }}%</span>
            </div>
          </div>
          <div>
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Milestones</div>
            <div style="display:flex;flex-direction:column;gap:8px">
              <div v-for="m in activeProject.milestones" :key="m.name" style="display:flex;align-items:center;gap:10px;padding:10px;border-radius:8px;background:#0d0f14">
                <span :style="m.done ? 'color:#22c55e;font-size:16px' : 'color:#4b5563;font-size:16px'">{{ m.done ? '✅' : '○' }}</span>
                <span style="font-size:13px">{{ m.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Report Modal -->
    <div class="modal-overlay" v-if="showReport" @click.self="showReport = false">
      <div class="modal">
        <div class="modal-header">
          <h2>📊 Generate Progress Report</h2>
          <button class="close-btn" @click="showReport = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Project</label>
              <select><option>All Projects</option><option v-for="p in projects" :key="p.id">{{ p.name }}</option></select>
            </div>
            <div class="form-group"><label>Report Type</label>
              <select><option>Weekly Summary</option><option>Monthly Report</option><option>Milestone Report</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>From</label><input type="date" /></div>
            <div class="form-group"><label>To</label><input type="date" /></div>
          </div>
          <div class="form-group full"><label>Format</label>
            <select><option>PDF</option><option>Excel</option><option>Word</option></select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showReport = false">Cancel</button>
          <button class="btn-primary amber" @click="showReport = false">Generate</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const selectedProject = ref('')
const activeProject = ref(null)
const showReport = ref(false)

const projects = ref([
  { id: 1, name: 'Nairobi Affordable Housing — Phase 1', site: 'Embakasi', county: 'Nairobi', status: 'on-track',    progress: 68, color: 'green',  startDate: '2024-06-01', endDate: '2025-08-31', budgetUsed: 71, workers: 142, milestones: [{ name: 'Foundation Complete', done: true }, { name: 'Structural Frame', done: true }, { name: 'Roofing', done: false }, { name: 'Finishing', done: false }] },
  { id: 2, name: 'Mombasa Port Road Infrastructure', site: 'Miritini',  county: 'Mombasa',  status: 'delayed',     progress: 42, color: 'red',    startDate: '2024-03-15', endDate: '2025-06-30', budgetUsed: 55, workers: 98,  milestones: [{ name: 'Survey & Design', done: true }, { name: 'Earthworks', done: true }, { name: 'Base Course', done: false }, { name: 'Tarmac Layer', done: false }] },
  { id: 3, name: 'Kisumu Commercial Complex',          site: 'Milimani', county: 'Kisumu',   status: 'on-track',    progress: 55, color: 'amber', startDate: '2024-09-01', endDate: '2026-03-31', budgetUsed: 48, workers: 76,  milestones: [{ name: 'Excavation', done: true }, { name: 'Foundation', done: true }, { name: 'Superstructure', done: false }, { name: 'MEP Works', done: false }] },
  { id: 4, name: 'Nakuru Ring Road — Section B',       site: 'Nakuru',   county: 'Nakuru',   status: 'in-progress', progress: 80, color: 'blue',  startDate: '2024-01-10', endDate: '2025-04-30', budgetUsed: 82, workers: 54,  milestones: [{ name: 'Earthworks', done: true }, { name: 'Base Course', done: true }, { name: 'Tarmac', done: true }, { name: 'Signage & Markings', done: false }] },
])

const tasks = ref([
  { id: 1, name: 'Roof Truss Installation',    category: 'Structural',   project: 'Nairobi Housing',       assignees: ['J','K','M'], progress: 65,  dueDate: '2025-03-15', status: 'in-progress', color: 'amber'  },
  { id: 2, name: 'Base Course Compaction',     category: 'Civil Works',  project: 'Mombasa Road',          assignees: ['P','O'],     progress: 30,  dueDate: '2025-03-20', status: 'delayed',    color: 'red'    },
  { id: 3, name: 'Electrical Rough-in',        category: 'MEP',          project: 'Kisumu Commercial',     assignees: ['A','W'],     progress: 45,  dueDate: '2025-04-01', status: 'in-progress', color: 'blue'   },
  { id: 4, name: 'Road Markings & Signage',    category: 'Finishing',    project: 'Nakuru Ring Road',      assignees: ['G','N'],     progress: 90,  dueDate: '2025-03-10', status: 'on-track',   color: 'green'  },
  { id: 5, name: 'Plastering — Floors 3-5',   category: 'Finishing',    project: 'Nairobi Housing',       assignees: ['D','R','S'], progress: 55,  dueDate: '2025-03-25', status: 'in-progress', color: 'amber'  },
])

const filteredProjects = computed(() =>
  selectedProject.value ? projects.value.filter(p => p.name === selectedProject.value) : projects.value
)
const activeProjects  = computed(() => projects.value.length)
const onTrackCount    = computed(() => projects.value.filter(p => p.status === 'on-track').length)
const delayedCount    = computed(() => projects.value.filter(p => p.status === 'delayed').length)
const totalWorkers    = computed(() => projects.value.reduce((a, b) => a + b.workers, 0))
const tasksCompleted  = computed(() => tasks.value.filter(t => t.progress === 100).length + 8)
const overallPct      = computed(() => Math.round(projects.value.reduce((a, b) => a + b.progress, 0) / projects.value.length))

const drawerFields = computed(() => activeProject.value ? [
  { label: 'County',      value: activeProject.value.county      },
  { label: 'Site',        value: activeProject.value.site        },
  { label: 'Start Date',  value: activeProject.value.startDate   },
  { label: 'End Date',    value: activeProject.value.endDate     },
  { label: 'Budget Used', value: activeProject.value.budgetUsed + '%' },
  { label: 'Workers',     value: activeProject.value.workers     },
] : [])
</script>

<style scoped>
@import '/src/assets/progress.css';
.kpi-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.section-title { font-size: 13px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px; font-family: 'DM Mono', monospace; }
.project-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.project-card { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 18px; cursor: pointer; transition: border-color 0.2s; }
.project-card:hover { border-color: #f5a623; }
.project-card-top { display: flex; justify-content: space-between; align-items: flex-start; }
.project-meta { display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; margin-top: 8px; }
.meta-item { display: flex; flex-direction: column; gap: 2px; }
.meta-label { font-size: 10px; color: #4b5563; font-family: 'DM Mono', monospace; text-transform: uppercase; }
.meta-val   { font-size: 12px; color: #e8e4dc; font-weight: 600; }
.milestone-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; padding-top: 12px; border-top: 1px solid #1e2230; }
.milestone { font-size: 10px; font-family: 'DM Mono', monospace; padding: 3px 8px; border-radius: 4px; }
.milestone.done    { background: #0d2818; color: #22c55e; }
.milestone.pending { background: #1a1e2a; color: #4b5563; }
.avatar-row { display: flex; gap: 4px; }
.mini-avatar { width: 24px; height: 24px; border-radius: 50%; background: #1e2230; color: #f5a623; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; border: 1px solid #2a2f3e; }
</style>