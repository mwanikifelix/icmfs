<template>
  <div class="qa-page">
    <div class="page-header">
      <div>
        <span class="page-tag rose">QA · ISSUES & NCRs</span>
        <h1>QA Issues & NCRs</h1>
        <p class="page-sub">Non-conformance reports, defects and corrective action tracking</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary rose" @click="showForm=true">+ Raise NCR</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card danger">
        <div class="stat-val">{{ issues.filter(i=>i.status==='open').length }}</div>
        <div class="stat-label">Open NCRs</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">{{ issues.filter(i=>i.status==='in-progress').length }}</div>
        <div class="stat-label">In Progress</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">{{ issues.filter(i=>i.status==='closed').length }}</div>
        <div class="stat-label">Closed</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-val">{{ issues.filter(i=>i.severity==='critical').length }}</div>
        <div class="stat-label">Critical Severity</div>
      </div>
      <div class="stat-card rose">
        <div class="stat-val">{{ overdueCount }}</div>
        <div class="stat-label">Overdue</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button v-for="t in tabs" :key="t.key" :class="['tab',activeTab===t.key?'active':'']" @click="activeTab=t.key">
        {{ t.label }} <span class="tab-count">{{ t.count }}</span>
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search NCR ref, title or project..." />
      </div>
      <select v-model="filterSeverity" class="filter-select">
        <option value="">All Severities</option>
        <option value="critical">Critical</option>
        <option value="major">Major</option>
        <option value="minor">Minor</option>
      </select>
      <select v-model="filterSite" class="filter-select">
        <option value="">All Sites</option>
        <option v-for="s in siteOptions" :key="s">{{ s }}</option>
      </select>
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>NCR Ref</th><th>Description</th><th>Site / Location</th>
            <th>Severity</th><th>Raised By</th><th>Assigned To</th>
            <th>Date Raised</th><th>Due Date</th><th>Status</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in filteredIssues" :key="i.id" class="table-row" :class="isOverdue(i)&&i.status!=='closed'?'overdue-row':''">
            <td class="cell-ref" style="color:#f43f5e">{{ i.ref }}</td>
            <td>
              <div class="cell-main">{{ i.title }}</div>
              <div class="cell-sub">{{ i.category }}</div>
            </td>
            <td>
              <div class="cell-main">{{ i.site }}</div>
              <div class="cell-sub">{{ i.location }}</div>
            </td>
            <td><span class="sev-badge" :class="i.severity">{{ i.severity }}</span></td>
            <td>
              <div class="cell-main">{{ i.raisedBy }}</div>
              <div class="cell-sub">{{ i.inspectionRef }}</div>
            </td>
            <td class="cell-muted" style="font-size:11px">{{ i.assignedTo }}</td>
            <td class="cell-date">{{ i.raised }}</td>
            <td class="cell-date" :style="isOverdue(i)&&i.status!=='closed'?'color:#ef4444;font-weight:700':''">{{ i.due }}</td>
            <td><span class="status-badge" :class="i.status">{{ i.status }}</span></td>
            <td><button class="btn-view" @click="active=i" style="border-color:#f43f5e55">View</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drawer -->
    <div class="drawer-overlay" v-if="active" @click.self="active=null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#f43f5e;display:block;margin-bottom:4px">{{ active.ref }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ active.title }}</h2>
            <div style="display:flex;gap:8px;margin-top:6px">
              <span class="sev-badge" :class="active.severity">{{ active.severity }}</span>
              <span class="status-badge" :class="active.status">{{ active.status }}</span>
            </div>
          </div>
          <button class="close-btn" @click="active=null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item"><span class="dlbl">Site</span><span class="dval">{{ active.site }}</span></div>
            <div class="detail-item"><span class="dlbl">Location</span><span class="dval">{{ active.location }}</span></div>
            <div class="detail-item"><span class="dlbl">Raised By</span><span class="dval">{{ active.raisedBy }}</span></div>
            <div class="detail-item"><span class="dlbl">Assigned To</span><span class="dval">{{ active.assignedTo }}</span></div>
            <div class="detail-item"><span class="dlbl">Date Raised</span><span class="dval">{{ active.raised }}</span></div>
            <div class="detail-item"><span class="dlbl">Due Date</span><span class="dval" :style="isOverdue(active)?'color:#ef4444':''">{{ active.due }}</span></div>
          </div>
          <div style="margin-bottom:14px">
            <div class="dlbl" style="margin-bottom:6px">Non-Conformance Description</div>
            <p style="font-size:13px;color:#9ca3af;line-height:1.6;background:#0d0f14;padding:12px;border-radius:8px">{{ active.description }}</p>
          </div>
          <div v-if="active.rootCause" style="margin-bottom:14px">
            <div class="dlbl" style="margin-bottom:6px">Root Cause</div>
            <p style="font-size:13px;color:#9ca3af;line-height:1.6">{{ active.rootCause }}</p>
          </div>
          <div style="margin-bottom:14px">
            <div class="dlbl" style="margin-bottom:8px">Corrective Action</div>
            <textarea v-model="active.correctiveAction" rows="3" style="width:100%;background:#0d0f14;border:1px solid #1e2230;color:#e8e4dc;padding:10px 12px;border-radius:7px;font-family:'Syne',sans-serif;font-size:13px;resize:vertical"></textarea>
          </div>
          <div style="display:flex;gap:8px">
            <button v-if="active.status==='open'" class="btn-primary rose" style="flex:1" @click="active.status='in-progress';active=null">Mark In Progress</button>
            <button v-if="active.status==='in-progress'" class="btn-primary green" style="flex:1" @click="active.status='closed';active=null">✓ Close NCR</button>
            <button class="btn-ghost" style="flex:1" @click="active=null">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Raise NCR Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm=false">
      <div class="modal">
        <div class="modal-header">
          <h2>🚨 Raise Non-Conformance Report</h2>
          <button class="close-btn" @click="showForm=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Title *</label><input v-model="form.title" placeholder="Brief description of issue" /></div>
            <div class="form-group"><label>Severity *</label>
              <select v-model="form.severity"><option value="minor">Minor</option><option value="major">Major</option><option value="critical">Critical</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Site *</label>
              <select v-model="form.site"><option value="">Select...</option><option v-for="s in siteOptions" :key="s">{{ s }}</option></select>
            </div>
            <div class="form-group"><label>Location *</label><input v-model="form.location" placeholder="e.g. Floor 3, Grid C" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Category</label>
              <select v-model="form.category"><option>Structural</option><option>Civil Works</option><option>MEP</option><option>Finishing</option><option>Materials</option></select>
            </div>
            <div class="form-group"><label>Assigned To *</label><input v-model="form.assignedTo" placeholder="Engineer / contractor" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Date Raised *</label><input type="date" v-model="form.raised" /></div>
            <div class="form-group"><label>Due Date for Resolution *</label><input type="date" v-model="form.due" /></div>
          </div>
          <div class="form-group full"><label>Detailed Description *</label><textarea v-model="form.description" rows="3" placeholder="Describe the non-conformance in detail..."></textarea></div>
          <div class="form-group full"><label>Root Cause (if known)</label><textarea v-model="form.rootCause" rows="2" placeholder="Identified root cause..."></textarea></div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm=false">Cancel</button>
          <button class="btn-primary rose" @click="raiseNCR">Raise NCR</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const activeTab = ref('all')
