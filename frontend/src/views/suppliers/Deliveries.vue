<template>
  <div class="suppliers-page">
    <div class="page-header">
      <div>
        <span class="page-tag green">SUPPLIERS · DELIVERIES</span>
        <h1>Deliveries</h1>
        <p class="page-sub">Goods received notes (GRNs), delivery tracking and inspection records</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary green" @click="showForm=true">+ Record Delivery</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card green">
        <div class="stat-val">{{ deliveries.filter(d=>d.status==='accepted').length }}</div>
        <div class="stat-label">Accepted</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">{{ deliveries.filter(d=>d.status==='partial').length }}</div>
        <div class="stat-label">Partial / Pending</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-val">{{ deliveries.filter(d=>d.status==='rejected').length }}</div>
        <div class="stat-label">Rejected</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ deliveries.filter(d=>d.status==='in-transit').length }}</div>
        <div class="stat-label">In Transit</div>
      </div>
      <div class="stat-card teal">
        <div class="stat-val">{{ deliveries.length }}</div>
        <div class="stat-label">Total GRNs</div>
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
        <input v-model="search" class="search-input" placeholder="Search GRN, supplier or site..." />
      </div>
      <select v-model="filterSite" class="filter-select">
        <option value="">All Sites</option>
        <option v-for="s in siteOptions" :key="s">{{ s }}</option>
      </select>
      <input v-model="filterDate" type="date" class="filter-select" />
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>GRN No.</th><th>PO Ref</th><th>Supplier</th><th>Items Delivered</th>
            <th>Site</th><th>Received By</th><th>Date</th>
            <th>Qty Ordered</th><th>Qty Received</th><th>Condition</th><th>Status</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in filteredDeliveries" :key="d.id" class="table-row">
            <td class="cell-ref" style="color:#22c55e">{{ d.grn }}</td>
            <td class="cell-ref" style="color:#f5a623">{{ d.poRef }}</td>
            <td>
              <div style="display:flex;align-items:center;gap:8px">
                <div class="s-avatar" style="width:28px;height:28px;font-size:11px">{{ d.supplier[0] }}</div>
                <div class="cell-main">{{ d.supplier }}</div>
              </div>
            </td>
            <td>
              <div class="cell-main">{{ d.description }}</div>
              <div class="cell-sub">{{ d.items.length }} item{{ d.items.length>1?'s':'' }}</div>
            </td>
            <td class="cell-muted" style="font-size:11px">{{ d.site }}</td>
            <td>
              <div class="cell-main">{{ d.receivedBy }}</div>
              <div class="cell-sub">{{ d.receiverRole }}</div>
            </td>
            <td class="cell-date">{{ d.date }}</td>
            <td class="mono" style="font-size:12px;color:#6b7280;text-align:center">{{ d.qtyOrdered }}</td>
            <td class="mono" style="font-size:12px;font-weight:700;text-align:center" :style="d.qtyReceived<d.qtyOrdered?'color:#f59e0b':'color:#22c55e'">{{ d.qtyReceived }}</td>
            <td><span class="cond-badge" :class="d.condition">{{ d.condition }}</span></td>
            <td><span class="status-badge" :class="d.status">{{ d.status }}</span></td>
            <td><button class="btn-view" @click="active=d">View</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drawer -->
    <div class="drawer-overlay" v-if="active" @click.self="active=null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#22c55e;display:block;margin-bottom:4px">{{ active.grn }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ active.supplier }}</h2>
            <div class="cell-sub">{{ active.site }} · {{ active.date }}</div>
          </div>
          <button class="close-btn" @click="active=null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item"><span class="dlbl">PO Reference</span><span class="dval" style="color:#f5a623">{{ active.poRef }}</span></div>
            <div class="detail-item"><span class="dlbl">Received By</span><span class="dval">{{ active.receivedBy }}</span></div>
            <div class="detail-item"><span class="dlbl">Date Received</span><span class="dval">{{ active.date }}</span></div>
            <div class="detail-item"><span class="dlbl">Condition</span><span class="dval"><span class="cond-badge" :class="active.condition">{{ active.condition }}</span></span></div>
            <div class="detail-item"><span class="dlbl">Qty Ordered</span><span class="dval">{{ active.qtyOrdered }}</span></div>
            <div class="detail-item"><span class="dlbl">Qty Received</span><span class="dval" :style="active.qtyReceived<active.qtyOrdered?'color:#f59e0b;font-weight:700':'color:#22c55e;font-weight:700'">{{ active.qtyReceived }}</span></div>
          </div>
          <!-- Items -->
          <div style="margin-bottom:14px">
            <div class="dlbl" style="margin-bottom:8px">Items Received</div>
            <div style="display:flex;flex-direction:column;gap:6px">
              <div v-for="item in active.items" :key="item.name"
                style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;background:#0d0f14;border-radius:8px">
                <div>
                  <div class="cell-main">{{ item.name }}</div>
                  <div class="cell-sub">Ordered: {{ item.ordered }} · Received: {{ item.received }} {{ item.unit }}</div>
                </div>
                <span class="cond-badge" :class="item.condition">{{ item.condition }}</span>
              </div>
            </div>
          </div>
          <!-- Inspection Notes -->
          <div v-if="active.inspectionNotes" style="background:#0d0f14;border:1px solid #1a1e2a;border-radius:8px;padding:12px;margin-bottom:14px">
            <div class="dlbl" style="margin-bottom:6px">Inspection Notes</div>
            <p style="font-size:12px;color:#9ca3af;line-height:1.6">{{ active.inspectionNotes }}</p>
          </div>
          <div v-if="active.status==='rejected'" style="background:#1f0808;border:1px solid #7f1d1d;border-radius:8px;padding:12px;margin-bottom:14px">
            <div class="dlbl" style="color:#ef4444;margin-bottom:6px">Rejection Reason</div>
            <p style="font-size:12px;color:#f87171">{{ active.rejectionReason }}</p>
          </div>
          <button class="btn-primary green" style="width:100%" @click="active=null">🖨️ Print GRN</button>
        </div>
      </div>
    </div>

    <!-- Record Delivery Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm=false">
      <div class="modal">
        <div class="modal-header">
          <h2>📦 Record Delivery (GRN)</h2>
          <button class="close-btn" @click="showForm=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>PO Reference *</label><input v-model="form.poRef" placeholder="LPO-2025-XXX" /></div>
            <div class="form-group"><label>Supplier *</label>
              <select v-model="form.supplier"><option value="">Select...</option><option v-for="s in supplierNames" :key="s">{{ s }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Site *</label>
              <select v-model="form.site"><option value="">Select...</option><option v-for="s in siteOptions" :key="s">{{ s }}</option></select>
            </div>
            <div class="form-group"><label>Date Received *</label><input type="date" v-model="form.date" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Qty Ordered</label><input type="number" v-model="form.qtyOrdered" /></div>
            <div class="form-group"><label>Qty Received *</label><input type="number" v-model="form.qtyReceived" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Condition *</label>
              <select v-model="form.condition"><option value="good">Good</option><option value="damaged">Damaged</option><option value="mixed">Mixed</option></select>
            </div>
            <div class="form-group"><label>Received By *</label><input v-model="form.receivedBy" placeholder="Full name" /></div>
          </div>
          <div class="form-group full"><label>Description</label><input v-model="form.description" placeholder="Brief description of goods" /></div>
          <div class="form-group full"><label>Inspection Notes</label><textarea v-model="form.inspectionNotes" rows="2" placeholder="Quality observations..."></textarea></div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm=false">Cancel</button>
          <button class="btn-primary green" @click="submitGRN">Submit GRN</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const activeTab = ref('all')
const search = ref('')
const filterSite = ref('')
const filterDate = ref('')
const showForm = ref(false)
const active = ref(null)
const siteOptions = ['Nairobi Housing — Phase 1','Mombasa Port Road','Kisumu Commercial Complex','Nakuru Ring Road']
const supplierNames = ['Bamburi Cement Ltd','Steel Fabricators Ltd','East Africa Cables','Nakuru Plant Hire','Safety Pro Kenya']
const form = ref({ poRef:'', supplier:'', site:'', date:'', qtyOrdered:'', qtyReceived:'', condition:'good', receivedBy:'', description:'', inspectionNotes:'' })

const deliveries = ref([
  { id:1, grn:'GRN-2025-018', poRef:'LPO-2025-022', supplier:'Bamburi Cement Ltd',    description:'OPC Cement 200 Bags',          site:'Nairobi Housing — Phase 1', receivedBy:'Eng. Kariuki', receiverRole:'Site Engineer', date:'2025-02-20', qtyOrdered:200, qtyReceived:200, condition:'good',    status:'accepted',  inspectionNotes:'All bags intact. Checked by lab — strength OK.', rejectionReason:null, items:[{name:'OPC Cement 32.5N',ordered:200,received:200,unit:'Bags',condition:'good'}] },
  { id:2, grn:'GRN-2025-017', poRef:'LPO-2025-021', supplier:'East Africa Cables',    description:'Electrical Cable Rolls x12',   site:'Mombasa Port Road',         receivedBy:'Eng. Oduya',   receiverRole:'RE',            date:'2025-02-18', qtyOrdered:20,  qtyReceived:12,  condition:'good',    status:'partial',   inspectionNotes:'Remaining 8 rolls expected 28 Feb.', rejectionReason:null, items:[{name:'2.5mm Cable Rolls',ordered:12,received:12,unit:'Rolls',condition:'good'},{name:'3-Phase Cable',ordered:4,received:0,unit:'Rolls',condition:'pending'}] },
  { id:3, grn:'GRN-2025-016', poRef:'LPO-2025-020', supplier:'Nakuru Plant Hire',     description:'CAT 320 Excavator + Operator', site:'Nakuru Ring Road',          receivedBy:'Eng. Mwangi',  receiverRole:'Site Engineer', date:'2025-02-15', qtyOrdered:14,  qtyReceived:14,  condition:'good',    status:'accepted',  inspectionNotes:'Machine in good working order. Operator certified.', rejectionReason:null, items:[{name:'CAT 320 Excavator',ordered:14,received:14,unit:'Days',condition:'good'}] },
  { id:4, grn:'GRN-2025-015', poRef:'LPO-2025-018', supplier:'Bamburi Cement Ltd',    description:'OPC Cement 500 Bags',          site:'Kisumu Commercial Complex', receivedBy:'Eng. Achieng', receiverRole:'Site Engineer', date:'2025-02-06', qtyOrdered:500, qtyReceived:480, condition:'mixed',   status:'partial',   inspectionNotes:'20 bags found torn on arrival. Supplier to replace.', rejectionReason:null, items:[{name:'OPC Cement 32.5N',ordered:500,received:480,unit:'Bags',condition:'mixed'}] },
  { id:5, grn:'GRN-2025-014', poRef:'LPO-2025-017', supplier:'Steel Fabricators Ltd', description:'Rebar Y12 2 Tonnes',           site:'Nairobi Housing — Phase 1', receivedBy:'Eng. Kariuki', receiverRole:'Site Engineer', date:'2025-01-30', qtyOrdered:2,   qtyReceived:2,   condition:'damaged', status:'rejected',  inspectionNotes:'Severe surface rust observed.', rejectionReason:'Material failed site inspection — excessive corrosion. Returned to supplier.', items:[{name:'Rebar Y12mm',ordered:2,received:2,unit:'Tonnes',condition:'damaged'}] },
  { id:6, grn:'GRN-2025-013', poRef:'LPO-2025-016', supplier:'Safety Pro Kenya',      description:'PPE Sets — 30 Units',          site:'All Sites',                 receivedBy:'Alice Wanjiku',receiverRole:'Safety Officer', date:'2025-01-25', qtyOrdered:30,  qtyReceived:30,  condition:'good',    status:'accepted',  inspectionNotes:'All items within spec. KEBS marks verified.', rejectionReason:null, items:[{name:'Safety Helmets',ordered:30,received:30,unit:'Units',condition:'good'},{name:'Reflector Vests',ordered:30,received:30,unit:'Units',condition:'good'}] },
])

const tabs = computed(() => [
  {key:'all',       label:'All',        count: deliveries.value.length},
  {key:'in-transit',label:'In Transit', count: deliveries.value.filter(d=>d.status==='in-transit').length},
  {key:'partial',   label:'Partial',    count: deliveries.value.filter(d=>d.status==='partial').length},
  {key:'accepted',  label:'Accepted',   count: deliveries.value.filter(d=>d.status==='accepted').length},
  {key:'rejected',  label:'Rejected',   count: deliveries.value.filter(d=>d.status==='rejected').length},
])

const filteredDeliveries = computed(() => deliveries.value.filter(d =>
  (activeTab.value==='all' || d.status===activeTab.value)
  && (!search.value || d.grn.includes(search.value) || d.supplier.toLowerCase().includes(search.value.toLowerCase()) || d.site.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterSite.value || d.site===filterSite.value)
  && (!filterDate.value || d.date===filterDate.value)
))

function submitGRN() {
  const n = deliveries.value.length+1
  deliveries.value.unshift({ id:Date.now(), grn:`GRN-2025-0${n<10?'0':''+(n)}`, ...form.value, qtyOrdered:Number(form.value.qtyOrdered), qtyReceived:Number(form.value.qtyReceived), receiverRole:'Site Engineer', status: Number(form.value.qtyReceived) < Number(form.value.qtyOrdered)?'partial':form.value.condition==='damaged'?'rejected':'accepted', rejectionReason:null, items:[] })
  showForm.value=false
  form.value = { poRef:'', supplier:'', site:'', date:'', qtyOrdered:'', qtyReceived:'', condition:'good', receivedBy:'', description:'', inspectionNotes:'' }
}
</script>

<style scoped>
@import '/src/assets/suppliers.css';
.cond-badge { font-family:'DM Mono',monospace; font-size:9px; padding:3px 8px; border-radius:4px; text-transform:uppercase; }
.cond-badge.good    { background:#0d2818; color:#22c55e; }
.cond-badge.mixed   { background:#1f1a08; color:#f59e0b; }
.cond-badge.damaged { background:#200e0e; color:#ef4444; }
.cond-badge.pending { background:#1a1e2a; color:#9ca3af; }
</style>