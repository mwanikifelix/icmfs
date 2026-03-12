<template>
  <div class="procurement-page">
    <div class="page-header">
      <div>
        <span class="page-tag green">PROCUREMENT · SUPPLIERS</span>
        <h1>Supplier Management</h1>
        <p class="page-sub">Registered vendors, performance ratings and contact management</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary green" @click="showForm = true">+ Register Supplier</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card green">
        <div class="stat-val">{{ suppliers.filter(s => s.status === 'active').length }}</div>
        <div class="stat-label">Active Suppliers</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-val">{{ suppliers.filter(s => s.status === 'review').length }}</div>
        <div class="stat-label">Under Review</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ categories.length }}</div>
        <div class="stat-label">Supply Categories</div>
      </div>
      <div class="stat-card teal">
        <div class="stat-val">{{ avgRating.toFixed(1) }}★</div>
        <div class="stat-label">Average Rating</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search supplier name or category..." />
      </div>
      <select v-model="filterCategory" class="filter-select">
        <option value="">All Categories</option>
        <option v-for="c in categories" :key="c">{{ c }}</option>
      </select>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
        <option value="review">Under Review</option>
      </select>
    </div>

    <!-- Supplier Cards -->
    <div class="supplier-grid">
      <div class="supplier-card" v-for="s in filteredSuppliers" :key="s.id" @click="activeSupplier = s">
        <div class="sc-header">
          <div class="sc-avatar">{{ s.name[0] }}</div>
          <div style="flex:1">
            <div style="font-size:14px;font-weight:700;color:#fff">{{ s.name }}</div>
            <div class="cell-sub">{{ s.category }}</div>
          </div>
          <span class="status-badge" :class="s.status">{{ s.status }}</span>
        </div>
        <div class="sc-rating">
          <span class="stars">{{ '★'.repeat(Math.floor(s.rating)) }}{{ s.rating % 1 ? '½' : '' }}</span>
          <span class="mono" style="font-size:11px;color:#9ca3af">{{ s.rating }}/5 · {{ s.totalOrders }} orders</span>
        </div>
        <div class="sc-meta">
          <div class="sc-meta-item"><span>📍</span> {{ s.location }}</div>
          <div class="sc-meta-item"><span>📞</span> {{ s.phone }}</div>
          <div class="sc-meta-item"><span>💰</span> KES {{ (s.totalValue / 1000).toFixed(0) }}K total</div>
          <div class="sc-meta-item"><span>📅</span> Last order: {{ s.lastOrder }}</div>
        </div>
        <div class="sc-tags">
          <span class="sc-tag" v-for="t in s.tags" :key="t">{{ t }}</span>
        </div>
      </div>
    </div>

    <!-- Supplier Detail Drawer -->
    <div class="drawer-overlay" v-if="activeSupplier" @click.self="activeSupplier = null">
      <div class="drawer">
        <div class="drawer-header">
          <div style="display:flex;align-items:center;gap:12px">
            <div class="sc-avatar" style="width:44px;height:44px;font-size:18px">{{ activeSupplier.name[0] }}</div>
            <div>
              <h2 style="font-size:16px;font-weight:700">{{ activeSupplier.name }}</h2>
              <div class="cell-sub">{{ activeSupplier.category }}</div>
            </div>
          </div>
          <button class="close-btn" @click="activeSupplier = null">✕</button>
        </div>
        <div class="drawer-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:18px">
            <div v-for="f in supplierDrawerFields" :key="f.label">
              <div class="cell-sub" style="text-transform:uppercase">{{ f.label }}</div>
              <div style="font-size:13px;color:#e8e4dc;margin-top:4px" :style="f.style||''">{{ f.value }}</div>
            </div>
          </div>
          <!-- Performance -->
          <div style="margin-bottom:16px">
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:10px">Performance Metrics</div>
            <div style="display:flex;flex-direction:column;gap:8px">
              <div v-for="m in activeSupplier.metrics" :key="m.label">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                  <span style="font-size:12px;color:#9ca3af">{{ m.label }}</span>
                  <span class="mono" style="font-size:11px;color:#e8e4dc">{{ m.val }}%</span>
                </div>
                <div class="prog-bar"><div class="prog-fill" :class="m.color" :style="{ width: m.val + '%' }"></div></div>
              </div>
            </div>
          </div>
          <!-- Order History -->
          <div>
            <div class="cell-sub" style="text-transform:uppercase;margin-bottom:8px">Recent Orders</div>
            <div style="display:flex;flex-direction:column;gap:6px">
              <div v-for="o in activeSupplier.orders" :key="o.ref"
                style="display:flex;justify-content:space-between;padding:8px 10px;background:#0d0f14;border-radius:8px;align-items:center">
                <div>
                  <div class="cell-main">{{ o.item }}</div>
                  <div class="cell-sub">{{ o.ref }} · {{ o.date }}</div>
                </div>
                <div style="text-align:right">
                  <div style="font-size:12px;font-weight:700;color:#22c55e">KES {{ o.value.toLocaleString() }}</div>
                  <span class="status-badge" :class="o.status">{{ o.status }}</span>
                </div>
              </div>
            </div>
          </div>
          <div style="margin-top:16px;display:flex;gap:8px">
            <button class="btn-primary green" style="flex:1;text-align:center" @click="activeSupplier = null">📋 New PR to this Supplier</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Register Supplier Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>🤝 Register New Supplier</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Company Name *</label><input v-model="form.name" type="text" placeholder="Company name" /></div>
            <div class="form-group"><label>Category *</label>
              <select v-model="form.category">
                <option value="">Select...</option>
                <option v-for="c in categories" :key="c">{{ c }}</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>KRA PIN *</label><input v-model="form.kra" type="text" placeholder="A0XXXXXXXXX" /></div>
            <div class="form-group"><label>Phone *</label><input v-model="form.phone" type="text" placeholder="07XXXXXXXX" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Email</label><input v-model="form.email" type="email" placeholder="info@company.co.ke" /></div>
            <div class="form-group"><label>Location / County</label><input v-model="form.location" type="text" placeholder="e.g. Nairobi" /></div>
          </div>
          <div class="form-group full"><label>Products / Services Offered</label>
            <textarea v-model="form.products" rows="2" placeholder="e.g. Cement, Sand, Ballast, Timber..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary green" @click="registerSupplier">Register Supplier</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const search = ref('')
