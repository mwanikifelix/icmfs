<template>
    <div class="grid">
        <div class="col-12">

            <div v-if="loading" class="card flex justify-content-center py-6">
                <ProgressSpinner style="width:3rem;height:3rem;" />
            </div>

            <template v-else-if="site">

                <!-- Header -->
                <div class="border-round-xl mb-4 p-4"
                    style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                    <div class="flex align-items-start justify-content-between flex-wrap gap-3">
                        <div class="flex align-items-center gap-3">
                            <Button icon="pi pi-arrow-left" text rounded style="color:#fff;"
                                @click="$router.push('/app/sites')" />
                            <div>
                                <h4 class="mt-0 mb-1" style="color:#fff;">{{ site.site_name }}</h4>
                                <div class="flex flex-wrap gap-3 text-sm" style="color:#b3c8e8;">
                                    <span><i class="pi pi-map-marker mr-1" />{{ site.county_name_display }}</span>
                                    <span v-if="site.town"><i class="pi pi-map mr-1" />{{ site.town }}</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <Tag :value="fmtStatus(site.status)"
                                :severity="statusSeverity(site.status)" style="font-size:0.9rem;" />
                            <Button label="Edit" icon="pi pi-pencil" size="small"
                                style="background:#e6a817;border-color:#e6a817;color:#0d2347;"
                                @click="editDialog = true" />
                        </div>
                    </div>
                </div>

                <!-- Tab nav -->
                <div class="card mb-3 py-2">
                    <div class="flex gap-2 flex-wrap">
                        <Button v-for="tab in tabs" :key="tab.name"
                            :label="tab.label" :icon="tab.icon" size="small"
                            :outlined="activeTab !== tab.name"
                            :style="activeTab === tab.name
                                ? 'background:#1976d2;border-color:#1976d2;'
                                : 'border-color:#1976d2;color:#1976d2;'"
                            @click="activeTab = tab.name" />
                    </div>
                </div>

                <!-- ── OVERVIEW ── -->
                <div v-if="activeTab === 'overview'" class="grid">
                    <div class="col-12 lg:col-8">
                        <div class="card">
                            <h5 class="mt-0 mb-4" style="color:#0d2347;">Site Information</h5>
                            <div class="grid text-sm">
                                <div class="col-6 md:col-4 mb-3">
                                    <div class="text-500 mb-1">Project</div>
                                    <div class="font-medium text-900">{{ site.project_name || '—' }}</div>
                                </div>
                                <div class="col-6 md:col-4 mb-3">
                                    <div class="text-500 mb-1">County</div>
                                    <div class="font-medium text-900">{{ site.county_name_display || '—' }}</div>
                                </div>
                                <div class="col-6 md:col-4 mb-3">
                                    <div class="text-500 mb-1">Town / Area</div>
                                    <div class="font-medium text-900">{{ site.town || '—' }}</div>
                                </div>
                                <div class="col-6 md:col-4 mb-3">
                                    <div class="text-500 mb-1">Status</div>
                                    <Tag :value="fmtStatus(site.status)" :severity="statusSeverity(site.status)" />
                                </div>
                                <div class="col-6 md:col-4 mb-3">
                                    <div class="text-500 mb-1">Created</div>
                                    <div class="font-medium text-900">{{ fmtDate(site.created_at) }}</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- GPS -->
                    <div class="col-12 lg:col-4">
                        <div class="card h-full">
                            <h5 class="mt-0 mb-4" style="color:#0d2347;">GPS Location</h5>
                            <div v-if="site.gps_latitude">
                                <div class="p-3 border-round-lg mb-3" style="background:var(--surface-50);">
                                    <div class="text-500 text-xs mb-1">Latitude</div>
                                    <div class="font-mono font-bold text-900">{{ site.gps_latitude }}</div>
                                </div>
                                <div class="p-3 border-round-lg mb-3" style="background:var(--surface-50);">
                                    <div class="text-500 text-xs mb-1">Longitude</div>
                                    <div class="font-mono font-bold text-900">{{ site.gps_longitude }}</div>
                                </div>
                                <a :href="`https://maps.google.com/?q=${site.gps_latitude},${site.gps_longitude}`"
                                    target="_blank" class="w-full">
                                    <Button label="View on Google Maps" icon="pi pi-map"
                                        outlined class="w-full" style="border-color:#1976d2;color:#1976d2;" />
                                </a>
                            </div>
                            <div v-else class="text-500 text-sm text-center py-3">
                                No GPS coordinates recorded.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ── DAILY REPORTS ── -->
                <div v-if="activeTab === 'reports'" class="card">
                    <div class="flex justify-content-between align-items-center mb-4">
                        <h5 class="mt-0 mb-0" style="color:#0d2347;">Daily Reports</h5>
                        <Button label="New Report" icon="pi pi-plus" size="small"
                            style="background:#1976d2;border-color:#1976d2;"
                            @click="$router.push('/app/sites/daily-reports')" />
                    </div>
                    <p class="text-500">Daily site reports will appear here.</p>
                </div>

                <!-- ── WORKFORCE ── -->
                <div v-if="activeTab === 'workforce'" class="card">
                    <h5 class="mt-0 mb-4" style="color:#0d2347;">Workforce</h5>
                    <p class="text-500">Workforce management for this site will appear here.</p>
                </div>

            </template>

            <div v-else class="card text-center py-6">
                <i class="pi pi-exclamation-triangle text-4xl mb-3 block" style="color:#e6a817;" />
                <div class="text-900 font-bold mb-2">Site not found</div>
                <Button label="Back to Sites" icon="pi pi-arrow-left"
                    @click="$router.push('/app/sites')" />
            </div>
        </div>

        <!-- Edit Dialog -->
        <Dialog v-model:visible="editDialog" header="Edit Site" :modal="true" style="width:520px;">
            <div class="grid mt-2">
                <div class="col-12 field">
                    <label class="block font-medium mb-2 text-600">Site Name</label>
                    <InputText v-model="editForm.site_name" class="w-full" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Town</label>
                    <InputText v-model="editForm.town" class="w-full" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Status</label>
                    <Dropdown v-model="editForm.status" :options="statusOptions"
                        optionLabel="label" optionValue="value" class="w-full" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Latitude</label>
                    <InputNumber v-model="editForm.gps_latitude" class="w-full"
                        :minFractionDigits="6" :maxFractionDigits="6" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Longitude</label>
                    <InputNumber v-model="editForm.gps_longitude" class="w-full"
                        :minFractionDigits="6" :maxFractionDigits="6" />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" text @click="editDialog = false" />
                <Button label="Save" icon="pi pi-check" :loading="saving"
                    style="background:#1976d2;border-color:#1976d2;" @click="saveSite" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api/api';

