<template>
  <div class="incident-reports">
    <!-- Header -->
    <div class="page-header">
      <div>
        <span class="page-tag">SAFETY MODULE</span>
        <h1>Incident Reports</h1>
        <p class="page-sub">Log, track, and certify site incidents with digital signatures</p>
      </div>
      <button class="btn-primary" @click="showForm = true">
        <span>+</span> New Incident Report
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input v-model="search" type="text" placeholder="Search incidents..." class="search-input" />
      </div>
      <select v-model="filterSeverity" class="filter-select">
        <option value="">All Severity</option>
        <option value="critical">Critical</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="open">Open</option>
        <option value="investigating">Investigating</option>
        <option value="resolved">Resolved</option>
        <option value="closed">Closed</option>
      </select>
      <select v-model="filterSite" class="filter-select">
        <option value="">All Sites</option>
        <option v-for="s in siteOptions" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>

    <!-- Stats Row -->
    <div class="stat-row">
      <div class="stat-pill" v-for="stat in stats" :key="stat.label" :class="stat.cls">
        <span class="stat-num">{{ stat.count }}</span>
        <span class="stat-lbl">{{ stat.label }}</span>
      </div>
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="incidents-table">
        <thead>
          <tr>
            <th>REF #</th>
            <th>Incident</th>
            <th>Site</th>
            <th>Reported By</th>
            <th>Date</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Signed</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="incident in filteredIncidents" :key="incident.id" class="table-row">
            <td class="ref-cell">
              <span class="mono">{{ incident.ref }}</span>
            </td>
            <td class="title-cell">
              <div class="inc-title">{{ incident.title }}</div>
              <div class="inc-desc">{{ incident.description }}</div>
            </td>
            <td class="site-cell">
              <div class="site-name">{{ incident.site }}</div>
              <div class="site-loc mono">{{ incident.location }}</div>
            </td>
            <td>
              <div class="reporter">
                <div class="avatar">{{ incident.reportedBy[0] }}</div>
                <div>
                  <div class="rep-name">{{ incident.reportedBy }}</div>
                  <div class="rep-role mono">{{ incident.role }}</div>
                </div>
              </div>
            </td>
            <td class="date-cell mono">{{ incident.date }}</td>
            <td>
              <span class="sev-badge" :class="incident.severity">{{ incident.severity }}</span>
            </td>
            <td>
              <span class="status-badge" :class="incident.status">{{ incident.status }}</span>
            </td>
            <td class="sig-cell">
              <div v-if="incident.signed" class="sig-ok">
                <span>🔏</span>
                <span class="mono sig-text">Signed</span>
              </div>
              <div v-else class="sig-pending">
                <span>⏳</span>
                <span class="mono sig-text">Pending</span>
              </div>
            </td>
            <td>
              <div class="action-btns">
                <button class="tbl-btn view" @click="viewIncident(incident)">View</button>
                <button class="tbl-btn sign" v-if="!incident.signed" @click="signIncident(incident)">Sign</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- New Incident Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>New Incident Report</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Incident Title *</label>
              <input v-model="form.title" type="text" placeholder="Brief description of incident" />
            </div>
            <div class="form-group">
              <label>Date & Time *</label>
              <input v-model="form.date" type="datetime-local" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Site *</label>
              <select v-model="form.site">
                <option value="">Select site...</option>
                <option v-for="s in siteOptions" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Severity *</label>
              <select v-model="form.severity">
                <option value="">Select severity...</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
          </div>
          <div class="form-group full">
            <label>Detailed Description *</label>
            <textarea v-model="form.description" rows="4" placeholder="Describe what happened, where, and who was involved..."></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Type of Incident</label>
              <select v-model="form.type">
                <option value="">Select type...</option>
                <option>Worker Injury</option>
                <option>Equipment Failure</option>
                <option>Structural Issue</option>
                <option>Fire/Electrical</option>
                <option>Near Miss</option>
                <option>Environmental</option>
              </select>
            </div>
            <div class="form-group">
              <label>Immediate Action Taken</label>
              <input v-model="form.action" type="text" placeholder="e.g. Area cordoned off, First aid given" />
            </div>
          </div>

          <!-- Digital Signature Section -->
          <div class="sig-section">
            <div class="sig-header">
              <span>🔏</span>
              <div>
                <div class="sig-title">Digital Signature (RSA)</div>
                <div class="sig-sub">Cryptographically sign this report per ICMFS security policy</div>
              </div>
            </div>
            <div class="sig-toggle">
              <label class="toggle-label">
                <input type="checkbox" v-model="form.signNow" />
                <span class="toggle-track"><span class="toggle-thumb"></span></span>
                Sign this report now using my private key
              </label>
            </div>
            <div v-if="form.signNow" class="sig-key-input">
              <label>Key Passphrase</label>
              <input type="password" v-model="form.passphrase" placeholder="Enter your key passphrase..." />
              <div class="sig-note mono">Your signature certifies this report is accurate and complete.</div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary" @click="submitIncident">Submit Report</button>
        </div>
      </div>
    </div>

    <!-- View Incident Drawer -->
    <div class="drawer-overlay" v-if="activeIncident" @click.self="activeIncident = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono ref-tag">{{ activeIncident.ref }}</span>
            <h2>{{ activeIncident.title }}</h2>
          </div>
          <button class="close-btn" @click="activeIncident = null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item">
              <span class="detail-lbl">Site</span>
              <span class="detail-val">{{ activeIncident.site }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-lbl">Date</span>
              <span class="detail-val mono">{{ activeIncident.date }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-lbl">Severity</span>
              <span class="sev-badge" :class="activeIncident.severity">{{ activeIncident.severity }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-lbl">Status</span>
              <span class="status-badge" :class="activeIncident.status">{{ activeIncident.status }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-lbl">Reported By</span>
              <span class="detail-val">{{ activeIncident.reportedBy }} ({{ activeIncident.role }})</span>
            </div>
            <div class="detail-item">
              <span class="detail-lbl">Digital Signature</span>
              <span class="detail-val">{{ activeIncident.signed ? '✅ Verified — RSA-2048' : '⏳ Awaiting signature' }}</span>
            </div>
          </div>
          <div class="detail-desc">
            <span class="detail-lbl">Description</span>
            <p>{{ activeIncident.fullDescription }}</p>
          </div>
          <div class="timeline">
            <div class="tl-header">Activity Log</div>
            <div class="tl-item" v-for="log in activeIncident.logs" :key="log.time">
              <div class="tl-dot"></div>
              <div class="tl-content">
                <div class="tl-text">{{ log.text }}</div>
                <div class="tl-time mono">{{ log.time }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const showForm = ref(false)
const activeIncident = ref(null)
const search = ref('')
const filterSeverity = ref('')
const filterStatus = ref('')
const filterSite = ref('')

const siteOptions = ['Nairobi Housing — Phase 1', 'Mombasa Infrastructure', 'Kisumu Commercial', 'Nakuru Road Project']

const form = ref({
  title: '', date: '', site: '', severity: '',
  description: '', type: '', action: '',
  signNow: false, passphrase: ''
})

const incidents = ref([
  {
    id: 1, ref: 'INC-2025-001',
    title: 'Scaffolding Partial Collapse',
    description: 'Section B scaffolding failed near grid line 4',
    fullDescription: 'At approximately 14:30hrs, scaffolding on the east face of Block C at grid line 4 partially collapsed. No workers were directly under the structure at the time. The area has been cordoned off and a structural engineer has been notified.',
    site: 'Nairobi Housing — Phase 1', location: 'Nairobi',
    reportedBy: 'James Mutua', role: 'Site Engineer',
    date: '2025-02-18', severity: 'critical', status: 'investigating', signed: true,
    logs: [
      { text: 'Incident reported by James Mutua', time: '2025-02-18 14:45' },
      { text: 'Area cordoned off — safety officer notified', time: '2025-02-18 15:00' },
      { text: 'Structural engineer dispatched', time: '2025-02-18 16:20' },
    ]
  },
  {
    id: 2, ref: 'INC-2025-002',
    title: 'Worker Minor Injury — Laceration',
    description: 'Worker sustained cut from exposed rebar on Level 2',
    fullDescription: 'A site worker sustained a minor laceration on the right forearm from exposed rebar on Level 2. First aid was administered on site. Worker was taken to the site clinic for dressing and tetanus shot.',
    site: 'Mombasa Infrastructure', location: 'Mombasa',
    reportedBy: 'Grace Otieno', role: 'Safety Officer',
    date: '2025-02-15', severity: 'medium', status: 'resolved', signed: true,
    logs: [
      { text: 'Injury reported — first aid administered', time: '2025-02-15 10:10' },
      { text: 'Worker transported to site clinic', time: '2025-02-15 10:35' },
      { text: 'Report signed and certified by Safety Officer', time: '2025-02-15 13:00' },
    ]
  },
  {
    id: 3, ref: 'INC-2025-003',
    title: 'Electrical Hazard — Exposed Wiring',
    description: 'Exposed live wires found in generator room',
    fullDescription: 'During routine inspection, exposed live wiring was discovered in the generator room on the ground floor. Power to the section was immediately cut. The electrical contractor has been notified.',
    site: 'Kisumu Commercial', location: 'Kisumu',
    reportedBy: 'Peter Kamau', role: 'Consultant',
    date: '2025-02-12', severity: 'high', status: 'open', signed: false,
    logs: [
      { text: 'Hazard identified during inspection', time: '2025-02-12 09:15' },
      { text: 'Power disconnected to affected section', time: '2025-02-12 09:30' },
    ]
  },
  {
    id: 4, ref: 'INC-2025-004',
    title: 'Near Miss — Falling Object',
    description: 'Tool dropped from Level 4 narrowly missed worker',
    fullDescription: 'A wrench was accidentally dropped from Level 4 scaffolding and narrowly missed a worker below. The worker was not injured. Toolbox tethering policy has been re-enforced.',
    site: 'Nakuru Road Project', location: 'Nakuru',
    reportedBy: 'Alice Wanjiku', role: 'Project Manager',
    date: '2025-02-10', severity: 'low', status: 'closed', signed: true,
    logs: [
      { text: 'Near miss reported — no injuries', time: '2025-02-10 11:00' },
      { text: 'Team briefing on toolbox tethering conducted', time: '2025-02-10 15:00' },
      { text: 'Incident closed — corrective action verified', time: '2025-02-11 08:30' },
    ]
  },
])

const stats = computed(() => [
  { label: 'Total', count: incidents.value.length, cls: 'all' },
  { label: 'Open', count: incidents.value.filter(i => i.status === 'open').length, cls: 'danger' },
  { label: 'Investigating', count: incidents.value.filter(i => i.status === 'investigating').length, cls: 'warning' },
  { label: 'Resolved', count: incidents.value.filter(i => i.status === 'resolved').length, cls: 'good' },
  { label: 'Critical', count: incidents.value.filter(i => i.severity === 'critical').length, cls: 'critical' },
])

const filteredIncidents = computed(() => {
  return incidents.value.filter(i => {
    const matchSearch = !search.value || i.title.toLowerCase().includes(search.value.toLowerCase()) || i.ref.includes(search.value)
    const matchSev = !filterSeverity.value || i.severity === filterSeverity.value
    const matchStatus = !filterStatus.value || i.status === filterStatus.value
    const matchSite = !filterSite.value || i.site === filterSite.value
    return matchSearch && matchSev && matchStatus && matchSite
  })
})

function viewIncident(incident) { activeIncident.value = incident }

function signIncident(incident) {
  if (confirm(`Sign incident ${incident.ref} with your digital key?`)) {
    incident.signed = true
    incident.logs.push({ text: 'Report digitally signed (RSA-2048)', time: new Date().toLocaleString() })
  }
}

function submitIncident() {
  if (!form.value.title || !form.value.site || !form.value.severity) {
    alert('Please fill in all required fields.')
    return
  }
  const newInc = {
    id: incidents.value.length + 1,
    ref: `INC-2025-00${incidents.value.length + 1}`,
    title: form.value.title,
    description: form.value.description.slice(0, 60) + '...',
    fullDescription: form.value.description,
    site: form.value.site, location: form.value.site.split(' ')[0],
    reportedBy: 'Current User', role: 'Site Engineer',
    date: form.value.date?.split('T')[0] || new Date().toISOString().split('T')[0],
    severity: form.value.severity, status: 'open',
    signed: form.value.signNow,
    logs: [{ text: 'Incident report submitted', time: new Date().toLocaleString() }]
  }
  incidents.value.unshift(newInc)
  showForm.value = false
  form.value = { title: '', date: '', site: '', severity: '', description: '', type: '', action: '', signNow: false, passphrase: '' }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.incident-reports {
  font-family: 'Syne', sans-serif;
  background: #0d0f14;
  color: #e8e4dc;
  min-height: 100vh;
  padding: 28px 32px;
}

.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.page-tag { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; color: #f5a623; text-transform: uppercase; display: block; margin-bottom: 6px; }
h1 { font-size: 28px; font-weight: 800; color: #fff; }
.page-sub { font-size: 13px; color: #6b7280; margin-top: 4px; }

.btn-primary { background: #f5a623; color: #0d0f14; border: none; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: opacity 0.2s; }
.btn-primary:hover { opacity: 0.9; }
.btn-ghost { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }

.filters-bar { display: flex; gap: 12px; margin-bottom: 16px; }
.search-wrap { position: relative; flex: 1; }
.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); font-size: 13px; }
.search-input { width: 100%; background: #13161f; border: 1px solid #1e2230; color: #e8e4dc; padding: 9px 12px 9px 34px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; }
.filter-select { background: #13161f; border: 1px solid #1e2230; color: #e8e4dc; padding: 9px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }

.stat-row { display: flex; gap: 10px; margin-bottom: 20px; }
.stat-pill { display: flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 20px; font-size: 12px; }
.stat-pill.all      { background: #1a1e2a; color: #9ca3af; }
.stat-pill.danger   { background: #200e0e; color: #ef4444; }
.stat-pill.warning  { background: #1f1a08; color: #f59e0b; }
.stat-pill.good     { background: #0d2818; color: #22c55e; }
.stat-pill.critical { background: #2a0808; color: #dc2626; border: 1px solid #dc2626; }
.stat-num { font-weight: 800; font-size: 16px; }

.table-wrap { overflow-x: auto; background: #13161f; border: 1px solid #1e2230; border-radius: 12px; }
.incidents-table { width: 100%; border-collapse: collapse; }
.incidents-table thead th { padding: 14px 16px; text-align: left; font-size: 10px; font-family: 'DM Mono', monospace; letter-spacing: 1px; color: #4b5563; border-bottom: 1px solid #1e2230; text-transform: uppercase; }
.table-row { border-bottom: 1px solid #1a1e2a; transition: background 0.15s; }
.table-row:hover { background: #161922; }
.table-row td { padding: 14px 16px; vertical-align: middle; }
.mono { font-family: 'DM Mono', monospace; }
.ref-cell .mono { font-size: 11px; color: #f5a623; }
.inc-title { font-size: 13px; font-weight: 600; color: #e8e4dc; }
.inc-desc { font-size: 11px; color: #4b5563; margin-top: 2px; }
.site-name { font-size: 12px; font-weight: 600; }
.site-loc { font-size: 10px; color: #4b5563; }
.reporter { display: flex; align-items: center; gap: 8px; }
.avatar { width: 28px; height: 28px; border-radius: 50%; background: #f5a623; color: #0d0f14; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 12px; flex-shrink: 0; }
.rep-name { font-size: 12px; font-weight: 600; }
.rep-role { font-size: 10px; color: #4b5563; }
.date-cell { font-size: 12px; color: #9ca3af; }

.sev-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; }
.sev-badge.critical { background: #2a0808; color: #dc2626; }
.sev-badge.high     { background: #200e0e; color: #ef4444; }
.sev-badge.medium   { background: #1f1a08; color: #f59e0b; }
.sev-badge.low      { background: #0d2818; color: #22c55e; }

.status-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.status-badge.open          { background: #200e0e; color: #ef4444; }
.status-badge.investigating { background: #1f1a08; color: #f59e0b; }
.status-badge.resolved      { background: #0d2818; color: #22c55e; }
.status-badge.closed        { background: #1a1e2a; color: #6b7280; }

.sig-cell .sig-ok, .sig-cell .sig-pending { display: flex; align-items: center; gap: 5px; }
.sig-text { font-size: 10px; }
.sig-ok .sig-text { color: #22c55e; }
.sig-pending .sig-text { color: #6b7280; }

.action-btns { display: flex; gap: 6px; }
.tbl-btn { padding: 4px 10px; border-radius: 5px; font-size: 11px; font-family: 'Syne', sans-serif; cursor: pointer; border: 1px solid; }
.tbl-btn.view { background: none; border-color: #2a2f3e; color: #9ca3af; }
.tbl-btn.view:hover { border-color: #3b82f6; color: #3b82f6; }
.tbl-btn.sign { background: none; border-color: #1a3020; color: #22c55e; }
.tbl-btn.sign:hover { background: #0d2818; }

/* MODAL */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 100; display: flex; align-items: center; justify-content: center; }
.modal { background: #13161f; border: 1px solid #2a2f3e; border-radius: 16px; width: 700px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 22px 28px; border-bottom: 1px solid #1e2230; }
.modal-header h2 { font-size: 18px; font-weight: 700; }
.close-btn { background: none; border: none; color: #6b7280; font-size: 18px; cursor: pointer; }
.modal-body { padding: 24px 28px; display: flex; flex-direction: column; gap: 16px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 18px 28px; border-top: 1px solid #1e2230; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group.full { grid-column: 1 / -1; }
.form-group label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; }
.form-group input, .form-group select, .form-group textarea {
  background: #0d0f14; border: 1px solid #1e2230; color: #e8e4dc;
  padding: 10px 12px; border-radius: 7px; font-family: 'Syne', sans-serif;
  font-size: 13px; transition: border-color 0.2s;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #f5a623; }

.sig-section { background: #0a0c10; border: 1px solid #1a2535; border-radius: 10px; padding: 16px; }
.sig-header { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 14px; font-size: 20px; }
.sig-title { font-size: 13px; font-weight: 700; color: #e8e4dc; }
.sig-sub { font-size: 11px; color: #4b5563; margin-top: 2px; }
.toggle-label { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #9ca3af; cursor: pointer; }
.toggle-label input { display: none; }
.toggle-track { width: 38px; height: 20px; background: #1e2230; border-radius: 10px; position: relative; flex-shrink: 0; transition: background 0.2s; }
.toggle-label input:checked + .toggle-track { background: #f5a623; }
.toggle-thumb { position: absolute; top: 3px; left: 3px; width: 14px; height: 14px; background: #fff; border-radius: 50%; transition: left 0.2s; }
.toggle-label input:checked + .toggle-track .toggle-thumb { left: 21px; }
.sig-key-input { margin-top: 12px; display: flex; flex-direction: column; gap: 8px; }
.sig-key-input label { font-size: 11px; color: #6b7280; font-family: 'DM Mono', monospace; }
.sig-key-input input { background: #0d0f14; border: 1px solid #1a2535; color: #e8e4dc; padding: 9px 12px; border-radius: 6px; font-family: 'DM Mono', monospace; font-size: 13px; }
.sig-note { font-size: 10px; color: #4b5563; }

/* DRAWER */
.drawer-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 100; display: flex; justify-content: flex-end; }
.drawer { background: #13161f; border-left: 1px solid #2a2f3e; width: 500px; height: 100%; overflow-y: auto; }
.drawer-header { padding: 24px; border-bottom: 1px solid #1e2230; display: flex; justify-content: space-between; align-items: flex-start; }
.ref-tag { font-family: 'DM Mono', monospace; font-size: 11px; color: #f5a623; display: block; margin-bottom: 4px; }
.drawer-header h2 { font-size: 16px; font-weight: 700; max-width: 380px; }
.drawer-body { padding: 24px; }

.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
.detail-item { display: flex; flex-direction: column; gap: 4px; }
.detail-lbl { font-size: 10px; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; }
.detail-val { font-size: 13px; color: #e8e4dc; }
.detail-desc { margin-bottom: 24px; }
.detail-desc p { font-size: 13px; color: #9ca3af; line-height: 1.6; margin-top: 8px; }

.tl-header { font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; margin-bottom: 14px; }
.tl-item { display: flex; gap: 12px; margin-bottom: 14px; }
.tl-dot { width: 8px; height: 8px; border-radius: 50%; background: #f5a623; flex-shrink: 0; margin-top: 4px; }
.tl-text { font-size: 12px; color: #d1d5db; }
.tl-time { font-size: 10px; color: #4b5563; margin-top: 3px; }
</style>