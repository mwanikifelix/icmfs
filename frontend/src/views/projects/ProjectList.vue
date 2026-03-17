<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-building text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">Projects</h4>
                        <span class="text-sm" style="color:#b3c8e8;">{{ projects.length }} projects loaded</span>
                    </div>
                </div>
                <Button label="New Project" icon="pi pi-plus"
                    style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                    @click="$router.push('/app/projects/create')" />
            </div>

            <!-- Stats -->
<div class="grid mb-3">

    <!-- Total -->
    <div class="col-12 md:col-3">
        <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
                <div>
                    <div class="text-500 text-sm mb-1">Total Projects</div>
                    <div class="font-bold text-3xl text-900">{{ projects.length }}</div>
                </div>
                <div class="flex align-items-center justify-content-center border-round"
                    style="width:2.5rem;height:2.5rem;background:#e8f0fe;">
                    <i class="pi pi-briefcase" style="color:#1976d2;" />
                </div>
            </div>
        </div>
    </div>

    <!-- Planned -->
    <div class="col-12 md:col-3">
        <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
                <div>
                    <div class="text-500 text-sm mb-1">Planned</div>
                    <div class="font-bold text-3xl" style="color:#3498db;">
                        {{ statusCount('planned') }}
                    </div>
                </div>
                <div class="flex align-items-center justify-content-center border-round"
                    style="width:2.5rem;height:2.5rem;background:#eaf4ff;">
                    <i class="pi pi-calendar" style="color:#3498db;" />
                </div>
            </div>
        </div>
    </div>

    <!-- Active -->
    <div class="col-12 md:col-3">
        <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
                <div>
                    <div class="text-500 text-sm mb-1">Active</div>
                    <div class="font-bold text-3xl" style="color:#2ecc71;">
                        {{ statusCount('active') + statusCount('in_progress') }}
                    </div>
                </div>
                <div class="flex align-items-center justify-content-center border-round"
                    style="width:2.5rem;height:2.5rem;background:#e8fdf0;">
                    <i class="pi pi-spinner" style="color:#2ecc71;" />
                </div>
            </div>
        </div>
    </div>

    <!-- On Hold -->
    <div class="col-12 md:col-3">
        <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
                <div>
                    <div class="text-500 text-sm mb-1">On Hold</div>
                    <div class="font-bold text-3xl" style="color:#e6a817;">
                        {{ statusCount('on_hold') }}
                    </div>
                </div>
                <div class="flex align-items-center justify-content-center border-round"
                    style="width:2.5rem;height:2.5rem;background:#fef9e7;">
                    <i class="pi pi-pause-circle" style="color:#e6a817;" />
                </div>
            </div>
        </div>
    </div>

    <!-- At Risk -->
    <div class="col-12 md:col-3">
        <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
                <div>
                    <div class="text-500 text-sm mb-1">At Risk</div>
                    <div class="font-bold text-3xl" style="color:#e74c3c;">
                        {{ statusCount('at_risk') }}
                    </div>
                </div>
                <div class="flex align-items-center justify-content-center border-round"
                    style="width:2.5rem;height:2.5rem;background:#fdecea;">
                    <i class="pi pi-exclamation-triangle" style="color:#e74c3c;" />
                </div>
            </div>
        </div>
    </div>

    <!-- Completed -->
    <div class="col-12 md:col-3">
        <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
                <div>
                    <div class="text-500 text-sm mb-1">Completed</div>
                    <div class="font-bold text-3xl" style="color:#1976d2;">
                        {{ statusCount('completed') }}
                    </div>
                </div>
                <div class="flex align-items-center justify-content-center border-round"
                    style="width:2.5rem;height:2.5rem;background:#e8f0fe;">
                    <i class="pi pi-check-circle" style="color:#1976d2;" />
                </div>
            </div>
        </div>
    </div>

    <!-- Cancelled -->
    <div class="col-12 md:col-3">
        <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
                <div>
                    <div class="text-500 text-sm mb-1">Cancelled</div>
                    <div class="font-bold text-3xl" style="color:#7f8c8d;">
                        {{ statusCount('cancelled') }}
                    </div>
                </div>
                <div class="flex align-items-center justify-content-center border-round"
                    style="width:2.5rem;height:2.5rem;background:#f4f6f7;">
                    <i class="pi pi-times-circle" style="color:#7f8c8d;" />
                </div>
            </div>
        </div>
    </div>

