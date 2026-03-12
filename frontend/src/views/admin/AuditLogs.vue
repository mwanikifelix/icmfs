<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-list text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">Audit Logs</h4>
                        <span class="text-sm" style="color:#b3c8e8;">Complete system activity trail · tamper-evident</span>
                    </div>
                </div>
                <Button label="Export Logs" icon="pi pi-download"
                    style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;" />
            </div>

            <!-- Stats row -->
            <div class="grid mb-3">
                <div class="col-6 lg:col-3" v-for="s in stats" :key="s.label">
                    <div class="card mb-0">
                        <div class="flex align-items-center gap-3">
                            <div class="flex align-items-center justify-content-center border-round flex-shrink-0"
                                style="width:2.5rem;height:2.5rem;" :style="{ background: s.bg }">
                                <i :class="s.icon" :style="{ color: s.color }" />
                            </div>
                            <div>
                                <div class="font-bold text-2xl text-900">{{ s.value }}</div>
                                <div class="text-500 text-xs">{{ s.label }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Filters + table -->
            <div class="card">
                <div class="flex flex-wrap gap-3 mb-4 align-items-center">
                    <div class="p-input-icon-left" style="flex:1;min-width:200px;max-width:300px;">
                        <i class="pi pi-search" />
                        <InputText v-model="search" placeholder="Search action, user or IP..." class="w-full" />
                    </div>
                    <Dropdown v-model="filterModule" :options="moduleOptions" placeholder="All Modules"
                        showClear style="min-width:160px;" />
                    <Dropdown v-model="filterAction" :options="actionTypes" placeholder="All Actions"
                        showClear style="min-width:160px;" />
                    <Dropdown v-model="filterUser" :options="userOptions" placeholder="All Users"
                        showClear style="min-width:160px;" />
                    <Calendar v-model="dateRange" selectionMode="range" placeholder="Date range"
                        showButtonBar style="min-width:200px;" />
                </div>

                <DataTable :value="filteredLogs" :paginator="true" :rows="15"
                    stripedRows responsiveLayout="scroll"
                    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                    currentPageReportTemplate="{first}–{last} of {totalRecords} events"
                    :rowClass="rowClass">

                    <Column header="Timestamp" sortable sortField="timestamp" style="min-width:160px;">
                        <template #body="{ data }">
                            <span class="font-mono text-sm text-600">{{ data.timestamp }}</span>
                        </template>
                    </Column>

                    <Column header="User" style="min-width:160px;">
                        <template #body="{ data }">
                            <div class="flex align-items-center gap-2">
                                <div class="flex align-items-center justify-content-center border-circle text-xs font-bold flex-shrink-0"
                                    style="width:1.8rem;height:1.8rem;background:#1976d2;color:#fff;">
                                    {{ initials(data.user) }}
                                </div>
                                <div>
                                    <div class="text-sm font-medium text-900">{{ data.user }}</div>
                                    <div class="text-400 text-xs font-mono">{{ data.ip }}</div>
                                </div>
                            </div>
                        </template>
                    </Column>

                    <Column header="Action" style="min-width:180px;">
                        <template #body="{ data }">
                            <div class="flex align-items-center gap-2">
                                <Tag :value="data.actionType"
                                    :style="actionStyle(data.actionType)"
                                    style="font-size:0.65rem;" />
                                <span class="text-sm text-900">{{ data.action }}</span>
                            </div>
                        </template>
                    </Column>

                    <Column header="Module">
                        <template #body="{ data }">
                            <Tag :value="data.module" severity="secondary" style="font-size:0.7rem;" />
                        </template>
                    </Column>

                    <Column header="Details" style="min-width:200px;">
                        <template #body="{ data }">
                            <span class="text-500 text-sm">{{ data.details }}</span>
                        </template>
                    </Column>

                    <Column header="Status" style="width:90px;">
                        <template #body="{ data }">
                            <Tag :value="data.status"
                                :severity="data.status==='Success'?'success':data.status==='Warning'?'warn':'danger'" />
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const search       = ref('');
const filterModule = ref(null);
const filterAction = ref(null);
const filterUser   = ref(null);
const dateRange    = ref(null);

const moduleOptions = ['Auth','Users','Roles','Projects','Finance','Payments','Procurement','QA','Safety','Settings'];
const actionTypes   = ['LOGIN','LOGOUT','CREATE','UPDATE','DELETE','APPROVE','EXPORT','FAILED'];
const userOptions   = ['Felix Mwaniki','Peter Kamau','Jane Achieng','David Oduya','Mary Wanjiku','System'];

const initials = (name) => name.split(' ').map(n=>n[0]).slice(0,2).join('').toUpperCase();

const actionStyle = (type) => {
    const map = {
        LOGIN:  'background:#e8fdf0;color:#2ecc71;',
        LOGOUT: 'background:#f3f4f6;color:#6b7280;',
        CREATE: 'background:#e8f0fe;color:#1976d2;',
        UPDATE: 'background:#fef9e7;color:#e6a817;',
        DELETE: 'background:#fde8e8;color:#ef4444;',
        APPROVE:'background:#f3e8ff;color:#a855f7;',
        EXPORT: 'background:#e8f0fe;color:#1976d2;',
        FAILED: 'background:#fde8e8;color:#ef4444;',
    };
    return map[type] || '';
};

const rowClass = (data) => data.status === 'Failed' ? 'surface-100' : '';

const stats = [
    { label:'Events Today',    value:'37',  icon:'pi pi-list',         color:'#1976d2', bg:'#e8f0fe' },
    { label:'Failed Attempts', value:'3',   icon:'pi pi-exclamation-triangle', color:'#ef4444', bg:'#fde8e8' },
    { label:'Active Users',    value:'8',   icon:'pi pi-users',        color:'#2ecc71', bg:'#e8fdf0' },
    { label:'Exports Today',   value:'5',   icon:'pi pi-download',     color:'#e6a817', bg:'#fef9e7' },
];

const logs = ref([
    { id:1,  timestamp:'2025-02-18 08:32:14', user:'Felix Mwaniki', ip:'192.168.1.12', actionType:'LOGIN',  action:'User logged in',           module:'Auth',        details:'Chrome / Kali Linux',           status:'Success' },
    { id:2,  timestamp:'2025-02-18 08:35:02', user:'Felix Mwaniki', ip:'192.168.1.12', actionType:'UPDATE', action:'User profile updated',      module:'Users',       details:'Changed email address',         status:'Success' },
    { id:3,  timestamp:'2025-02-18 08:40:11', user:'Peter Kamau',   ip:'192.168.1.20', actionType:'LOGIN',  action:'User logged in',           module:'Auth',        details:'Chrome / Windows',              status:'Success' },
    { id:4,  timestamp:'2025-02-18 09:02:55', user:'Peter Kamau',   ip:'192.168.1.20', actionType:'APPROVE',action:'Invoice approved',          module:'Finance',     details:'INV-NPH-2025-019 · KES 208K',   status:'Success' },
    { id:5,  timestamp:'2025-02-18 09:11:33', user:'Mary Wanjiku',  ip:'10.0.0.8',     actionType:'CREATE', action:'Inspection scheduled',      module:'QA',          details:'INS-044 · Nairobi Housing',     status:'Success' },
    { id:6,  timestamp:'2025-02-18 09:22:47', user:'Unknown',       ip:'41.90.4.22',   actionType:'FAILED', action:'Failed login attempt',      module:'Auth',        details:'User: admin · Wrong password',  status:'Failed'  },
    { id:7,  timestamp:'2025-02-18 09:30:19', user:'Jane Achieng',  ip:'192.168.1.31', actionType:'LOGIN',  action:'User logged in',           module:'Auth',        details:'Firefox / Linux',               status:'Success' },
    { id:8,  timestamp:'2025-02-18 09:45:08', user:'Felix Mwaniki', ip:'192.168.1.12', actionType:'UPDATE', action:'Role permissions updated',  module:'Roles',       details:'Role: Site Engineer',           status:'Success' },
    { id:9,  timestamp:'2025-02-18 10:02:14', user:'Felix Mwaniki', ip:'192.168.1.12', actionType:'CREATE', action:'New user created',          module:'Users',       details:'User: grace.njoroge',           status:'Success' },
    { id:10, timestamp:'2025-02-18 10:15:33', user:'David Oduya',   ip:'10.0.0.14',    actionType:'EXPORT', action:'Finance report exported',   module:'Finance',     details:'Monthly report · Feb 2025',     status:'Success' },
    { id:11, timestamp:'2025-02-18 10:30:00', user:'Unknown',       ip:'197.232.1.88', actionType:'FAILED', action:'Failed login attempt',      module:'Auth',        details:'User: peter.k · Wrong password',status:'Failed'  },
    { id:12, timestamp:'2025-02-18 11:00:12', user:'System',        ip:'127.0.0.1',    actionType:'CREATE', action:'Scheduled backup completed',module:'Settings',    details:'DB backup · 2.3 GB',            status:'Success' },
]);

const filteredLogs = computed(() => logs.value.filter(l => {
    const q = search.value.toLowerCase();
    return (
        (!q || l.action.toLowerCase().includes(q) || l.user.toLowerCase().includes(q) || l.ip.includes(q)) &&
        (!filterModule.value || l.module     === filterModule.value) &&
        (!filterAction.value || l.actionType === filterAction.value) &&
        (!filterUser.value   || l.user       === filterUser.value)
    );
}));
</script>