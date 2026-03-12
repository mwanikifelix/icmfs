<template>
  <div class="safety-audits">
    <!-- Header -->
    <div class="page-header">
      <div>
        <span class="page-tag">SAFETY MODULE</span>
        <h1>Safety Audits</h1>
        <p class="page-sub">Schedule, conduct, and certify safety inspections across all sites</p>
      </div>
      <button class="btn-primary" @click="showForm = true">+ Schedule Audit</button>
    </div>

    <!-- Calendar / List Toggle -->
    <div class="view-toggle">
      <button :class="['toggle-btn', viewMode === 'list' ? 'active' : '']" @click="viewMode = 'list'">☰ List</button>
      <button :class="['toggle-btn', viewMode === 'calendar' ? 'active' : '']" @click="viewMode = 'calendar'">📅 Calendar</button>
    </div>

    <!-- Summary Cards -->
    <div class="summary-cards">
      <div class="sum-card" v-for="s in summaryStats" :key="s.label" :class="s.cls">
        <div class="sum-icon">{{ s.icon }}</div>
        <div class="sum-val">{{ s.value }}</div>
        <div class="sum-label">{{ s.label }}</div>
      </div>
    </div>

    <!-- LIST VIEW -->
    <div v-if="viewMode === 'list'">
      <!-- Tabs -->
      <div class="tabs">
        <button v-for="tab in tabs" :key="tab.key"
          :class="['tab', activeTab === tab.key ? 'active' : '']"
          @click="activeTab = tab.key">
          {{ tab.label }}
          <span class="tab-count">{{ tab.count }}</span>
        </button>
      </div>

      <!-- Audit Cards -->
      <div class="audit-list">
        <div class="audit-card" v-for="audit in filteredAudits" :key="audit.id" :class="audit.status">
          <div class="audit-left">
            <div class="audit-type-icon">{{ audit.icon }}</div>
          </div>
          <div class="audit-main">
            <div class="audit-header-row">
              <div>
                <div class="audit-ref mono">{{ audit.ref }}</div>
                <div class="audit-title">{{ audit.title }}</div>
              </div>
              <span class="audit-status-badge" :class="audit.status">{{ audit.status }}</span>
            </div>
            <div class="audit-meta-row">
              <span class="meta-item">📍 {{ audit.site }}</span>
              <span class="meta-item">📅 {{ audit.scheduledDate }}</span>
              <span class="meta-item">👤 {{ audit.auditor }}</span>
              <span class="meta-item">🏷 {{ audit.type }}</span>
            </div>
            <div class="audit-checklist-preview" v-if="audit.checklist">
              <div class="checklist-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: (audit.checklist.done / audit.checklist.total * 100) + '%' }"></div>
                </div>
                <span class="progress-text mono">{{ audit.checklist.done }}/{{ audit.checklist.total }} items</span>
              </div>
            </div>
          </div>
          <div class="audit-actions">
            <button class="tbl-btn view" @click="viewAudit(audit)">Details</button>
            <button class="tbl-btn sign" v-if="audit.status === 'completed' && !audit.certified" @click="certifyAudit(audit)">Certify</button>
            <button class="tbl-btn conduct" v-if="audit.status === 'scheduled'" @click="conductAudit(audit)">Conduct</button>
          </div>
        </div>
      </div>
    </div>

    <!-- CALENDAR VIEW -->
    <div v-if="viewMode === 'calendar'" class="calendar-view">
      <div class="cal-header">
        <button class="cal-nav" @click="prevMonth">‹</button>
        <h2>{{ calMonthLabel }}</h2>
        <button class="cal-nav" @click="nextMonth">›</button>
      </div>
      <div class="cal-grid">
        <div class="cal-day-name" v-for="d in dayNames" :key="d">{{ d }}</div>
        <div v-for="(day, i) in calDays" :key="i"
          :class="['cal-cell', day ? '' : 'empty', isToday(day) ? 'today' : '']">
          <div v-if="day">
            <span class="day-num">{{ day }}</span>
            <div class="day-audits">
              <div v-for="a in auditsOnDay(day)" :key="a.id" class="cal-audit-dot" :class="a.status" :title="a.title">
                {{ a.title.slice(0, 20) }}…
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Schedule Audit Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>Schedule Safety Audit</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Audit Title *</label>
              <input v-model="form.title" type="text" placeholder="e.g. Fire Safety Inspection" />
            </div>
            <div class="form-group">
              <label>Audit Type *</label>
              <select v-model="form.type">
                <option value="">Select type...</option>
                <option>Fire Safety</option>
                <option>Electrical Safety</option>
                <option>PPE Compliance</option>
                <option>Structural Inspection</option>
                <option>Environmental</option>
                <option>General Site Safety</option>
              </select>
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
              <label>Scheduled Date *</label>
              <input v-model="form.date" type="date" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Lead Auditor *</label>
              <select v-model="form.auditor">
                <option value="">Assign auditor...</option>
                <option>Grace Otieno — Safety Officer</option>
                <option>James Mutua — Site Engineer</option>
                <option>Peter Kamau — Consultant</option>
                <option>Dr. Kariuki — Supervisor</option>
              </select>
            </div>
            <div class="form-group">
              <label>Priority</label>
              <select v-model="form.priority">
                <option value="normal">Normal</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>
          <div class="form-group full">
            <label>Notes / Scope</label>
            <textarea v-model="form.notes" rows="3" placeholder="Describe the scope and focus of this audit..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary" @click="submitAudit">Schedule Audit</button>
        </div>
      </div>
    </div>

    <!-- Audit Detail Drawer -->
    <div class="drawer-overlay" v-if="activeAudit" @click.self="activeAudit = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono ref-tag">{{ activeAudit.ref }}</span>
            <h2>{{ activeAudit.title }}</h2>
          </div>
          <button class="close-btn" @click="activeAudit = null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item"><span class="detail-lbl">Site</span><span class="detail-val">{{ activeAudit.site }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Date</span><span class="detail-val mono">{{ activeAudit.scheduledDate }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Auditor</span><span class="detail-val">{{ activeAudit.auditor }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Type</span><span class="detail-val">{{ activeAudit.type }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Status</span><span class="audit-status-badge" :class="activeAudit.status">{{ activeAudit.status }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Certified</span><span class="detail-val">{{ activeAudit.certified ? '✅ Yes' : '⏳ Pending' }}</span></div>
          </div>

          <!-- Checklist -->
          <div class="checklist-section" v-if="activeAudit.checklistItems">
            <div class="section-title">Inspection Checklist</div>
            <div class="check-item" v-for="(item, idx) in activeAudit.checklistItems" :key="idx">
              <input type="checkbox" :id="`chk-${idx}`" v-model="item.checked" />
              <label :for="`chk-${idx}`" :class="item.checked ? 'checked' : ''">{{ item.label }}</label>
              <span class="check-result" v-if="item.checked">✓ Pass</span>
            </div>
          </div>

          <!-- Score -->
          <div class="score-section" v-if="activeAudit.score !== undefined">
            <div class="section-title">Compliance Score</div>
            <div class="score-display">
              <div class="score-ring" :class="scoreClass(activeAudit.score)">
                <span class="score-num">{{ activeAudit.score }}%</span>
              </div>
              <div class="score-breakdown">
                <div v-for="c in activeAudit.categories" :key="c.name" class="score-cat">
                  <span class="cat-name">{{ c.name }}</span>
                  <div class="cat-bar">
                    <div class="cat-fill" :style="{ width: c.score + '%' }" :class="scoreClass(c.score)"></div>
                  </div>
                  <span class="cat-score mono">{{ c.score }}%</span>
                </div>
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

const viewMode = ref('list')
const activeTab = ref('all')
const showForm = ref(false)
const activeAudit = ref(null)
const currentCalMonth = ref(new Date(2025, 1))

const siteOptions = ['Nairobi Housing — Phase 1', 'Mombasa Infrastructure', 'Kisumu Commercial', 'Nakuru Road Project']
const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const form = ref({ title: '', type: '', site: '', date: '', auditor: '', priority: 'normal', notes: '' })

const audits = ref([
  {
    id: 1, ref: 'AUD-2025-001', icon: '🔥',
    title: 'Fire Safety Full Inspection',
    type: 'Fire Safety', site: 'Nairobi Housing — Phase 1',
    scheduledDate: '2025-02-20', auditor: 'Grace Otieno',
    status: 'completed', certified: true, score: 87,
    checklist: { done: 14, total: 16 },
    checklistItems: [
      { label: 'Fire extinguishers present and tagged', checked: true },
      { label: 'Emergency exits clearly marked', checked: true },
      { label: 'Fire hose reels operational', checked: false },
      { label: 'Smoke detectors installed', checked: true },
      { label: 'Assembly point signage visible', checked: true },
    ],
    categories: [
      { name: 'Equipment', score: 90 }, { name: 'Signage', score: 85 }, { name: 'Training', score: 80 }
    ]
  },
  {
    id: 2, ref: 'AUD-2025-002', icon: '⚡',
    title: 'Electrical Systems Compliance Check',
    type: 'Electrical Safety', site: 'Kisumu Commercial',
    scheduledDate: '2025-02-25', auditor: 'Peter Kamau',
    status: 'scheduled', certified: false, score: undefined,
    checklist: { done: 0, total: 12 },
    checklistItems: [
      { label: 'All panels properly labelled', checked: false },
      { label: 'Earth bonding verified', checked: false },
      { label: 'No exposed wiring present', checked: false },
      { label: 'RCD protection installed', checked: false },
    ],
    categories: []
  },
  {
    id: 3, ref: 'AUD-2025-003', icon: '🦺',
    title: 'PPE Usage Compliance Audit',
    type: 'PPE Compliance', site: 'Mombasa Infrastructure',
    scheduledDate: '2025-02-15', auditor: 'James Mutua',
    status: 'completed', certified: false, score: 74,
    checklist: { done: 10, total: 10 },
    checklistItems: [
      { label: 'Hard hats worn in required zones', checked: true },
      { label: 'Safety vests visible on all workers', checked: true },
      { label: 'Steel-toed boots compliance', checked: false },
      { label: 'Eye protection available', checked: true },
    ],
    categories: [
      { name: 'Head Protection', score: 95 }, { name: 'Body Protection', score: 80 }, { name: 'Foot Protection', score: 60 }
    ]
  },
  {
    id: 4, ref: 'AUD-2025-004', icon: '🏗️',
    title: 'Structural Safety & Scaffolding',
    type: 'Structural Inspection', site: 'Nairobi Housing — Phase 1',
    scheduledDate: '2025-03-01', auditor: 'Dr. Kariuki',
    status: 'scheduled', certified: false, score: undefined,
    checklist: { done: 0, total: 18 },
    checklistItems: [],
    categories: []
  },
])

const summaryStats = computed(() => [
  { label: 'Total Audits', value: audits.value.length, icon: '📋', cls: 'info' },
  { label: 'Scheduled', value: audits.value.filter(a => a.status === 'scheduled').length, icon: '📅', cls: 'scheduled' },
  { label: 'Completed', value: audits.value.filter(a => a.status === 'completed').length, icon: '✅', cls: 'completed' },
  { label: 'Certified', value: audits.value.filter(a => a.certified).length, icon: '🔏', cls: 'certified' },
])

const tabs = computed(() => [
  { key: 'all', label: 'All', count: audits.value.length },
  { key: 'scheduled', label: 'Scheduled', count: audits.value.filter(a => a.status === 'scheduled').length },
  { key: 'completed', label: 'Completed', count: audits.value.filter(a => a.status === 'completed').length },
])

const filteredAudits = computed(() => {
  if (activeTab.value === 'all') return audits.value
  return audits.value.filter(a => a.status === activeTab.value)
})

const calMonthLabel = computed(() => currentCalMonth.value.toLocaleString('default', { month: 'long', year: 'numeric' }))

const calDays = computed(() => {
  const d = new Date(currentCalMonth.value)
  const year = d.getFullYear(), month = d.getMonth()
  const first = new Date(year, month, 1).getDay()
  const days = new Date(year, month + 1, 0).getDate()
  const cells = []
  for (let i = 0; i < first; i++) cells.push(null)
  for (let i = 1; i <= days; i++) cells.push(i)
  return cells
})

function auditsOnDay(day) {
  const d = currentCalMonth.value
  const dateStr = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  return audits.value.filter(a => a.scheduledDate === dateStr)
}

function isToday(day) {
  if (!day) return false
  const today = new Date()
  return today.getDate() === day && today.getMonth() === currentCalMonth.value.getMonth() && today.getFullYear() === currentCalMonth.value.getFullYear()
}

function prevMonth() { currentCalMonth.value = new Date(currentCalMonth.value.getFullYear(), currentCalMonth.value.getMonth() - 1) }
function nextMonth() { currentCalMonth.value = new Date(currentCalMonth.value.getFullYear(), currentCalMonth.value.getMonth() + 1) }

function viewAudit(a) { activeAudit.value = { ...a, checklistItems: a.checklistItems.map(i => ({ ...i })) } }

function certifyAudit(a) {
  if (confirm(`Digitally certify audit ${a.ref}?`)) {
    a.certified = true
  }
}

function conductAudit(a) {
  a.status = 'in-progress'
}

function scoreClass(score) {
  if (score >= 85) return 'good'
  if (score >= 65) return 'warning'
  return 'danger'
}

function submitAudit() {
  if (!form.value.title || !form.value.site || !form.value.date) {
    alert('Please fill required fields.')
    return
  }
  audits.value.unshift({
    id: audits.value.length + 1,
    ref: `AUD-2025-00${audits.value.length + 1}`,
    icon: '📋',
    title: form.value.title, type: form.value.type,
    site: form.value.site, scheduledDate: form.value.date,
    auditor: form.value.auditor || 'Unassigned',
    status: 'scheduled', certified: false, score: undefined,
    checklist: { done: 0, total: 0 }, checklistItems: [], categories: []
  })
  showForm.value = false
  form.value = { title: '', type: '', site: '', date: '', auditor: '', priority: 'normal', notes: '' }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.safety-audits {
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

.btn-primary { background: #f5a623; color: #0d0f14; border: none; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; cursor: pointer; }
.btn-ghost { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }
.mono { font-family: 'DM Mono', monospace; }

.view-toggle { display: flex; gap: 4px; margin-bottom: 20px; background: #13161f; border: 1px solid #1e2230; border-radius: 8px; padding: 4px; width: fit-content; }
.toggle-btn { padding: 6px 16px; border-radius: 5px; font-family: 'Syne', sans-serif; font-size: 12px; border: none; cursor: pointer; background: none; color: #6b7280; }
.toggle-btn.active { background: #f5a623; color: #0d0f14; font-weight: 700; }

.summary-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }
.sum-card { background: #13161f; border: 1px solid #1e2230; border-radius: 10px; padding: 16px; display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center; }
.sum-icon { font-size: 24px; }
.sum-val { font-size: 32px; font-weight: 800; color: #fff; }
.sum-label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }
.sum-card.info     { border-left: 3px solid #3b82f6; }
.sum-card.scheduled{ border-left: 3px solid #f59e0b; }
.sum-card.completed{ border-left: 3px solid #22c55e; }
.sum-card.certified{ border-left: 3px solid #a855f7; }

.tabs { display: flex; gap: 0; margin-bottom: 20px; border-bottom: 1px solid #1e2230; }
.tab { background: none; border: none; padding: 10px 20px; font-family: 'Syne', sans-serif; font-size: 13px; color: #6b7280; cursor: pointer; display: flex; align-items: center; gap: 8px; border-bottom: 2px solid transparent; margin-bottom: -1px; }
.tab.active { color: #f5a623; border-bottom-color: #f5a623; }
.tab-count { background: #1e2230; padding: 1px 7px; border-radius: 10px; font-size: 10px; font-family: 'DM Mono', monospace; }
.tab.active .tab-count { background: #2a1f05; color: #f5a623; }

.audit-list { display: flex; flex-direction: column; gap: 12px; }
.audit-card { display: flex; align-items: center; gap: 16px; background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 16px 20px; transition: border-color 0.2s; }
.audit-card:hover { border-color: #2a2f3e; }
.audit-card.completed { border-left: 3px solid #22c55e; }
.audit-card.scheduled { border-left: 3px solid #3b82f6; }
.audit-card.in-progress { border-left: 3px solid #f59e0b; }
.audit-left { flex-shrink: 0; font-size: 28px; }
.audit-main { flex: 1; }
.audit-header-row { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.audit-ref { font-size: 10px; color: #f5a623; }
.audit-title { font-size: 15px; font-weight: 700; color: #fff; }
.audit-meta-row { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 8px; }
.meta-item { font-size: 11px; color: #6b7280; }

.audit-status-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 9px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.audit-status-badge.scheduled   { background: #0d1a2e; color: #3b82f6; }
.audit-status-badge.completed   { background: #0d2818; color: #22c55e; }
.audit-status-badge.in-progress { background: #1f1a08; color: #f59e0b; }

.checklist-progress { display: flex; align-items: center; gap: 10px; }
.progress-bar { flex: 1; height: 4px; background: #1e2230; border-radius: 2px; overflow: hidden; max-width: 200px; }
.progress-fill { height: 100%; background: #f5a623; border-radius: 2px; transition: width 0.6s ease; }
.progress-text { font-size: 10px; color: #4b5563; }

.audit-actions { display: flex; gap: 6px; flex-shrink: 0; }
.tbl-btn { padding: 6px 12px; border-radius: 6px; font-size: 11px; font-family: 'Syne', sans-serif; cursor: pointer; border: 1px solid; }
.tbl-btn.view { background: none; border-color: #2a2f3e; color: #9ca3af; }
.tbl-btn.view:hover { border-color: #3b82f6; color: #3b82f6; }
.tbl-btn.sign { background: none; border-color: #1a3020; color: #22c55e; }
.tbl-btn.sign:hover { background: #0d2818; }
.tbl-btn.conduct { background: none; border-color: #1a2a40; color: #3b82f6; }

/* CALENDAR */
.calendar-view { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 20px; }
.cal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.cal-header h2 { font-size: 16px; font-weight: 700; }
.cal-nav { background: #1a1e2a; border: 1px solid #2a2f3e; color: #e8e4dc; width: 32px; height: 32px; border-radius: 6px; font-size: 18px; cursor: pointer; }
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
.cal-day-name { text-align: center; font-size: 10px; font-family: 'DM Mono', monospace; color: #4b5563; padding: 6px; text-transform: uppercase; }
.cal-cell { background: #0d0f14; border-radius: 6px; padding: 8px; min-height: 80px; border: 1px solid #1a1e2a; }
.cal-cell.empty { background: transparent; border: none; }
.cal-cell.today { border-color: #f5a623; }
.day-num { font-size: 12px; font-weight: 700; color: #9ca3af; }
.cal-cell.today .day-num { color: #f5a623; }
.day-audits { margin-top: 4px; display: flex; flex-direction: column; gap: 2px; }
.cal-audit-dot { font-size: 9px; padding: 2px 4px; border-radius: 3px; overflow: hidden; white-space: nowrap; }
.cal-audit-dot.scheduled { background: #0d1a2e; color: #3b82f6; }
.cal-audit-dot.completed { background: #0d2818; color: #22c55e; }

/* MODAL */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 100; display: flex; align-items: center; justify-content: center; }
.modal { background: #13161f; border: 1px solid #2a2f3e; border-radius: 16px; width: 640px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 22px 28px; border-bottom: 1px solid #1e2230; }
.modal-header h2 { font-size: 18px; font-weight: 700; }
.close-btn { background: none; border: none; color: #6b7280; font-size: 18px; cursor: pointer; }
.modal-body { padding: 24px 28px; display: flex; flex-direction: column; gap: 16px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 18px 28px; border-top: 1px solid #1e2230; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group.full { grid-column: 1 / -1; }
.form-group label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; }
.form-group input, .form-group select, .form-group textarea { background: #0d0f14; border: 1px solid #1e2230; color: #e8e4dc; padding: 10px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #f5a623; }

/* DRAWER */
.drawer-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 100; display: flex; justify-content: flex-end; }
.drawer { background: #13161f; border-left: 1px solid #2a2f3e; width: 520px; height: 100%; overflow-y: auto; }
.drawer-header { padding: 24px; border-bottom: 1px solid #1e2230; display: flex; justify-content: space-between; align-items: flex-start; }
.ref-tag { font-family: 'DM Mono', monospace; font-size: 11px; color: #f5a623; display: block; margin-bottom: 4px; }
.drawer-header h2 { font-size: 16px; font-weight: 700; max-width: 400px; }
.drawer-body { padding: 24px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
.detail-item { display: flex; flex-direction: column; gap: 4px; }
.detail-lbl { font-size: 10px; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; }
.detail-val { font-size: 13px; color: #e8e4dc; }

.section-title { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; margin-bottom: 12px; }
.checklist-section { margin-bottom: 24px; }
.check-item { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #1a1e2a; }
.check-item input { accent-color: #f5a623; width: 14px; height: 14px; cursor: pointer; }
.check-item label { flex: 1; font-size: 13px; color: #9ca3af; cursor: pointer; }
.check-item label.checked { color: #e8e4dc; text-decoration: none; }
.check-result { font-family: 'DM Mono', monospace; font-size: 10px; color: #22c55e; }

.score-section { margin-top: 24px; }
.score-display { display: flex; gap: 24px; align-items: flex-start; margin-top: 12px; }
.score-ring { width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; border: 4px solid; }
.score-ring.good    { border-color: #22c55e; }
.score-ring.warning { border-color: #f59e0b; }
.score-ring.danger  { border-color: #ef4444; }
.score-num { font-size: 18px; font-weight: 800; }
.score-ring.good .score-num    { color: #22c55e; }
.score-ring.warning .score-num { color: #f59e0b; }
.score-ring.danger .score-num  { color: #ef4444; }
.score-breakdown { flex: 1; display: flex; flex-direction: column; gap: 10px; }
.score-cat { display: flex; align-items: center; gap: 10px; }
.cat-name { font-size: 12px; color: #9ca3af; flex: 0 0 130px; }
.cat-bar { flex: 1; height: 6px; background: #1e2230; border-radius: 3px; overflow: hidden; }
.cat-fill { height: 100%; border-radius: 3px; }
.cat-fill.good    { background: #22c55e; }
.cat-fill.warning { background: #f59e0b; }
.cat-fill.danger  { background: #ef4444; }
.cat-score { font-family: 'DM Mono', monospace; font-size: 11px; color: #6b7280; width: 36px; text-align: right; }
</style>