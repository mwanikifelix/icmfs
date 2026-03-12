<template>
  <div class="suppliers-page">
    <div class="page-header">
      <div>
        <span class="page-tag purple">SUPPLIERS · INVOICES</span>
        <h1>Supplier Invoices</h1>
        <p class="page-sub">Tax invoices received from suppliers — verification and payment approval</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary purple" @click="showForm=true">+ Upload Invoice</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card warn">
        <div class="stat-val">{{ invoices.filter(i=>i.status==='pending').length }}</div>
        <div class="stat-label">Pending Review</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ invoices.filter(i=>i.status==='approved').length }}</div>
        <div class="stat-label">Approved</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">{{ invoices.filter(i=>i.status==='paid').length }}</div>
        <div class="stat-label">Paid</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-val">{{ invoices.filter(i=>i.status==='overdue').length }}</div>
        <div class="stat-label">Overdue</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-val">KES {{ totalUnpaid }}</div>
        <div class="stat-label">Unpaid Balance</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button v-for="t in tabs" :key="t.key" :class="['tab',activeTab===t.key?'active':'']" @click="activeTab=t.key">
        {{ t.label }} <span class="tab-count">{{ t.count }}</span>
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search invoice no. or supplier..." />
      </div>
      <select v-model="filterSupplier" class="filter-select">
        <option value="">All Suppliers</option>
        <option v-for="s in supplierNames" :key="s">{{ s }}</option>
      </select>
      <select v-model="filterMonth" class="filter-select">
        <option value="">All Months</option>
        <option value="2025-02">Feb 2025</option>
        <option value="2025-01">Jan 2025</option>
        <option value="2024-12">Dec 2024</option>
      </select>
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Invoice No.</th><th>Supplier</th><th>PO Ref</th><th>Description</th>
            <th>Invoice Date</th><th>Due Date</th><th>Amount (KES)</th>
            <th>VAT (KES)</th><th>Total (KES)</th><th>Status</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inv in filteredInvoices" :key="inv.id" class="table-row" :class="inv.status==='overdue'?'overdue-row':''">
            <td class="cell-ref" style="color:#a855f7">{{ inv.invoiceNo }}</td>
            <td>
              <div style="display:flex;align-items:center;gap:8px">
                <div class="s-avatar" style="width:28px;height:28px;font-size:11px">{{ inv.supplier[0] }}</div>
                <div class="cell-main">{{ inv.supplier }}</div>
              </div>
            </td>
            <td class="cell-ref" style="color:#f5a623">{{ inv.poRef }}</td>
            <td>
              <div class="cell-main">{{ inv.description }}</div>
              <div class="cell-sub">{{ inv.grn }}</div>
            </td>
            <td class="cell-date">{{ inv.invoiceDate }}</td>
            <td class="cell-date" :style="inv.status==='overdue'?'color:#ef4444;font-weight:700':''">{{ inv.dueDate }}</td>
            <td class="mono" style="font-size:12px;color:#e8e4dc">{{ inv.amount.toLocaleString() }}</td>
            <td class="mono" style="font-size:12px;color:#a855f7">{{ inv.vat.toLocaleString() }}</td>
            <td class="cell-amount" style="color:#f5a623">{{ (inv.amount+inv.vat).toLocaleString() }}</td>
            <td><span class="status-badge" :class="inv.status">{{ inv.status }}</span></td>
            <td><button class="btn-view" @click="active=inv">Review</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drawer -->
    <div class="drawer-overlay" v-if="active" @click.self="active=null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#a855f7;display:block;margin-bottom:4px">{{ active.invoiceNo }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ active.supplier }}</h2>
            <div class="cell-sub">{{ active.description }}</div>
          </div>
          <button class="close-btn" @click="active=null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item"><span class="dlbl">PO Reference</span><span class="dval" style="color:#f5a623">{{ active.poRef }}</span></div>
            <div class="detail-item"><span class="dlbl">GRN Reference</span><span class="dval" style="color:#22c55e">{{ active.grn }}</span></div>
            <div class="detail-item"><span class="dlbl">Invoice Date</span><span class="dval">{{ active.invoiceDate }}</span></div>
            <div class="detail-item"><span class="dlbl">Due Date</span><span class="dval" :style="active.status==='overdue'?'color:#ef4444':''">{{ active.dueDate }}</span></div>
            <div class="detail-item"><span class="dlbl">Net Amount</span><span class="dval">KES {{ active.amount.toLocaleString() }}</span></div>
            <div class="detail-item"><span class="dlbl">VAT (16%)</span><span class="dval" style="color:#a855f7">KES {{ active.vat.toLocaleString() }}</span></div>
          </div>
          <!-- Total box -->
          <div style="background:#0d0f14;border:1px solid #2a2f3e;border-radius:10px;padding:16px;text-align:center;margin-bottom:18px">
            <div class="dlbl" style="margin-bottom:6px">Invoice Total (incl. VAT)</div>
            <div style="font-size:28px;font-weight:800;color:#f5a623">KES {{ (active.amount+active.vat).toLocaleString() }}</div>
          </div>
          <!-- 3-way match -->
          <div style="margin-bottom:16px">
            <div class="dlbl" style="margin-bottom:10px">3-Way Match Verification</div>
            <div style="display:flex;flex-direction:column;gap:6px">
              <div v-for="check in active.threeWayMatch" :key="check.label"
                style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;background:#0d0f14;border-radius:8px">
                <span style="font-size:12px;color:#9ca3af">{{ check.label }}</span>
                <span :style="check.ok?'color:#22c55e':'color:#ef4444'" style="font-size:13px;font-weight:700">{{ check.ok?'✓ Match':'✗ Mismatch' }}</span>
              </div>
            </div>
          </div>
          <div v-if="active.status==='pending' || active.status==='approved'" style="display:flex;gap:8px">
            <button v-if="active.status==='pending'" class="btn-primary purple" style="flex:1;text-align:center" @click="approveInvoice(active)">✓ Approve</button>
            <button v-if="active.status==='approved'" class="btn-primary green" style="flex:1;text-align:center" @click="active=null">💳 Process Payment</button>
            <button class="btn-ghost" style="flex:1;text-align:center" @click="active=null">✗ Dispute</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Invoice Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm=false">
      <div class="modal">
        <div class="modal-header">
          <h2>📄 Upload Supplier Invoice</h2>
          <button class="close-btn" @click="showForm=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Invoice Number *</label><input v-model="form.invoiceNo" placeholder="INV-XXXX" /></div>
            <div class="form-group"><label>Supplier *</label>
              <select v-model="form.supplier"><option value="">Select...</option><option v-for="s in supplierNames" :key="s">{{ s }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>PO Reference *</label><input v-model="form.poRef" placeholder="LPO-2025-XXX" /></div>
            <div class="form-group"><label>GRN Reference</label><input v-model="form.grn" placeholder="GRN-2025-XXX" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Invoice Date *</label><input type="date" v-model="form.invoiceDate" /></div>
            <div class="form-group"><label>Due Date *</label><input type="date" v-model="form.dueDate" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Net Amount (KES) *</label><input type="number" v-model="form.amount" placeholder="0.00" /></div>
            <div class="form-group"><label>VAT Amount (KES)</label><input type="number" v-model="form.vat" placeholder="Auto: 16%" /></div>
          </div>
          <div class="form-group full"><label>Description</label><input v-model="form.description" placeholder="Brief description of goods/services" /></div>
          <div class="form-group full">
            <label>Attach Invoice (PDF)</label>
            <div style="border:1px dashed #2a2f3e;border-radius:8px;padding:20px;text-align:center;color:#4b5563;font-size:12px;cursor:pointer">
              📎 Click to upload or drag PDF here
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm=false">Cancel</button>
          <button class="btn-primary purple" @click="uploadInvoice">Upload Invoice</button>
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
const filterMonth = ref('')
const showForm = ref(false)
const active = ref(null)
const supplierNames = ['Bamburi Cement Ltd','Steel Fabricators Ltd','East Africa Cables','Nakuru Plant Hire','Safety Pro Kenya']
const form = ref({ invoiceNo:'', supplier:'', poRef:'', grn:'', invoiceDate:'', dueDate:'', amount:'', vat:'', description:'' })

const invoices = ref([
  { id:1, invoiceNo:'INV-BAM-2025-044', supplier:'Bamburi Cement Ltd',    poRef:'LPO-2025-022', grn:'GRN-2025-018', description:'OPC Cement 200 Bags',          invoiceDate:'2025-02-20', dueDate:'2025-03-20', amount:50000,  vat:8000,   status:'approved', threeWayMatch:[{label:'PO vs Invoice Amount',ok:true},{label:'GRN vs Invoice Qty',ok:true},{label:'Supplier Details Match',ok:true}] },
  { id:2, invoiceNo:'INV-EAC-2025-031', supplier:'East Africa Cables',    poRef:'LPO-2025-021', grn:'GRN-2025-017', description:'Electrical Cable Rolls x12',   invoiceDate:'2025-02-18', dueDate:'2025-03-18', amount:52800,  vat:8448,   status:'pending',  threeWayMatch:[{label:'PO vs Invoice Amount',ok:true},{label:'GRN vs Invoice Qty',ok:false},{label:'Supplier Details Match',ok:true}] },
  { id:3, invoiceNo:'INV-NPH-2025-019', supplier:'Nakuru Plant Hire',     poRef:'LPO-2025-020', grn:'GRN-2025-016', description:'CAT 320 Excavator Hire',       invoiceDate:'2025-02-15', dueDate:'2025-03-15', amount:180000, vat:28800,  status:'paid',     threeWayMatch:[{label:'PO vs Invoice Amount',ok:true},{label:'GRN vs Invoice Qty',ok:true},{label:'Supplier Details Match',ok:true}] },
  { id:4, invoiceNo:'INV-BAM-2025-038', supplier:'Bamburi Cement Ltd',    poRef:'LPO-2025-018', grn:'GRN-2025-015', description:'OPC Cement 480 Bags',          invoiceDate:'2025-02-06', dueDate:'2025-02-20', amount:120000, vat:19200,  status:'overdue',  threeWayMatch:[{label:'PO vs Invoice Amount',ok:false},{label:'GRN vs Invoice Qty',ok:false},{label:'Supplier Details Match',ok:true}] },
  { id:5, invoiceNo:'INV-SPK-2025-012', supplier:'Safety Pro Kenya',      poRef:'LPO-2025-016', grn:'GRN-2025-013', description:'PPE Sets 30 Units',            invoiceDate:'2025-01-25', dueDate:'2025-02-24', amount:27000,  vat:4320,   status:'paid',     threeWayMatch:[{label:'PO vs Invoice Amount',ok:true},{label:'GRN vs Invoice Qty',ok:true},{label:'Supplier Details Match',ok:true}] },
  { id:6, invoiceNo:'INV-STL-2025-029', supplier:'Steel Fabricators Ltd', poRef:'LPO-2025-023', grn:'GRN-PENDING',  description:'Steel Rebar Y16 5 Tonnes',    invoiceDate:'2025-02-17', dueDate:'2025-03-19', amount:320000, vat:51200,  status:'pending',  threeWayMatch:[{label:'PO vs Invoice Amount',ok:true},{label:'GRN vs Invoice Qty',ok:false},{label:'Supplier Details Match',ok:true}] },
])

const tabs = computed(() => [
  {key:'all',      label:'All',      count: invoices.value.length},
  {key:'pending',  label:'Pending',  count: invoices.value.filter(i=>i.status==='pending').length},
  {key:'approved', label:'Approved', count: invoices.value.filter(i=>i.status==='approved').length},
  {key:'paid',     label:'Paid',     count: invoices.value.filter(i=>i.status==='paid').length},
  {key:'overdue',  label:'Overdue',  count: invoices.value.filter(i=>i.status==='overdue').length},
])

const filteredInvoices = computed(() => invoices.value.filter(i =>
  (activeTab.value==='all' || i.status===activeTab.value)
  && (!search.value || i.invoiceNo.includes(search.value) || i.supplier.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterSupplier.value || i.supplier===filterSupplier.value)
  && (!filterMonth.value || i.invoiceDate.startsWith(filterMonth.value))
))

const totalUnpaid = computed(() => {
  const s = invoices.value.filter(i=>i.status!=='paid').reduce((a,b)=>a+(b.amount+b.vat),0)
  return s>=1000000?(s/1000000).toFixed(1)+'M':(s/1000).toFixed(0)+'K'
})

function approveInvoice(inv) { inv.status='approved'; active.value=null }

function uploadInvoice() {
  invoices.value.unshift({ id:Date.now(), ...form.value, amount:Number(form.value.amount), vat:Number(form.value.vat)||Math.round(Number(form.value.amount)*0.16), status:'pending', threeWayMatch:[{label:'PO vs Invoice Amount',ok:true},{label:'GRN vs Invoice Qty',ok:true},{label:'Supplier Details Match',ok:true}] })
  showForm.value=false
  form.value = { invoiceNo:'', supplier:'', poRef:'', grn:'', invoiceDate:'', dueDate:'', amount:'', vat:'', description:'' }
}
</script>

<style scoped>
@import '/src/assets/suppliers.css';
.overdue-row { background: #100808 !important; }
.btn-view { background:none; border:1px solid #2a2f3e; color:#9ca3af; padding:4px 12px; border-radius:5px; font-size:11px; cursor:pointer; font-family:'Syne',sans-serif; }
.btn-view:hover { border-color:#a855f7; color:#a855f7; }
</style>