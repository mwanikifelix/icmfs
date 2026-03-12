<template>
  <div class="qa-page">
    <div class="page-header">
      <div>
        <span class="page-tag indigo">ICMFS · QUALITY ASSURANCE</span>
        <h1>QA Overview</h1>
        <p class="page-sub">Quality assurance status across all active projects and sites</p>
      </div>
      <div style="display:flex;gap:10px">
        <select v-model="selectedProject" class="filter-select">
          <option value="">All Projects</option>
          <option v-for="p in projects" :key="p">{{ p }}</option>
        </select>
        <button class="btn-primary indigo" @click="$router.push('/app/qa/inspections')">+ New Inspection</button>
      </div>
    </div>

    <!-- KPIs -->
    <div class="kpi-row">
      <div class="kpi indigo">
        <div class="kpi-top"><span>🔍</span><span class="mono" style="font-size:10px;color:#6366f1">This month</span></div>
        <div class="kpi-val">{{ totalInspections }}</div>
        <div class="kpi-label">Inspections Conducted</div>
      </div>
      <div class="kpi green">
        <div class="kpi-top"><span>✅</span><span class="mono" style="font-size:10px;color:#22c55e">Rate</span></div>
        <div class="kpi-val">{{ passRate }}%</div>
        <div class="kpi-label">Pass Rate</div>
      </div>
      <div class="kpi danger">
        <div class="kpi-top"><span>🚨</span><span class="mono" style="font-size:10px;color:#ef4444">Open</span></div>
        <div class="kpi-val">{{ openIssues }}</div>
        <div class="kpi-label">Open Issues / NCRs</div>
      </div>
      <div class="kpi amber">
        <div class="kpi-top"><span>📜</span><span class="mono" style="font-size:10px;color:#f5a623">Active</span></div>
        <div class="kpi-val">{{ activeCerts }}</div>
        <div class="kpi-label">Certifications Active</div>
      </div>
      <div class="kpi teal">
        <div class="kpi-top"><span>📋</span><span class="mono" style="font-size:10px;color:#14b8a6">Pending</span></div>
        <div class="kpi-val">{{ pendingReports }}</div>
        <div class="kpi-label">Reports Pending Sign-Off</div>
      </div>
    </div>

    <!-- Project QA Cards -->
    <div class="qa-grid">
      <div class="qa-project-card" v-for="p in projectQA" :key="p.id">
        <div class="qa-card-top">
          <div>
            <div style="font-size:14px;font-weight:700;color:#fff">{{ p.name }}</div>
            <div class="cell-sub">{{ p.site }} · {{ p.county }}</div>
          </div>
          <div class="score-circle" :class="p.score>=85?'pass':p.score>=70?'warn':'fail'">{{ p.score }}%</div>
        </div>

        <div style="margin:14px 0">
          <div style="display:flex;justify-content:space-between;margin-bottom:6px">
            <span style="font-size:11px;color:#9ca3af">QA Score</span>
            <span class="mono" style="font-size:11px" :style="p.score>=85?'color:#22c55e':p.score>=70?'color:#f59e0b':'color:#ef4444'">{{ p.score }}%</span>
          </div>
          <div class="prog-bar" style="height:8px">
            <div class="prog-fill" :class="p.score>=85?'green':p.score>=70?'amber':'red'" :style="{width:p.score+'%'}"></div>
          </div>
        </div>

        <div class="qa-stats-row">
          <div class="qa-stat"><div class="qa-stat-val indigo">{{ p.inspections }}</div><div class="qa-stat-lbl">Inspections</div></div>
          <div class="qa-stat"><div class="qa-stat-val green">{{ p.passed }}</div><div class="qa-stat-lbl">Passed</div></div>
          <div class="qa-stat"><div class="qa-stat-val danger">{{ p.failed }}</div><div class="qa-stat-lbl">Failed</div></div>
          <div class="qa-stat"><div class="qa-stat-val warn">{{ p.openNCRs }}</div><div class="qa-stat-lbl">Open NCRs</div></div>
        </div>

        <div class="qa-activity">
          <div class="qa-activity-item" v-for="a in p.recentActivity" :key="a.ref">
            <span class="status-badge" :class="a.result">{{ a.result }}</span>
            <span style="font-size:11px;color:#9ca3af;flex:1">{{ a.title }}</span>
            <span class="cell-date">{{ a.date }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Issues Summary -->
    <div class="panel" style="margin-top:16px">
      <div class="panel-header">
        <h2>Open Issues / NCRs</h2>
        <button class="btn-view" @click="$router.push('/app/qa/issues')">View All</button>
      </div>
      <div class="table-wrap" style="margin-bottom:0">
        <table class="data-table">
          <thead>
            <tr><th>NCR Ref</th><th>Description</th><th>Project</th><th>Severity</th><th>Raised</th><th>Due</th><th>Status</th></tr>
          </thead>
          <tbody>
            <tr v-for="i in openNCRs" :key="i.id" class="table-row">
              <td class="cell-ref" style="color:#6366f1">{{ i.ref }}</td>
              <td><div class="cell-main">{{ i.title }}</div><div class="cell-sub">{{ i.location }}</div></td>
              <td class="cell-muted" style="font-size:11px">{{ i.project }}</td>
              <td><span class="sev-badge" :class="i.severity">{{ i.severity }}</span></td>
              <td class="cell-date">{{ i.raised }}</td>
              <td class="cell-date" :style="isOverdue(i.due)?'color:#ef4444':''">{{ i.due }}</td>
              <td><span class="status-badge" :class="i.status">{{ i.status }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const selectedProject = ref('')
const projects = ['Nairobi Housing — Phase 1','Mombasa Port Road','Kisumu Commercial Complex','Nakuru Ring Road']

const projectQA = ref([
  { id:1, name:'Nairobi Housing — Phase 1',  site:'Embakasi',  county:'Nairobi',  score:88, inspections:14, passed:12, failed:2, openNCRs:3, recentActivity:[{ref:'INS-041',title:'Roof Truss Weld Inspection',result:'passed',date:'2025-02-18'},{ref:'INS-040',title:'Floor 4 Concrete Cube Test',result:'passed',date:'2025-02-16'},{ref:'INS-039',title:'Plumbing Pressure Test',result:'failed',date:'2025-02-14'}] },
  { id:2, name:'Mombasa Port Road',           site:'Miritini',  county:'Mombasa',  score:71, inspections:11, passed:8,  failed:3, openNCRs:5, recentActivity:[{ref:'INS-038',title:'Base Course CBR Test',result:'failed',date:'2025-02-18'},{ref:'INS-037',title:'Compaction Test Ch.0+350',result:'pending',date:'2025-02-17'},{ref:'INS-036',title:'Survey Alignment Check',result:'passed',date:'2025-02-15'}] },
  { id:3, name:'Kisumu Commercial Complex',   site:'Milimani',  county:'Kisumu',   score:92, inspections:9,  passed:9,  failed:0, openNCRs:1, recentActivity:[{ref:'INS-035',title:'Column Casting — Grid E',result:'passed',date:'2025-02-17'},{ref:'INS-034',title:'Rebar Cover Check Floor 3',result:'passed',date:'2025-02-15'},{ref:'INS-033',title:'Formwork Alignment',result:'passed',date:'2025-02-13'}] },
  { id:4, name:'Nakuru Ring Road',            site:'Nakuru',    county:'Nakuru',   score:95, inspections:8,  passed:8,  failed:0, openNCRs:0, recentActivity:[{ref:'INS-032',title:'Road Marking Reflectivity',result:'passed',date:'2025-02-17'},{ref:'INS-031',title:'Guardrail Torque Check',result:'passed',date:'2025-02-15'},{ref:'INS-030',title:'Drainage Gradient Survey',result:'passed',date:'2025-02-13'}] },
])

const openNCRs = ref([
  {id:1,ref:'NCR-2025-008',title:'Insufficient rebar cover — Column C4',location:'Floor 3, Grid C',project:'Nairobi Housing',severity:'major',raised:'2025-02-14',due:'2025-02-21',status:'open'},
  {id:2,ref:'NCR-2025-009',title:'Base course CBR below spec (62% vs 80%)',location:'Ch.0+350 to Ch.0+450',project:'Mombasa Port Road',severity:'critical',raised:'2025-02-18',due:'2025-02-22',status:'open'},
  {id:3,ref:'NCR-2025-007',title:'Plumbing pressure test failure — Block A',location:'Floor 2, Zone B',project:'Nairobi Housing',severity:'major',raised:'2025-02-12',due:'2025-02-19',status:'in-progress'},
  {id:4,ref:'NCR-2025-006',title:'Concrete mix ratio deviation',location:'Slab pour Floor 2',project:'Mombasa Port Road',severity:'critical',raised:'2025-02-10',due:'2025-02-17',status:'open'},
])

const totalInspections = computed(()=>projectQA.value.reduce((a,b)=>a+b.inspections,0))
const passRate          = computed(()=>Math.round(projectQA.value.reduce((a,b)=>a+b.passed,0)/totalInspections.value*100))
const openIssues        = computed(()=>projectQA.value.reduce((a,b)=>a+b.openNCRs,0))
const activeCerts       = ref(7)
const pendingReports    = ref(4)
const isOverdue         = (date) => new Date(date) < new Date()
</script>

<style scoped>
@import '/src/assets/qa.css';
.qa-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 14px; }
.qa-project-card { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 18px; }
.qa-card-top { display: flex; justify-content: space-between; align-items: flex-start; }
.qa-stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; margin-bottom: 14px; }
.qa-stat { background: #0d0f14; border-radius: 8px; padding: 10px; text-align: center; }
.qa-stat-val { font-size: 20px; font-weight: 800; }
.qa-stat-val.indigo { color: #6366f1; }
.qa-stat-val.green  { color: #22c55e; }
.qa-stat-val.danger { color: #ef4444; }
.qa-stat-val.warn   { color: #f59e0b; }
.qa-stat-lbl { font-size: 9px; color: #4b5563; text-transform: uppercase; font-family: 'DM Mono', monospace; margin-top: 2px; }
.qa-activity { display: flex; flex-direction: column; gap: 4px; padding-top: 12px; border-top: 1px solid #1e2230; }
.qa-activity-item { display: flex; align-items: center; gap: 8px; padding: 4px 0; }
</style>