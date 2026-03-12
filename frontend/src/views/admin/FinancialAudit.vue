<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-file-check text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">Financial Audit</h4>
                        <span class="text-sm" style="color:#b3c8e8;">All financial transactions, approvals and discrepancies</span>
                    </div>
                </div>
                <div class="flex gap-2">
                    <Button label="Export Report" icon="pi pi-download" size="small"
                        style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;" />
                    <Button label="Flag Review" icon="pi pi-flag" size="small" severity="danger" outlined
                        style="border-color:#fff;color:#fff;" />
                </div>
            </div>

            <!-- KPI strip -->
            <div class="grid mb-3">
                <div class="col-6 lg:col-3" v-for="k in kpis" :key="k.label">
                    <div class="card mb-0">
                        <div class="flex justify-content-between align-items-start">
                            <div>
                                <div class="text-500 text-sm mb-1">{{ k.label }}</div>
                                <div class="font-bold text-2xl" :style="{ color: k.color }">{{ k.value }}</div>
                                <div class="text-400 text-xs mt-1">{{ k.sub }}</div>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round"
                                style="width:2.5rem;height:2.5rem;" :style="{ background: k.bg }">
                                <i :class="k.icon" :style="{ color: k.color }" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tabs -->
            <div class="card">
                <TabView>

                    <!-- ── Transaction Log ── -->
                    <TabPanel header="Transaction Log">
                        <div class="flex flex-wrap gap-3 mb-4 align-items-center">
                            <div class="p-input-icon-left" style="flex:1;min-width:200px;max-width:300px;">
                                <i class="pi pi-search" />
                                <InputText v-model="txSearch" placeholder="Reference, project, amount..." class="w-full" />
                            </div>
                            <Dropdown v-model="txType" :options="txTypes" placeholder="All Types" showClear style="min-width:160px;" />
                            <Dropdown v-model="txStatus" :options="['Approved','Pending','Flagged','Rejected']" placeholder="All Status" showClear style="min-width:140px;" />
                            <Calendar v-model="txDateRange" selectionMode="range" placeholder="Date range" showButtonBar style="min-width:200px;" />
                        </div>

                        <DataTable :value="filteredTx" :paginator="true" :rows="10"
                            stripedRows responsiveLayout="scroll"
                            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                            currentPageReportTemplate="{first}–{last} of {totalRecords}">
                            <Column field="reference" header="Reference" sortable>
                                <template #body="{ data }">
                                    <span class="font-mono font-medium text-sm" style="color:#1976d2;">{{ data.reference }}</span>
                                </template>
                            </Column>
                            <Column field="date" header="Date" sortable>
                                <template #body="{ data }">
                                    <span class="text-sm text-600">{{ data.date }}</span>
                                </template>
                            </Column>
                            <Column field="project" header="Project" style="min-width:160px;" />
                            <Column header="Type">
                                <template #body="{ data }">
                                    <Tag :value="data.type" :style="typeStyle(data.type)" style="font-size:0.7rem;" />
                                </template>
                            </Column>
                            <Column header="Amount (KES)" sortable sortField="amount">
                                <template #body="{ data }">
                                    <span class="font-bold text-sm" :style="{ color: data.amount < 0 ? '#ef4444' : '#0d2347' }">
                                        {{ formatAmount(data.amount) }}
                                    </span>
                                </template>
                            </Column>
                            <Column field="approvedBy" header="Approved By" />
                            <Column header="Status">
                                <template #body="{ data }">
                                    <Tag :value="data.status"
                                        :severity="data.status==='Approved'?'success':data.status==='Pending'?'warn':data.status==='Flagged'?'warn':'danger'" />
                                </template>
                            </Column>
                            <Column header="" style="width:60px;">
                                <template #body="{ data }">
                                    <Button v-if="data.status==='Flagged'" icon="pi pi-flag-fill"
                                        text rounded size="small" v-tooltip.top="'Flagged for review'"
                                        style="color:#ef4444;" />
                                </template>
                            </Column>
                        </DataTable>
                    </TabPanel>

                    <!-- ── Approval Trail ── -->
                    <TabPanel header="Approval Trail">
                        <div class="flex flex-column gap-3">
                            <div v-for="item in approvalTrail" :key="item.id"
                                class="p-3 border-round-lg border-1"
                                :style="item.status==='Approved'?'border-color:#2ecc71;':item.status==='Pending'?'border-color:#e6a817;':'border-color:#ef4444;'">
                                <div class="flex align-items-center justify-content-between flex-wrap gap-2">
                                    <div class="flex align-items-center gap-3">
                                        <div class="flex align-items-center justify-content-center border-round flex-shrink-0"
                                            style="width:2.5rem;height:2.5rem;"
                                            :style="{ background: item.status==='Approved'?'#e8fdf0':item.status==='Pending'?'#fef9e7':'#fde8e8' }">
                                            <i :class="item.status==='Approved'?'pi pi-check':item.status==='Pending'?'pi pi-clock':'pi pi-times'"
                                                :style="{ color: item.status==='Approved'?'#2ecc71':item.status==='Pending'?'#e6a817':'#ef4444' }" />
                                        </div>
                                        <div>
                                            <div class="font-semibold text-900 text-sm">{{ item.reference }} · {{ item.description }}</div>
                                            <div class="text-500 text-xs">{{ item.submittedBy }} → {{ item.approver }} · {{ item.date }}</div>
                                        </div>
                                    </div>
                                    <div class="flex align-items-center gap-3">
                                        <span class="font-bold" style="color:#0d2347;">{{ formatAmount(item.amount) }}</span>
                                        <Tag :value="item.status"
                                            :severity="item.status==='Approved'?'success':item.status==='Pending'?'warn':'danger'" />
                                    </div>
                                </div>
                                <div v-if="item.note" class="mt-2 text-sm text-500 pl-5 ml-3">
                                    <i class="pi pi-comment mr-1" />{{ item.note }}
                                </div>
                            </div>
                        </div>
                    </TabPanel>

                    <!-- ── Discrepancies ── -->
                    <TabPanel header="Discrepancies">
                        <div class="mb-4">
                            <Message severity="warn" :closable="false">
                                {{ discrepancies.filter(d=>d.severity==='High').length }} high-severity discrepancies require immediate attention.
                            </Message>
                        </div>
                        <DataTable :value="discrepancies" stripedRows size="small">
                            <Column field="id" header="#" style="width:60px;" />
                            <Column field="project" header="Project" />
                            <Column field="description" header="Discrepancy" style="min-width:200px;" />
                            <Column header="Expected">
                                <template #body="{ data }">
                                    <span class="font-mono text-sm">{{ formatAmount(data.expected) }}</span>
                                </template>
                            </Column>
                            <Column header="Actual">
                                <template #body="{ data }">
                                    <span class="font-mono text-sm font-bold" style="color:#ef4444;">{{ formatAmount(data.actual) }}</span>
                                </template>
                            </Column>
                            <Column header="Variance">
                                <template #body="{ data }">
                                    <span class="font-bold text-sm" style="color:#ef4444;">{{ formatAmount(data.actual - data.expected) }}</span>
                                </template>
                            </Column>
                            <Column header="Severity">
                                <template #body="{ data }">
                                    <Tag :value="data.severity"
                                        :severity="data.severity==='High'?'danger':data.severity==='Medium'?'warn':'info'" />
                                </template>
                            </Column>
                            <Column field="flaggedBy" header="Flagged By" />
                            <Column header="">
                                <template #body>
                                    <Button label="Investigate" icon="pi pi-search" text size="small"
                                        style="color:#1976d2;" />
                                </template>
                            </Column>
                        </DataTable>
                    </TabPanel>

                </TabView>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const txSearch    = ref('');