</div>
            <!-- Filters -->
            <div class="card mb-3">
                <div class="flex flex-wrap gap-3 align-items-end">
                    <div class="p-input-icon-left" style="flex:1;min-width:200px;">
                        <i class="pi pi-search" />
                        <InputText v-model="search" placeholder="Search projects..." class="w-full" @input="onSearch" />
                    </div>
                    <Select v-model="filterStatus" :options="statusOptions"
                        optionLabel="label" optionValue="value"
                        placeholder="All Statuses" showClear style="min-width:160px;" @change="loadProjects" />
                    <Select v-model="filterRegion" :options="regions"
                        optionLabel="name" optionValue="id"
                        placeholder="All Regions" showClear style="min-width:160px;"
                        :loading="loadingRegions" @change="loadProjects" />
                    <Select v-model="filterCounty" :options="filterCounties"
                        optionLabel="name" optionValue="id"
                        placeholder="All Counties" showClear style="min-width:160px;"
                        :loading="loadingFilterCounties"
                        :disabled="!filterRegion" @change="loadProjects" />
                
                        <Select v-model="filterSubCounty"
                        :options="filterSubCounties"
                        optionLabel="name"
                        optionValue="id"
                        placeholder="All Subcounties"
                        showClear
                        style="min-width:160px;"
                        :loading="loadingFilterSubCounties"
                        :disabled="!filterCounty"
                        @change="loadProjects" />

                    <Select v-model="filterWard"
                        :options="filterWards"
                        optionLabel="name"
                        optionValue="id"
                        placeholder="All Wards"
                        showClear
                        style="min-width:160px;"
                        :loading="loadingFilterWards"
                        :disabled="!filterSubCounty"
                        @change="loadProjects" />
                    <Button icon="pi pi-refresh" outlined severity="secondary"
                        :loading="loading" @click="loadProjects" />
                </div>
            </div>

            <!-- Table -->
            <div class="card">
                <DataTable :value="projects" :loading="loading"
                    :paginator="true" :rows="10" :rowsPerPageOptions="[5,10,20,50]"
                    stripedRows responsiveLayout="scroll"
                    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                    currentPageReportTemplate="{first}–{last} of {totalRecords}">

                    <Column header="Project" sortable sortField="name" style="min-width:220px;">
                        <template #body="{ data }">
                            <div>
                                <div class="font-semibold text-900">{{ data.name }}</div>
                                <div class="text-500 text-xs mt-1">
                                    <i class="pi pi-user text-xs mr-1" />{{ data.sponsor_name }}
                                </div>
                            </div>
                        </template>
                    </Column>

                    <Column header="Location">
                        <template #body="{ data }">
                            <div class="text-sm">
                                <div v-if="data.region_detail" class="text-600">{{ data.region_detail.name }}</div>
                                <div v-if="data.county_detail" class="text-400 text-xs">{{ data.county_detail.name }}</div>
                            </div>
                        </template>
                    </Column>

                    <Column header="Status" sortable sortField="status">
                        <template #body="{ data }">
                            <Tag :value="data.status_display || data.status"
                                :severity="statusSeverity(data.status)" />
                        </template>
                    </Column>

                    <Column header="Progress" style="min-width:140px;">
                        <template #body="{ data }">
                            <ProgressBar :value="data.progress || 0" :showValue="false" style="height:6px;"
                                :pt="{ value: { style: { background: progressColor(data.progress) } } }" />
                            <small class="text-600">{{ data.progress || 0 }}%</small>
                        </template>
                    </Column>

                    <Column header="Budget (KES)" sortable sortField="budget">
                        <template #body="{ data }">
                            <span class="text-sm font-medium">
                                {{ data.budget ? fmtBudget(data.budget) : '—' }}
                            </span>
                        </template>
                    </Column>

                    <Column header="Start" sortable sortField="start_date">
                        <template #body="{ data }">
                            <span class="text-500 text-sm">{{ fmtDate(data.start_date) }}</span>
                        </template>
                    </Column>

                    <Column header="Actions" style="width:90px;">
                        <template #body="{ data }">
                            <div class="flex gap-1">
                                <Button icon="pi pi-eye" text rounded size="small"
                                    v-tooltip.top="'View'"
                                    @click="$router.push(`/app/projects/${data.id}`)" />
                                <Button icon="pi pi-pencil" text rounded size="small"
                                    severity="secondary" v-tooltip.top="'Edit'"
                                    @click="$router.push(`/app/projects/${data.id}/edit`)" />
                            </div>
                        </template>
                    </Column>

                    <template #empty>
                        <div class="text-center py-6 text-500">
                            <i class="pi pi-building text-4xl mb-2 block text-300" />
                            <div>No projects found.</div>
                            <Button label="Create First Project" icon="pi pi-plus" class="mt-3" size="small"
                                style="background:#1976d2;border-color:#1976d2;"
                                @click="$router.push('/app/projects/create')" />
                        </div>
                    </template>
                </DataTable>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '@/api/api';
