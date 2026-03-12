<template>
  <div class="suppliers-page">
    <div class="page-header">
      <div>
        <span class="page-tag amber">SUPPLIERS · PURCHASE ORDERS</span>
        <h1>Purchase Orders</h1>
        <p class="page-sub">Formal LPOs and purchase orders issued to suppliers</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary amber" @click="showForm=true">+ Create PO</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card amber">
        <div class="stat-val">{{ orders.length }}</div>
        <div class="stat-label">Total POs</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ orders.filter(o=>o.status==='sent').length }}</div>
        <div class="stat-label">Sent / Open</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">{{ orders.filter(o=>o.status==='partial').length }}</div>
        <div class="stat-label">Part Delivered</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">{{ orders.filter(o=>o.status==='completed').length }}</div>
        <div class="stat-label">Completed</div>
      </div>
      <div class="stat-card teal">
        <div class="stat-val">KES {{ totalPOValue }}</div>
        <div class="stat-label">Total PO Value</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button v-for="t in tabs" :key="t.key" :class="['tab', activeTab===t.key?'active':'']" @click="activeTab=t.key">
        {{ t.label }} <span class="tab-count">{{ t.count }}</span>
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search PO number or supplier..." />
      </div>
      <select v-model="filterSupplier" class="filter-select">
        <option value="">All Suppliers</option>
        <option v-for="s in supplierNames" :key="s">{{ s }}</option>
      </select>
      <input v-model="filterFrom" type="date" class="filter-select" />
      <input v-model="filterTo"   type="date" class="filter-select" />
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>PO Number</th><th>Supplier</th><th>Description</th><th>Site</th>
            <th>Issue Date</th><th>Delivery Date</th><th>Amount (KES)</th>
            <th>Delivered</th><th>Status</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="o in filteredOrders" :key="o.id" class="table-row">
            <td class="cell-ref" style="color:#f5a623">{{ o.ref }}</td>
            <td>
              <div style="display:flex;align-items:center;gap:8px">
                <div class="s-avatar" style="width:28px;height:28px;font-size:11px">{{ o.supplier[0] }}</div>
                <div class="cell-main">{{ o.supplier }}</div>
              </div>
            </td>
            <td>
              <div class="cell-main">{{ o.description }}</div>
              <div class="cell-sub">{{ o.items.length }} line item{{ o.items.length>1?'s':'' }}</div>
            </td>
            <td class="cell-muted" style="font-size:11px">{{ o.site }}</td>
            <td class="cell-date">{{ o.issueDate }}</td>
            <td class="cell-date" :style="isOverdue(o)?'color:#ef4444':''">{{ o.deliveryDate }}</td>
            <td class="cell-amount" style="color:#f5a623">{{ o.amount.toLocaleString() }}</td>
            <td style="min-width:120px">
              <div class="prog-bar-wrap">
                <div class="prog-bar"><div class="prog-fill" :class="o.deliveredPct===100?'green':o.deliveredPct>0?'amber':'red'" :style="{width:o.deliveredPct+'%'}"></div></div>
                <span class="prog-pct">{{ o.deliveredPct }}%</span>
              </div>
            </td>
            <td><span class="status-badge" :class="o.status">{{ o.status }}</span></td>
            <td><button class="btn-view" @click="active=o">View</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail Drawer -->
    <div class="drawer-overlay" v-if="active" @click.self="active=null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#f5a623;display:block;margin-bottom:4px">{{ active.ref }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ active.supplier }}</h2>
            <div class="cell-sub">{{ active.site }} · {{ active.issueDate }}</div>
          </div>
          <button class="close-btn" @click="active=null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item"><span class="dlbl">Issue Date</span><span class="dval">{{ active.issueDate }}</span></div>
            <div class="detail-item"><span class="dlbl">Delivery Date</span><span class="dval" :style="isOverdue(active)?'color:#ef4444':''">{{ active.deliveryDate }}</span></div>
            <div class="detail-item"><span class="dlbl">Total Amount</span><span class="dval" style="color:#f5a623;font-weight:700">KES {{ active.amount.toLocaleString() }}</span></div>
            <div class="detail-item"><span class="dlbl">Delivery Progress</span><span class="dval">{{ active.deliveredPct }}%</span></div>
          </div>
          <!-- Line Items -->
          <div style="margin-bottom:16px">
            <div class="dlbl" style="margin-bottom:10px">Line Items</div>
            <table style="width:100%;border-collapse:collapse">
              <thead>
                <tr style="border-bottom:1px solid #1e2230">
                  <th style="text-align:left;font-size:9px;font-family:'DM Mono',monospace;color:#4b5563;padding:6px 8px;text-transform:uppercase">Item</th>
                  <th style="text-align:right;font-size:9px;font-family:'DM Mono',monospace;color:#4b5563;padding:6px 8px;text-transform:uppercase">Qty</th>
                  <th style="text-align:right;font-size:9px;font-family:'DM Mono',monospace;color:#4b5563;padding:6px 8px;text-transform:uppercase">Unit (KES)</th>
                  <th style="text-align:right;font-size:9px;font-family:'DM Mono',monospace;color:#4b5563;padding:6px 8px;text-transform:uppercase">Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in active.items" :key="item.name" style="border-bottom:1px solid #1a1e2a">
                  <td style="padding:8px;font-size:12px;color:#e8e4dc">{{ item.name }}</td>
                  <td style="padding:8px;font-size:12px;color:#9ca3af;text-align:right;font-family:'DM Mono',monospace">{{ item.qty }} {{ item.unit }}</td>
                  <td style="padding:8px;font-size:12px;color:#9ca3af;text-align:right;font-family:'DM Mono',monospace">{{ item.unitCost.toLocaleString() }}</td>
                  <td style="padding:8px;font-size:13px;color:#f5a623;font-weight:700;text-align:right">{{ (item.qty*item.unitCost).toLocaleString() }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="active.notes" style="background:#0d0f14;border-radius:8px;padding:12px;font-size:12px;color:#9ca3af;line-height:1.6;margin-bottom:16px">
            📝 {{ active.notes }}
          </div>
          <div style="display:flex;gap:8px">
            <button class="btn-primary amber" style="flex:1" @click="active=null">🖨️ Print LPO</button>
            <button class="btn-ghost" style="flex:1" @click="active=null">✓ Confirm Delivery</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create PO Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm=false">
      <div class="modal">
        <div class="modal-header">
          <h2>📄 Create Purchase Order</h2>
          <button class="close-btn" @click="showForm=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Supplier *</label>
              <select v-model="form.supplier"><option value="">Select...</option><option v-for="s in supplierNames" :key="s">{{ s }}</option></select>
            </div>
            <div class="form-group"><label>Site *</label>
              <select v-model="form.site"><option value="">Select...</option><option v-for="s in siteOptions" :key="s">{{ s }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Issue Date *</label><input type="date" v-model="form.issueDate" /></div>
            <div class="form-group"><label>Required Delivery Date *</label><input type="date" v-model="form.deliveryDate" /></div>
          </div>
          <div class="form-group full"><label>Description / Items *</label>
            <textarea v-model="form.description" rows="3" placeholder="Describe items being ordered..."></textarea>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Total Amount (KES) *</label><input type="number" v-model="form.amount" placeholder="0.00" /></div>
            <div class="form-group"><label>Payment Terms</label>
              <select v-model="form.terms"><option>30 days net</option><option>Advance payment</option><option>On delivery</option><option>60 days net</option></select>
            </div>
          </div>
          <div class="form-group full"><label>Notes</label><textarea v-model="form.notes" rows="2" placeholder="Special instructions..."></textarea></div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm=false">Cancel</button>
          <button class="btn-secondary" @click="createDraft">Save Draft</button>
          <button class="btn-primary amber" @click="createPO">Issue PO</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const activeTab = ref('all')
const search = ref('')
const filterSupplier = ref('')
const filterFrom = ref('')
const filterTo = ref('')
const showForm = ref(false)
const active = ref(null)
const siteOptions = ['Nairobi Housing — Phase 1','Mombasa Port Road','Kisumu Commercial Complex','Nakuru Ring Road']
const supplierNames = ['Bamburi Cement Ltd','Steel Fabricators Ltd','East Africa Cables','Nakuru Plant Hire','Safety Pro Kenya']
const form = ref({ supplier:'', site:'', issueDate:'', deliveryDate:'', description:'', amount:'', terms:'30 days net', notes:'' })

const orders = ref([
  { id:1, ref:'LPO-2025-022', supplier:'Bamburi Cement Ltd',     description:'OPC Cement 200 Bags',            site:'Nairobi Housing — Phase 1', issueDate:'2025-02-15', deliveryDate:'2025-02-20', amount:50000,  deliveredPct:100, status:'completed', notes:'Deliver to Block A site store.', items:[{name:'OPC Cement 32.5N',qty:200,unit:'Bags',unitCost:250}] },
  { id:2, ref:'LPO-2025-023', supplier:'Steel Fabricators Ltd',  description:'Steel Rebar Y16 — 5 Tonnes',     site:'Kisumu Commercial Complex', issueDate:'2025-02-17', deliveryDate:'2025-02-22', amount:320000, deliveredPct:0,   status:'sent',      notes:'Must include test certificates.', items:[{name:'Rebar Y16mm',qty:5,unit:'Tonnes',unitCost:64000}] },
  { id:3, ref:'LPO-2025-021', supplier:'East Africa Cables',     description:'Electrical Cables & Accessories', site:'Mombasa Port Road',         issueDate:'2025-02-10', deliveryDate:'2025-02-18', amount:88000,  deliveredPct:60,  status:'partial',   notes:'Remaining rolls to be delivered by 28 Feb.', items:[{name:'2.5mm Cable Rolls',qty:12,unit:'Rolls',unitCost:4400},{name:'3-Phase Cable',qty:4,unit:'Rolls',unitCost:8200}] },
  { id:4, ref:'LPO-2025-020', supplier:'Nakuru Plant Hire',      description:'Excavator Hire — 2 Weeks',        site:'Nakuru Ring Road',          issueDate:'2025-02-14', deliveryDate:'2025-02-15', amount:180000, deliveredPct:100, status:'completed', notes:'Include operator and fuel.', items:[{name:'CAT 320 Excavator + Operator',qty:14,unit:'Days',unitCost:12857}] },
  { id:5, ref:'LPO-2025-019', supplier:'Safety Pro Kenya',       description:'PPE Sets — 50 Units',             site:'All Sites',                 issueDate:'2025-02-08', deliveryDate:'2025-02-15', amount:45000,  deliveredPct:0,   status:'sent',      notes:'Mixed sizes required.', items:[{name:'Safety Helmet',qty:50,unit:'Units',unitCost:450},{name:'Reflector Vest',qty:50,unit:'Units',unitCost:350},{name:'Safety Boots',qty:20,unit:'Pairs',unitCost:850}] },
  { id:6, ref:'LPO-2025-018', supplier:'Bamburi Cement Ltd',     description:'OPC Cement 500 Bags',             site:'Kisumu Commercial Complex', issueDate:'2025-02-01', deliveryDate:'2025-02-06', amount:125000, deliveredPct:100, status:'completed', notes:null, items:[{name:'OPC Cement 32.5N',qty:500,unit:'Bags',unitCost:250}] },
])

const tabs = computed(() => [
  {key:'all',       label:'All',          count: orders.value.length},
  {key:'sent',      label:'Open',         count: orders.value.filter(o=>o.status==='sent').length},
  {key:'partial',   label:'Part Delivered',count:orders.value.filter(o=>o.status==='partial').length},
  {key:'completed', label:'Completed',    count: orders.value.filter(o=>o.status==='completed').length},
  {key:'draft',     label:'Draft',        count: orders.value.filter(o=>o.status==='draft').length},
])

const filteredOrders = computed(() => orders.value.filter(o =>
  (activeTab.value==='all' || o.status===activeTab.value)
  && (!search.value || o.ref.includes(search.value) || o.supplier.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterSupplier.value || o.supplier===filterSupplier.value)
))

const totalPOValue = computed(() => {
  const s = orders.value.reduce((a,b)=>a+b.amount,0)
  return s>=1000000?(s/1000000).toFixed(1)+'M':(s/1000).toFixed(0)+'K'
})

function isOverdue(o) { return o.status!=='completed' && new Date(o.deliveryDate) < new Date() }

function createDraft() { createPO('draft') }
function createPO(status='sent') {
  orders.value.unshift({ id:Date.now(), ref:`LPO-2025-0${orders.value.length+23}`, ...form.value, amount:Number(form.value.amount), deliveredPct:0, status, items:[] })
  showForm.value=false
  form.value = { supplier:'', site:'', issueDate:'', deliveryDate:'', description:'', amount:'', terms:'30 days net', notes:'' }
}
</script>

<style scoped>
@import '/src/assets/suppliers.css';
</style>