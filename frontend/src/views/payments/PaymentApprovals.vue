<!-- <template>
  <div class="payment-approvals">
    <div class="page-header">
      <div>
        <span class="page-tag">PAYMENTS · APPROVALS</span>
        <h1>Payment Approvals</h1>
        <p class="page-sub">Review and authorise pending payment requests across all projects</p>
      </div>
      <div class="header-meta mono">Logged in as: <span class="user-tag">Alice Wanjiku — Finance Manager</span></div>
    </div>

    <!-- Tabs --
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.key" :class="['tab', activeTab === tab.key ? 'active' : '']" @click="activeTab = tab.key">
        {{ tab.label }} <span class="tab-count" :class="tab.key">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Approval Cards --
    <div class="approval-list">
      <div class="approval-card" v-for="req in filteredRequests" :key="req.id" :class="req.status">
        <div class="card-left">
          <div class="pay-type-icon" :class="req.channel">{{ req.channel === 'mpesa' ? '📱' : '🏦' }}</div>
        </div>
        <div class="card-main">
          <div class="card-top-row">
            <div>
              <span class="req-ref mono">{{ req.ref }}</span>
              <div class="req-title">{{ req.title }}</div>
            </div>
            <div class="card-badges">
              <span class="channel-badge" :class="req.channel">{{ req.channel === 'mpesa' ? 'M-Pesa' : 'Bank' }}</span>
              <span class="priority-badge" :class="req.priority">{{ req.priority }}</span>
            </div>
          </div>
          <div class="card-meta">
            <span>👤 {{ req.requestedBy }}</span>
            <span>📍 {{ req.site }}</span>
            <span>📅 {{ req.date }}</span>
            <span>🏷 {{ req.category }}</span>
          </div>
          <div class="card-desc">{{ req.description }}</div>
          <div class="approval-trail">
            <div class="trail-step" v-for="step in req.trail" :key="step.role" :class="step.status">
              <div class="trail-dot"></div>
              <div class="trail-info">
                <span class="trail-role">{{ step.role }}</span>
                <span class="trail-status mono">{{ step.status }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="card-right">
          <div class="req-amount">KES {{ req.amount.toLocaleString() }}</div>
          <div class="card-actions" v-if="req.status === 'pending'">
            <button class="approve-btn" @click="approve(req)">✓ Approve</button>
            <button class="reject-btn" @click="reject(req)">✕ Reject</button>
            <button class="view-btn" @click="viewReq(req)">Details</button>
          </div>
          <div v-else class="card-done-status" :class="req.status">
            {{ req.status === 'approved' ? '✅ Approved' : '❌ Rejected' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Drawer --
    <div class="drawer-overlay" v-if="activeReq" @click.self="activeReq = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono ref-tag">{{ activeReq.ref }}</span>
            <h2>{{ activeReq.title }}</h2>
          </div>
          <button class="close-btn" @click="activeReq = null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item"><span class="dlbl">Amount</span><span class="dval amount-big">KES {{ activeReq.amount.toLocaleString() }}</span></div>
            <div class="detail-item"><span class="dlbl">Channel</span><span class="dval">{{ activeReq.channel }}</span></div>
            <div class="detail-item"><span class="dlbl">Site</span><span class="dval">{{ activeReq.site }}</span></div>
            <div class="detail-item"><span class="dlbl">Category</span><span class="dval">{{ activeReq.category }}</span></div>
            <div class="detail-item"><span class="dlbl">Requested By</span><span class="dval">{{ activeReq.requestedBy }}</span></div>
            <div class="detail-item"><span class="dlbl">Date</span><span class="dval mono">{{ activeReq.date }}</span></div>
          </div>
          <div class="detail-desc">
            <span class="dlbl">Description</span>
            <p>{{ activeReq.description }}</p>
          </div>
          <div class="supporting-docs">
            <span class="dlbl">Supporting Documents</span>
            <div class="doc-list">
              <div class="doc-item" v-for="doc in activeReq.docs" :key="doc">📄 {{ doc }}</div>
            </div>
          </div>
          <div class="drawer-actions" v-if="activeReq.status === 'pending'">
            <button class="approve-btn full" @click="approve(activeReq); activeReq = null">✓ Approve Payment</button>
            <button class="reject-btn full" @click="reject(activeReq); activeReq = null">✕ Reject Payment</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const activeTab = ref('pending')
const activeReq = ref(null)

const requests = ref([
  { id: 1, ref: 'APR-001', title: 'Roofing Materials — Mombasa Site', requestedBy: 'James Mutua', site: 'Mombasa Infrastructure', date: '2025-02-18', amount: 420000, channel: 'bank', category: 'Materials', priority: 'urgent', status: 'pending', description: 'Payment for 200 iron sheets and ridge caps from Mabati Rolling Mills. LPO #2025-034 attached.', trail: [{ role: 'Site Manager', status: 'approved' }, { role: 'Project Manager', status: 'approved' }, { role: 'Finance Manager', status: 'pending' }], docs: ['LPO-2025-034.pdf', 'Delivery Note.pdf', 'Invoice-MRM-001.pdf'] },
  { id: 2, ref: 'APR-002', title: 'Electrical Contractor — Kisumu', requestedBy: 'Grace Otieno', site: 'Kisumu Commercial', date: '2025-02-17', amount: 180000, channel: 'mpesa', category: 'Labour', priority: 'normal', status: 'pending', description: 'Payment to electrical subcontractor for wiring of floors 1–3. Completion certificate attached.', trail: [{ role: 'Site Manager', status: 'approved' }, { role: 'Project Manager', status: 'pending' }, { role: 'Finance Manager', status: 'pending' }], docs: ['Completion-Cert.pdf', 'Invoice-ELEC-002.pdf'] },
  { id: 3, ref: 'APR-003', title: 'Site Labour — Nairobi Week 7', requestedBy: 'Peter Kamau', site: 'Nairobi Housing — Phase 1', date: '2025-02-16', amount: 290000, channel: 'mpesa', category: 'Labour', priority: 'high', status: 'approved', description: 'Weekly casual labour payment for 45 workers — Week 7 payroll.', trail: [{ role: 'Site Manager', status: 'approved' }, { role: 'Project Manager', status: 'approved' }, { role: 'Finance Manager', status: 'approved' }], docs: ['Payroll-Week7.xlsx', 'Attendance-Sheet.pdf'] },
  { id: 4, ref: 'APR-004', title: 'Aggregate Supplier — Nakuru', requestedBy: 'Alice Njeri', site: 'Nakuru Road Project', date: '2025-02-14', amount: 95000, channel: 'bank', category: 'Materials', priority: 'normal', status: 'rejected', description: 'Payment for ballast and sand delivery. Request rejected — invoice amounts do not match LPO.', trail: [{ role: 'Site Manager', status: 'approved' }, { role: 'Project Manager', status: 'rejected' }, { role: 'Finance Manager', status: 'pending' }], docs: ['Invoice-AGG-004.pdf'] },
])

const tabs = computed(() => [
  { key: 'pending', label: 'Pending', count: requests.value.filter(r => r.status === 'pending').length },
  { key: 'approved', label: 'Approved', count: requests.value.filter(r => r.status === 'approved').length },
  { key: 'rejected', label: 'Rejected', count: requests.value.filter(r => r.status === 'rejected').length },
  { key: 'all', label: 'All', count: requests.value.length },
])

const filteredRequests = computed(() => activeTab.value === 'all' ? requests.value : requests.value.filter(r => r.status === activeTab.value))

function approve(req) { req.status = 'approved' }
function reject(req)  { req.status = 'rejected' }
function viewReq(req) { activeReq.value = req }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
.payment-approvals { font-family: 'Syne', sans-serif; background: #0d0f14; color: #e8e4dc; min-height: 100vh; padding: 28px 32px; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.page-tag { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; color: #f5a623; text-transform: uppercase; display: block; margin-bottom: 6px; }
h1 { font-size: 28px; font-weight: 800; color: #fff; }
.page-sub { font-size: 13px; color: #6b7280; margin-top: 4px; }
.header-meta { font-size: 12px; color: #4b5563; }
.user-tag { color: #f5a623; }
.mono { font-family: 'DM Mono', monospace; }

.tabs { display: flex; gap: 0; margin-bottom: 20px; border-bottom: 1px solid #1e2230; }
.tab { background: none; border: none; padding: 10px 20px; font-family: 'Syne', sans-serif; font-size: 13px; color: #6b7280; cursor: pointer; display: flex; align-items: center; gap: 8px; border-bottom: 2px solid transparent; margin-bottom: -1px; }
.tab.active { color: #f5a623; border-bottom-color: #f5a623; }
.tab-count { font-family: 'DM Mono', monospace; font-size: 10px; padding: 1px 7px; border-radius: 10px; background: #1e2230; }
.tab-count.pending  { background: #1f1a08; color: #f59e0b; }
.tab-count.approved { background: #0d2818; color: #22c55e; }
.tab-count.rejected { background: #200e0e; color: #ef4444; }

.approval-list { display: flex; flex-direction: column; gap: 12px; }
.approval-card { display: flex; gap: 16px; background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 18px 20px; transition: border-color 0.2s; }
.approval-card.pending  { border-left: 3px solid #f59e0b; }
.approval-card.approved { border-left: 3px solid #22c55e; }
.approval-card.rejected { border-left: 3px solid #ef4444; }
.card-left { flex-shrink: 0; }
.pay-type-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.pay-type-icon.mpesa { background: #0d2010; }
.pay-type-icon.bank  { background: #0d1a2e; }
.card-main { flex: 1; }
.card-top-row { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.req-ref { font-size: 10px; color: #f5a623; display: block; margin-bottom: 2px; }
.req-title { font-size: 15px; font-weight: 700; color: #fff; }
.card-badges { display: flex; gap: 6px; flex-shrink: 0; }
.channel-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 2px 8px; border-radius: 3px; text-transform: uppercase; }
.channel-badge.mpesa { background: #0d2010; color: #22c55e; }
.channel-badge.bank  { background: #0d1a2e; color: #3b82f6; }
.priority-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 2px 8px; border-radius: 3px; text-transform: uppercase; }
.priority-badge.urgent { background: #2a0808; color: #ef4444; }
.priority-badge.high   { background: #200e0e; color: #f59e0b; }
.priority-badge.normal { background: #1a1e2a; color: #6b7280; }
.card-meta { display: flex; flex-wrap: wrap; gap: 12px; font-size: 11px; color: #6b7280; margin-bottom: 8px; }
.card-desc { font-size: 12px; color: #9ca3af; margin-bottom: 10px; }
.approval-trail { display: flex; gap: 16px; }
.trail-step { display: flex; align-items: center; gap: 6px; }
.trail-dot { width: 8px; height: 8px; border-radius: 50%; }
.trail-step.approved .trail-dot { background: #22c55e; }
.trail-step.pending .trail-dot  { background: #f59e0b; }
.trail-step.rejected .trail-dot { background: #ef4444; }
.trail-role { font-size: 10px; color: #9ca3af; }
.trail-status { font-size: 9px; margin-left: 4px; }
.trail-step.approved .trail-status { color: #22c55e; }
.trail-step.pending .trail-status  { color: #f59e0b; }
.trail-step.rejected .trail-status { color: #ef4444; }

.card-right { flex-shrink: 0; display: flex; flex-direction: column; align-items: flex-end; gap: 12px; min-width: 140px; }
.req-amount { font-size: 20px; font-weight: 800; color: #fff; }
.card-actions { display: flex; flex-direction: column; gap: 6px; width: 100%; }
.approve-btn { background: #0d2010; border: 1px solid #22c55e; color: #22c55e; padding: 7px 14px; border-radius: 6px; font-family: 'Syne', sans-serif; font-size: 12px; cursor: pointer; font-weight: 600; }
.reject-btn  { background: none; border: 1px solid #2a2f3e; color: #6b7280; padding: 7px 14px; border-radius: 6px; font-family: 'Syne', sans-serif; font-size: 12px; cursor: pointer; }
.reject-btn:hover { border-color: #ef4444; color: #ef4444; }
.view-btn { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 7px 14px; border-radius: 6px; font-family: 'Syne', sans-serif; font-size: 12px; cursor: pointer; }
.approve-btn.full, .reject-btn.full { width: 100%; text-align: center; }
.card-done-status { font-family: 'DM Mono', monospace; font-size: 12px; }
.card-done-status.approved { color: #22c55e; }
.card-done-status.rejected { color: #ef4444; }

.drawer-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 100; display: flex; justify-content: flex-end; }
.drawer { background: #13161f; border-left: 1px solid #2a2f3e; width: 480px; height: 100%; overflow-y: auto; }
.drawer-header { padding: 22px 24px; border-bottom: 1px solid #1e2230; display: flex; justify-content: space-between; align-items: flex-start; }
.ref-tag { font-family: 'DM Mono', monospace; font-size: 11px; color: #f5a623; display: block; margin-bottom: 4px; }
.drawer-header h2 { font-size: 15px; font-weight: 700; max-width: 360px; }
.close-btn { background: none; border: none; color: #6b7280; font-size: 18px; cursor: pointer; }
.drawer-body { padding: 22px 24px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 18px; }
.detail-item { display: flex; flex-direction: column; gap: 4px; }
.dlbl { font-size: 10px; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; display: block; margin-bottom: 2px; }
.dval { font-size: 13px; color: #e8e4dc; }
.amount-big { font-size: 18px; font-weight: 800; color: #f5a623; }
.detail-desc { margin-bottom: 18px; }
.detail-desc p { font-size: 13px; color: #9ca3af; line-height: 1.6; margin-top: 6px; }
.supporting-docs { margin-bottom: 20px; }
.doc-list { display: flex; flex-direction: column; gap: 6px; margin-top: 8px; }
.doc-item { font-size: 12px; color: #3b82f6; padding: 6px 10px; background: #0d1a2e; border-radius: 6px; cursor: pointer; }
.drawer-actions { display: flex; flex-direction: column; gap: 8px; }
</style> -->



<template>
  <div class="payments-page">
    <div class="page-header">
      <div>
        <span class="page-tag amber">PAYMENTS · APPROVALS</span>
        <h1>Payment Approvals</h1>
        <p class="page-sub">Review and authorise pending payment requests across all projects</p>
      </div>
      <div class="mono" style="font-size:12px;color:#4b5563">
        Logged in as: <span style="color:#f5a623">Alice Wanjiku — Finance Manager</span>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.key" :class="['tab', activeTab === tab.key ? 'active' : '']" @click="activeTab = tab.key">
        {{ tab.label }} <span class="tab-count" :class="tab.key">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Approval Cards -->
    <div class="approval-list">
      <div class="approval-card" v-for="req in filteredRequests" :key="req.id" :class="req.status">
        <div class="pay-type-icon" :class="req.channel">{{ req.channel === 'mpesa' ? '📱' : '🏦' }}</div>
        <div class="card-main">
          <div class="card-top-row">
            <div>
              <span class="mono" style="font-size:10px;color:#f5a623;display:block;margin-bottom:2px">{{ req.ref }}</span>
              <div style="font-size:15px;font-weight:700;color:#fff">{{ req.title }}</div>
            </div>
            <div style="display:flex;gap:6px;flex-shrink:0">
              <span class="channel-badge" :class="req.channel">{{ req.channel === 'mpesa' ? 'M-Pesa' : 'Bank' }}</span>
              <span class="priority-badge" :class="req.priority">{{ req.priority }}</span>
            </div>
          </div>
          <div class="card-meta">
            <span>👤 {{ req.requestedBy }}</span>
            <span>📍 {{ req.site }}</span>
            <span>📅 {{ req.date }}</span>
            <span>🏷 {{ req.category }}</span>
          </div>
          <div class="cell-muted" style="margin-bottom:10px">{{ req.description }}</div>
          <div class="approval-trail">
            <div class="trail-step" v-for="step in req.trail" :key="step.role" :class="step.status">
              <div class="trail-dot"></div>
              <div>
                <span style="font-size:10px;color:#9ca3af">{{ step.role }}</span>
                <span class="mono" style="font-size:9px;margin-left:4px" :class="'trail-' + step.status">{{ step.status }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="card-right">
          <div style="font-size:20px;font-weight:800;color:#fff">KES {{ req.amount.toLocaleString() }}</div>
          <div class="card-actions" v-if="req.status === 'pending'">
            <button class="approve-btn" @click="approve(req)">✓ Approve</button>
            <button class="reject-btn"  @click="reject(req)">✕ Reject</button>
            <button class="btn-ghost" style="padding:7px 14px;font-size:12px" @click="activeReq = req">Details</button>
          </div>
          <div v-else class="mono" style="font-size:12px" :class="req.status === 'approved' ? 'text-green' : 'text-red'">
            {{ req.status === 'approved' ? '✅ Approved' : '❌ Rejected' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Drawer -->
    <div class="drawer-overlay" v-if="activeReq" @click.self="activeReq = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:11px;color:#f5a623;display:block;margin-bottom:4px">{{ activeReq.ref }}</span>
            <h2 style="font-size:15px;font-weight:700;max-width:360px">{{ activeReq.title }}</h2>
          </div>
          <button class="close-btn" @click="activeReq = null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div v-for="d in detailFields" :key="d.label" style="display:flex;flex-direction:column;gap:4px">
              <span class="mono" style="font-size:10px;color:#4b5563;text-transform:uppercase">{{ d.label }}</span>
              <span :style="d.style || 'font-size:13px;color:#e8e4dc'">{{ d.value }}</span>
            </div>
          </div>
          <div style="margin-bottom:18px">
            <span class="mono" style="font-size:10px;color:#4b5563;text-transform:uppercase">Description</span>
            <p class="cell-muted" style="margin-top:6px;line-height:1.6">{{ activeReq.description }}</p>
          </div>
          <div style="margin-bottom:20px">
            <span class="mono" style="font-size:10px;color:#4b5563;text-transform:uppercase">Supporting Documents</span>
            <div style="display:flex;flex-direction:column;gap:6px;margin-top:8px">
              <div v-for="doc in activeReq.docs" :key="doc" style="font-size:12px;color:#3b82f6;padding:6px 10px;background:#0d1a2e;border-radius:6px;cursor:pointer">📄 {{ doc }}</div>
            </div>
          </div>
          <div v-if="activeReq.status === 'pending'" style="display:flex;flex-direction:column;gap:8px">
            <button class="approve-btn" style="width:100%;text-align:center" @click="approve(activeReq);activeReq=null">✓ Approve Payment</button>
            <button class="reject-btn"  style="width:100%;text-align:center" @click="reject(activeReq);activeReq=null">✕ Reject Payment</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const activeTab = ref('pending')
const activeReq = ref(null)

const requests = ref([
  { id: 1, ref: 'APR-001', title: 'Roofing Materials — Mombasa Site', requestedBy: 'James Mutua',  site: 'Mombasa Infrastructure',    date: '2025-02-18', amount: 420000, channel: 'bank',  category: 'Materials', priority: 'urgent', status: 'pending',  description: 'Payment for 200 iron sheets and ridge caps from Mabati Rolling Mills. LPO #2025-034 attached.', trail: [{ role: 'Site Manager', status: 'approved' }, { role: 'Project Manager', status: 'approved' }, { role: 'Finance Manager', status: 'pending' }], docs: ['LPO-2025-034.pdf', 'Delivery Note.pdf', 'Invoice-MRM-001.pdf'] },
  { id: 2, ref: 'APR-002', title: 'Electrical Contractor — Kisumu',  requestedBy: 'Grace Otieno',  site: 'Kisumu Commercial',         date: '2025-02-17', amount: 180000, channel: 'mpesa', category: 'Labour',    priority: 'normal', status: 'pending',  description: 'Payment to electrical subcontractor for wiring of floors 1–3.', trail: [{ role: 'Site Manager', status: 'approved' }, { role: 'Project Manager', status: 'pending' }, { role: 'Finance Manager', status: 'pending' }], docs: ['Completion-Cert.pdf', 'Invoice-ELEC-002.pdf'] },
  { id: 3, ref: 'APR-003', title: 'Site Labour — Nairobi Week 7',    requestedBy: 'Peter Kamau',   site: 'Nairobi Housing — Phase 1', date: '2025-02-16', amount: 290000, channel: 'mpesa', category: 'Labour',    priority: 'high',   status: 'approved', description: 'Weekly casual labour payment for 45 workers — Week 7 payroll.', trail: [{ role: 'Site Manager', status: 'approved' }, { role: 'Project Manager', status: 'approved' }, { role: 'Finance Manager', status: 'approved' }], docs: ['Payroll-Week7.xlsx'] },
  { id: 4, ref: 'APR-004', title: 'Aggregate Supplier — Nakuru',     requestedBy: 'Alice Njeri',   site: 'Nakuru Road Project',       date: '2025-02-14', amount: 95000,  channel: 'bank',  category: 'Materials', priority: 'normal', status: 'rejected', description: 'Rejected — invoice amounts do not match LPO.', trail: [{ role: 'Site Manager', status: 'approved' }, { role: 'Project Manager', status: 'rejected' }, { role: 'Finance Manager', status: 'pending' }], docs: ['Invoice-AGG-004.pdf'] },
])

const detailFields = computed(() => activeReq.value ? [
  { label: 'Amount',       value: 'KES ' + activeReq.value.amount.toLocaleString(), style: 'font-size:18px;font-weight:800;color:#f5a623' },
  { label: 'Channel',      value: activeReq.value.channel },
  { label: 'Site',         value: activeReq.value.site },
  { label: 'Category',     value: activeReq.value.category },
  { label: 'Requested By', value: activeReq.value.requestedBy },
  { label: 'Date',         value: activeReq.value.date },
] : [])

const tabs = computed(() => [
  { key: 'pending',  label: 'Pending',  count: requests.value.filter(r => r.status === 'pending').length  },
  { key: 'approved', label: 'Approved', count: requests.value.filter(r => r.status === 'approved').length },
  { key: 'rejected', label: 'Rejected', count: requests.value.filter(r => r.status === 'rejected').length },
  { key: 'all',      label: 'All',      count: requests.value.length },
])

const filteredRequests = computed(() =>
  activeTab.value === 'all' ? requests.value : requests.value.filter(r => r.status === activeTab.value)
)

function approve(req) { req.status = 'approved' }
function reject(req)  { req.status = 'rejected' }
</script>

<style scoped>
@import '/src/assets/payments.css';

.tabs { display: flex; gap: 0; margin-bottom: 20px; border-bottom: 1px solid #1e2230; }
.tab { background: none; border: none; padding: 10px 20px; font-family: 'Syne', sans-serif; font-size: 13px; color: #6b7280; cursor: pointer; display: flex; align-items: center; gap: 8px; border-bottom: 2px solid transparent; margin-bottom: -1px; }
.tab.active { color: #f5a623; border-bottom-color: #f5a623; }
.tab-count { font-family: 'DM Mono', monospace; font-size: 10px; padding: 1px 7px; border-radius: 10px; background: #1e2230; }
.tab-count.pending  { background: #1f1a08; color: #f59e0b; }
.tab-count.approved { background: #0d2818; color: #22c55e; }
.tab-count.rejected { background: #200e0e; color: #ef4444; }

.approval-list { display: flex; flex-direction: column; gap: 12px; }
.approval-card { display: flex; gap: 16px; background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 18px 20px; }
.approval-card.pending  { border-left: 3px solid #f59e0b; }
.approval-card.approved { border-left: 3px solid #22c55e; }
.approval-card.rejected { border-left: 3px solid #ef4444; }
.pay-type-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.pay-type-icon.mpesa { background: #0d2010; }
.pay-type-icon.bank  { background: #0d1a2e; }
.card-main { flex: 1; }
.card-top-row { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.card-meta { display: flex; flex-wrap: wrap; gap: 12px; font-size: 11px; color: #6b7280; margin-bottom: 8px; }
.priority-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 2px 8px; border-radius: 3px; text-transform: uppercase; }
.priority-badge.urgent { background: #2a0808; color: #ef4444; }
.priority-badge.high   { background: #200e0e; color: #f59e0b; }
.priority-badge.normal { background: #1a1e2a; color: #6b7280; }
.approval-trail { display: flex; gap: 16px; }
.trail-step { display: flex; align-items: center; gap: 6px; }
.trail-dot { width: 8px; height: 8px; border-radius: 50%; }
.trail-step.approved .trail-dot { background: #22c55e; }
.trail-step.pending .trail-dot  { background: #f59e0b; }
.trail-step.rejected .trail-dot { background: #ef4444; }
.trail-approved { color: #22c55e; }
.trail-pending  { color: #f59e0b; }
.trail-rejected { color: #ef4444; }
.card-right { flex-shrink: 0; display: flex; flex-direction: column; align-items: flex-end; gap: 12px; min-width: 140px; }
.card-actions { display: flex; flex-direction: column; gap: 6px; width: 100%; }
.text-green { color: #22c55e; }
.text-red   { color: #ef4444; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 18px; }
</style>