import 'primeicons/primeicons.css'
import Select from 'primevue/select';


const projects      = ref([]);
const loading       = ref(false);
const apiError      = ref('');
const search        = ref('');
const filterStatus  = ref(null);
const filterRegion  = ref(null);
const filterCounty  = ref(null);

const regions             = ref([]);
const filterCounties      = ref([]);
const loadingRegions      = ref(false);
const loadingFilterCounties = ref(false);
const filterSubCounty = ref(null);
const filterWard = ref(null);

const filterSubCounties = ref([]);
const filterWards = ref([]);

const loadingFilterSubCounties = ref(false);
const loadingFilterWards = ref(false);

const statusOptions = [
    { label: 'Planned',     value: 'planned'     },
    { label: 'Active',      value: 'active'      },
    { label: 'In Progress', value: 'in_progress' },
    { label: 'On Hold',     value: 'on_hold'     },
    { label: 'At Risk',     value: 'at_risk'     },
    { label: 'Completed',   value: 'completed'   },
    { label: 'Cancelled',   value: 'cancelled'   },
];

const fmtDate = (d) => {
    if (!d) return '—';
    return new Date(d).toLocaleDateString('en-KE', { day:'2-digit', month:'short', year:'numeric' });
};
const fmtBudget = (v) => {
    const n = Number(v);
    if (n >= 1e9) return `KES ${(n/1e9).toFixed(2)}B`;
    if (n >= 1e6) return `KES ${(n/1e6).toFixed(1)}M`;
    return `KES ${n.toLocaleString('en-KE')}`;
};
const statusSeverity = (s) => ({
    planned:'info', active:'success', in_progress:'success',
    on_hold:'warn', at_risk:'danger', completed:'secondary', cancelled:'danger',
}[s] || 'info');
const progressColor = (p) => (p||0) >= 80 ? '#2ecc71' : (p||0) >= 40 ? '#e6a817' : '#1976d2';
const statusCount = (s) => projects.value.filter(p => p.status === s).length;

async function loadRegions() {
    loadingRegions.value = true;
    try {
        const res = await api.get('/api/projects/regions/');
        regions.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingRegions.value = false; }
}

