<template>
  <div class="payment-audit">
    <div class="page-header">
      <div>
        <span class="page-tag">PAYMENTS · AUDIT TRAIL</span>
        <h1>Payment Audit</h1>
        <p class="page-sub">Complete immutable audit log of all payment activities and approvals</p>
      </div>
      <button class="btn-export" @click="exportAudit">📥 Export Audit Log</button>
    </div>

    <!-- Alert Banner -->
    <div class="alert-banner" v-if="anomalies.length">
      <span class="alert-icon">⚠️</span>
      <div>
        <div class="alert-title">{{ anomalies.length }} Anomaly{{ anomalies.length > 1 ? 'ies' : '' }} Detected</div>
        <div class="alert-sub">Review flagged transactions below for potential irregularities.</div>
      </div>
    </div>

    <!-- Stats -->
    <div class="audit-stats">
      <div class="astat" v-for="s in auditStats" :key="s.label" :class="s.cls">
        <div class="astat-val">{{ s.val }}</div>
        <div class="astat-label">{{ s.label }}</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" type="text" placeholder="Search user, action, or reference..." class="search-input" />
      </div>
      <select v-model="filterAction" class="filter-select">
        <option value="">All Actions</option>
        <option value="created">Created</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
        <option value="reversed">Reversed</option>
        <option value="modified">Modified</option>
      </select>
      <select v-model="filterFlag" class="filter-select">
        <option value="">All Records</option>
        <option value="true">Flagged Only</option>
        <option value="false">Clean Only</option>
      </select>
    </div>

    <!-- Audit Log Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Action</th>
            <th>User</th>
            <th>Role</th>
            <th>Payment Ref</th>
            <th>Description</th>
            <th>Amount (KES)</th>
            <th>IP Address</th>
            <th>Flag</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in filteredLogs" :key="log.id" class="table-row" :class="log.flagged ? 'flagged' : ''">
            <td class="mono timestamp">{{ log.timestamp }}</td>
            <td><span class="action-badge" :class="log.action">{{ log.action }}</span></td>
            <td>
              <div class="user-name">{{ log.user }}</div>
              <div class="user-dept mono">{{ log.dept }}</div>
            </td>
            <td class="role-cell">{{ log.role }}</td>
            <td class="mono ref-cell">{{ log.ref }}</td>
            <td class="desc-cell">{{ log.description }}</td>
            <td class="amount-cell">{{ log.amount ? 'KES ' + log.amount.toLocaleString() : '—' }}</td>
            <td class="mono ip-cell">{{ log.ip }}</td>
            <td>
              <span v-if="log.flagged" class="flag-badge">⚑ Flagged</span>
              <span v-else class="clean-badge">✓ Clean</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const search = ref('')
const filterAction = ref('')
const filterFlag = ref('')

const logs = ref([
  { id: 1, timestamp: '2025-02-18 14:32:11', action: 'created', user: 'James Mutua', dept: 'Engineering', role: 'Site Engineer', ref: 'APR-001', description: 'Payment request created for roofing materials', amount: 420000, ip: '192.168.1.45', flagged: false },
  { id: 2, timestamp: '2025-02-18 15:10:03', action: 'approved', user: 'Grace Otieno', dept: 'Safety & QA', role: 'Site Manager', ref: 'APR-001', description: 'Approved at Level 1 — Site Manager', amount: 420000, ip: '192.168.1.52', flagged: false },
  { id: 3, timestamp: '2025-02-18 16:45:22', action: 'approved', user: 'Peter Kamau', dept: 'Projects', role: 'Project Manager', ref: 'APR-001', description: 'Approved at Level 2 — Project Manager', amount: 420000, ip: '10.8.0.14', flagged: false },
  { id: 4, timestamp: '2025-02-17 09:15:44', action: 'created', user: 'Alice Njeri', dept: 'Finance', role: 'Accounts Clerk', ref: 'MPE-004', description: 'M-Pesa payment initiated to Bamburi Hardware', amount: 78000, ip: '192.168.1.71', flagged: true },
  { id: 5, timestamp: '2025-02-17 09:18:02', action: 'modified', user: 'Alice Njeri', dept: 'Finance', role: 'Accounts Clerk', ref: 'MPE-004', description: 'Amount modified from KES 45,000 to KES 78,000 before approval', amount: 78000, ip: '192.168.1.71', flagged: true },
  { id: 6, timestamp: '2025-02-16 11:30:55', action: 'rejected', user: 'Alice Wanjiku', dept: 'Finance', role: 'Finance Manager', ref: 'APR-004', description: 'Rejected — invoice does not match LPO amount', amount: 95000, ip: '10.8.0.23', flagged: false },
  { id: 7, timestamp: '2025-02-15 14:05:18', action: 'reversed', user: 'Alice Wanjiku', dept: 'Finance', role: 'Finance Manager', ref: 'MPE-007', description: 'Transaction reversed — duplicate payment detected', amount: 9500, ip: '10.8.0.23', flagged: true },
  { id: 8, timestamp: '2025-02-14 08:22:33', action: 'approved', user: 'Alice Wanjiku', dept: 'Finance', role: 'Finance Manager', ref: 'BNK-002', description: 'Bank transfer approved — consultant fee', amount: 250000, ip: '10.8.0.23', flagged: false },
])