const search = ref('')
const filterSeverity = ref('')
const filterSite = ref('')
const showForm = ref(false)
const active = ref(null)
const siteOptions = ['Nairobi Housing — Phase 1','Mombasa Port Road','Kisumu Commercial Complex','Nakuru Ring Road']
const form = ref({ title:'', severity:'major', site:'', location:'', category:'Structural', assignedTo:'', raised:'', due:'', description:'', rootCause:'' })

const issues = ref([
  { id:1, ref:'NCR-2025-009', title:'Base course CBR below specification',   category:'Civil Works', site:'Mombasa Port Road',         location:'Ch.0+350 to Ch.0+450', raisedBy:'Eng. Oduya',   inspectionRef:'INS-038', assignedTo:'Contractor — Tarmac EA', raised:'2025-02-18', due:'2025-02-22', severity:'critical', status:'open',        description:'CBR value of 62% recorded against minimum specification of 80%. Material does not comply with road design requirements.', rootCause:'Quarry source changed without engineer approval. New material not pre-tested.', correctiveAction:'' },
  { id:2, ref:'NCR-2025-008', title:'Insufficient rebar cover — Column C4', category:'Structural', site:'Nairobi Housing — Phase 1',  location:'Floor 3, Grid C',       raisedBy:'Eng. Kariuki', inspectionRef:'INS-036', assignedTo:'Eng. Kariuki',           raised:'2025-02-14', due:'2025-02-21', severity:'major',    status:'in-progress', description:'Concrete cover measured at 28mm against specified minimum of 40mm on column C4. Risk of corrosion to reinforcement.', rootCause:'Spacers were dislodged during rebar fixing. Not re-checked before pour.', correctiveAction:'Additional render coat applied to affected area. Future pours to have pre-pour checklist sign-off.' },
  { id:3, ref:'NCR-2025-007', title:'Plumbing pressure test failure',        category:'MEP',        site:'Nairobi Housing — Phase 1',  location:'Floor 2, Zone B',       raisedBy:'Eng. Njoroge', inspectionRef:'INS-039', assignedTo:'Plumbing Sub.',          raised:'2025-02-14', due:'2025-02-19', severity:'major',    status:'open',        description:'Pressure drop of 0.8 bar observed after 30-minute test at Zone B junction. Joint failure suspected.', rootCause:null, correctiveAction:'' },
  { id:4, ref:'NCR-2025-006', title:'Concrete mix ratio deviation',          category:'Materials',  site:'Mombasa Port Road',         location:'Slab pour Floor 2',     raisedBy:'Eng. Oduya',   inspectionRef:'INS-034', assignedTo:'Site Manager',           raised:'2025-02-10', due:'2025-02-17', severity:'critical', status:'open',        description:'Concrete mixed on-site with water-cement ratio exceeding 0.55. Delivery note ratio 0.62 observed.', rootCause:'Mixer operator added water without supervision to improve workability.', correctiveAction:'' },
  { id:5, ref:'NCR-2025-005', title:'Formwork premature removal',            category:'Structural', site:'Kisumu Commercial Complex',  location:'Floor 2 Slab',          raisedBy:'Eng. Achieng', inspectionRef:'INS-030', assignedTo:'Eng. Achieng',           raised:'2025-02-05', due:'2025-02-12', severity:'major',    status:'closed',      description:'Slab formwork removed after 3 days. Specification requires minimum 7 days strike.', rootCause:'Foreman misread strike time. Training gap.', correctiveAction:'Foreman re-trained. Strike time schedule posted at site store and signed off daily.' },
])