watch(filterRegion, async (val) => {
    filterCounty.value   = null;
    filterCounties.value = [];
     filterSubCounty.value = null;
    filterWard.value = null;

  
    filterSubCounties.value = [];
    filterWards.value = [];
    if (!val) return;
    loadingFilterCounties.value = true;
    try {
        const res = await api.get('/api/projects/counties/', { params: { region: val } });
        filterCounties.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingFilterCounties.value = false; }
    loadProjects();
});

watch(filterCounty, async (val) => {
    filterSubCounty.value = null;
    filterWard.value = null;

    filterSubCounties.value = [];
    filterWards.value = [];

    if (!val) return;

    loadingFilterSubCounties.value = true;
    try {
        const res = await api.get('/api/projects/subcounties/', { params: { county: val } });
        filterSubCounties.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally {
        loadingFilterSubCounties.value = false;
    }
});

watch(filterSubCounty, async (val) => {
    filterWard.value = null;
    filterWards.value = [];

    if (!val) return;

    loadingFilterWards.value = true;
    try {
        const res = await api.get('/api/projects/wards/', { params: { sub_county: val } });
        filterWards.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally {
        loadingFilterWards.value = false;
    }
});
async function loadProjects() {
    loading.value  = true;
    apiError.value = '';
    try {
        const params = {};
        if (filterStatus.value) params.status = filterStatus.value;
        if (filterRegion.value) params.region = filterRegion.value;
        if (filterCounty.value) params.county = filterCounty.value;
        if (filterSubCounty.value) params.sub_county = filterSubCounty.value;
        if (filterWard.value) params.ward = filterWard.value;

if (search.value) params.search = search.value;

        const res = await api.get('/api/projects/projects/', { params });
        projects.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } catch (e) {
        apiError.value = e.response?.data?.detail || 'Failed to load projects.';
    } finally { loading.value = false; }
}

let searchTimer = null;
function onSearch() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadProjects, 400);
}

onMounted(() => {
    loadProjects();
    loadRegions();
});
</script>


<style>
/* ===============================
   Dashboard Modern Styling
   =============================== */

/* Card upgrade */
.grid.mb-3{
    display:flex;
    flex-wrap:nowrap;
    gap:3rem;
}

.card {
    border-radius: 14px;
    border: 1px solid #0f4734;
    font-size: x-large;
    box-shadow: 0 1px 4px rgba(173, 7, 132, 0.04);
    transition: all 0.25s ease;
}

/* Card hover */
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(133, 18, 18, 0.08);
}

/* Header polish */
.border-round-xl {
    border-radius: 16px !important;
}

/* Stats number look */
.text-3xl {
    letter-spacing: -0.5px;
}

/* Sub labels */
.text-500 {
    font-size:medium;
    font-weight: 500;
    color: brown;
    
}

/* Icon containers in stat cards */
.card .border-round {
    transition: transform 0.2s ease;
}

.card:hover .border-round {
    transform: scale(3.1);
}

/* DataTable container polish */
.p-datatable {
    border-radius: 14px;
    overflow: hidden;


}

/* Table header */
.p-datatable thead th {
    background: #83a359;
    font-weight: 1000;
    font-size: x-large;
    color: #0e6bec;
}

/* Table row hover */
.p-datatable tbody tr:hover {
    background: #85754dd2;
    font-size: x-large;
    

}

/* Progress bar modern look */
.p-progressbar {
    border-radius: 6px;
    background-color: chocolate;
}

/* Filter card spacing */
.p-inputtext,
.p-dropdown {
    border-radius: 8px;
    background-color: #b5c0bb;
    font-size: large;
    
}

/* Button hover smoothness */
.p-button {
    transition: all 0.2s ease;
}

.p-button:hover {
    transform: translateY(-1px);
}

/* Tag polish */
.p-tag {
    border-radius: 6px;
    font-weight: 1000;
}

/* Search input icon spacing */
.p-input-icon-left i {
    color: #2875e0;
}
</style>