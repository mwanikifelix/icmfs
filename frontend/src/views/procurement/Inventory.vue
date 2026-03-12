<template>
  <div class="procurement-page">
    <div class="page-header">
      <div>
        <span class="page-tag teal">PROCUREMENT · INVENTORY</span>
        <h1>Inventory</h1>
        <p class="page-sub">Real-time stock levels, deliveries and material consumption across all sites</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary teal" @click="showForm = true">+ Add Stock</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card teal">
        <div class="stat-val">{{ inventory.length }}</div>
        <div class="stat-label">Total Stock Items</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-val">{{ criticalItems }}</div>
        <div class="stat-label">Critical / Out of Stock</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">{{ lowItems }}</div>
        <div class="stat-label">Low Stock</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">{{ deliveriesThisWeek }}</div>
        <div class="stat-label">Deliveries This Week</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">KES {{ totalStockValue }}</div>
        <div class="stat-label">Total Stock Value</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search item name or category..." />
      </div>
      <select v-model="filterCategory" class="filter-select">
        <option value="">All Categories</option>
        <option value="materials">Materials</option>
        <option value="mep">MEP</option>
        <option value="safety">Safety</option>
        <option value="tools">Tools</option>
        <option value="equipment">Equipment</option>
      </select>
      <select v-model="filterSite" class="filter-select">
        <option value="">All Sites</option>
        <option v-for="s in siteOptions" :key="s">{{ s }}</option>
      </select>
      <select v-model="filterLevel" class="filter-select">
        <option value="">All Levels</option>
        <option value="critical">Critical</option>
        <option value="low">Low</option>
        <option value="ok">OK</option>
      </select>
    </div>

    <!-- Inventory Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Item</th><th>Category</th><th>Site</th><th>In Stock</th>
            <th>Reorder Level</th><th>Stock Level</th><th>Unit Cost (KES)</th>
            <th>Total Value</th><th>Last Delivery</th><th>Status</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredInventory" :key="item.id" class="table-row" :class="item.level === 'critical' ? 'critical-row' : ''">
            <td>
              <div class="cell-main">{{ item.name }}</div>
              <div class="cell-sub">{{ item.sku }}</div>
            </td>
            <td><span class="cat-badge" :class="item.category">{{ item.category }}</span></td>
            <td class="cell-muted" style="font-size:11px">{{ item.site }}</td>
            <td>
              <span style="font-size:16px;font-weight:800" :style="stockColor(item)">{{ item.qty }}</span>
              <span class="mono" style="font-size:10px;color:#4b5563;margin-left:4px">{{ item.unit }}</span>
            </td>
            <td class="mono" style="font-size:12px;color:#6b7280">{{ item.reorderLevel }} {{ item.unit }}</td>
            <td style="min-width:130px">
              <div class="prog-bar-wrap">
                <div class="prog-bar">
                  <div class="prog-fill" :class="stockFill(item)" :style="{ width: Math.min((item.qty / item.maxStock * 100), 100) + '%' }"></div>
                </div>
                <span class="prog-pct">{{ Math.round(item.qty / item.maxStock * 100) }}%</span>
              </div>
            </td>
            <td class="mono" style="font-size:12px;color:#e8e4dc">{{ item.unitCost.toLocaleString() }}</td>
            <td class="cell-amount" style="color:#14b8a6">{{ (item.qty * item.unitCost).toLocaleString() }}</td>
            <td class="cell-date">{{ item.lastDelivery }}</td>
            <td><span class="status-badge" :class="item.level">{{ item.level }}</span></td>
            <td>
              <button v-if="item.level !== 'ok'" class="reorder-btn" @click="createReorder(item)">Reorder</button>
              <button v-else class="use-btn" @click="activeItem = item">Consume</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Consumption / Reorder Drawer -->
    <div class="drawer-overlay" v-if="activeItem" @click.self="activeItem = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#14b8a6;display:block;margin-bottom:4px">{{ activeItem.sku }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ activeItem.name }}</h2>
            <div class="cell-sub">{{ activeItem.site }}</div>
          </div>
          <button class="close-btn" @click="activeItem = null">✕</button>
        </div>
        <div class="drawer-body">
          <!-- Current Stock -->
          <div style="background:#0d0f14;border:1px solid #1a1e2a;border-radius:8px;padding:16px;margin-bottom:16px;text-align:center">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:6px">Current Stock</div>
            <div style="font-size:36px;font-weight:800" :style="stockColor(activeItem)">{{ activeItem.qty }}</div>
            <div class="mono" style="font-size:12px;color:#4b5563">{{ activeItem.unit }}</div>
          </div>
          <!-- Consume Form -->
          <div style="margin-bottom:18px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:10px">Record Consumption</div>
            <div style="display:flex;flex-direction:column;gap:10px">
              <div class="form-group">
                <label>Quantity Used</label>
                <input v-model="consumeQty" type="number" :placeholder="'Max ' + activeItem.qty" :max="activeItem.qty" />
              </div>
              <div class="form-group">
                <label>Used For / Activity</label>
                <input v-model="consumeNote" type="text" placeholder="e.g. Plastering Floor 4 Block A" />
              </div>
              <button class="btn-primary teal" @click="consumeStock">Record Usage</button>
            </div>
          </div>
          <!-- Delivery History -->
          <div>
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Delivery History</div>
            <div style="display:flex;flex-direction:column;gap:6px">
              <div v-for="d in activeItem.deliveries" :key="d.date"
                style="display:flex;justify-content:space-between;padding:8px 10px;background:#0d0f14;border-radius:8px;align-items:center">
                <div>
                  <div class="cell-main">{{ d.qty }} {{ activeItem.unit }}</div>
                  <div class="cell-sub">{{ d.supplier }}</div>
                </div>
                <div class="cell-date">{{ d.date }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Stock Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>📦 Add Stock Item</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Item Name *</label><input v-model="form.name" type="text" placeholder="e.g. OPC Cement" /></div>
            <div class="form-group"><label>SKU / Code</label><input v-model="form.sku" type="text" placeholder="e.g. MAT-CEM-001" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Category *</label>
              <select v-model="form.category">
                <option value="">Select...</option>
                <option value="materials">Materials</option>
                <option value="mep">MEP</option>
                <option value="safety">Safety</option>
                <option value="tools">Tools</option>
              </select>
            </div>
            <div class="form-group"><label>Unit *</label>
              <select v-model="form.unit">
                <option>Bags</option><option>Tonnes</option><option>Units</option>
                <option>Rolls</option><option>Litres</option><option>Kg</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Opening Qty *</label><input v-model="form.qty" type="number" placeholder="0" /></div>
            <div class="form-group"><label>Reorder Level *</label><input v-model="form.reorderLevel" type="number" placeholder="Min stock before reorder" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Unit Cost (KES)</label><input v-model="form.unitCost" type="number" placeholder="0.00" /></div>
            <div class="form-group"><label>Site *</label>
              <select v-model="form.site">
                <option value="">Select site...</option>
                <option v-for="s in siteOptions" :key="s">{{ s }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary teal" @click="addStock">Add to Inventory</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const search = ref('')
const filterCategory = ref('')
const filterSite = ref('')
const filterLevel = ref('')
const showForm = ref(false)
const activeItem = ref(null)
const consumeQty = ref('')
const consumeNote = ref('')
const siteOptions = ['Nairobi Housing — Phase 1', 'Mombasa Port Road', 'Kisumu Commercial Complex', 'Nakuru Ring Road']
const form = ref({ name: '', sku: '', category: '', unit: 'Units', qty: '', reorderLevel: '', unitCost: '', site: '' })

const inventory = ref([
  { id: 1, name: 'OPC Cement 32.5N',    sku: 'MAT-CEM-001', category: 'materials', site: 'Nairobi Housing — Phase 1',  qty: 45,  reorderLevel: 100, maxStock: 500, unit: 'Bags',   unitCost: 850,   lastDelivery: '2025-02-10', level: 'low',      deliveries: [{ date: '2025-02-10', qty: 200, supplier: 'Bamburi Cement' }, { date: '2025-01-25', qty: 300, supplier: 'Bamburi Cement' }] },
  { id: 2, name: 'Steel Rebar Y16',     sku: 'MAT-STL-002', category: 'materials', site: 'Kisumu Commercial Complex',  qty: 2.5, reorderLevel: 5,   maxStock: 20,  unit: 'Tonnes', unitCost: 64000, lastDelivery: '2025-02-05', level: 'low',      deliveries: [{ date: '2025-02-05', qty: 5, supplier: 'Steel Fabricators' }] },
  { id: 3, name: 'Binding Wire',        sku: 'MAT-WIR-003', category: 'materials', site: 'Kisumu Commercial Complex',  qty: 3,   reorderLevel: 10,  maxStock: 50,  unit: 'Rolls',  unitCost: 1200,  lastDelivery: '2025-01-20', level: 'critical', deliveries: [{ date: '2025-01-20', qty: 20, supplier: 'Hardware Depot' }] },
  { id: 4, name: 'Safety Helmets',      sku: 'SAF-HLM-001', category: 'safety',    site: 'All Sites',                  qty: 8,   reorderLevel: 20,  maxStock: 80,  unit: 'Units',  unitCost: 850,   lastDelivery: '2025-01-15', level: 'critical', deliveries: [{ date: '2025-01-15', qty: 30, supplier: 'Safety Pro Kenya' }] },
  { id: 5, name: 'Electrical Cable 2.5mm', sku: 'MEP-CAB-001', category: 'mep',   site: 'Mombasa Port Road',          qty: 18,  reorderLevel: 10,  maxStock: 50,  unit: 'Rolls',  unitCost: 4400,  lastDelivery: '2025-02-08', level: 'ok',       deliveries: [{ date: '2025-02-08', qty: 20, supplier: 'East Africa Cables' }] },
  { id: 6, name: 'Ballast (20mm)',      sku: 'MAT-BLS-001', category: 'materials', site: 'Nakuru Ring Road',           qty: 280, reorderLevel: 100, maxStock: 500, unit: 'Tonnes', unitCost: 1800,  lastDelivery: '2025-02-14', level: 'ok',       deliveries: [{ date: '2025-02-14', qty: 150, supplier: 'Nakuru Aggregates' }] },
  { id: 7, name: 'Nails 4" Round',     sku: 'TOL-NAL-001', category: 'tools',     site: 'Nairobi Housing — Phase 1',  qty: 12,  reorderLevel: 50,  maxStock: 200, unit: 'Kg',     unitCost: 180,   lastDelivery: '2025-01-28', level: 'low',      deliveries: [{ date: '2025-01-28', qty: 50, supplier: 'Hardware Depot' }] },
  { id: 8, name: 'Plywood 18mm 8x4',   sku: 'MAT-PLY-001', category: 'materials', site: 'Nairobi Housing — Phase 1',  qty: 35,  reorderLevel: 20,  maxStock: 100, unit: 'Sheets', unitCost: 3200,  lastDelivery: '2025-02-12', level: 'ok',       deliveries: [{ date: '2025-02-12', qty: 50, supplier: 'Timber Depot' }] },
])

const criticalItems      = computed(() => inventory.value.filter(i => i.level === 'critical').length)
const lowItems           = computed(() => inventory.value.filter(i => i.level === 'low').length)
const deliveriesThisWeek = ref(7)
const totalStockValue    = computed(() => {
  const sum = inventory.value.reduce((a, b) => a + (b.qty * b.unitCost), 0)
  return sum >= 1000000 ? (sum / 1000000).toFixed(1) + 'M' : (sum / 1000).toFixed(0) + 'K'
})

const filteredInventory = computed(() => inventory.value.filter(i =>
  (!search.value || i.name.toLowerCase().includes(search.value.toLowerCase()) || i.sku.includes(search.value))
  && (!filterCategory.value || i.category === filterCategory.value)
  && (!filterSite.value || i.site === filterSite.value)
  && (!filterLevel.value || i.level === filterLevel.value)
))

function stockColor(item) { return item.level === 'critical' ? 'color:#ef4444' : item.level === 'low' ? 'color:#f59e0b' : 'color:#22c55e' }
function stockFill(item)  { return item.level === 'critical' ? 'red' : item.level === 'low' ? 'amber' : 'green' }

function consumeStock() {
  if (!consumeQty.value || Number(consumeQty.value) > activeItem.value.qty) return
  activeItem.value.qty -= Number(consumeQty.value)
  if (activeItem.value.qty <= 0)            activeItem.value.level = 'critical'
  else if (activeItem.value.qty < activeItem.value.reorderLevel) activeItem.value.level = 'low'
  consumeQty.value = ''
  consumeNote.value = ''
  activeItem.value = null
}

function createReorder(item) { alert(`Reorder request created for ${item.name}`) }

function addStock() {
  inventory.value.push({
    id: Date.now(), ...form.value,
    qty: Number(form.value.qty), reorderLevel: Number(form.value.reorderLevel),
    maxStock: Number(form.value.qty) * 3, unitCost: Number(form.value.unitCost),
    lastDelivery: new Date().toISOString().split('T')[0],
    level: Number(form.value.qty) <= Number(form.value.reorderLevel) ? 'low' : 'ok',
    deliveries: []
  })
  showForm.value = false
  form.value = { name: '', sku: '', category: '', unit: 'Units', qty: '', reorderLevel: '', unitCost: '', site: '' }
}
</script>

<style scoped>
@import '/src/assets/procurement.css';
.cat-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 2px 8px; border-radius: 3px; text-transform: uppercase; }
.cat-badge.materials { background: #1f1a08; color: #f5a623; }
.cat-badge.mep       { background: #0d1a2e; color: #3b82f6; }
.cat-badge.safety    { background: #200e0e; color: #ef4444; }
.cat-badge.tools     { background: #1a0d2e; color: #a855f7; }
.cat-badge.equipment { background: #0d2010; color: #22c55e; }
.critical-row { background: #100808 !important; }
.reorder-btn { background: none; border: 1px solid #f5a623; color: #f5a623; padding: 4px 10px; border-radius: 5px; font-size: 11px; cursor: pointer; font-family: 'Syne', sans-serif; white-space: nowrap; }
.use-btn     { background: none; border: 1px solid #14b8a6; color: #14b8a6; padding: 4px 10px; border-radius: 5px; font-size: 11px; cursor: pointer; font-family: 'Syne', sans-serif; }
</style>