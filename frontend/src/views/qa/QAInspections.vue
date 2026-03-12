<template>
  <div class="qa-page">
    <div class="page-header">
      <div>
        <span class="page-tag indigo">QA · INSPECTIONS</span>
        <h1>QA Inspections</h1>
        <p class="page-sub">Scheduled and completed quality inspection records across all sites</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary indigo" @click="showForm=true">+ Schedule Inspection</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card indigo">
        <div class="stat-val">{{ inspections.length }}</div>
        <div class="stat-label">Total Inspections</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">{{ inspections.filter(i=>i.result==='passed').length }}</div>
        <div class="stat-label">Passed</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-val">{{ inspections.filter(i=>i.result==='failed').length }}</div>
        <div class="stat-label">Failed</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">{{ inspections.filter(i=>i.result==='pending').length }}</div>
        <div class="stat-label">Pending</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ inspections.filter(i=>i.result==='scheduled').length }}</div>
        <div class="stat-label">Scheduled</div>
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
        <input v-model="search" class="search-input" placeholder="Search inspection title or site..." />
      </div>
      <select v-model="filterType" class="filter-select">
        <option value="">All Types</option>
        <option v-for="t in inspectionTypes" :key="t">{{ t }}</option>
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
            <th>Ref</th><th>Inspection Title</th><th>Type</th><th>Site / Location</th>
            <th>Inspector</th><th>Date</th><th>Score</th><th>NCRs</th><th>Result</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ins in filteredInspections" :key="ins.id" class="table-row">
            <td class="cell-ref" style="color:#6366f1">{{ ins.ref }}</td>
            <td>
              <div class="cell-main">{{ ins.title }}</div>
              <div class="cell-sub">{{ ins.category }}</div>
            </td>
            <td><span class="type-pill" :class="ins.type">{{ ins.type }}</span></td>
            <td>
              <div class="cell-main">{{ ins.site }}</div>
              <div class="cell-sub">{{ ins.location }}</div>
            </td>
            <td>
              <div class="cell-main">{{ ins.inspector }}</div>
              <div class="cell-sub">{{ ins.inspectorRole }}</div>
            </td>
            <td class="cell-date">{{ ins.date }}</td>
            <td>
              <span v-if="ins.score" style="font-size:14px;font-weight:800"
                :style="ins.score>=85?'color:#22c55e':ins.score>=70?'color:#f59e0b':'color:#ef4444'">
                {{ ins.score }}%
              </span>
              <span v-else class="cell-muted">—</span>
            </td>
            <td>
              <span v-if="ins.ncrs>0" style="font-family:'DM Mono',monospace;font-size:12px;color:#ef4444;font-weight:700">{{ ins.ncrs }}</span>
              <span v-else style="font-family:'DM Mono',monospace;font-size:12px;color:#22c55e">0</span>
            </td>
            <td><span class="status-badge" :class="ins.result">{{ ins.result }}</span></td>
            <td><button class="btn-view" @click="active=ins">View</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drawer -->
    <div class="drawer-overlay" v-if="active" @click.self="active=null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#6366f1;display:block;margin-bottom:4px">{{ active.ref }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ active.title }}</h2>
            <div class="cell-sub">{{ active.site }} · {{ active.date }}</div>
          </div>
          <button class="close-btn" @click="active=null">✕</button>
        </div>
        <div class="drawer-body">
          <!-- Score hero -->
          <div v-if="active.score" style="display:flex;gap:16px;background:#0d0f14;border-radius:10px;padding:16px;margin-bottom:18px;align-items:center">
            <div class="score-circle" :class="active.score>=85?'pass':active.score>=70?'warn':'fail'" style="width:72px;height:72px;font-size:20px">
              {{ active.score }}%
            </div>
            <div>
              <div style="font-size:18px;font-weight:800;color:#fff">{{ active.score>=85?'PASSED':active.score>=70?'MARGINAL':'FAILED' }}</div>
              <div class="cell-sub">{{ active.ncrs }} NCR{{ active.ncrs!==1?'s':'' }} raised · {{ active.checklistItems }} checklist items</div>
            </div>
          </div>
          <div class="detail-grid">
            <div class="detail-item"><span class="dlbl">Inspector</span><span class="dval">{{ active.inspector }}</span></div>
            <div class="detail-item"><span class="dlbl">Role</span><span class="dval">{{ active.inspectorRole }}</span></div>
            <div class="detail-item"><span class="dlbl">Type</span><span class="dval">{{ active.type }}</span></div>
            <div class="detail-item"><span class="dlbl">Category</span><span class="dval">{{ active.category }}</span></div>
            <div class="detail-item"><span class="dlbl">Location</span><span class="dval">{{ active.location }}</span></div>
            <div class="detail-item"><span class="dlbl">Date</span><span class="dval">{{ active.date }}</span></div>
          </div>
          <div v-if="active.findings" style="margin-bottom:14px">
            <div class="dlbl" style="margin-bottom:6px">Findings / Observations</div>
            <p style="font-size:13px;color:#9ca3af;line-height:1.6">{{ active.findings }}</p>
          </div>
          <div v-if="active.ncrs>0" style="background:#200e0e;border:1px solid #7f1d1d;border-radius:8px;padding:12px;margin-bottom:14px">
            <div class="dlbl" style="color:#ef4444;margin-bottom:4px">{{ active.ncrs }} Non-Conformance Report{{ active.ncrs!==1?'s':'' }} Raised</div>
            <p style="font-size:12px;color:#f87171">View in QA Issues for full NCR details and corrective action tracking.</p>
          </div>
          <div style="display:flex;gap:8px">
            <button class="btn-primary indigo" style="flex:1;text-align:center" @click="active=null">🖨️ Print Report</button>
            <button v-if="active.result==='pending'" class="btn-ghost" style="flex:1;text-align:center" @click="active=null">✓ Record Result</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Schedule Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm=false">
      <div class="modal">
        <div class="modal-header">
          <h2>🔍 Schedule Inspection</h2>
          <button class="close-btn" @click="showForm=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Inspection Title *</label><input v-model="form.title" placeholder="e.g. Concrete Cube Test — Floor 3" /></div>
            <div class="form-group"><label>Type *</label>
              <select v-model="form.type"><option value="">Select...</option><option v-for="t in inspectionTypes" :key="t">{{ t }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Site *</label>
              <select v-model="form.site"><option value="">Select...</option><option v-for="s in siteOptions" :key="s">{{ s }}</option></select>
            </div>
            <div class="form-group"><label>Location / Element *</label><input v-model="form.location" placeholder="e.g. Floor 3, Grid C-D" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Inspection Date *</label><input type="date" v-model="form.date" /></div>
            <div class="form-group"><label>Inspector *</label><input v-model="form.inspector" placeholder="Engineer name" /></div>
          </div>
          <div class="form-group full"><label>Category</label>
            <select v-model="form.category">
              <option value="">Select...</option>
              <option>Structural</option><option>Civil Works</option><option>MEP</option>
              <option>Finishing</option><option>Materials</option><option>Safety</option>
            </select>
          </div>
          <div class="form-group full"><label>Notes / Instructions</label><textarea v-model="form.notes" rows="2" placeholder="Any pre-inspection notes..."></textarea></div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm=false">Cancel</button>
          <button class="btn-primary indigo" @click="scheduleInspection">Schedule</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const activeTab = ref('all')
const search = ref('')
const filterType = ref('')
const filterSite = ref('')
const showForm = ref(false)
const active = ref(null)
const siteOptions = ['Nairobi Housing — Phase 1','Mombasa Port Road','Kisumu Commercial Complex','Nakuru Ring Road']
const inspectionTypes = ['Structural','Material Test','Civil Works','MEP','Finishing','Safety']
const form = ref({ title:'', type:'', site:'', location:'', date:'', inspector:'', category:'', notes:'' })

const inspections = ref([
  { id:1,  ref:'INS-041', title:'Roof Truss Weld Inspection',      type:'Structural',    category:'Structural', site:'Nairobi Housing — Phase 1',  location:'Block A Roofline',       inspector:'Eng. Kariuki',  inspectorRole:'Site Engineer',  date:'2025-02-18', score:91, ncrs:0, checklistItems:18, result:'passed',    findings:'All welds inspected. No visible defects. Penetrant test clear.' },
  { id:2,  ref:'INS-040', title:'Floor 4 Concrete Cube Test',      type:'Material Test', category:'Structural', site:'Nairobi Housing — Phase 1',  location:'Floor 4 Slab',          inspector:'Eng. Kariuki',  inspectorRole:'Site Engineer',  date:'2025-02-16', score:88, ncrs:0, checklistItems:8,  result:'passed',    findings:'28-day cube strength 28.4 MPa. Spec: 25 MPa. Pass.' },
  { id:3,  ref:'INS-039', title:'Plumbing Pressure Test',          type:'MEP',           category:'MEP',        site:'Nairobi Housing — Phase 1',  location:'Floor 2, Zone B',       inspector:'Eng. Njoroge',  inspectorRole:'MEP Engineer',   date:'2025-02-14', score:62, ncrs:1, checklistItems:12, result:'failed',    findings:'Pressure drop observed at Zone B junction. Likely joint failure.' },
  { id:4,  ref:'INS-038', title:'Base Course CBR Test',            type:'Material Test', category:'Civil Works', site:'Mombasa Port Road',          location:'Ch.0+350 to Ch.0+450', inspector:'Eng. Oduya',    inspectorRole:'RE',             date:'2025-02-18', score:58, ncrs:1, checklistItems:6,  result:'failed',    findings:'CBR value 62% against minimum 80%. Material does not comply.' },
  { id:5,  ref:'INS-037', title:'Compaction Test Ch.0+350',        type:'Civil Works',   category:'Civil Works', site:'Mombasa Port Road',          location:'Ch.0+350',              inspector:'Lab Tech. Mweu', inspectorRole:'Lab Technician', date:'2025-02-17', score:null,ncrs:0,checklistItems:4,  result:'pending',   findings:null },
  { id:6,  ref:'INS-035', title:'Column Casting — Grid E',         type:'Structural',    category:'Structural', site:'Kisumu Commercial Complex',   location:'Floor 3, Grid E',       inspector:'Eng. Achieng',  inspectorRole:'Site Engineer',  date:'2025-02-17', score:96, ncrs:0, checklistItems:14, result:'passed',    findings:'Concrete slump 75mm within spec. Vibration adequate. All good.' },
  { id:7,  ref:'INS-032', title:'Road Marking Reflectivity Test',  type:'Finishing',     category:'Finishing',  site:'Nakuru Ring Road',           location:'Section B, km 3.2-4.0', inspector:'Eng. Mwangi',   inspectorRole:'Site Engineer',  date:'2025-02-17', score:97, ncrs:0, checklistItems:10, result:'passed',    findings:'Retroreflectivity readings all above 150 mcd/m²/lux.' },
  { id:8,  ref:'INS-043', title:'Electrical Conduit Inspection',   type:'MEP',           category:'MEP',        site:'Nairobi Housing — Phase 1',  location:'Floor 5, Zone A-C',     inspector:'Eng. Njoroge',  inspectorRole:'MEP Engineer',   date:'2025-02-25', score:null,ncrs:0,checklistItems:16, result:'scheduled', findings:null },
])

const tabs = computed(()=>[
  {key:'all',       label:'All',       count:inspections.value.length},
  {key:'scheduled', label:'Scheduled', count:inspections.value.filter(i=>i.result==='scheduled').length},
  {key:'pending',   label:'Pending',   count:inspections.value.filter(i=>i.result==='pending').length},
  {key:'passed',    label:'Passed',    count:inspections.value.filter(i=>i.result==='passed').length},
  {key:'failed',    label:'Failed',    count:inspections.value.filter(i=>i.result==='failed').length},
])

const filteredInspections = computed(()=>inspections.value.filter(i=>
  (activeTab.value==='all'||i.result===activeTab.value)
  &&(!search.value||i.title.toLowerCase().includes(search.value.toLowerCase())||i.site.toLowerCase().includes(search.value.toLowerCase()))
  &&(!filterType.value||i.type===filterType.value)
  &&(!filterSite.value||i.site===filterSite.value)
))

function scheduleInspection() {
  inspections.value.unshift({ id:Date.now(), ref:`INS-0${inspections.value.length+44}`, ...form.value, inspectorRole:'Site Engineer', score:null, ncrs:0, checklistItems:0, result:'scheduled', findings:null })
  showForm.value=false
  form.value = { title:'', type:'', site:'', location:'', date:'', inspector:'', category:'', notes:'' }
}
</script>

<style scoped>
@import '/src/assets/qa.css';
.type-pill { font-family:'DM Mono',monospace; font-size:9px; padding:2px 8px; border-radius:10px; background:#1a1e2e; color:#6366f1; white-space:nowrap; }
</style>