<template>
  <div class="payments-page">
    <div class="page-header">
      <div>
        <span class="page-tag amber">ICMFS — PAYMENTS MODULE</span>
        <h1>Payments Dashboard</h1>
        <p class="page-sub">Financial transactions overview across all projects and sites</p>
      </div>
      <div class="header-actions">
        <select v-model="selectedMonth" class="filter-select">
          <option>Feb 2025</option><option>Jan 2025</option><option>Dec 2024</option>
        </select>
        <button class="btn-primary amber" @click="$router.push('/app/payments/mpesa')">+ New Payment</button>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-row">
      <div class="kpi" v-for="k in kpis" :key="k.label" :class="k.cls">
        <div class="kpi-top">
         <!--  <span>{{ k.icon }}</span> -->
          <span class="kpi-trend" :class="k.trendCls">{{ k.trend }}</span>
        </div>
        <div class="kpi-val">{{ k.value }}</div>
        <div class="kpi-label">{{ k.label }}</div>
        <div class="kpi-bar"><div class="kpi-fill" :style="{ width: k.pct + '%' }"></div></div>
      </div>
    </div>

    <div class="mid-row">
      <!-- Payment Channels -->
      <div class="panel">
        <div class="panel-header"><h2>Payment Channels</h2></div>
        <div class="channel-list">
          <div class="channel-item" v-for="ch in channels" :key="ch.name">
            <div class="ch-left">
              <div class="ch-icon" :class="ch.cls">{{ ch.icon }}</div>
              <div>
                <div class="cell-main">{{ ch.name }}</div>
                <div class="cell-sub">{{ ch.count }} transactions</div>
              </div>
            </div>
            <div class="ch-right">
              <div class="cell-main">{{ ch.amount }}</div>
              <div class="ch-bar-wrap">
                <div class="ch-bar"><div class="ch-fill" :class="ch.cls" :style="{ width: ch.pct + '%' }"></div></div>
                <span class="cell-sub">{{ ch.pct }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Transactions -->
      <div class="panel">
        <div class="panel-header">
          <h2>Recent Transactions</h2>
          <button class="btn-ghost" style="padding:4px 10px;font-size:11px" @click="$router.push('/app/payments/transactions')">View All</button>
        </div>
        <div class="txn-list">
          <div class="txn-item" v-for="txn in recentTxns" :key="txn.id">
            <div class="txn-icon" :class="txn.type">{{ txn.icon }}</div>
            <div class="txn-body">
              <div class="cell-main">{{ txn.name }}</div>
              <div class="cell-sub">{{ txn.ref }} · {{ txn.date }}</div>
            </div>
            <div class="txn-right">
              <div class="cell-amount" :class="txn.type === 'mpesa' ? 'green' : 'blue'">{{ txn.amount }}</div>
              <div class="status-badge" :class="txn.status">{{ txn.status }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-row">
      <!-- Pending Approvals -->
      <div class="panel">
        <div class="panel-header">
          <h2>Pending Approvals</h2>
          <span class="badge-count">{{ pendingApprovals.length }}</span>
        </div>
        <div class="pending-list">
          <div class="pending-item" v-for="p in pendingApprovals" :key="p.id">
            <div class="pend-info">
              <div class="cell-main">{{ p.name }}</div>
              <div class="cell-sub">{{ p.site }} · {{ p.date }}</div>
            </div>
            <div class="cell-amount amber">{{ p.amount }}</div>
            <div style="display:flex;gap:6px">
              <button class="approve-btn" style="padding:5px 10px;font-size:11px" @click="approve(p)">✓</button>
              <button class="reject-btn"  style="padding:5px 8px;font-size:11px"  @click="reject(p)">✕</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Monthly Chart -->
      <div class="panel">
        <div class="panel-header"><h2>Monthly Spend (KES)</h2></div>
        <div class="bar-chart">
          <div class="chart-bars">
            <div class="chart-col" v-for="m in monthlySpend" :key="m.label">
              <div class="bar-wrap">
                <div class="bar-fill" :style="{ height: (m.amount / maxSpend * 100) + '%' }"></div>
              </div>
              <span class="cell-sub">{{ m.label }}</span>
              <span class="mono" style="font-size:9px;color:#f5a623">{{ m.short }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const selectedMonth = ref('Feb 2025')

const kpis = ref([
  { label: 'Total Disbursed',    value: 'KES 4.2M', icon: '💸', trend: '↑ 12%',          trendCls: 'up',   cls: 'primary', pct: 72 },
  { label: 'Pending Approval',   value: 'KES 890K', icon: '⏳', trend: '3 requests',      trendCls: 'warn', cls: 'warn',    pct: 45 },
  { label: 'M-Pesa Volume',      value: 'KES 2.1M', icon: '📱', trend: '↑ 8%',            trendCls: 'up',   cls: 'green',   pct: 58 },
  { label: 'Failed Transactions',value: '7',        icon: '❌', trend: '↓ 2 from last mo', trendCls: 'good', cls: 'danger',  pct: 20 },
])
const channels = ref([
  { name: 'M-Pesa',        icon: '📱', count: 142, amount: 'KES 2.1M', pct: 50, cls: 'mpesa'  },
  { name: 'Bank Transfer', icon: '🏦', count: 38,  amount: 'KES 1.6M', pct: 38, cls: 'bank'   },
  { name: 'Cheque',        icon: '📝', count: 12,  amount: 'KES 500K', pct: 12, cls: 'cheque' },
])
const recentTxns = ref([
  { id: 1, icon: '📱', name: 'Cement Supplier — Bamburi',  ref: 'TXN-0891', date: '18 Feb', amount: 'KES 145,000', type: 'mpesa', status: 'completed' },
  { id: 2, icon: '🏦', name: 'Steel Fabricators Ltd',      ref: 'TXN-0890', date: '17 Feb', amount: 'KES 320,000', type: 'bank',  status: 'completed' },
  { id: 3, icon: '📱', name: 'Casual Labour — Nairobi',    ref: 'TXN-0889', date: '17 Feb', amount: 'KES 78,500',  type: 'mpesa', status: 'pending'   },
  { id: 4, icon: '📱', name: 'Hardware — Kisumu',          ref: 'TXN-0888', date: '16 Feb', amount: 'KES 34,200',  type: 'mpesa', status: 'failed'    },
  { id: 5, icon: '🏦', name: 'Consulting Fee — Arch. Oduya', ref: 'TXN-0887', date: '15 Feb', amount: 'KES 250,000', type: 'bank', status: 'completed' },
])
const pendingApprovals = ref([
  { id: 1, name: 'Roofing Materials — Mombasa',  site: 'Mombasa Infra',    date: '18 Feb', amount: 'KES 420,000' },
  { id: 2, name: 'Electrical Contractor Payment', site: 'Kisumu Commercial',date: '17 Feb', amount: 'KES 180,000' },
  { id: 3, name: 'Site Labour — Week 7',          site: 'Nairobi Housing',  date: '16 Feb', amount: 'KES 290,000' },
])
const monthlySpend = ref([
  { label: 'SEP', amount: 1800000, short: '1.8M' },
  { label: 'OCT', amount: 2400000, short: '2.4M' },
  { label: 'NOV', amount: 2100000, short: '2.1M' },
  { label: 'DEC', amount: 1600000, short: '1.6M' },
  { label: 'JAN', amount: 3200000, short: '3.2M' },
  { label: 'FEB', amount: 4200000, short: '4.2M' },
])
const maxSpend = computed(() => Math.max(...monthlySpend.value.map(m => m.amount)))
function approve(p) { pendingApprovals.value = pendingApprovals.value.filter(x => x.id !== p.id) }
function reject(p)  { pendingApprovals.value = pendingApprovals.value.filter(x => x.id !== p.id) }
</script>


<style scoped>
@import '/src/assets/payments.css';

/* HEADER */
.header-actions{
display:flex;
gap:10px;
align-items:center
}

.page-tag.amber{
color:#facc15;
}

/* KPI */
.kpi{
position:relative;
overflow:hidden;
background:#0f3f79;
border-radius:10px;
}

.kpi-top{
display:flex;
justify-content:space-between;
margin-bottom:10px;
color:#ffffff
}

.kpi-trend.up{
font-family:'DM Mono',monospace;
font-size:10px;
color:#16a34a;
}

.kpi-trend.warn{
font-family:'DM Mono',monospace;
font-size:10px;
color:#facc15;
}

.kpi-trend.good{
font-family:'DM Mono',monospace;
font-size:10px;
color:#16a34a;
}

.kpi-bar{
position:absolute;
bottom:0;
left:0;
right:0;
height:3px;
background:#1e293b;
}

.kpi-fill{
height:100%;
background:#facc15;
}

/* GRID */
.mid-row{
display:grid;
grid-template-columns:1fr 1fr;
gap:16px;
margin-bottom:16px;
}

.bottom-row{
display:grid;
grid-template-columns:1.4fr 1fr;
gap:16px;
}

/* CHANNELS */
.channel-list{
display:flex;
flex-direction:column;
gap:14px;
}

.channel-item{
display:flex;
justify-content:space-between;
align-items:center;
}

.ch-left{
display:flex;
align-items:center;
gap:10px;
}

.ch-icon{
width:36px;
height:36px;
border-radius:8px;
display:flex;
align-items:center;
justify-content:center;
font-size:18px;
}

.ch-icon.mpesa{
background:#16a34a33;
}

.ch-icon.bank{
background:#0b2e5933;
}

.ch-icon.cheque{
background:#facc1533;
}

.ch-right{
text-align:right;
}

.ch-bar-wrap{
display:flex;
align-items:center;
gap:6px;
}

.ch-bar{
width:80px;
height:4px;
background:#1e293b;
border-radius:2px;
overflow:hidden;
}

.ch-fill{
height:100%;
border-radius:2px;
}

.ch-fill.mpesa{
background:#16a34a;
}

.ch-fill.bank{
background:#3b82f6;
}

.ch-fill.cheque{
background:#facc15;
}

/* TRANSACTIONS */
.txn-list{
display:flex;
flex-direction:column;
gap:8px;
}

.txn-item{
display:flex;
align-items:center;
gap:10px;
padding:10px;
background:#0f3f79;
border-radius:8px;
border:1px solid #1e293b;
}

.txn-icon{
width:32px;
height:32px;
border-radius:8px;
display:flex;
align-items:center;
justify-content:center;
font-size:16px;
flex-shrink:0;
}

.txn-icon.mpesa{
background:#16a34a;
}

.txn-icon.bank{
background:#0b2e59;
}

.txn-body{
flex:1;
}

.txn-right{
text-align:right;
}

.cell-amount.green{
color:#16a34a;
}

.cell-amount.blue{
color:#3b82f6;
}

.cell-amount.amber{
color:#facc15;
}

/* BADGE */
.badge-count{
background:#facc15;
color:#0b2e59;
font-size:11px;
font-weight:800;
padding:2px 8px;
border-radius:10px;
}

/* PENDING */
.pending-list{
display:flex;
flex-direction:column;
gap:10px;
}

.pending-item{
display:flex;
align-items:center;
gap:12px;
padding:12px;
background:#0f3f79;
border-radius:8px;
border:1px solid #1e293b;
}

.pend-info{
flex:1;
}

/* CHART */
.bar-chart{
padding-top:8px;
}

.chart-bars{
display:flex;
align-items:flex-end;
gap:10px;
height:120px;
}

.chart-col{
flex:1;
display:flex;
flex-direction:column;
align-items:center;
height:100%;
}

.bar-wrap{
flex:1;
width:100%;
display:flex;
align-items:flex-end;
}

.bar-fill{
width:100%;
background:linear-gradient(to top,#facc15,#facc1555);
border-radius:4px 4px 0 0;
transition:height .8s ease;
}
</style>