const route     = useRoute();
const site      = ref(null);
const loading   = ref(false);
const saving    = ref(false);
const editDialog = ref(false);
const activeTab  = ref('overview');
const editForm   = ref({});

const tabs = [
    { name: 'overview',  label: 'Overview',      icon: 'pi pi-eye'        },
    { name: 'reports',   label: 'Daily Reports',  icon: 'pi pi-file-edit'  },
    { name: 'workforce', label: 'Workforce',      icon: 'pi pi-users'      },
];

const statusOptions = [
    { label: 'Active',    value: 'active'    },
    { label: 'On Hold',   value: 'on_hold'   },
    { label: 'Completed', value: 'completed' },
    { label: 'Inactive',  value: 'inactive'  },
];

const fmtDate = (d) => d ? new Date(d).toLocaleDateString('en-KE', { day:'2-digit', month:'short', year:'numeric' }) : '—';
const fmtStatus = (s) => ({ active:'Active', on_hold:'On Hold', completed:'Completed', inactive:'Inactive' }[s] || s);
const statusSeverity = (s) => ({ active:'success', on_hold:'warn', completed:'info', inactive:'secondary' }[s] || 'info');

async function loadSite() {
    loading.value = true;
    try {
        const res = await api.get(`/api/projects/sites/${route.params.id}/`);
        site.value = res.data;
        editForm.value = {
            site_name:     res.data.site_name,
            town:          res.data.town,
            status:        res.data.status,
            gps_latitude:  res.data.gps_latitude  ? Number(res.data.gps_latitude)  : null,
            gps_longitude: res.data.gps_longitude ? Number(res.data.gps_longitude) : null,
        };
    } catch { site.value = null; }
    finally  { loading.value = false; }
}

async function saveSite() {
    saving.value = true;
    try {
        const res = await api.patch(`/api/projects/sites/${route.params.id}/`, editForm.value);
        site.value = { ...site.value, ...res.data };
        editDialog.value = false;
    } finally { saving.value = false; }
}

onMounted(loadSite);
</script>