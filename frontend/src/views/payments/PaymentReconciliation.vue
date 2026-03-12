<template>
  <div class="reconciliation">
    <div class="page-header">
      <div>
        <span class="page-tag">PAYMENTS · RECONCILIATION</span>
        <h1>Payment Reconciliation</h1>
        <p class="page-sub">Match M-Pesa and bank statements against project expenditure records</p>
      </div>
      <div class="header-actions">
        <button class="btn-secondary" @click="runAutoMatch">🔄 Auto-Match</button>
        <button class="btn-primary" @click="showUpload = true">📤 Upload Statement</button>
      </div>
    </div>

    <!-- Reconciliation Summary -->
    <div class="recon-summary">
      <div class="sum-card matched">
        <div class="sum-icon">✅</div>
        <div class="sum-val">{{ matched }}</div>
        <div class="sum-label">Matched</div>
        <div class="sum-amount">KES {{ matchedAmount.toLocaleString() }}</div>
      </div>
      <div class="sum-card unmatched">
        <div class="sum-icon">❓</div>
        <div class="sum-val">{{ unmatched }}</div>
        <div class="sum-label">Unmatched</div>
        <div class="sum-amount">KES {{ unmatchedAmount.toLocaleString() }}</div>
      </div>
      <div class="sum-card variance">
        <div class="sum-icon">⚖️</div>
        <div class="sum-val">{{ variance >= 0 ? '+' : '' }}KES {{ Math.abs(variance).toLocaleString() }}</div>
        <div class="sum-label">Variance</div>
        <div class="sum-amount" :class="variance === 0 ? 'zero' : 'nonzero'">{{ variance === 0 ? 'Balanced' : 'Investigate' }}</div>
      </div>
      <div class="sum-card progress-card">
        <div class="sum-icon">📊</div>
        <div class="sum-val">{{ Math.round(matched / records.length * 100) }}%</div>
        <div class="sum-label">Reconciled</div>
        <div class="recon-bar"><div class="recon-fill" :style="{ width: (matched / records.length * 100) + '%' }"></div></div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" type="text" placeholder="Search reference, name or code..." class="search-input" />
      </div>
      <select v-model="filterMatch" class="filter-select">
        <option value="">All Records</option>
        <option value="matched">Matched</option>
        <option value="unmatched">Unmatched</option>
        <option value="partial">Partial</option>
      </select>
      <select v-model="filterChannel" class="filter-select">
        <option value="">All Channels</option>
        <option value="mpesa">M-Pesa</option>
        <option value="bank">Bank</option>
      </select>
    </div>

    <!-- Reconciliation Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>System Ref</th>
            <th>Statement Entry</th>
            <th>Channel</th>
            <th>System Amount (KES)</th>
            <th>Statement Amount (KES)</th>
            <th>Difference (KES)</th>
            <th>Date</th>
            <th>Match Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rec in filteredRecords" :key="rec.id" class="table-row" :class="rec.match">
            <td class="mono sys-ref">{{ rec.sysRef }}</td>
            <td>
              <div class="entry-name">{{ rec.entryName }}</div>
              <div class="entry-code mono">{{ rec.statementCode }}</div>
            </td>
            <td><span class="channel-badge" :class="rec.channel">{{ rec.channel }}</span></td>
            <td class="sys-amount">{{ rec.sysAmount.toLocaleString() }}</td>
            <td class="stmt-amount">{{ rec.stmtAmount.toLocaleString() }}</td>
            <td class="diff" :class="rec.sysAmount - rec.stmtAmount !== 0 ? 'nonzero' : 'zero'">
              {{ rec.sysAmount - rec.stmtAmount === 0 ? '0' : (rec.sysAmount - rec.stmtAmount > 0 ? '+' : '') + (rec.sysAmount - rec.stmtAmount).toLocaleString() }}
            </td>
            <td class="mono date-cell">{{ rec.date }}</td>
            <td>
              <span class="match-badge" :class="rec.match">{{ rec.match }}</span>
            </td>
            <td>
              <button v-if="rec.match !== 'matched'" class="match-btn" @click="manualMatch(rec)">Match</button>
              <span v-else class="matched-tick">✓</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Upload Modal -->
    <div class="modal-overlay" v-if="showUpload" @click.self="showUpload = false">
      <div class="modal">
        <div class="modal-header">
          <h2>📤 Upload Bank / M-Pesa Statement</h2>
          <button class="close-btn" @click="showUpload = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Statement Source</label>
            <select v-model="uploadForm.source">
              <option value="">Select source...</option>
              <option>M-Pesa Statement (CSV)</option>
              <option>KCB Bank Statement (CSV/PDF)</option>
              <option>Equity Bank Statement</option>
              <option>Co-operative Bank Statement</option>
            </select>
          </div>
          <div class="form-group">
            <label>Period</label>
            <div class="form-row">
              <input type="date" v-model="uploadForm.from" />
              <input type="date" v-model="uploadForm.to" />
            </div>
          </div>
          <div class="upload-zone">
            <div class="upload-icon">📂</div>
            <div class="upload-text">Drop statement file here or <span class="upload-link">browse</span></div>
            <div class="upload-hint mono">Supported: CSV, XLSX, PDF</div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showUpload = false">Cancel</button>
          <button class="btn-primary" @click="showUpload = false">Upload & Reconcile</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const search = ref('')