const txType      = ref(null);
const txStatus    = ref(null);
const txDateRange = ref(null);

const txTypes = ['Payment','Invoice','Expense','Budget Adjustment','Refund','Transfer'];

const formatAmount = (v) => {
    const abs = Math.abs(v);
    const sign = v < 0 ? '-' : '';
    if (abs >= 1e9) return `${sign}KES ${(abs/1e9).toFixed(2)}B`;
    if (abs >= 1e6) return `${sign}KES ${(abs/1e6).toFixed(1)}M`;
    return `${sign}KES ${abs.toLocaleString()}`;
};

const typeStyle = (type) => {
    const map = {
        Payment:            'background:#e8f0fe;color:#1976d2;',
        Invoice:            'background:#fef9e7;color:#e6a817;',
        Expense:            'background:#fde8e8;color:#ef4444;',
        'Budget Adjustment':'background:#f3e8ff;color:#a855f7;',
        Refund:             'background:#e8fdf0;color:#2ecc71;',
        Transfer:           'background:#f3f4f6;color:#6b7280;',
    };
    return map[type] || '';
};

const kpis = [
    { label:'Total Audited',    value:'KES 2.3B', sub:'This financial year',  color:'#0d2347', bg:'#e8ecf4', icon:'pi pi-dollar'            },
    { label:'Approved',         value:'94.2%',    sub:'1,247 transactions',   color:'#2ecc71', bg:'#e8fdf0', icon:'pi pi-check-circle'       },
    { label:'Pending Review',   value:'18',       sub:'Requires action',      color:'#e6a817', bg:'#fef9e7', icon:'pi pi-clock'              },
    { label:'Flagged / Issues', value:'7',        sub:'3 high severity',      color:'#ef4444', bg:'#fde8e8', icon:'pi pi-exclamation-triangle'},
];

