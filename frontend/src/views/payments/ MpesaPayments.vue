<template>
  <div class="mpesa-payments">
    <div class="page-header">
      <div>
        <span class="page-tag">PAYMENTS · M-PESA</span>
        <h1>M-Pesa Payments</h1>
        <p class="page-sub">Initiate and track M-Pesa transactions for suppliers and labour</p>
      </div>
      <button class="btn-primary" @click="showForm = true">+ Initiate Payment</button>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card" v-for="s in stats" :key="s.label" :class="s.cls">
        <div class="stat-val">{{ s.val }}</div>
        <div class="stat-label">{{ s.label }}</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" type="text" placeholder="Search by name, phone or ref..." class="search-input" />
      </div>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="completed">Completed</option>
        <option value="pending">Pending</option>
        <option value="failed">Failed</option>
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
            <th>REF</th>
            <th>Recipient</th>
            <th>Phone</th>
            <th>Site</th>
            <th>Purpose</th>
            <th>Amount (KES)</th>
            <th>Date</th>
            <th>M-Pesa Code</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filteredPayments" :key="p.id" class="table-row">
            <td class="mono ref">{{ p.ref }}</td>
            <td>
              <div class="recipient">
                <div class="avatar">{{ p.name[0] }}</div>
                <div>
                  <div class="rec-name">{{ p.name }}</div>
                  <div class="rec-role mono">{{ p.role }}</div>
                </div>
              </div>
            </td>
            <td class="mono phone">{{ p.phone }}</td>
            <td class="site-cell">{{ p.site }}</td>
            <td class="purpose">{{ p.purpose }}</td>
            <td class="amount">{{ p.amount.toLocaleString() }}</td>
            <td class="mono date-cell">{{ p.date }}</td>
            <td class="mono mpesa-code">{{ p.mpesaCode || '—' }}</td>
            <td><span class="status-badge" :class="p.status">{{ p.status }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Initiate Payment Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title-wrap">
            <span class="mpesa-logo">📱</span>
            <h2>Initiate M-Pesa Payment</h2>
          </div>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Recipient Name *</label>
              <input v-model="form.name" type="text" placeholder="Full name" />
            </div>
            <div class="form-group">
              <label>Phone Number *</label>
              <input v-model="form.phone" type="text" placeholder="07XXXXXXXX or 01XXXXXXXX" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Amount (KES) *</label>
              <input v-model="form.amount" type="number" placeholder="0.00" />
            </div>
            <div class="form-group">
              <label>Site *</label>
              <select v-model="form.site">
                <option value="">Select site...</option>
                <option v-for="s in siteOptions" :key="s">{{ s }}</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Purpose *</label>
              <select v-model="form.purpose">
                <option value="">Select purpose...</option>
                <option>Labour Payment</option>
                <option>Material Purchase</option>
                <option>Supplier Payment</option>
                <option>Petty Cash</option>
                <option>Equipment Hire</option>
              </select>
            </div>
            <div class="form-group">
              <label>Recipient Role</label>
              <input v-model="form.role" type="text" placeholder="e.g. Casual Worker, Supplier" />
            </div>
          </div>
          <div class="form-group full">
            <label>Description</label>
            <textarea v-model="form.description" rows="2" placeholder="Payment details..."></textarea>
          </div>
          <div class="stk-notice">
            <span>📲</span>
            <div>
              <div class="notice-title">STK Push will be sent</div>
              <div class="notice-sub">Recipient will receive an M-Pesa prompt on their phone to confirm the transaction.</div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary" @click="submitPayment">Send Payment</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const showForm = ref(false)
const search = ref('')
const filterStatus = ref('')
const filterSite = ref('')
const siteOptions = ['Nairobi Housing — Phase 1', 'Mombasa Infrastructure', 'Kisumu Commercial', 'Nakuru Road Project']

const form = ref({ name: '', phone: '', amount: '', site: '', purpose: '', role: '', description: '' })

const payments = ref([
  { id: 1, ref: 'MPE-001', name: 'John Kariuki', role: 'Casual Worker', phone: '0712345678', site: 'Nairobi Housing — Phase 1', purpose: 'Labour Payment', amount: 12500, date: '2025-02-18', mpesaCode: 'QJK8X1Y23P', status: 'completed' },
  { id: 2, ref: 'MPE-002', name: 'Mary Akinyi', role: 'Supplier', phone: '0723456789', site: 'Mombasa Infrastructure', purpose: 'Material Purchase', amount: 145000, date: '2025-02-18', mpesaCode: 'RLM9Z2A45Q', status: 'completed' },
  { id: 3, ref: 'MPE-003', name: 'Peter Otieno', role: 'Casual Worker', phone: '0734567890', site: 'Kisumu Commercial', purpose: 'Labour Payment', amount: 8750, date: '2025-02-17', mpesaCode: null, status: 'pending' },
  { id: 4, ref: 'MPE-004', name: 'Bamburi Hardware', role: 'Supplier', phone: '0745678901', site: 'Nairobi Housing — Phase 1', purpose: 'Supplier Payment', amount: 78000, date: '2025-02-17', mpesaCode: null, status: 'failed' },
  { id: 5, ref: 'MPE-005', name: 'Grace Wanjiku', role: 'Casual Worker', phone: '0756789012', site: 'Nakuru Road Project', purpose: 'Labour Payment', amount: 11000, date: '2025-02-16', mpesaCode: 'TNP3B4C67R', status: 'completed' },
  { id: 6, ref: 'MPE-006', name: 'James Mwangi', role: 'Equipment Operator', phone: '0767890123', site: 'Mombasa Infrastructure', purpose: 'Equipment Hire', amount: 35000, date: '2025-02-15', mpesaCode: 'VQR5D6E89S', status: 'completed' },
])

const stats = computed(() => [
  { label: 'Total Sent', val: 'KES ' + payments.value.filter(p => p.status === 'completed').reduce((a, b) => a + b.amount, 0).toLocaleString(), cls: 'green' },
  { label: 'Pending', val: payments.value.filter(p => p.status === 'pending').length, cls: 'warn' },
  { label: 'Failed', val: payments.value.filter(p => p.status === 'failed').length, cls: 'danger' },
  { label: 'Transactions', val: payments.value.length, cls: 'info' },
])

const filteredPayments = computed(() => payments.value.filter(p => {
  return (!search.value || p.name.toLowerCase().includes(search.value.toLowerCase()) || p.ref.includes(search.value) || p.phone.includes(search.value))
    && (!filterStatus.value || p.status === filterStatus.value)
    && (!filterSite.value || p.site === filterSite.value)
}))

function submitPayment() {
  if (!form.value.name || !form.value.phone || !form.value.amount) { alert('Fill required fields'); return }
  payments.value.unshift({
    id: payments.value.length + 1,
    ref: `MPE-00${payments.value.length + 1}`,
    name: form.value.name, role: form.value.role,
    phone: form.value.phone, site: form.value.site,
    purpose: form.value.purpose, amount: Number(form.value.amount),
    date: new Date().toISOString().split('T')[0],
    mpesaCode: null, status: 'pending'
  })
  showForm.value = false
  form.value = { name: '', phone: '', amount: '', site: '', purpose: '', role: '', description: '' }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
.mpesa-payments { font-family: 'Syne', sans-serif; background: #0d0f14; color: #e8e4dc; min-height: 100vh; padding: 28px 32px; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.page-tag { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; color: #22c55e; text-transform: uppercase; display: block; margin-bottom: 6px; }
h1 { font-size: 28px; font-weight: 800; color: #fff; }
.page-sub { font-size: 13px; color: #6b7280; margin-top: 4px; }
.btn-primary { background: #22c55e; color: #0d0f14; border: none; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; cursor: pointer; }
.btn-ghost { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }
.mono { font-family: 'DM Mono', monospace; }

.stat-row { display: flex; gap: 12px; margin-bottom: 20px; }
.stat-card { background: #13161f; border: 1px solid #1e2230; border-radius: 10px; padding: 16px 24px; flex: 1; text-align: center; }
.stat-card.green  { border-left: 3px solid #22c55e; }
.stat-card.warn   { border-left: 3px solid #f59e0b; }
.stat-card.danger { border-left: 3px solid #ef4444; }
.stat-card.info   { border-left: 3px solid #3b82f6; }
.stat-val { font-size: 24px; font-weight: 800; color: #fff; }
.stat-label { font-size: 11px; color: #6b7280; margin-top: 4px; text-transform: uppercase; }

.filters-bar { display: flex; gap: 10px; margin-bottom: 16px; }
.search-wrap { flex: 1; display: flex; align-items: center; gap: 8px; background: #13161f; border: 1px solid #1e2230; border-radius: 7px; padding: 0 12px; }
.search-input { flex: 1; background: none; border: none; color: #e8e4dc; padding: 9px 0; font-family: 'Syne', sans-serif; font-size: 13px; outline: none; }
.filter-select { background: #13161f; border: 1px solid #1e2230; color: #e8e4dc; padding: 9px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; }

.table-wrap { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table thead th { padding: 12px 14px; text-align: left; font-size: 10px; font-family: 'DM Mono', monospace; letter-spacing: 1px; color: #4b5563; border-bottom: 1px solid #1e2230; text-transform: uppercase; white-space: nowrap; }
.table-row { border-bottom: 1px solid #1a1e2a; transition: background 0.15s; }
.table-row:hover { background: #161922; }
.table-row td { padding: 12px 14px; vertical-align: middle; }
.ref { font-size: 11px; color: #22c55e; }
.recipient { display: flex; align-items: center; gap: 8px; }
.avatar { width: 28px; height: 28px; border-radius: 50%; background: #22c55e; color: #0d0f14; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 12px; flex-shrink: 0; }
.rec-name { font-size: 12px; font-weight: 600; }
.rec-role { font-size: 10px; color: #4b5563; }
.phone { font-size: 12px; color: #9ca3af; }
.site-cell { font-size: 11px; color: #9ca3af; max-width: 140px; }
.purpose { font-size: 12px; color: #d1d5db; }
.amount { font-size: 13px; font-weight: 700; color: #22c55e; }
.date-cell { font-size: 11px; color: #6b7280; }
.mpesa-code { font-size: 11px; color: #f5a623; letter-spacing: 1px; }

.status-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }
.status-badge.completed { background: #0d2818; color: #22c55e; }
.status-badge.pending   { background: #1f1a08; color: #f59e0b; }
.status-badge.failed    { background: #200e0e; color: #ef4444; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 100; display: flex; align-items: center; justify-content: center; }
.modal { background: #13161f; border: 1px solid #2a2f3e; border-radius: 16px; width: 620px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 28px; border-bottom: 1px solid #1e2230; }
.modal-title-wrap { display: flex; align-items: center; gap: 10px; }
.mpesa-logo { font-size: 24px; }
.modal-header h2 { font-size: 17px; font-weight: 700; }
.close-btn { background: none; border: none; color: #6b7280; font-size: 18px; cursor: pointer; }
.modal-body { padding: 24px 28px; display: flex; flex-direction: column; gap: 14px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 16px 28px; border-top: 1px solid #1e2230; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group.full { grid-column: 1/-1; }
.form-group label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; }
.form-group input, .form-group select, .form-group textarea { background: #0d0f14; border: 1px solid #1e2230; color: #e8e4dc; padding: 10px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; }
.form-group input:focus, .form-group select:focus { outline: none; border-color: #22c55e; }
.stk-notice { background: #0a1810; border: 1px solid #1a3020; border-radius: 8px; padding: 12px 14px; display: flex; gap: 10px; align-items: flex-start; }
.notice-title { font-size: 13px; font-weight: 600; color: #22c55e; }
.notice-sub { font-size: 11px; color: #4b5563; margin-top: 2px; }
</style>