const filterCategory = ref('')
const filterStatus = ref('')
const showForm = ref(false)
const activeSupplier = ref(null)
const form = ref({ name: '', category: '', kra: '', phone: '', email: '', location: '', products: '' })
const categories = ['Construction Materials', 'Equipment & Machinery', 'MEP & Electrical', 'Safety Equipment', 'Tools & Hardware', 'Concrete & Aggregates', 'Timber & Joinery']

const suppliers = ref([
  { id: 1, name: 'Bamburi Cement Ltd',      category: 'Construction Materials', location: 'Mombasa',   phone: '0722100200', email: 'orders@bamburi.co.ke', kra: 'A001234567B', status: 'active',   rating: 4.8, totalOrders: 18, lastOrder: '2025-02-15', totalValue: 820000, tags: ['Certified', 'ISO 9001', 'KEBS'], metrics: [{ label: 'On-Time Delivery', val: 94, color: 'green' }, { label: 'Quality Score', val: 96, color: 'green' }, { label: 'Price Competitiveness', val: 82, color: 'blue' }], orders: [{ ref: 'PO-2025-021', item: 'OPC Cement 200 Bags', date: '2025-02-15', value: 50000, status: 'delivered' }, { ref: 'PO-2025-015', item: 'OPC Cement 500 Bags', date: '2025-02-01', value: 125000, status: 'delivered' }] },
  { id: 2, name: 'Steel Fabricators Ltd',   category: 'Construction Materials', location: 'Nairobi',   phone: '0711234567', email: 'sales@steelfab.co.ke',  kra: 'A009876543C', status: 'active',   rating: 4.6, totalOrders: 12, lastOrder: '2025-02-17', totalValue: 650000, tags: ['Certified', 'Local Manufacturer'], metrics: [{ label: 'On-Time Delivery', val: 88, color: 'green' }, { label: 'Quality Score', val: 92, color: 'green' }, { label: 'Price Competitiveness', val: 78, color: 'blue' }], orders: [{ ref: 'PO-2025-022', item: 'Steel Rebar 16mm 5T', date: '2025-02-17', value: 320000, status: 'ordered' }] },
  { id: 3, name: 'East Africa Cables',       category: 'MEP & Electrical',       location: 'Nairobi',   phone: '0733456789', email: 'info@eac.co.ke',       kra: 'A005544332D', status: 'active',   rating: 4.5, totalOrders: 8,  lastOrder: '2025-02-10', totalValue: 320000, tags: ['ISO Certified'], metrics: [{ label: 'On-Time Delivery', val: 90, color: 'green' }, { label: 'Quality Score', val: 89, color: 'green' }, { label: 'Price Competitiveness', val: 85, color: 'blue' }], orders: [{ ref: 'PO-2025-018', item: 'Cable Rolls x20', date: '2025-02-10', value: 88000, status: 'in-transit' }] },
  { id: 4, name: 'Nakuru Plant Hire',        category: 'Equipment & Machinery',  location: 'Nakuru',    phone: '0744567890', email: 'hire@nakuruplant.co.ke',kra: 'A007788990E', status: 'active',   rating: 4.7, totalOrders: 6,  lastOrder: '2025-02-14', totalValue: 480000, tags: ['24/7 Support'], metrics: [{ label: 'Equipment Availability', val: 92, color: 'green' }, { label: 'Maintenance Quality', val: 88, color: 'green' }, { label: 'Price Competitiveness', val: 80, color: 'blue' }], orders: [{ ref: 'PO-2025-020', item: 'Excavator Hire 2 Weeks', date: '2025-02-14', value: 180000, status: 'delivered' }] },
  { id: 5, name: 'Kisumu Aggregates Co.',    category: 'Concrete & Aggregates',  location: 'Kisumu',    phone: '0755678901', email: 'sales@kisumuagg.co.ke', kra: 'A003322110F', status: 'review',   rating: 3.9, totalOrders: 4,  lastOrder: '2025-01-28', totalValue: 180000, tags: ['New Supplier'], metrics: [{ label: 'On-Time Delivery', val: 72, color: 'amber' }, { label: 'Quality Score', val: 76, color: 'amber' }, { label: 'Price Competitiveness', val: 91, color: 'green' }], orders: [{ ref: 'PO-2025-010', item: 'Ballast 20 Loads', date: '2025-01-28', value: 80000, status: 'delivered' }] },
])

