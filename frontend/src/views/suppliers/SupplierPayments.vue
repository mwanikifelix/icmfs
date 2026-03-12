<template>
  <div class="suppliers-page">
    <div class="page-header">
      <div>
        <span class="page-tag rose">SUPPLIERS · PAYMENTS</span>
        <h1>Supplier Payments</h1>
        <p class="page-sub">EFT, RTGS and cheque payments disbursed to suppliers</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary rose" @click="showForm=true">+ New Payment</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card rose">
        <div class="stat-val">KES {{ totalPaid }}</div>
        <div class="stat-label">Total Paid (Feb 2025)</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">KES {{ totalPending }}</div>
        <div class="stat-label">Pending Disbursement</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">{{ payments.filter(p=>p.status==='completed').length }}</div>
        <div class="stat-label">Completed Payments</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ payments.filter(p=>p.status==='processing').length }}</div>
        <div class="stat-label">Processing</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-val">{{ payments.filter(p=>p.status==='failed').length }}</div>
        <div class="stat-label">Failed</div>
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
        <input v-model="search" class="search-input" placeholder="Search payment ref or supplier..." />
      </div>
      <select v-model="filterSupplier" class="filter-select">
        <option value="">All Suppliers</option>
        <option v-for="s in supplierNames" :key="s">{{ s }}</option>
      </select>
      <select v-model="filterMethod" class="filter-select">
        <option value="">All Methods</option>
        <option value="EFT">EFT</option>
        <option value="RTGS">RTGS</option>
        <option value="Cheque">Cheque</option>
      </select>
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Payment Ref</th><th>Supplier</th><th>Invoice No.</th>
            <th>Method</th><th>Bank</th><th>Account No.</th>
            <th>Amount (KES)</th><th>Initiated By</th><th>Date</th>
            <th>Approval</th><th>Status</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filteredPayments" :key="p.id" class="table-row">
            <td class="cell-ref" style="color:#f43f5e">{{ p.ref }}</td>
            <td>
              <div style="display:flex;align-items:center;gap:8px">
                <div class="s-avatar" style="width:28px;height:28px;font-size:11px">{{ p.supplier[0] }}</div>
                <div>
                  <div class="cell-main">{{ p.supplier }}</div>
                  <div class="cell-sub">{{ p.accountName }}</div>
                </div>
              </div>
            </td>
            <td class="cell-ref" style="color:#a855f7">{{ p.invoiceNo }}</td>
            <td><span class="method-badge" :class="p.method.toLowerCase()">{{ p.method }}</span></td>
            <td class="cell-muted" style="font-size:11px">{{ p.bank }}</td>
            <td class="cell-ref" style="color:#9ca3af">{{ p.accountNo }}</td>
            <td class="cell-amount" style="color:#f43f5e">{{ p.amount.toLocaleString() }}</td>
            <td>
              <div class="cell-main">{{ p.initiatedBy }}</div>
              <div class="cell-sub">{{ p.role }}</div>
            </td>
            <td class="cell-date">{{ p.date }}</td>
            <td>
              <div class="trail-mini">
                <div v-for="a in p.approvals" :key="a.role" class="trail-step-mini" :class="a.status">
                  <div class="trail-dot-mini"></div>
                  <span style="font-size:9px;font-family:'DM Mono',monospace;color:#6b7280">{{ a.role }}</span>
                </div>
              </div>
            </td>
            <td><span class="status-badge" :class="p.status">{{ p.status }}</span></td>
            <td><button class="btn-view" @click="active=p">View</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drawer -->
    <div class="drawer-overlay" v-if="active" @click.self="active=null">
      <div class="drawer">
        <div class="drawer-header">
          <div>
            <span class="mono" style="font-size:10px;color:#f43f5e;display:block;margin-bottom:4px">{{ active.ref }}</span>
            <h2 style="font-size:16px;font-weight:700">{{ active.supplier }}</h2>
            <div class="cell-sub">{{ active.accountName }} · {{ active.bank }}</div>
          </div>
          <button class="close-btn" @click="active=null">✕</button>
        </div>
        <div class="drawer-body">
          <!-- Amount hero -->
          <div style="background:#0d0f14;border:1px solid #2a2f3e;border-radius:10px;padding:16px;text-align:center;margin-bottom:18px">
            <div class="dlbl" style="margin-bottom:6px">Payment Amount</div>
            <div style="font-size:32px;font-weight:800;color:#f43f5e">KES {{ active.amount.toLocaleString() }}</div>
            <span class="status-badge" :class="active.status" style="margin-top:8px;display:inline-block">{{ active.status }}</span>
          </div>
          <div class="detail-grid">
            <div class="detail-item"><span class="dlbl">Invoice No.</span><span class="dval" style="color:#a855f7">{{ active.invoiceNo }}</span></div>
            <div class="detail-item"><span class="dlbl">Payment Method</span><span class="dval"><span class="method-badge" :class="active.method.toLowerCase()">{{ active.method }}</span></span></div>
            <div class="detail-item"><span class="dlbl">Bank</span><span class="dval">{{ active.bank }}</span></div>
            <div class="detail-item"><span class="dlbl">Account No.</span><span class="dval mono">{{ active.accountNo }}</span></div>
            <div class="detail-item"><span class="dlbl">Date</span><span class="dval">{{ active.date }}</span></div>
            <div class="detail-item"><span class="dlbl">Transaction ID</span><span class="dval mono" style="color:#22c55e">{{ active.txnId || '—' }}</span></div>
            <div class="detail-item"><span class="dlbl">Initiated By</span><span class="dval">{{ active.initiatedBy }}</span></div>
            <div class="detail-item"><span class="dlbl">Role</span><span class="dval">{{ active.role }}</span></div>
          </div>
          <!-- Approval trail -->
          <div style="margin-bottom:16px">
            <div class="dlbl" style="margin-bottom:10px">Approval Trail</div>
            <div style="display:flex;flex-direction:column;gap:6px">
              <div v-for="a in active.approvals" :key="a.role"
                style="display:flex;align-items:center;gap:10px;padding:10px;background:#0d0f14;border-radius:8px">
                <div style="width:10px;height:10px;border-radius:50%;flex-shrink:0"
                  :style="a.status==='approved'?'background:#22c55e':a.status==='pending'?'background:#f59e0b':'background:#ef4444'"></div>
                <div style="flex:1">
                  <div class="cell-main">{{ a.role }}</div>
                  <div class="cell-sub">{{ a.name || 'Awaiting' }}</div>
                </div>
                <span class="status-badge" :class="a.status">{{ a.status }}</span>
              </div>
            </div>
          </div>
          <div v-if="active.notes" style="background:#0d0f14;border-radius:8px;padding:12px;font-size:12px;color:#9ca3af;line-height:1.6;margin-bottom:14px">
            📝 {{ active.notes }}
          </div>
          <div v-if="active.status==='processing'" style="display:flex;gap:8px">
            <button class="btn-primary rose" style="flex:1" @click="active=null">✓ Confirm Payment</button>
            <button class="btn-ghost" style="flex:1" @click="active=null">✗ Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- New Payment Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm=false">
      <div class="modal">
        <div class="modal-header">
          <h2>💳 New Supplier Payment</h2>
          <button class="close-btn" @click="showForm=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Supplier *</label>
              <select v-model="form.supplier"><option value="">Select...</option><option v-for="s in supplierNames" :key="s">{{ s }}</option></select>
            </div>
            <div class="form-group"><label>Invoice No. *</label><input v-model="form.invoiceNo" placeholder="INV-XXXX" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Amount (KES) *</label><input type="number" v-model="form.amount" placeholder="0.00" /></div>
            <div class="form-group"><label>Payment Method *</label>
              <select v-model="form.method"><option value="EFT">EFT</option><option value="RTGS">RTGS</option><option value="Cheque">Cheque</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Bank *</label>
              <select v-model="form.bank"><option value="">Select...</option><option v-for="b in banks" :key="b">{{ b }}</option></select>
            </div>
            <div class="form-group"><label>Account No. *</label><input v-model="form.accountNo" placeholder="0000000000" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Account Name *</label><input v-model="form.accountName" placeholder="Company Ltd" /></div>
            <div class="form-group"><label>Payment Date *</label><input type="date" v-model="form.date" /></div>
          </div>
          <div class="form-group full"><label>Notes</label><textarea v-model="form.notes" rows="2" placeholder="Payment reference or notes..."></textarea></div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm=false">Cancel</button>
          <button class="btn-primary rose" @click="submitPayment">Submit Payment</button>
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
const filterMethod = ref('')
const showForm = ref(false)
const active = ref(null)
const supplierNames = ['Bamburi Cement Ltd','Steel Fabricators Ltd','East Africa Cables','Nakuru Plant Hire','Safety Pro Kenya']
const banks = ['KCB Bank','Equity Bank','Co-operative Bank','NCBA Bank','Standard Chartered','Absa Bank','Stanbic Bank']
const form = ref({ supplier:'', invoiceNo:'', amount:'', method:'EFT', bank:'', accountNo:'', accountName:'', date:'', notes:'' })

