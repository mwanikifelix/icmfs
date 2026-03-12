<template>
  <div class="procurement-page">
    <div class="page-header">
      <div>
        <span class="page-tag blue">PROCUREMENT · PURCHASE REQUESTS</span>
        <h1>Purchase Requests</h1>
        <p class="page-sub">Create, track and approve material and equipment purchase requests</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary blue" @click="showForm = true">+ New Request</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card blue">
        <div class="stat-val">{{ requests.length }}</div>
        <div class="stat-label">Total Requests</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">{{ requests.filter(r => r.status === 'pending').length }}</div>
        <div class="stat-label">Pending Approval</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">{{ requests.filter(r => r.status === 'approved').length }}</div>
        <div class="stat-label">Approved</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-val">{{ requests.filter(r => r.status === 'ordered').length }}</div>
        <div class="stat-label">Ordered</div>
      </div>
      <div class="stat-card teal">
        <div class="stat-val">KES {{ totalValue }}</div>
        <div class="stat-label">Total Value</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.key" :class="['tab', activeTab === tab.key ? 'active' : '']" @click="activeTab = tab.key">
        {{ tab.label }} <span class="tab-count">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search title, ref or site..." />
      </div>
      <select v-model="filterCategory" class="filter-select">
        <option value="">All Categories</option>
        <option value="materials">Materials</option>
        <option value="equipment">Equipment</option>
        <option value="mep">MEP</option>
        <option value="safety">Safety</option>
        <option value="tools">Tools</option>
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
            <th>Ref</th><th>Item / Description</th><th>Category</th><th>Site</th>
            <th>Qty</th><th>Est. Cost (KES)</th><th>Requested By</th>
            <th>Date</th><th>Approval Trail</th><th>Status</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in filteredRequests" :key="r.id" class="table-row">
            <td class="cell-ref" style="color:#3b82f6">{{ r.ref }}</td>
            <td>
              <div class="cell-main">{{ r.title }}</div>
              <div class="cell-sub">{{ r.specs }}</div>
            </td>
            <td><span class="cat-badge" :class="r.category">{{ r.category }}</span></td>
            <td class="cell-muted" style="font-size:11px">{{ r.site }}</td>
            <td class="mono" style="font-size:12px;color:#e8e4dc">{{ r.qty }} {{ r.unit }}</td>
            <td class="cell-amount" style="color:#f5a623">{{ r.cost.toLocaleString() }}</td>
            <td>
              <div class="cell-main">{{ r.requestedBy }}</div>
              <div class="cell-sub">{{ r.role }}</div>
            </td>
            <td class="cell-date">{{ r.date }}</td>
            <td>
              <div class="trail">
                <div class="trail-step" v-for="step in r.trail" :key="step.role" :class="step.status">
                  <div class="trail-dot"></div>
                  <span class="trail-role">{{ step.role }}</span>
                  <span class="trail-txt">{{ step.status }}</span>
                </div>
              </div>
            </td>
            <td><span class="status-badge" :class="r.status">{{ r.status }}</span></td>
            <td>
              <button class="btn-view" @click="activeRequest = r">View</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail Drawer -->
    <div class="drawer-overlay" v-if="activeRequest" @click.self="activeRequest = null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#3b82f6;display:block;margin-bottom:4px">{{ activeRequest.ref }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ activeRequest.title }}</h2>
            <div class="cell-sub">{{ activeRequest.site }} · {{ activeRequest.date }}</div>
          </div>
          <button class="close-btn" @click="activeRequest = null">✕</button>
        </div>
        <div class="drawer-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:18px">
            <div v-for="f in drawerFields" :key="f.label">
              <div class="cell-sub" style="text-transform:uppercase">{{ f.label }}</div>
              <div style="font-size:13px;color:#e8e4dc;margin-top:4px" :style="f.style || ''">{{ f.value }}</div>
            </div>
          </div>
          <div style="margin-bottom:14px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:6px">Justification</div>
            <p style="font-size:13px;color:#9ca3af;line-height:1.6">{{ activeRequest.justification }}</p>
          </div>
          <div style="margin-bottom:14px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Approval Trail</div>
            <div style="display:flex;flex-direction:column;gap:8px">
              <div v-for="step in activeRequest.trail" :key="step.role"
                style="display:flex;align-items:center;gap:10px;padding:10px;background:#0d0f14;border-radius:8px">
                <div class="trail-dot" style="width:10px;height:10px;flex-shrink:0" :class="step.status === 'approved' ? 'bg-green' : step.status === 'pending' ? 'bg-amber' : 'bg-red'"></div>
                <div style="flex:1">
                  <div class="cell-main">{{ step.role }}</div>
                  <div class="cell-sub">{{ step.name || 'Awaiting' }}</div>
                </div>
                <span class="status-badge" :class="step.status">{{ step.status }}</span>
              </div>
            </div>
          </div>
          <div v-if="activeRequest.status === 'pending'" style="display:flex;gap:8px">
            <button class="approve-btn" style="flex:1;text-align:center;padding:10px" @click="approve(activeRequest)">✓ Approve</button>
            <button class="reject-btn"  style="flex:1;text-align:center;padding:10px" @click="activeRequest = null">✕ Reject</button>
          </div>
        </div>
      </div>
    </div>

    <!-- New PR Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>📋 New Purchase Request</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Item / Description *</label>
              <input v-model="form.title" type="text" placeholder="e.g. OPC Cement — 200 bags" />
            </div>
            <div class="form-group">
              <label>Category *</label>
              <select v-model="form.category">
                <option value="">Select...</option>
                <option value="materials">Materials</option>
                <option value="equipment">Equipment</option>
                <option value="mep">MEP</option>
                <option value="safety">Safety</option>
                <option value="tools">Tools</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Quantity *</label>
              <input v-model="form.qty" type="number" placeholder="0" />
            </div>
            <div class="form-group">
              <label>Unit</label>
              <select v-model="form.unit">
                <option>Bags</option><option>Tonnes</option><option>Units</option>
                <option>Rolls</option><option>Litres</option><option>Sets</option><option>Kg</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Estimated Cost (KES) *</label>
              <input v-model="form.cost" type="number" placeholder="0.00" />
            </div>
            <div class="form-group">
              <label>Required By Date *</label>
              <input v-model="form.requiredBy" type="date" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Site *</label>
              <select v-model="form.site">
                <option value="">Select site...</option>
                <option v-for="s in siteOptions" :key="s">{{ s }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Preferred Supplier</label>
              <input v-model="form.supplier" type="text" placeholder="Optional" />
            </div>
          </div>
          <div class="form-group full">
            <label>Specifications</label>
            <input v-model="form.specs" type="text" placeholder="e.g. 32.5N grade, Kenya Bureau of Standards approved" />
          </div>
          <div class="form-group full">
            <label>Justification *</label>
            <textarea v-model="form.justification" rows="3" placeholder="Why is this item needed?"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-secondary" @click="saveDraft">Save Draft</button>
          <button class="btn-primary blue" @click="submitRequest">Submit for Approval</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const activeTab = ref('all')
const search = ref('')
const filterCategory = ref('')
const filterSite = ref('')
const showForm = ref(false)
const activeRequest = ref(null)
const siteOptions = ['Nairobi Housing — Phase 1', 'Mombasa Port Road', 'Kisumu Commercial Complex', 'Nakuru Ring Road']
const form = ref({ title: '', category: '', qty: '', unit: 'Units', cost: '', requiredBy: '', site: '', supplier: '', specs: '', justification: '' })

const requests = ref([
  { id: 1, ref: 'PR-2025-041', title: 'OPC Cement — 500 Bags',         specs: '32.5N grade, KEBS approved',         category: 'materials', site: 'Nairobi Housing — Phase 1',  qty: 500, unit: 'Bags',  cost: 125000, requestedBy: 'Eng. Kariuki', role: 'Site Engineer', date: '2025-02-18', requiredBy: '2025-02-25', status: 'pending',  justification: 'Plastering works for Block A floors 3-5 commencing next week.', trail: [{ role: 'Site Mgr', name: 'Grace Otieno', status: 'approved' }, { role: 'PM', name: 'Peter Kamau', status: 'pending' }] },
  { id: 2, ref: 'PR-2025-040', title: 'Steel Rebar 16mm — 5 Tonnes',   specs: 'Grade Y16, BS4449 standard',          category: 'materials', site: 'Kisumu Commercial Complex',  qty: 5,   unit: 'Tonnes',cost: 320000, requestedBy: 'Eng. Achieng', role: 'Site Engineer', date: '2025-02-17', requiredBy: '2025-02-22', status: 'approved', justification: 'Floor 3 slab reinforcement. LPO issued to Steel Fabricators Ltd.', trail: [{ role: 'Site Mgr', name: 'James Mutua', status: 'approved' }, { role: 'PM', name: 'Peter Kamau', status: 'approved' }] },
  { id: 3, ref: 'PR-2025-039', title: 'Electrical Cable Rolls x20',    specs: '2.5mm twin & earth, armoured',        category: 'mep',       site: 'Mombasa Port Road',          qty: 20,  unit: 'Rolls', cost: 88000,  requestedBy: 'Eng. Oduya',   role: 'RE',            date: '2025-02-16', requiredBy: '2025-02-28', status: 'ordered',  justification: 'Electrical rough-in works for site offices and lighting circuits.', trail: [{ role: 'Site Mgr', name: 'Alice Njeri', status: 'approved' }, { role: 'PM', name: 'Peter Kamau', status: 'approved' }] },
  { id: 4, ref: 'PR-2025-038', title: 'Excavator Hire — 2 Weeks',      specs: 'CAT 320 or equivalent, with operator', category: 'equipment', site: 'Nakuru Ring Road',           qty: 1,   unit: 'Units', cost: 180000, requestedBy: 'Eng. Mwangi',  role: 'Site Engineer', date: '2025-02-15', requiredBy: '2025-02-20', status: 'approved', justification: 'Drainage trench excavation km 4.8 to km 5.4.', trail: [{ role: 'Site Mgr', name: 'Grace Otieno', status: 'approved' }, { role: 'PM', name: 'Peter Kamau', status: 'approved' }] },
  { id: 5, ref: 'PR-2025-037', title: 'Safety Gear Sets — 50',         specs: 'Helmet, vest, gloves, boots',         category: 'safety',    site: 'All Sites',                  qty: 50,  unit: 'Sets',  cost: 45000,  requestedBy: 'Alice Wanjiku', role: 'Safety Officer', date: '2025-02-14', requiredBy: '2025-03-01', status: 'draft',    justification: 'Replenishment of PPE stock across all sites before March influx.', trail: [{ role: 'Site Mgr', name: null, status: 'pending' }, { role: 'PM', name: null, status: 'pending' }] },
])

const tabs = computed(() => [
  { key: 'all',      label: 'All',      count: requests.value.length },
  { key: 'draft',    label: 'Draft',    count: requests.value.filter(r => r.status === 'draft').length    },
  { key: 'pending',  label: 'Pending',  count: requests.value.filter(r => r.status === 'pending').length  },
  { key: 'approved', label: 'Approved', count: requests.value.filter(r => r.status === 'approved').length },
  { key: 'ordered',  label: 'Ordered',  count: requests.value.filter(r => r.status === 'ordered').length  },
])

const filteredRequests = computed(() => requests.value.filter(r =>
  (activeTab.value === 'all' || r.status === activeTab.value)
  && (!search.value || r.title.toLowerCase().includes(search.value.toLowerCase()) || r.ref.includes(search.value))
  && (!filterCategory.value || r.category === filterCategory.value)
  && (!filterSite.value || r.site === filterSite.value)
))

const totalValue = computed(() => {
  const sum = requests.value.reduce((a, b) => a + b.cost, 0)
  return sum >= 1000000 ? (sum / 1000000).toFixed(1) + 'M' : (sum / 1000).toFixed(0) + 'K'
})

const drawerFields = computed(() => activeRequest.value ? [
  { label: 'Category',    value: activeRequest.value.category                          },
  { label: 'Quantity',    value: activeRequest.value.qty + ' ' + activeRequest.value.unit },
  { label: 'Est. Cost',   value: 'KES ' + activeRequest.value.cost.toLocaleString(), style: 'color:#f5a623;font-weight:700' },
  { label: 'Required By', value: activeRequest.value.requiredBy                        },
  { label: 'Requested By',value: activeRequest.value.requestedBy                       },
  { label: 'Specs',       value: activeRequest.value.specs                             },
] : [])

function approve(req) { req.status = 'approved'; activeRequest.value = null }
function saveDraft()    { submitRequest('draft') }
function submitRequest(status = 'pending') {
  requests.value.unshift({ id: Date.now(), ref: `PR-2025-0${requests.value.length + 42}`, ...form.value, qty: Number(form.value.qty), cost: Number(form.value.cost), requestedBy: 'Current User', role: 'Site Engineer', date: new Date().toISOString().split('T')[0], status, trail: [{ role: 'Site Mgr', name: null, status: 'pending' }, { role: 'PM', name: null, status: 'pending' }] })
  showForm.value = false
  form.value = { title: '', category: '', qty: '', unit: 'Units', cost: '', requiredBy: '', site: '', supplier: '', specs: '', justification: '' }
}
</script>

<style scoped>
@import '/src/assets/procurement.css';
.cat-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 2px 8px; border-radius: 3px; text-transform: uppercase; }
.cat-badge.materials { background: #1f1a08; color: #f5a623; }
.cat-badge.equipment { background: #0d2010; color: #22c55e; }
.cat-badge.mep       { background: #0d1a2e; color: #3b82f6; }
.cat-badge.safety    { background: #200e0e; color: #ef4444; }
.cat-badge.tools     { background: #1a0d2e; color: #a855f7; }
.btn-view { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 4px 12px; border-radius: 5px; font-size: 11px; cursor: pointer; font-family: 'Syne', sans-serif; }
.btn-view:hover { border-color: #3b82f6; color: #3b82f6; }
.approve-btn { background: #0d2010; border: 1px solid #22c55e; color: #22c55e; border-radius: 6px; font-family: 'Syne', sans-serif; font-size: 12px; cursor: pointer; font-weight: 600; }
.reject-btn  { background: none; border: 1px solid #2a2f3e; color: #6b7280; border-radius: 6px; font-family: 'Syne', sans-serif; font-size: 12px; cursor: pointer; }
.bg-green { background: #22c55e !important; }
.bg-amber { background: #f59e0b !important; }
.bg-red   { background: #ef4444 !important; }
</style>