const filterMatch = ref('')
const filterChannel = ref('')
const showUpload = ref(false)
const uploadForm = ref({ source: '', from: '', to: '' })

const records = ref([
  { id: 1, sysRef: 'MPE-001', entryName: 'John Kariuki — Labour', statementCode: 'QJK8X1Y23P', channel: 'mpesa', sysAmount: 12500, stmtAmount: 12500, date: '2025-02-18', match: 'matched' },
  { id: 2, sysRef: 'MPE-002', entryName: 'Mary Akinyi Supplies', statementCode: 'RLM9Z2A45Q', channel: 'mpesa', sysAmount: 145000, stmtAmount: 145000, date: '2025-02-18', match: 'matched' },
  { id: 3, sysRef: 'BNK-001', entryName: 'Steel Fabricators Ltd', statementCode: 'EFT-20250217-001', channel: 'bank', sysAmount: 320000, stmtAmount: 320000, date: '2025-02-17', match: 'matched' },
  { id: 4, sysRef: 'MPE-004', entryName: 'Bamburi Hardware', statementCode: 'FAILED0004', channel: 'mpesa', sysAmount: 78000, stmtAmount: 0, date: '2025-02-17', match: 'unmatched' },
  { id: 5, sysRef: 'BNK-002', entryName: 'Arch. Daniel Oduya', statementCode: 'EFT-20250215-002', channel: 'bank', sysAmount: 250000, stmtAmount: 248500, date: '2025-02-15', match: 'partial' },
  { id: 6, sysRef: 'MPE-005', entryName: 'Grace Wanjiku — Labour', statementCode: 'TNP3B4C67R', channel: 'mpesa', sysAmount: 11000, stmtAmount: 11000, date: '2025-02-16', match: 'matched' },
  { id: 7, sysRef: 'BNK-003', entryName: 'Kisumu Aggregate Suppliers', statementCode: 'EFT-PENDING', channel: 'bank', sysAmount: 180000, stmtAmount: 0, date: '2025-02-14', match: 'unmatched' },
])

const matched = computed(() => records.value.filter(r => r.match === 'matched').length)
const unmatched = computed(() => records.value.filter(r => r.match !== 'matched').length)
const matchedAmount = computed(() => records.value.filter(r => r.match === 'matched').reduce((a, b) => a + b.sysAmount, 0))
const unmatchedAmount = computed(() => records.value.filter(r => r.match !== 'matched').reduce((a, b) => a + b.sysAmount, 0))
const variance = computed(() => records.value.reduce((a, b) => a + (b.sysAmount - b.stmtAmount), 0))

const filteredRecords = computed(() => records.value.filter(r =>
  (!search.value || r.sysRef.includes(search.value) || r.entryName.toLowerCase().includes(search.value.toLowerCase()) || r.statementCode.includes(search.value))
  && (!filterMatch.value || r.match === filterMatch.value)
  && (!filterChannel.value || r.channel === filterChannel.value)
))

