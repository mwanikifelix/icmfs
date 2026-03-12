<template>
  <div class="procurement-page">
    <div class="page-header">
      <div>
        <span class="page-tag amber">ICMFS · PROCUREMENT</span>
        <h1>Procurement Dashboard</h1>
        <p class="page-sub">Overview of purchase requests, supplier activity and inventory levels</p>
      </div>
      <div style="display:flex;gap:10px">
        <select v-model="selectedMonth" class="filter-select">
          <option>Feb 2025</option><option>Jan 2025</option><option>Dec 2024</option>
        </select>
        <button class="btn-primary amber" @click="$router.push('/app/procurement/requests')">+ New Request</button>
      </div>
    </div>

    <!-- KPIs -->
    <div class="kpi-row">
      <div class="kpi amber">
        <div class="kpi-top"><span>📋</span><span class="mono" style="font-size:10px;color:#f5a623">This month</span></div>
        <div class="kpi-val">{{ totalRequests }}</div>
        <div class="kpi-label">Purchase Requests</div>
      </div>
      <div class="kpi warn">
        <div class="kpi-top"><span>⏳</span><span class="mono" style="font-size:10px;color:#f59e0b">Awaiting approval</span></div>
        <div class="kpi-val">{{ pendingRequests }}</div>
        <div class="kpi-label">Pending Approval</div>
      </div>
      <div class="kpi green">
        <div class="kpi-top"><span>🤝</span><span class="mono" style="font-size:10px;color:#22c55e">Registered</span></div>
        <div class="kpi-val">{{ totalSuppliers }}</div>
        <div class="kpi-label">Active Suppliers</div>
      </div>
      <div class="kpi danger">
        <div class="kpi-top"><span>📦</span><span class="mono" style="font-size:10px;color:#ef4444">Reorder needed</span></div>
        <div class="kpi-val">{{ lowStockCount }}</div>
        <div class="kpi-label">Low Stock Items</div>
      </div>
      <div class="kpi blue">
        <div class="kpi-top"><span>💰</span><span class="mono" style="font-size:10px;color:#3b82f6">Feb 2025</span></div>
        <div class="kpi-val">KES 6.8M</div>
        <div class="kpi-label">Total Procurement Value</div>
      </div>
    </div>

    <div class="mid-grid">
      <!-- Recent PRs -->
      <div class="panel">
        <div class="panel-header">
          <h2>Recent Purchase Requests</h2>
          <button class="btn-ghost" style="padding:4px 10px;font-size:11px" @click="$router.push('/app/procurement/requests')">View All</button>
        </div>
        <div style="display:flex;flex-direction:column;gap:8px">
          <div class="pr-item" v-for="pr in recentPRs" :key="pr.id">
            <div class="pr-icon" :class="pr.category">{{ pr.icon }}</div>
            <div style="flex:1">
              <div class="cell-main">{{ pr.title }}</div>
              <div class="cell-sub">{{ pr.ref }} · {{ pr.site }}</div>
            </div>
            <div style="text-align:right">
              <div class="cell-amount" style="color:#f5a623">KES {{ pr.amount.toLocaleString() }}</div>
              <span class="status-badge" :class="pr.status">{{ pr.status }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Suppliers -->
      <div class="panel">
        <div class="panel-header">
          <h2>Top Suppliers</h2>
          <button class="btn-ghost" style="padding:4px 10px;font-size:11px" @click="$router.push('/app/procurement/suppliers')">View All</button>
        </div>
        <div style="display:flex;flex-direction:column;gap:12px">
          <div v-for="s in topSuppliers" :key="s.name" style="display:flex;align-items:center;gap:10px">
            <div class="supplier-avatar">{{ s.name[0] }}</div>
            <div style="flex:1">
              <div class="cell-main">{{ s.name }}</div>
              <div class="cell-sub">{{ s.category }} · {{ s.orders }} orders</div>
            </div>
            <div style="text-align:right">
              <div style="font-size:12px;font-weight:700;color:#22c55e">{{ s.rating }}★</div>
              <div class="cell-sub">KES {{ (s.value/1000).toFixed(0) }}K</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Category Spend + Low Stock -->
    <div class="bottom-grid">
      <div class="panel">
        <div class="panel-header"><h2>Spend by Category</h2></div>
        <div style="display:flex;flex-direction:column;gap:12px">
          <div v-for="c in categorySpend" :key="c.name">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px">
              <span style="font-size:12px;color:#e8e4dc">{{ c.icon }} {{ c.name }}</span>
              <span class="mono" style="font-size:11px;color:#f5a623">KES {{ (c.amount/1000000).toFixed(1) }}M</span>
            </div>
            <div class="prog-bar-wrap">
              <div class="prog-bar" style="height:8px">
                <div class="prog-fill" :class="c.color" :style="{ width: (c.amount / maxSpend * 100) + '%' }"></div>
              </div>
              <span class="prog-pct">{{ c.pct }}%</span>
            </div>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h2>Low Stock Alerts</h2>
          <span style="background:#200e0e;color:#ef4444;font-family:'DM Mono',monospace;font-size:10px;padding:2px 8px;border-radius:10px">{{ lowStockCount }} items</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:8px">
          <div v-for="item in lowStockItems" :key="item.id" class="stock-alert-item">
            <div style="flex:1">
              <div class="cell-main">{{ item.name }}</div>
              <div class="cell-sub">{{ item.unit }} · {{ item.site }}</div>
            </div>
            <div style="text-align:right">
              <div style="font-size:13px;font-weight:800" :style="item.qty <= item.reorder ? 'color:#ef4444' : 'color:#f59e0b'">
                {{ item.qty }} {{ item.unit }}
              </div>
              <div class="cell-sub">Min: {{ item.reorder }}</div>
            </div>
            <button class="reorder-btn" @click="reorder(item)">Reorder</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const selectedMonth = ref('Feb 2025')

const recentPRs = ref([
  { id: 1, ref: 'PR-2025-041', title: 'Cement — 500 Bags',          icon: '🧱', category: 'materials', site: 'Nairobi Housing', amount: 125000, status: 'pending'  },
  { id: 2, ref: 'PR-2025-040', title: 'Steel Rebar 16mm — 5 Tonnes', icon: '🔩', category: 'materials', site: 'Kisumu Complex',  amount: 320000, status: 'approved' },
  { id: 3, ref: 'PR-2025-039', title: 'Electrical Cable Rolls x20',  icon: '⚡', category: 'mep',       site: 'Mombasa Road',   amount: 88000,  status: 'ordered'  },
  { id: 4, ref: 'PR-2025-038', title: 'Excavator Hire — 2 Weeks',    icon: '🚜', category: 'equipment', site: 'Nakuru Road',    amount: 180000, status: 'approved' },
  { id: 5, ref: 'PR-2025-037', title: 'Safety Gear — 50 Sets',       icon: '🦺', category: 'safety',    site: 'All Sites',      amount: 45000,  status: 'draft'    },
])

const topSuppliers = ref([
  { name: 'Bamburi Cement Ltd',     category: 'Materials', orders: 18, rating: 4.8, value: 820000  },
  { name: 'Steel Fabricators Ltd',  category: 'Materials', orders: 12, rating: 4.6, value: 650000  },
  { name: 'East Africa Cables',     category: 'MEP',       orders: 8,  rating: 4.5, value: 320000  },
  { name: 'Nakuru Plant Hire',      category: 'Equipment', orders: 6,  rating: 4.7, value: 480000  },
])

const categorySpend = ref([
  { name: 'Construction Materials', icon: '🧱', amount: 3200000, pct: 47, color: 'amber'  },
  { name: 'Equipment & Machinery',  icon: '🚜', amount: 1800000, pct: 26, color: 'blue'   },
  { name: 'MEP & Electrical',       icon: '⚡', amount: 980000,  pct: 14, color: 'teal'   },
  { name: 'Safety Equipment',       icon: '🦺', amount: 480000,  pct: 7,  color: 'green'  },
  { name: 'Tools & Consumables',    icon: '🔧', amount: 340000,  pct: 5,  color: 'purple' },
])

const lowStockItems = ref([
  { id: 1, name: 'OPC Cement',         unit: 'Bags',  qty: 45,  reorder: 100, site: 'Nairobi Housing' },
  { id: 2, name: 'Binding Wire',       unit: 'Rolls', qty: 8,   reorder: 20,  site: 'Kisumu Complex'  },
  { id: 3, name: 'Nails — 4"',         unit: 'Kg',    qty: 12,  reorder: 50,  site: 'Mombasa Road'    },
  { id: 4, name: 'Safety Helmets',     unit: 'Units', qty: 6,   reorder: 15,  site: 'All Sites'       },
])

const maxSpend     = computed(() => Math.max(...categorySpend.value.map(c => c.amount)))
const totalRequests  = ref(41)
const pendingRequests = computed(() => recentPRs.value.filter(p => p.status === 'pending' || p.status === 'draft').length + 3)
const totalSuppliers = ref(24)
const lowStockCount  = computed(() => lowStockItems.value.length)

function reorder(item) { alert(`Reorder request created for ${item.name}`) }
</script>

<style scoped>
@import '/src/assets/procurement.css';
.kpi-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.mid-grid    { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.pr-item { display: flex; align-items: center; gap: 10px; padding: 10px; background: #0d0f14; border-radius: 8px; border: 1px solid #1a1e2a; }
.pr-icon { width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.pr-icon.materials { background: #1f1a08; }
.pr-icon.mep       { background: #0d1a2e; }
.pr-icon.equipment { background: #0d2010; }
.pr-icon.safety    { background: #200e0e; }
.supplier-avatar { width: 34px; height: 34px; border-radius: 50%; background: #14b8a6; color: #0d0f14; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px; flex-shrink: 0; }
.stock-alert-item { display: flex; align-items: center; gap: 10px; padding: 10px; background: #0d0f14; border-radius: 8px; border: 1px solid #1a1e2a; }
.reorder-btn { background: none; border: 1px solid #f5a623; color: #f5a623; padding: 4px 10px; border-radius: 5px; font-size: 11px; cursor: pointer; font-family: 'Syne', sans-serif; white-space: nowrap; }
</style>