const payments = ref([
  { id:1, ref:'PMT-2025-031', supplier:'Nakuru Plant Hire',     invoiceNo:'INV-NPH-2025-019', method:'EFT',    bank:'NCBA Bank',   accountNo:'4567890123', accountName:'Nakuru Plant Hire Ltd', amount:208800, initiatedBy:'Alice Wanjiku', role:'Finance Manager', date:'2025-02-16', txnId:'TXN20250216NPH', status:'completed', notes:'Full payment. Inv total incl. VAT.', approvals:[{role:'PM',name:'Peter Kamau',status:'approved'},{role:'Finance',name:'Alice Wanjiku',status:'approved'},{role:'Director',name:'Dr. Kariuki',status:'approved'}] },
  { id:2, ref:'PMT-2025-030', supplier:'Safety Pro Kenya',      invoiceNo:'INV-SPK-2025-012', method:'EFT',    bank:'Absa Bank',   accountNo:'6789012345', accountName:'Safety Pro Kenya Ltd', amount:31320,  initiatedBy:'Alice Wanjiku', role:'Finance Manager', date:'2025-02-10', txnId:'TXN20250210SPK', status:'completed', notes:null,                        approvals:[{role:'PM',name:'Peter Kamau',status:'approved'},{role:'Finance',name:'Alice Wanjiku',status:'approved'},{role:'Director',name:'Dr. Kariuki',status:'approved'}] },
  { id:3, ref:'PMT-2025-032', supplier:'Bamburi Cement Ltd',    invoiceNo:'INV-BAM-2025-044', method:'RTGS',   bank:'KCB Bank',    accountNo:'1234567890', accountName:'Bamburi Cement Ltd',   amount:58000,  initiatedBy:'Alice Wanjiku', role:'Finance Manager', date:'2025-02-21', txnId:null,                status:'processing', notes:'Awaiting RTGS confirmation.',    approvals:[{role:'PM',name:'Peter Kamau',status:'approved'},{role:'Finance',name:'Alice Wanjiku',status:'approved'},{role:'Director',name:null,          status:'pending'}]  },
  { id:4, ref:'PMT-2025-029', supplier:'Steel Fabricators Ltd', invoiceNo:'INV-STL-2025-029', method:'EFT',    bank:'Equity Bank', accountNo:'2345678901', accountName:'Steel Fabricators Ltd',amount:371200, initiatedBy:'Alice Wanjiku', role:'Finance Manager', date:'2025-02-18', txnId:null,                status:'processing', notes:'Awaiting director approval.',    approvals:[{role:'PM',name:'Peter Kamau',status:'approved'},{role:'Finance',name:'Alice Wanjiku',status:'approved'},{role:'Director',name:null,          status:'pending'}]  },
  { id:5, ref:'PMT-2025-028', supplier:'Bamburi Cement Ltd',    invoiceNo:'INV-BAM-2025-038', method:'Cheque', bank:'KCB Bank',    accountNo:'1234567890', accountName:'Bamburi Cement Ltd',   amount:139200, initiatedBy:'James Kamau',  role:'Accounts Clerk',  date:'2025-02-07', txnId:null,                status:'failed',     notes:'Cheque bounced — insufficient funds.', approvals:[{role:'PM',name:'Peter Kamau',status:'approved'},{role:'Finance',name:'Alice Wanjiku',status:'approved'},{role:'Director',name:'Dr. Kariuki',status:'approved'}] },
])