const anomalies = computed(() => logs.value.filter(l => l.flagged))

const auditStats = computed(() => [
  { label: 'Total Log Entries', val: logs.value.length, cls: 'info' },
  { label: 'Flagged', val: logs.value.filter(l => l.flagged).length, cls: 'danger' },
  { label: 'Approvals', val: logs.value.filter(l => l.action === 'approved').length, cls: 'green' },
  { label: 'Reversals', val: logs.value.filter(l => l.action === 'reversed').length, cls: 'warn' },
])

const filteredLogs = computed(() => logs.value.filter(l =>
  (!search.value || l.user.toLowerCase().includes(search.value.toLowerCase()) || l.ref.includes(search.value) || l.description.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterAction.value || l.action === filterAction.value)
  && (filterFlag.value === '' || String(l.flagged) === filterFlag.value)
))

function exportAudit() { alert('Exporting audit log...') }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
.payment-audit { font-family: 'Syne', sans-serif; background: #0d0f14; color: #e8e4dc; min-height: 100vh; padding: 28px 32px; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.page-tag { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; color: #a855f7; text-transform: uppercase; display: block; margin-bottom: 6px; }
h1 { font-size: 28px; font-weight: 800; color: #fff; }
.page-sub { font-size: 13px; color: #6b7280; margin-top: 4px; }
.btn-export { background: #13161f; border: 1px solid #2a2f3e; color: #e8e4dc; padding: 10px 18px; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }
.mono { font-family: 'DM Mono', monospace; }

.alert-banner { background: #1f1008; border: 1px solid #f59e0b; border-radius: 10px; padding: 14px 18px; display: flex; gap: 12px; align-items: flex-start; margin-bottom: 18px; }
.alert-icon { font-size: 20px; }
.alert-title { font-size: 14px; font-weight: 700; color: #f59e0b; }
.alert-sub { font-size: 12px; color: #92400e; margin-top: 2px; }

.audit-stats { display: flex; gap: 12px; margin-bottom: 18px; }
.astat { background: #13161f; border: 1px solid #1e2230; border-radius: 8px; padding: 12px 20px; flex: 1; }
.astat.info   { border-left: 3px solid #3b82f6; }
.astat.danger { border-left: 3px solid #ef4444; }
.astat.green  { border-left: 3px solid #22c55e; }
.astat.warn   { border-left: 3px solid #f59e0b; }
.astat-val { font-size: 26px; font-weight: 800; color: #fff; }
.astat-label { font-size: 11px; color: #6b7280; text-transform: uppercase; margin-top: 4px; }

.filters-bar { display: flex; gap: 10px; margin-bottom: 16px; }
.search-wrap { flex: 1; display: flex; align-items: center; gap: 8px; background: #13161f; border: 1px solid #1e2230; border-radius: 7px; padding: 0 12px; }
.search-input { flex: 1; background: none; border: none; color: #e8e4dc; padding: 9px 0; font-family: 'Syne', sans-serif; font-size: 13px; outline: none; }
.filter-select { background: #13161f; border: 1px solid #1e2230; color: #e8e4dc; padding: 9px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; }

.table-wrap { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table thead th { padding: 12px 14px; text-align: left; font-size: 10px; font-family: 'DM Mono', monospace; letter-spacing: 1px; color: #4b5563; border-bottom: 1px solid #1e2230; text-transform: uppercase; white-space: nowrap; }
.table-row { border-bottom: 1px solid #1a1e2a; transition: background 0.15s; }
.table-row:hover { background: #161922; }
.table-row.flagged { background: #120a05; }
.table-row.flagged:hover { background: #1a0e08; }
.table-row td { padding: 11px 14px; vertical-align: middle; }
.timestamp { font-size: 11px; color: #6b7280; white-space: nowrap; }
.action-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }
.action-badge.created  { background: #0d1a2e; color: #3b82f6; }
.action-badge.approved { background: #0d2818; color: #22c55e; }
.action-badge.rejected { background: #200e0e; color: #ef4444; }
.action-badge.reversed { background: #1a1e2a; color: #9ca3af; }
.action-badge.modified { background: #1f1008; color: #f59e0b; }
.user-name { font-size: 12px; font-weight: 600; }
.user-dept { font-size: 10px; color: #4b5563; }
.role-cell { font-size: 11px; color: #9ca3af; }
.ref-cell { font-size: 11px; color: #f5a623; }
.desc-cell { font-size: 11px; color: #9ca3af; max-width: 240px; }
.amount-cell { font-size: 12px; font-weight: 700; color: #e8e4dc; white-space: nowrap; }
.ip-cell { font-size: 10px; color: #4b5563; }
.flag-badge  { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; background: #2a0808; color: #ef4444; }
.clean-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; background: #0d2818; color: #22c55e; }
</style>