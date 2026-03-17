<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-map-marker text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">Project Sites</h4>
                        <span class="text-sm" style="color:#b3c8e8;">{{ sites.length }} sites loaded</span>
                    </div>
                </div>
                <Button label="New Site" icon="pi pi-plus"
                    style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                    @click="$router.push('/app/sites/create')" />
            </div>

            <!-- Stats -->
            <div class="grid mb-3">
                <div class="col-6 lg:col-3">
                    <div class="card mb-0">
                        <div class="flex justify-content-between align-items-start">
                            <div>
                                <div class="text-500 text-sm mb-1">Total Sites</div>
                                <div class="font-bold text-3xl text-900">{{ sites.length }}</div>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round"
                                style="width:2.5rem;height:2.5rem;background:#e8f0fe;">
                                <i class="pi pi-map-marker" style="color:#1976d2;" />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-6 lg:col-3">
                    <div class="card mb-0">
                        <div class="flex justify-content-between align-items-start">
                            <div>
                                <div class="text-500 text-sm mb-1">Active</div>
                                <div class="font-bold text-3xl" style="color:#2ecc71;">
                                    {{ sites.filter(s => s.status === 'active').length }}
                                </div>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round"
                                style="width:2.5rem;height:2.5rem;background:#e8fdf0;">
                                <i class="pi pi-check-circle" style="color:#2ecc71;" />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-6 lg:col-3">
                    <div class="card mb-0">
                        <div class="flex justify-content-between align-items-start">
                            <div>
                                <div class="text-500 text-sm mb-1">On Hold</div>
                                <div class="font-bold text-3xl" style="color:#e6a817;">
                                    {{ sites.filter(s => s.status === 'on_hold').length }}
                                </div>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round"
                                style="width:2.5rem;height:2.5rem;background:#fef9e7;">
                                <i class="pi pi-pause-circle" style="color:#e6a817;" />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-6 lg:col-3">
                    <div class="card mb-0">
                        <div class="flex justify-content-between align-items-start">
                            <div>
                                <div class="text-500 text-sm mb-1">Completed</div>
                                <div class="font-bold text-3xl" style="color:#1976d2;">
                                    {{ sites.filter(s => s.status === 'completed').length }}
                                </div>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round"
                                style="width:2.5rem;height:2.5rem;background:#e8f0fe;">
                                <i class="pi pi-flag-fill" style="color:#1976d2;" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <Message v-if="apiError" severity="error" :closable="true" class="mb-3"
                @close="apiError = ''">{{ apiError }}</Message>

            <!-- Filters -->
            <div class="card mb-3">
                <div class="flex flex-wrap gap-3 align-items-end">
                    <div class="p-input-icon-left" style="flex:1;min-width:200px;">
                        <i class="pi pi-search" />
                        <InputText v-model="search" placeholder="Search sites..."
                            class="w-full" @input="onSearch" />
                    </div>
                    <Dropdown v-model="filterProject" :options="projects"
                        optionLabel="name" optionValue="id"
                        placeholder="All Projects" showClear style="min-width:200px;"
                        :loading="loadingProjects" @change="loadSites" />
                    <Dropdown v-model="filterStatus" :options="statusOptions"
                        optionLabel="label" optionValue="value"
                        placeholder="All Statuses" showClear style="min-width:150px;"
                        @change="loadSites" />
                    <Button icon="pi pi-refresh" outlined severity="secondary"
                        :loading="loading" @click="loadSites" />
                </div>
            </div>

            <!-- Table -->
            <div class="card">
                <DataTable :value="sites" :loading="loading"
                    :paginator="true" :rows="10" :rowsPerPageOptions="[5,10,20,50]"
                    stripedRows responsiveLayout="scroll"
                    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                    currentPageReportTemplate="{first}–{last} of {totalRecords}">

                    <Column header="Site Name" sortable sortField="site_name" style="min-width:200px;">
                        <template #body="{ data }">
                            <div>
                                <div class="font-semibold text-900">{{ data.site_name }}</div>
                                <div class="text-500 text-xs mt-1">
                                    <i class="pi pi-map-marker text-xs mr-1" />
                                    {{ data.county_name_display }}
                                    <span v-if="data.town"> · {{ data.town }}</span>
                                </div>
                            </div>
                        </template>
                    </Column>

                    <Column header="Project">
                        <template #body="{ data }">
                            <span class="text-sm text-600">{{ data.project_name || '—' }}</span>
                        </template>
                    </Column>

                    <Column header="Location">
                        <template #body="{ data }">
                            <div class="text-sm">
                                <div v-if="data.county_name_display" class="text-600">{{ data.county_name_display }}</div>
                                <div v-if="data.town" class="text-400 text-xs">{{ data.town }}</div>
                            </div>
                        </template>
                    </Column>

                    <Column header="GPS">
                        <template #body="{ data }">
                            <span v-if="data.gps_latitude" class="text-xs font-mono text-500">
                                {{ Number(data.gps_latitude).toFixed(4) }},
                                {{ Number(data.gps_longitude).toFixed(4) }}
                            </span>
                            <span v-else class="text-400 text-xs">—</span>
                        </template>
                    </Column>

                    <Column header="Status">
                        <template #body="{ data }">
                            <Tag :value="fmtStatus(data.status)"
                                :severity="statusSeverity(data.status)" />
                        </template>
                    </Column>

                    <Column header="Actions" style="width:100px;">
                        <template #body="{ data }">
                            <div class="flex gap-1">
                                <Button icon="pi pi-eye" text rounded size="small"
                                    v-tooltip.top="'View'"
                                    @click="$router.push(`/app/sites/${data.id}`)" />
                                <Button icon="pi pi-pencil" text rounded size="small"
                                    severity="secondary" v-tooltip.top="'Edit'"
                                    @click="openEdit(data)" />
                                <Button icon="pi pi-trash" text rounded size="small"
                                    severity="danger" v-tooltip.top="'Delete'"
                                    @click="confirmDelete(data)" />
                            </div>
                        </template>
                    </Column>

                    <template #empty>
                        <div class="text-center py-6 text-500">
                            <i class="pi pi-map-marker text-4xl mb-2 block text-300" />
                            <div>No sites found.</div>
                            <Button label="Create First Site" icon="pi pi-plus" class="mt-3" size="small"
                                style="background:#1976d2;border-color:#1976d2;"
                                @click="$router.push('/app/sites/create')" />
                        </div>
                    </template>
                </DataTable>
            </div>
        </div>

        <!-- Delete confirm dialog -->
        <Dialog v-model:visible="deleteDialog" header="Delete Site" :modal="true" style="width:380px;">
            <p class="text-600">Are you sure you want to delete <strong>{{ siteToDelete?.site_name }}</strong>? This cannot be undone.</p>
            <template #footer>
                <Button label="Cancel" text @click="deleteDialog = false" />
                <Button label="Delete" severity="danger" icon="pi pi-trash"
                    :loading="deleting" @click="deleteSite" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api/api';

