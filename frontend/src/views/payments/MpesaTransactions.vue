<template>
  <div class="payments-page">
    <div class="page-header">
      <div>
        <span class="page-tag green">PAYMENTS · TRANSACTIONS</span>
        <h1>M-Pesa Transactions</h1>
        <p class="page-sub">Full transaction history — all M-Pesa STK push records</p>
      </div>
      <button class="btn-export" @click="exportCSV">📥 Export CSV</button>
    </div>

    <div class="stat-row">
      <div class="stat-card" v-for="s in summary" :key="s.label" :class="s.cls">
        <div class="stat-val">{{ s.val }}</div>
        <div class="stat-label">{{ s.label }}</div>
      </div>
    </div>

    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" type="text" placeholder="Search ref, name, M-Pesa code..." class="search-input" />
      </div>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="success">Success</option>
        <option value="pending">Pending</option>
        <option value="failed">Failed</option>
        <option value="reversed">Reversed</option>
      </select>
      <select v-model="filterType" class="filter-select">
        <option value="">All Types</option>
        <option value="stk_push">STK Push</option>
        <option value="b2c">B2C</option>
        <option value="paybill">Paybill</option>
      </select>
      <input v-model="dateFrom" type="date" class="filter-select" />
      <input v-model="dateTo"   type="date" class="filter-select" />
    </div>

    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>M-Pesa Code</th><th>Type</th><th>Sender / Recipient</th><th>Phone</th>
            <th>Amount (KES)</th><th>Charge</th><th>Net (KES)</th><th>Date & Time</th><th>Status</th><th>Project Ref</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="txn in filteredTxns" :key="txn.id" class="table-row">
            <td class="mono" style="font-size:11px;color:#f5a623;letter-spacing:1px">{{ txn.code }}</td>
            <td><span class="type-badge" :class="txn.type">{{ txn.type }}</span></td>
            <td>
              <div class="cell-main">{{ txn.party }}</div>
              <div class="cell-sub">Acc: {{ txn.account }}</div>
            </td>
            <td class="mono" style="font-size:11px;color:#9ca3af">{{ txn.phone }}</td>
            <td class="cell-amount" style="color:#22c55e">{{ txn.amount.toLocaleString() }}</td>
            <td class="mono cell-sub" style="font-size:11px">{{ txn.charge }}</td>
            <td style="font-size:12px;font-weight:600;color:#d1d5db">{{ (txn.amount - txn.charge).toLocaleString() }}</td>
            <td class="cell-date">{{ txn.datetime }}</td>
            <td><span class="status-badge" :class="txn.status">{{ txn.status }}</span></td>
            <td class="mono" style="font-size:11px;color:#f5a623">{{ txn.projectRef }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <span class="page-info">Showing {{ filteredTxns.length }} of {{ transactions.length }} records</span>
      <div class="page-btns">
        <button class="page-btn">‹ Prev</button>
        <button class="page-btn active">1</button>
        <button class="page-btn">2</button>
        <button class="page-btn">Next ›</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const search = ref('')
const filterStatus = ref('')
const filterType = ref('')
const dateFrom = ref('')
const dateTo = ref('')

const transactions = ref([
  { id: 1, code: 'QJK8X1Y23P', type: 'stk_push', party: 'John Kariuki',          account: '254712345678', phone: '0712345678', amount: 12500,  charge: 55, datetime: '2025-02-18 14:32', status: 'success',  projectRef: 'NBO-001' },
  { id: 2, code: 'RLM9Z2A45Q', type: 'b2c',      party: 'Mary Akinyi Supplies',   account: '254723456789', phone: '0723456789', amount: 145000, charge: 0,  datetime: '2025-02-18 13:15', status: 'success',  projectRef: 'MSA-002' },
  { id: 3, code: 'PENDING003', type: 'stk_push', party: 'Peter Otieno',            account: '254734567890', phone: '0734567890', amount: 8750,   charge: 35, datetime: '2025-02-17 16:45', status: 'pending',  projectRef: 'KSM-003' },
  { id: 4, code: 'FAILED0004', type: 'stk_push', party: 'Bamburi Hardware Ltd',    account: '254745678901', phone: '0745678901', amount: 78000,  charge: 0,  datetime: '2025-02-17 11:20', status: 'failed',   projectRef: 'NBO-001' },
  { id: 5, code: 'TNP3B4C67R', type: 'paybill',  party: 'Grace Wanjiku',           account: '254756789012', phone: '0756789012', amount: 11000,  charge: 55, datetime: '2025-02-16 09:50', status: 'success',  projectRef: 'NAK-004' },
  { id: 6, code: 'VQR5D6E89S', type: 'b2c',      party: 'Mombasa Equip Hire Co.',  account: '254767890123', phone: '0767890123', amount: 35000,  charge: 0,  datetime: '2025-02-15 15:10', status: 'success',  projectRef: 'MSA-002' },
  { id: 7, code: 'WXT7F8G01T', type: 'stk_push', party: 'Alice Njeri',             account: '254778901234', phone: '0778901234', amount: 9500,   charge: 35, datetime: '2025-02-14 08:30', status: 'reversed', projectRef: 'NBO-001' },
])

const summary = computed(() => [
  { label: 'Total Volume', val: 'KES ' + transactions.value.reduce((a, b) => a + b.amount, 0).toLocaleString(), cls: 'primary' },
  { label: 'Successful',   val: transactions.value.filter(t => t.status === 'success').length,   cls: 'green'  },
  { label: 'Pending',      val: transactions.value.filter(t => t.status === 'pending').length,   cls: 'warn'   },
  { label: 'Failed',       val: transactions.value.filter(t => t.status === 'failed').length,    cls: 'danger' },
  { label: 'Reversed',     val: transactions.value.filter(t => t.status === 'reversed').length,  cls: 'info'   },
])

const filteredTxns = computed(() => transactions.value.filter(t =>
  (!search.value || t.code.includes(search.value) || t.party.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterStatus.value || t.status === filterStatus.value)
  && (!filterType.value || t.type === filterType.value)
))

function exportCSV() { alert('Exporting...') }
</script>

<style scoped>
@import '/src/assets/payments.css';
</style>