const transactions = ref([
    { id:1,  reference:'PAY-MSA-001', date:'18 Feb 2025', project:'Mombasa Affordable Housing', type:'Payment',  amount:5200000,  approvedBy:'Felix M.',  status:'Approved' },
    { id:2,  reference:'INV-NPH-019', date:'17 Feb 2025', project:'Nairobi Housing Phase 2',    type:'Invoice',  amount:208000,   approvedBy:'Peter K.',  status:'Approved' },
    { id:3,  reference:'EXP-KLF-003', date:'17 Feb 2025', project:'Kilifi Road Expansion',      type:'Expense',  amount:-45000,   approvedBy:'—',         status:'Pending'  },
    { id:4,  reference:'PAY-NPH-022', date:'16 Feb 2025', project:'Nairobi Housing Phase 2',    type:'Payment',  amount:3100000,  approvedBy:'Felix M.',  status:'Approved' },
    { id:5,  reference:'ADJ-MSA-007', date:'15 Feb 2025', project:'Mombasa Affordable Housing', type:'Budget Adjustment', amount:500000, approvedBy:'Felix M.', status:'Flagged' },
    { id:6,  reference:'EXP-MSA-011', date:'14 Feb 2025', project:'Mombasa Affordable Housing', type:'Expense',  amount:-120000,  approvedBy:'Mary W.',   status:'Approved' },
    { id:7,  reference:'REF-KLF-001', date:'13 Feb 2025', project:'Kilifi Road Expansion',      type:'Refund',   amount:80000,    approvedBy:'Felix M.',  status:'Approved' },
]);

const filteredTx = computed(() => transactions.value.filter(t => {
    const q = txSearch.value.toLowerCase();
    return (
        (!q || t.reference.toLowerCase().includes(q) || t.project.toLowerCase().includes(q)) &&
        (!txType.value   || t.type   === txType.value) &&
        (!txStatus.value || t.status === txStatus.value)
    );
}));

const approvalTrail = ref([
    { id:1, reference:'PAY-MSA-001', description:'Contractor milestone payment', submittedBy:'Peter K.', approver:'Felix M.', date:'18 Feb 2025', amount:5200000,  status:'Approved', note:'Verified against BOQ milestone 3'         },
    { id:2, reference:'INV-NPH-019', description:'Materials invoice — Steel',    submittedBy:'Jane A.',  approver:'Peter K.', date:'17 Feb 2025', amount:208000,   status:'Approved', note:null                                       },
    { id:3, reference:'EXP-KLF-003', description:'Fuel & machinery expenses',    submittedBy:'Samuel M.',approver:'Felix M.', date:'17 Feb 2025', amount:45000,    status:'Pending',  note:'Awaiting supporting receipts'             },
    { id:4, reference:'ADJ-MSA-007', description:'Budget reallocation request',  submittedBy:'Felix M.', approver:'Board',    date:'15 Feb 2025', amount:500000,   status:'Pending',  note:'Flagged for board approval threshold'     },
    { id:5, reference:'PAY-NPH-022', description:'Subcontractor payment',        submittedBy:'Peter K.', approver:'Felix M.', date:'16 Feb 2025', amount:3100000,  status:'Approved', note:null                                       },
]);

const discrepancies = ref([
    { id:1, project:'Mombasa Affordable Housing', description:'Budget adjustment exceeds approved limit', expected:200000, actual:500000, severity:'High',   flaggedBy:'System'   },
    { id:2, project:'Kilifi Road Expansion',       description:'Expense receipt amounts mismatch',        expected:45000,  actual:52000,  severity:'Medium', flaggedBy:'Mary W.'  },
    { id:3, project:'Nairobi Housing Phase 2',     description:'Duplicate invoice reference detected',    expected:208000, actual:416000, severity:'High',   flaggedBy:'System'   },
    { id:4, project:'Mombasa Affordable Housing', description:'Petty cash variance — Q4',                expected:15000,  actual:13500,  severity:'Low',    flaggedBy:'David O.' },
]);
</script>