const filteredSuppliers = computed(() => suppliers.value.filter(s =>
  (!search.value || s.name.toLowerCase().includes(search.value.toLowerCase()) || s.category.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterCategory.value || s.category === filterCategory.value)
  && (!filterStatus.value || s.status === filterStatus.value)
))

const avgRating = computed(() => suppliers.value.reduce((a, b) => a + b.rating, 0) / suppliers.value.length)

const supplierDrawerFields = computed(() => activeSupplier.value ? [
  { label: 'Category',     value: activeSupplier.value.category  },
  { label: 'Location',     value: activeSupplier.value.location  },
  { label: 'Phone',        value: activeSupplier.value.phone     },
  { label: 'Email',        value: activeSupplier.value.email     },
  { label: 'KRA PIN',      value: activeSupplier.value.kra       },
  { label: 'Rating',       value: activeSupplier.value.rating + '/5 ★', style: 'color:#f5a623;font-weight:700' },
  { label: 'Total Orders', value: activeSupplier.value.totalOrders },
  { label: 'Total Value',  value: 'KES ' + activeSupplier.value.totalValue.toLocaleString(), style: 'color:#22c55e' },
] : [])

function registerSupplier() {
  suppliers.value.unshift({ id: Date.now(), ...form.value, status: 'review', rating: 0, totalOrders: 0, lastOrder: '—', totalValue: 0, tags: ['New Supplier'], metrics: [], orders: [] })
  showForm.value = false
  form.value = { name: '', category: '', kra: '', phone: '', email: '', location: '', products: '' }
}
</script>

<style scoped>
@import '/src/assets/procurement.css';
.supplier-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.supplier-card { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 18px; cursor: pointer; transition: border-color 0.2s; }
.supplier-card:hover { border-color: #22c55e; }
.sc-header { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; }
.sc-avatar { width: 38px; height: 38px; border-radius: 50%; background: #14b8a6; color: #0d0f14; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 14px; flex-shrink: 0; }
.sc-rating { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.stars { color: #f5a623; font-size: 14px; }
.sc-meta { display: flex; flex-direction: column; gap: 4px; margin-bottom: 10px; }
.sc-meta-item { font-size: 11px; color: #6b7280; display: flex; align-items: center; gap: 6px; }
.sc-tags { display: flex; flex-wrap: wrap; gap: 5px; }
.sc-tag { font-size: 10px; font-family: 'DM Mono', monospace; padding: 2px 8px; border-radius: 3px; background: #1a1e2a; color: #9ca3af; }
</style>