function runAutoMatch() { alert('Auto-matching in progress...') }
function manualMatch(rec) { rec.match = 'matched'; rec.stmtAmount = rec.sysAmount }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
.reconciliation { font-family: 'Syne', sans-serif; background: #0d0f14; color: #e8e4dc; min-height: 100vh; padding: 28px 32px; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.page-tag { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; color: #a855f7; text-transform: uppercase; display: block; margin-bottom: 6px; }
h1 { font-size: 28px; font-weight: 800; color: #fff; }
.page-sub { font-size: 13px; color: #6b7280; margin-top: 4px; }
.header-actions { display: flex; gap: 10px; }
.btn-primary { background: #a855f7; color: #fff; border: none; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; cursor: pointer; }
.btn-secondary { background: #13161f; border: 1px solid #2a2f3e; color: #e8e4dc; padding: 10px 16px; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }
.btn-ghost { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }
.mono { font-family: 'DM Mono', monospace; }

.recon-summary { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 20px; }
.sum-card { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 18px; text-align: center; }
.sum-card.matched   { border-top: 3px solid #22c55e; }
.sum-card.unmatched { border-top: 3px solid #ef4444; }
.sum-card.variance  { border-top: 3px solid #f59e0b; }
.sum-card.progress-card { border-top: 3px solid #a855f7; }
.sum-icon { font-size: 22px; margin-bottom: 8px; }
.sum-val { font-size: 28px; font-weight: 800; color: #fff; }
.sum-label { font-size: 11px; color: #6b7280; text-transform: uppercase; margin-top: 4px; }
.sum-amount { font-size: 12px; font-family: 'DM Mono', monospace; margin-top: 6px; }
.sum-amount.zero    { color: #22c55e; }
.sum-amount.nonzero { color: #f59e0b; }
.recon-bar { width: 100%; height: 4px; background: #1e2230; border-radius: 2px; overflow: hidden; margin-top: 10px; }
.recon-fill { height: 100%; background: #a855f7; border-radius: 2px; transition: width 0.8s ease; }

.filters-bar { display: flex; gap: 10px; margin-bottom: 16px; }
.search-wrap { flex: 1; display: flex; align-items: center; gap: 8px; background: #13161f; border: 1px solid #1e2230; border-radius: 7px; padding: 0 12px; }
.search-input { flex: 1; background: none; border: none; color: #e8e4dc; padding: 9px 0; font-family: 'Syne', sans-serif; font-size: 13px; outline: none; }
.filter-select { background: #13161f; border: 1px solid #1e2230; color: #e8e4dc; padding: 9px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; }

.table-wrap { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table thead th { padding: 12px 14px; text-align: left; font-size: 10px; font-family: 'DM Mono', monospace; letter-spacing: 1px; color: #4b5563; border-bottom: 1px solid #1e2230; text-transform: uppercase; white-space: nowrap; }
.table-row { border-bottom: 1px solid #1a1e2a; transition: background 0.15s; }
.table-row:hover { background: #161922; }
.table-row.unmatched { background: #100808; }
.table-row.partial   { background: #0f0c06; }
.table-row td { padding: 12px 14px; vertical-align: middle; }
.sys-ref { font-size: 11px; color: #a855f7; }
.entry-name { font-size: 12px; font-weight: 600; }
.entry-code { font-size: 10px; color: #4b5563; margin-top: 2px; }
.channel-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 2px 7px; border-radius: 3px; text-transform: uppercase; }
.channel-badge.mpesa { background: #0d2010; color: #22c55e; }
.channel-badge.bank  { background: #0d1a2e; color: #3b82f6; }
.sys-amount  { font-size: 12px; font-weight: 700; color: #e8e4dc; }
.stmt-amount { font-size: 12px; color: #9ca3af; }
.diff.zero    { font-size: 12px; color: #22c55e; font-family: 'DM Mono', monospace; }
.diff.nonzero { font-size: 12px; color: #ef4444; font-family: 'DM Mono', monospace; font-weight: 700; }
.date-cell { font-size: 11px; color: #6b7280; }
.match-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }
.match-badge.matched   { background: #0d2818; color: #22c55e; }
.match-badge.unmatched { background: #200e0e; color: #ef4444; }
.match-badge.partial   { background: #1f1a08; color: #f59e0b; }
.match-btn { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 4px 10px; border-radius: 5px; font-size: 11px; cursor: pointer; font-family: 'Syne', sans-serif; }
.match-btn:hover { border-color: #a855f7; color: #a855f7; }
.matched-tick { color: #22c55e; font-size: 14px; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 100; display: flex; align-items: center; justify-content: center; }
.modal { background: #13161f; border: 1px solid #2a2f3e; border-radius: 16px; width: 560px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 28px; border-bottom: 1px solid #1e2230; }
.modal-header h2 { font-size: 16px; font-weight: 700; }
.close-btn { background: none; border: none; color: #6b7280; font-size: 18px; cursor: pointer; }
.modal-body { padding: 24px 28px; display: flex; flex-direction: column; gap: 16px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 16px 28px; border-top: 1px solid #1e2230; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 11px; color: #6b7280; text-transform: uppercase; font-family: 'DM Mono', monospace; }
.form-group select, .form-group input { background: #0d0f14; border: 1px solid #1e2230; color: #e8e4dc; padding: 10px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.upload-zone { border: 2px dashed #2a2f3e; border-radius: 10px; padding: 32px; text-align: center; cursor: pointer; transition: border-color 0.2s; }
.upload-zone:hover { border-color: #a855f7; }
.upload-icon { font-size: 32px; margin-bottom: 8px; }
.upload-text { font-size: 14px; color: #9ca3af; }
.upload-link { color: #a855f7; cursor: pointer; }
.upload-hint { font-size: 11px; color: #4b5563; margin-top: 4px; }
</style>