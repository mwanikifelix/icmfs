<template>
  <div class="qa-page">
    <div class="page-header">
      <div>
        <span class="page-tag amber">QA · CERTIFICATIONS</span>
        <h1>QA Certifications</h1>
        <p class="page-sub">Material test certificates, compliance documents and third-party approvals</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary amber" @click="showForm=true">+ Upload Certificate</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card green">
        <div class="stat-val">{{ certs.filter(c=>c.status==='active').length }}</div>
        <div class="stat-label">Active Certs</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">{{ certs.filter(c=>c.status==='expiring').length }}</div>
        <div class="stat-label">Expiring Soon</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-val">{{ certs.filter(c=>c.status==='overdue').length }}</div>
        <div class="stat-label">Expired</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-val">{{ certs.filter(c=>c.status==='pending').length }}</div>
        <div class="stat-label">Awaiting Issue</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ certs.length }}</div>
        <div class="stat-label">Total Records</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search certificate, material or project..." />
      </div>
      <select v-model="filterType" class="filter-select">
        <option value="">All Types</option>
        <option v-for="t in certTypes" :key="t">{{ t }}</option>
      </select>
      <select v-model="filterProject" class="filter-select">
        <option value="">All Projects</option>
        <option v-for="p in projects" :key="p">{{ p }}</option>
      </select>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="expiring">Expiring</option>
        <option value="overdue">Expired</option>
        <option value="pending">Pending</option>
      </select>
    </div>

    <!-- Certs grid -->
    <div class="cert-grid">
      <div v-for="cert in filteredCerts" :key="cert.id" class="cert-card" @click="active=cert">
        <div class="cert-card-top">
          <div class="cert-icon">{{ certIcon(cert.type) }}</div>
          <span class="status-badge" :class="cert.status">{{ cert.status }}</span>
        </div>
        <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:4px">{{ cert.title }}</div>
        <div class="cell-sub" style="margin-bottom:12px">{{ cert.material }} · {{ cert.project }}</div>
        <div class="cert-meta">
          <div class="cert-meta-item"><span class="dlbl">Issued By</span><span class="dval" style="font-size:12px">{{ cert.issuedBy }}</span></div>
          <div class="cert-meta-item"><span class="dlbl">Issue Date</span><span class="dval" style="font-size:12px">{{ cert.issueDate }}</span></div>
          <div class="cert-meta-item"><span class="dlbl">Expiry</span><span class="dval" style="font-size:12px" :style="cert.status==='overdue'?'color:#ef4444':cert.status==='expiring'?'color:#f59e0b':''">{{ cert.expiry || 'N/A' }}</span></div>
          <div class="cert-meta-item"><span class="dlbl">Cert No.</span><span class="dval mono" style="font-size:11px;color:#6366f1">{{ cert.certNo }}</span></div>
        </div>
      </div>
    </div>

    <!-- Drawer -->
    <div class="drawer-overlay" v-if="active" @click.self="active=null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#f5a623;display:block;margin-bottom:4px">{{ active.certNo }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ active.title }}</h2>
            <div style="display:flex;gap:8px;margin-top:6px">
              <span class="status-badge" :class="active.status">{{ active.status }}</span>
              <span class="cell-sub">{{ active.type }}</span>
            </div>
          </div>
          <button class="close-btn" @click="active=null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item"><span class="dlbl">Material / Item</span><span class="dval">{{ active.material }}</span></div>
            <div class="detail-item"><span class="dlbl">Project</span><span class="dval">{{ active.project }}</span></div>
            <div class="detail-item"><span class="dlbl">Issued By</span><span class="dval">{{ active.issuedBy }}</span></div>
            <div class="detail-item"><span class="dlbl">Issue Date</span><span class="dval">{{ active.issueDate }}</span></div>
            <div class="detail-item"><span class="dlbl">Expiry Date</span><span class="dval" :style="active.status==='overdue'?'color:#ef4444':active.status==='expiring'?'color:#f59e0b':''">{{ active.expiry || 'No expiry' }}</span></div>
            <div class="detail-item"><span class="dlbl">Standard</span><span class="dval">{{ active.standard }}</span></div>
          </div>
          <div v-if="active.results" style="margin-bottom:14px">
            <div class="dlbl" style="margin-bottom:8px">Test Results</div>
            <div style="display:flex;flex-direction:column;gap:6px">
              <div v-for="r in active.results" :key="r.param"
                style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;background:#0d0f14;border-radius:8px">
                <span style="font-size:12px;color:#9ca3af">{{ r.param }}</span>
                <div style="display:flex;align-items:center;gap:8px">
                  <span class="mono" style="font-size:12px;color:#e8e4dc">{{ r.value }}</span>
                  <span :style="r.pass?'color:#22c55e':'color:#ef4444'" style="font-size:13px">{{ r.pass?'✓':'✗' }}</span>
                </div>
              </div>
            </div>
          </div>
          <div v-if="active.notes" style="background:#0d0f14;border-radius:8px;padding:12px;font-size:12px;color:#9ca3af;line-height:1.6;margin-bottom:14px">
            📝 {{ active.notes }}
          </div>
          <div style="display:flex;gap:8px">
            <button class="btn-primary amber" style="flex:1;text-align:center" @click="active=null">📥 Download PDF</button>
            <button class="btn-ghost" style="flex:1;text-align:center" @click="active=null">✏️ Edit</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm=false">
      <div class="modal">
        <div class="modal-header">
          <h2>📜 Upload Certificate</h2>
          <button class="close-btn" @click="showForm=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Certificate Title *</label><input v-model="form.title" placeholder="e.g. Concrete Cube Test — 28 Day" /></div>
            <div class="form-group"><label>Type *</label>
              <select v-model="form.type"><option v-for="t in certTypes" :key="t">{{ t }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Material / Item *</label><input v-model="form.material" placeholder="e.g. OPC Cement Grade 32.5N" /></div>
            <div class="form-group"><label>Project *</label>
              <select v-model="form.project"><option value="">Select...</option><option v-for="p in projects" :key="p">{{ p }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Certificate No. *</label><input v-model="form.certNo" placeholder="CERT-XXXX" /></div>
            <div class="form-group"><label>Issued By *</label><input v-model="form.issuedBy" placeholder="Issuing laboratory / body" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Issue Date *</label><input type="date" v-model="form.issueDate" /></div>
            <div class="form-group"><label>Expiry Date</label><input type="date" v-model="form.expiry" /></div>
          </div>
          <div class="form-group full"><label>Applicable Standard</label><input v-model="form.standard" placeholder="e.g. BS EN 206, KS 02-1070" /></div>
          <div class="form-group full">
            <label>Attach Certificate (PDF)</label>
            <div style="border:1px dashed #2a2f3e;border-radius:8px;padding:20px;text-align:center;color:#4b5563;font-size:12px;cursor:pointer">📎 Click to upload or drag PDF here</div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm=false">Cancel</button>
          <button class="btn-primary amber" @click="uploadCert">Upload</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const search = ref('')
const filterType = ref('')
const filterProject = ref('')
const filterStatus = ref('')
const showForm = ref(false)
const active = ref(null)
const certTypes = ['Concrete Test','Material Test','Compaction Test','Weld Certificate','KEBS Approval','Third-Party Inspection','Equipment Calibration']
const projects  = ['Nairobi Housing — Phase 1','Mombasa Port Road','Kisumu Commercial Complex','Nakuru Ring Road']
const form = ref({ title:'', type:'Concrete Test', material:'', project:'', certNo:'', issuedBy:'', issueDate:'', expiry:'', standard:'' })

const certs = ref([
  { id:1, title:'Concrete Cube Test — 28 Day',           type:'Concrete Test',           material:'OPC Cement Grade 32.5N — Floor 4 Slab',  project:'Nairobi Housing — Phase 1', certNo:'CCT-2025-044', issuedBy:'SGS Kenya Lab',          issueDate:'2025-02-16', expiry:null,        status:'active',   standard:'BS EN 12390', results:[{param:'28-Day Strength',value:'28.4 MPa',pass:true},{param:'Slump',value:'80mm',pass:true},{param:'W/C Ratio',value:'0.52',pass:true}], notes:'All 6 cubes passed. Minimum spec 25 MPa.' },
  { id:2, title:'Steel Rebar Tensile Test',               type:'Material Test',           material:'Steel Y16 Rebar — 5 Tonne Delivery',     project:'Kisumu Commercial Complex', certNo:'SRT-2025-029', issuedBy:'Kenya Bureau of Standards',  issueDate:'2025-02-17', expiry:null,        status:'active',   standard:'BS4449', results:[{param:'Yield Strength',value:'520 MPa',pass:true},{param:'UTS',value:'620 MPa',pass:true},{param:'Elongation',value:'18%',pass:true}], notes:'Batch tested at KEBS lab. Certified.' },
  { id:3, title:'Compaction Test — CBR Report',           type:'Compaction Test',         material:'Base Course Material — Ch.0+350',        project:'Mombasa Port Road',         certNo:'CBR-2025-012', issuedBy:'Geotechnical Lab EA',        issueDate:'2025-02-18', expiry:null,        status:'active',   standard:'ASTM D1883', results:[{param:'CBR Value',value:'62%',pass:false},{param:'MDD',value:'1.85 t/m³',pass:true},{param:'OMC',value:'8.2%',pass:true}], notes:'CBR FAILED — below 80% minimum. NCR raised.' },
  { id:4, title:'Scaffolding Inspection Certificate',     type:'Third-Party Inspection',  material:'Ringlock Scaffolding — Block A',         project:'Nairobi Housing — Phase 1', certNo:'SCI-2025-008', issuedBy:'DOSH Approved Inspector',    issueDate:'2025-02-10', expiry:'2025-05-10', status:'active',   standard:'KS 2394', results:null, notes:'Valid for 3 months. Re-inspect before May 10.' },
  { id:5, title:'Concrete Pump Calibration Certificate', type:'Equipment Calibration',    material:'Schwing Stetter CP30 Pump',             project:'Kisumu Commercial Complex', certNo:'ECC-2025-003', issuedBy:'Pump Services Ltd',          issueDate:'2025-01-15', expiry:'2025-07-15', status:'active',   standard:'Manufacturer Spec', results:null, notes:'Calibrated January 2025. Valid 6 months.' },
  { id:6, title:'Cement KEBS Approval Letter',           type:'KEBS Approval',           material:'Bamburi OPC 32.5N — Batch Mar 2025',    project:'All Projects',              certNo:'KEBS-2025-BC4', issuedBy:'Kenya Bureau of Standards', issueDate:'2025-02-01', expiry:'2025-08-01', status:'active',   standard:'KS EAS 18-1', results:null, notes:'Covers full March production batch.' },
  { id:7, title:'Weld Inspection Certificate — Trusses', type:'Weld Certificate',         material:'MS Roof Trusses — Block A',             project:'Nairobi Housing — Phase 1', certNo:'WIC-2025-011', issuedBy:'Certified Welding Inspector',issueDate:'2025-02-18', expiry:null,        status:'active',   standard:'AWS D1.1', results:[{param:'Visual Inspection',value:'Pass',pass:true},{param:'Penetrant Test',value:'No defects',pass:true}], notes:'All 22 trusses inspected and approved.' },
  { id:8, title:'Tower Crane Load Test Certificate',     type:'Equipment Calibration',    material:'Liebherr 100 EC-B Tower Crane',         project:'Kisumu Commercial Complex', certNo:'ECC-2024-091', issuedBy:'DOSH Approved Inspector',    issueDate:'2024-11-20', expiry:'2025-03-01', status:'expiring', standard:'KS ISO 4306', results:null, notes:'Expiring in 10 days. Schedule re-inspection.' },
])

const filteredCerts = computed(()=>certs.value.filter(c=>
  (!search.value||c.title.toLowerCase().includes(search.value.toLowerCase())||c.material.toLowerCase().includes(search.value.toLowerCase()))
  &&(!filterType.value||c.type===filterType.value)
  &&(!filterProject.value||c.project===filterProject.value)
  &&(!filterStatus.value||c.status===filterStatus.value)
))

function certIcon(type) {
  const m = { 'Concrete Test':'🧪','Material Test':'🔬','Compaction Test':'📐','Weld Certificate':'⚡','KEBS Approval':'📜','Third-Party Inspection':'🔍','Equipment Calibration':'⚙️' }
  return m[type] || '📄'
}

function uploadCert() {
  certs.value.unshift({ id:Date.now(), ...form.value, status:'active', results:null, notes:'' })
  showForm.value=false
  form.value = { title:'', type:'Concrete Test', material:'', project:'', certNo:'', issuedBy:'', issueDate:'', expiry:'', standard:'' }
}
</script>

<style scoped>
@import '/src/assets/qa.css';
.cert-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
.cert-card { background:#13161f; border:1px solid #1e2230; border-radius:12px; padding:18px; cursor:pointer; transition:border-color 0.2s; }
.cert-card:hover { border-color:#f5a623; }
.cert-card-top { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px; }
.cert-icon { font-size:24px; }
.cert-meta { display:grid; grid-template-columns:1fr 1fr; gap:8px; padding-top:12px; border-top:1px solid #1e2230; }
.cert-meta-item { display:flex; flex-direction:column; gap:2px; }
</style>