const sites          = ref([]);
const projects       = ref([]);
const loading        = ref(false);
const loadingProjects = ref(false);
const apiError       = ref('');
const search         = ref('');
const filterProject  = ref(null);
const filterStatus   = ref(null);
const deleteDialog   = ref(false);
const deleting       = ref(false);
const siteToDelete   = ref(null);

const statusOptions = [
    { label: 'Active',    value: 'active'    },
    { label: 'On Hold',   value: 'on_hold'   },
    { label: 'Completed', value: 'completed' },
    { label: 'Inactive',  value: 'inactive'  },
];

const fmtStatus = (s) => ({ active:'Active', on_hold:'On Hold', completed:'Completed', inactive:'Inactive' }[s] || s);
const statusSeverity = (s) => ({ active:'success', on_hold:'warn', completed:'info', inactive:'secondary' }[s] || 'info');

async function loadProjects() {
    loadingProjects.value = true;
    try {
        const res = await api.get('/api/projects/projects/', { params: { ordering: 'name' } });
        projects.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingProjects.value = false; }
}

async function loadSites() {
    loading.value  = true;
    apiError.value = '';
    try {
        const params = {};
        if (filterProject.value) params.project = filterProject.value;
        if (filterStatus.value)  params.status  = filterStatus.value;
        if (search.value)        params.search  = search.value;

        const res = await api.get('/api/projects/sites/', { params });
        const raw = Array.isArray(res.data) ? res.data : (res.data.results ?? []);

        // Attach project name from projects list
        const projectMap = Object.fromEntries(projects.value.map(p => [p.id, p.name]));
        sites.value = raw.map(s => ({ ...s, project_name: projectMap[s.project] || '—' }));
    } catch (e) {
        apiError.value = e.response?.data?.detail || 'Failed to load sites.';
    } finally { loading.value = false; }
}

let searchTimer = null;
function onSearch() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadSites, 400);
}

function openEdit(site) {
    // Navigate to site detail edit tab
    window.$router?.push(`/app/sites/${site.id}`);
}

function confirmDelete(site) {
    siteToDelete.value = site;
    deleteDialog.value = true;
}

async function deleteSite() {
    deleting.value = true;
    try {
        await api.delete(`/api/projects/sites/${siteToDelete.value.id}/`);
        deleteDialog.value = false;
        await loadSites();
    } catch (e) {
        apiError.value = 'Failed to delete site.';
    } finally { deleting.value = false; }
}

onMounted(async () => {
    await loadProjects();
    await loadSites();
});
</script>