const tabs = computed(() => [
  {key:'all',        label:'All',        count: payments.value.length},
  {key:'processing', label:'Processing', count: payments.value.filter(p=>p.status==='processing').length},
  {key:'completed',  label:'Completed',  count: payments.value.filter(p=>p.status==='completed').length},
  {key:'failed',     label:'Failed',     count: payments.value.filter(p=>p.status==='failed').length},
])

const filteredPayments = computed(() => payments.value.filter(p =>
  (activeTab.value==='all' || p.status===activeTab.value)
  && (!search.value || p.ref.includes(search.value) || p.supplier.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterSupplier.value || p.supplier===filterSupplier.value)
  && (!filterMethod.value || p.method===filterMethod.value)
))

const totalPaid    = computed(() => { const s=payments.value.filter(p=>p.status==='completed').reduce((a,b)=>a+b.amount,0); return s>=1000000?(s/1000000).toFixed(1)+'M':(s/1000).toFixed(0)+'K' })
const totalPending = computed(() => { const s=payments.value.filter(p=>p.status==='processing').reduce((a,b)=>a+b.amount,0); return s>=1000000?(s/1000000).toFixed(1)+'M':(s/1000).toFixed(0)+'K' })

function submitPayment() {
  payments.value.unshift({ id:Date.now(), ref:`PMT-2025-0${payments.value.length+32}`, ...form.value, amount:Number(form.value.amount), role:'Finance Manager', initiatedBy:'Current User', txnId:null, status:'processing', approvals:[{role:'PM',name:null,status:'pending'},{role:'Finance',name:null,status:'pending'},{role:'Director',name:null,status:'pending'}] })
  showForm.value=false
  form.value = { supplier:'', invoiceNo:'', amount:'', method:'EFT', bank:'', accountNo:'', accountName:'', date:'', notes:'' }
}
</script>

<style scoped>
@import '/src/assets/suppliers.css';
.method-badge { font-family:'DM Mono',monospace; font-size:9px; padding:3px 8px; border-radius:4px; text-transform:uppercase; }
.method-badge.eft    { background:#0d2818; color:#22c55e; }
.method-badge.rtgs   { background:#0d1a2e; color:#3b82f6; }
.method-badge.cheque { background:#1a0d2e; color:#a855f7; }
.trail-mini { display:flex; gap:6px; align-items:center; }
.trail-step-mini { display:flex; align-items:center; gap:3px; }
.trail-dot-mini { width:7px; height:7px; border-radius:50%; }
.trail-step-mini.approved .trail-dot-mini { background:#22c55e; }
.trail-step-mini.pending  .trail-dot-mini { background:#f59e0b; }
.trail-step-mini.rejected .trail-dot-mini { background:#ef4444; }
.btn-view { background:none; border:1px solid #2a2f3e; color:#9ca3af; padding:4px 12px; border-radius:5px; font-size:11px; cursor:pointer; font-family:'Syne',sans-serif; }
.btn-view:hover { border-color:#f43f5e; color:#f43f5e; }
</style>