const tabs = computed(()=>[
  {key:'all',         label:'All',         count:issues.value.length},
  {key:'open',        label:'Open',        count:issues.value.filter(i=>i.status==='open').length},
  {key:'in-progress', label:'In Progress', count:issues.value.filter(i=>i.status==='in-progress').length},
  {key:'closed',      label:'Closed',      count:issues.value.filter(i=>i.status==='closed').length},
])

const filteredIssues = computed(()=>issues.value.filter(i=>
  (activeTab.value==='all'||i.status===activeTab.value)
  &&(!search.value||i.ref.includes(search.value)||i.title.toLowerCase().includes(search.value.toLowerCase())||i.site.toLowerCase().includes(search.value.toLowerCase()))
  &&(!filterSeverity.value||i.severity===filterSeverity.value)
  &&(!filterSite.value||i.site===filterSite.value)
))

const isOverdue     = (i) => new Date(i.due) < new Date()
const overdueCount  = computed(()=>issues.value.filter(i=>isOverdue(i)&&i.status!=='closed').length)

function raiseNCR() {
  issues.value.unshift({ id:Date.now(), ref:`NCR-2025-0${issues.value.length+10}`, ...form.value, raisedBy:'Current User', inspectionRef:'Manual', status:'open', correctiveAction:'' })
  showForm.value=false
  form.value = { title:'', severity:'major', site:'', location:'', category:'Structural', assignedTo:'', raised:'', due:'', description:'', rootCause:'' }
}
</script>

<style scoped>
@import '/src/assets/qa.css';
.overdue-row { background: #100808 !important; }
.btn-view { background:none; border:1px solid #2a2f3e; color:#9ca3af; padding:4px 12px; border-radius:5px; font-size:11px; cursor:pointer; font-family:'Syne',sans-serif; }
.btn-view:hover { border-color:#f43f5e; color:#f43f5e; }
</style>