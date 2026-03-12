<template>
  <div class="suppliers-page">
    <div class="page-header">
      <div>
        <span class="page-tag teal">ICMFS · SUPPLIERS</span>
        <h1>Supplier List</h1>
        <p class="page-sub">Master directory of all registered vendors and subcontractors</p>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn-export">📥 Export</button>
        <button class="btn-primary teal" @click="showForm = true">+ Add Supplier</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stat-row">
      <div class="stat-card teal">
        <div class="stat-val">{{ suppliers.length }}</div>
        <div class="stat-label">Total Suppliers</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">{{ suppliers.filter(s=>s.status==='active').length }}</div>
        <div class="stat-label">Active</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-val">{{ suppliers.filter(s=>s.status==='review').length }}</div>
        <div class="stat-label">Under Review</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-val">{{ suppliers.filter(s=>s.status==='inactive').length }}</div>
        <div class="stat-label">Inactive</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-val">{{ avgRating.toFixed(1) }}★</div>
        <div class="stat-label">Avg Rating</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" class="search-input" placeholder="Search name, category or county..." />
      </div>
      <select v-model="filterCategory" class="filter-select">
        <option value="">All Categories</option>
        <option v-for="c in categories" :key="c">{{ c }}</option>
      </select>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="review">Under Review</option>
        <option value="inactive">Inactive</option>
      </select>
      <select v-model="filterCounty" class="filter-select">
        <option value="">All Counties</option>
        <option v-for="c in counties" :key="c">{{ c }}</option>
      </select>
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Supplier</th><th>Category</th><th>County</th><th>Contact</th>
            <th>KRA PIN</th><th>Rating</th><th>Total Orders</th>
            <th>Total Value (KES)</th><th>Status</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in filteredSuppliers" :key="s.id" class="table-row">
            <td>
              <div style="display:flex;align-items:center;gap:10px">
                <div class="s-avatar">{{ s.name[0] }}</div>
                <div>
                  <div class="cell-main">{{ s.name }}</div>
                  <div class="cell-sub">{{ s.email }}</div>
                </div>
              </div>
            </td>
            <td><span class="cat-pill">{{ s.category }}</span></td>
            <td class="cell-muted" style="font-size:11px">{{ s.county }}</td>
            <td>
              <div class="cell-main">{{ s.contactPerson }}</div>
              <div class="cell-sub">{{ s.phone }}</div>
            </td>
            <td class="cell-ref" style="color:#14b8a6">{{ s.kra }}</td>
            <td>
              <div style="display:flex;align-items:center;gap:4px">
                <span style="color:#f5a623;font-size:13px">{{ '★'.repeat(Math.floor(s.rating)) }}</span>
                <span class="mono" style="font-size:11px;color:#9ca3af">{{ s.rating }}</span>
              </div>
            </td>
            <td class="mono" style="font-size:12px;text-align:center;color:#e8e4dc">{{ s.totalOrders }}</td>
            <td class="cell-amount" style="color:#22c55e">{{ (s.totalValue/1000).toFixed(0) }}K</td>
            <td><span class="status-badge" :class="s.status">{{ s.status }}</span></td>
            <td><button class="btn-view" @click="active = s">View</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drawer -->
    <div class="drawer-overlay" v-if="active" @click.self="active=null">
      <div class="drawer">
        <div class="drawer-header">
          <div style="display:flex;align-items:center;gap:12px">
            <div class="s-avatar" style="width:44px;height:44px;font-size:18px">{{ active.name[0] }}</div>
            <div>
              <h2 style="font-size:16px;font-weight:700">{{ active.name }}</h2>
              <div class="cell-sub">{{ active.category }}</div>
            </div>
          </div>
          <button class="close-btn" @click="active=null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item" v-for="f in drawerFields" :key="f.l">
              <span class="dlbl">{{ f.l }}</span>
              <span class="dval" :style="f.s||''">{{ f.v }}</span>
            </div>
          </div>
          <div style="margin-bottom:16px">
            <div class="dlbl" style="margin-bottom:10px">Performance</div>
            <div style="display:flex;flex-direction:column;gap:8px">
              <div v-for="m in active.metrics" :key="m.label">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                  <span style="font-size:12px;color:#9ca3af">{{ m.label }}</span>
                  <span class="mono" style="font-size:11px;color:#e8e4dc">{{ m.val }}%</span>
                </div>
                <div class="prog-bar"><div class="prog-fill" :class="m.color" :style="{width:m.val+'%'}"></div></div>
              </div>
            </div>
          </div>
          <div v-if="active.notes" style="background:#0d0f14;border-radius:8px;padding:12px;font-size:12px;color:#9ca3af;line-height:1.6">
            📝 {{ active.notes }}
          </div>
          <div style="display:flex;gap:8px;margin-top:16px">
            <button class="btn-primary teal" style="flex:1" @click="active=null">📋 New PO</button>
            <button class="btn-ghost" style="flex:1" @click="active=null">✏️ Edit</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Supplier Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm=false">
      <div class="modal">
        <div class="modal-header">
          <h2>🤝 Add New Supplier</h2>
          <button class="close-btn" @click="showForm=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group"><label>Company Name *</label><input v-model="form.name" placeholder="Company name" /></div>
            <div class="form-group"><label>Category *</label>
              <select v-model="form.category"><option value="">Select...</option><option v-for="c in categories" :key="c">{{ c }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>KRA PIN *</label><input v-model="form.kra" placeholder="A0XXXXXXXXX" /></div>
            <div class="form-group"><label>County *</label>
              <select v-model="form.county"><option value="">Select...</option><option v-for="c in counties" :key="c">{{ c }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Contact Person</label><input v-model="form.contactPerson" placeholder="Full name" /></div>
            <div class="form-group"><label>Phone *</label><input v-model="form.phone" placeholder="07XXXXXXXX" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Email</label><input v-model="form.email" type="email" placeholder="info@company.co.ke" /></div>
            <div class="form-group"><label>Bank Name</label>
              <select v-model="form.bank"><option value="">Select...</option><option v-for="b in banks" :key="b">{{ b }}</option></select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Account Number</label><input v-model="form.accountNo" placeholder="0000000000" /></div>
            <div class="form-group"><label>Account Name</label><input v-model="form.accountName" placeholder="Company Ltd" /></div>
          </div>
          <div class="form-group full"><label>Notes</label><textarea v-model="form.notes" rows="2" placeholder="Any additional notes..."></textarea></div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm=false">Cancel</button>
          <button class="btn-primary teal" @click="addSupplier">Add Supplier</button>
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
const filterCounty = ref('')
const showForm = ref(false)
const active = ref(null)

const categories = ['Construction Materials','Equipment & Machinery','MEP & Electrical','Safety Equipment','Tools & Hardware','Concrete & Aggregates','Timber & Joinery','Subcontractor']
const counties   = ['Nairobi','Mombasa','Kisumu','Nakuru','Kiambu','Machakos','Kajiado','Uasin Gishu']
const banks      = ['KCB Bank','Equity Bank','Co-operative Bank','NCBA Bank','Standard Chartered','Absa Bank','Stanbic Bank','Family Bank']

const form = ref({ name:'', category:'', kra:'', county:'', contactPerson:'', phone:'', email:'', bank:'', accountNo:'', accountName:'', notes:'' })

const suppliers = ref([
  { id:1, name:'Bamburi Cement Ltd',      category:'Construction Materials', county:'Mombasa',  contactPerson:'James Kariuki', phone:'0722100200', email:'orders@bamburi.co.ke',   kra:'A001234567B', status:'active',   rating:4.8, totalOrders:18, totalValue:820000, bank:'KCB Bank',   accountNo:'1234567890', accountName:'Bamburi Cement Ltd',   notes:'Preferred cement supplier. Volume discounts above 500 bags.', metrics:[{label:'On-Time Delivery',val:94,color:'green'},{label:'Quality Score',val:96,color:'green'},{label:'Price Competitiveness',val:82,color:'blue'}] },
  { id:2, name:'Steel Fabricators Ltd',   category:'Construction Materials', county:'Nairobi',  contactPerson:'Peter Mutua',   phone:'0711234567', email:'sales@steelfab.co.ke',  kra:'A009876543C', status:'active',   rating:4.6, totalOrders:12, totalValue:650000, bank:'Equity Bank', accountNo:'2345678901', accountName:'Steel Fabricators Ltd', notes:'BS4449 certified rebar manufacturer.', metrics:[{label:'On-Time Delivery',val:88,color:'green'},{label:'Quality Score',val:92,color:'green'},{label:'Price Competitiveness',val:78,color:'blue'}] },
  { id:3, name:'East Africa Cables',      category:'MEP & Electrical',       county:'Nairobi',  contactPerson:'Grace Wanjiku', phone:'0733456789', email:'info@eac.co.ke',        kra:'A005544332D', status:'active',   rating:4.5, totalOrders:8,  totalValue:320000, bank:'Co-operative Bank', accountNo:'3456789012', accountName:'East Africa Cables', notes:'ISO certified cable manufacturer.', metrics:[{label:'On-Time Delivery',val:90,color:'green'},{label:'Quality Score',val:89,color:'green'},{label:'Price Competitiveness',val:85,color:'blue'}] },
  { id:4, name:'Nakuru Plant Hire',       category:'Equipment & Machinery',  county:'Nakuru',   contactPerson:'David Odhiambo',phone:'0744567890', email:'hire@nakuruplant.co.ke',kra:'A007788990E', status:'active',   rating:4.7, totalOrders:6,  totalValue:480000, bank:'NCBA Bank',   accountNo:'4567890123', accountName:'Nakuru Plant Hire Ltd', notes:'24/7 breakdown support. CAT and Komatsu fleet.', metrics:[{label:'Equipment Availability',val:92,color:'green'},{label:'Maintenance Quality',val:88,color:'green'},{label:'Price Competitiveness',val:80,color:'blue'}] },
  { id:5, name:'Kisumu Aggregates Co.',   category:'Concrete & Aggregates',  county:'Kisumu',   contactPerson:'Alice Otieno',  phone:'0755678901', email:'sales@kisumuagg.co.ke', kra:'A003322110F', status:'review',   rating:3.9, totalOrders:4,  totalValue:180000, bank:'KCB Bank',   accountNo:'5678901234', accountName:'Kisumu Aggregates Co', notes:'New supplier. Under review for quality compliance.', metrics:[{label:'On-Time Delivery',val:72,color:'amber'},{label:'Quality Score',val:76,color:'amber'},{label:'Price Competitiveness',val:91,color:'green'}] },
  { id:6, name:'Safety Pro Kenya',        category:'Safety Equipment',       county:'Nairobi',  contactPerson:'Samuel Njoroge',phone:'0766789012', email:'info@safetypro.co.ke',  kra:'A008877665G', status:'active',   rating:4.4, totalOrders:9,  totalValue:230000, bank:'Absa Bank',   accountNo:'6789012345', accountName:'Safety Pro Kenya Ltd', notes:'KEBS approved PPE supplier.', metrics:[{label:'On-Time Delivery',val:86,color:'green'},{label:'Quality Score',val:90,color:'green'},{label:'Price Competitiveness',val:83,color:'blue'}] },
  { id:7, name:'Mombasa Hardware Depot',  category:'Tools & Hardware',       county:'Mombasa',  contactPerson:'Fatuma Hassan', phone:'0777890123', email:'orders@mombasahw.co.ke', kra:'A002211009H', status:'inactive', rating:3.2, totalOrders:3,  totalValue:65000,  bank:'Equity Bank', accountNo:'7890123456', accountName:'Mombasa Hardware Depot', notes:'Suspended pending VAT compliance review.', metrics:[{label:'On-Time Delivery',val:60,color:'amber'},{label:'Quality Score',val:65,color:'amber'},{label:'Price Competitiveness',val:88,color:'green'}] },
])

const filteredSuppliers = computed(() => suppliers.value.filter(s =>
  (!search.value || s.name.toLowerCase().includes(search.value.toLowerCase()) || s.category.toLowerCase().includes(search.value.toLowerCase()) || s.county.toLowerCase().includes(search.value.toLowerCase()))
  && (!filterCategory.value || s.category === filterCategory.value)
  && (!filterStatus.value  || s.status   === filterStatus.value)
  && (!filterCounty.value  || s.county   === filterCounty.value)
))

const avgRating = computed(() => suppliers.value.reduce((a,b) => a+b.rating,0) / suppliers.value.length)

const drawerFields = computed(() => active.value ? [
  {l:'County',       v: active.value.county                                          },
  {l:'Contact',      v: active.value.contactPerson                                   },
  {l:'Phone',        v: active.value.phone                                           },
  {l:'Email',        v: active.value.email                                           },
  {l:'KRA PIN',      v: active.value.kra                                             },
  {l:'Bank',         v: active.value.bank                                            },
  {l:'Account No',   v: active.value.accountNo                                       },
  {l:'Rating',       v: active.value.rating+'/5 ★', s:'color:#f5a623;font-weight:700'},
  {l:'Total Orders', v: active.value.totalOrders                                     },
  {l:'Total Value',  v:'KES '+(active.value.totalValue/1000).toFixed(0)+'K', s:'color:#22c55e;font-weight:700'},
] : [])

function addSupplier() {
  suppliers.value.push({ id:Date.now(), ...form.value, status:'review', rating:0, totalOrders:0, totalValue:0, metrics:[] })
  showForm.value = false
  form.value = { name:'', category:'', kra:'', county:'', contactPerson:'', phone:'', email:'', bank:'', accountNo:'', accountName:'', notes:'' }
}
</script>

<style scoped>
@import '/src/assets/suppliers.css';
.cat-pill { font-family:'DM Mono',monospace; font-size:9px; padding:2px 8px; border-radius:10px; background:#1e2230; color:#9ca3af; white-space:nowrap; }
</style>