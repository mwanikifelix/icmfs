<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <Button icon="pi pi-arrow-left" text rounded style="color:#fff;"
                    @click="$router.push(`/app/projects/${route.params.id}`)" />
                <div>
                    <h4 class="mt-0 mb-1" style="color:#fff;">Edit Project</h4>
                    <span class="text-sm" style="color:#b3c8e8;">{{ form.name || 'Loading...' }}</span>
                </div>
            </div>

            <Message v-if="apiError" severity="error" :closable="true" class="mb-3"
                @close="apiError = ''">{{ apiError }}</Message>

            <!-- Loading skeleton -->
            <div v-if="loading" class="card flex justify-content-center py-6">
                <ProgressSpinner style="width:3rem;height:3rem;" />
            </div>

            <div v-else class="card">

                <!-- ── BASIC INFORMATION ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #1976d2;">
                    <i class="pi pi-briefcase" style="color:#1976d2;" />
                    <span class="font-bold text-900">Basic Information</span>
                </div>
                <div class="grid mb-4">
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Project Name <span class="text-red-500">*</span></label>
                        <InputText v-model="form.name" class="w-full"
                            :class="{ 'p-invalid': errors.name }" />
                        <small class="p-error">{{ fieldErr('name') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Client / Sponsor <span class="text-red-500">*</span></label>
                        <InputText v-model="form.client_name" class="w-full"
                            :class="{ 'p-invalid': errors.client_name }" />
                        <small class="p-error">{{ fieldErr('client_name') }}</small>
                    </div>
                    <div class="col-12 field">
                        <label class="block font-medium mb-2 text-600">Description</label>
                        <Textarea v-model="form.description" rows="4" class="w-full" />
                    </div>
                </div>

                <!-- ── SCHEDULE & BUDGET ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #e6a817;">
                    <i class="pi pi-calendar" style="color:#e6a817;" />
                    <span class="font-bold text-900">Schedule & Budget</span>
                </div>
                <div class="grid mb-4">
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Start Date <span class="text-red-500">*</span></label>
                        <Calendar v-model="form.start_date" dateFormat="yy-mm-dd" showIcon class="w-full"
                            :class="{ 'p-invalid': errors.start_date }" />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">End Date</label>
                        <Calendar v-model="form.end_date" dateFormat="yy-mm-dd" showIcon class="w-full" />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Budget (KES)</label>
                        <InputNumber v-model="form.budget" mode="decimal" :useGrouping="true" class="w-full" />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Status</label>
                        <Dropdown v-model="form.status" :options="statusOptions"
                            optionLabel="label" optionValue="value" class="w-full" />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Owner Type</label>
                        <Dropdown v-model="form.owner_type" :options="ownerTypeOptions"
                            optionLabel="label" optionValue="value" class="w-full" showClear />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Progress (%)</label>
                        <InputNumber v-model="form.progress" :min="0" :max="100" class="w-full"
                            suffix="%" />
                    </div>
                </div>

                <!-- ── LOCATION ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #2ecc71;">
                    <i class="pi pi-map-marker" style="color:#2ecc71;" />
                    <span class="font-bold text-900">Location</span>
                </div>
                <div class="grid mb-4">
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">Region</label>
                        <Dropdown v-model="form.region" :options="regions"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select region" :loading="loadingRegions"
                            showClear @change="onRegionChange" />
                    </div>
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">County</label>
                        <Dropdown v-model="form.county" :options="counties"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select county" :loading="loadingCounties"
                            :disabled="!form.region" showClear @change="onCountyChange" />
                    </div>
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">Sub-County</label>
                        <Dropdown v-model="form.sub_county" :options="subCounties"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select sub-county" :loading="loadingSubCounties"
                            :disabled="!form.county" showClear @change="onSubCountyChange" />
                    </div>
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">Ward</label>
                        <Dropdown v-model="form.ward" :options="wards"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select ward" :loading="loadingWards"
                            :disabled="!form.sub_county" showClear />
                    </div>
                </div>

                <!-- ── CLASSIFICATION ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #a855f7;">
                    <i class="pi pi-tags" style="color:#a855f7;" />
                    <span class="font-bold text-900">Classification</span>
                </div>
                <div class="grid mb-4">
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Category</label>
                        <Dropdown v-model="form.category" :options="categoryOptions"
                            optionLabel="label" optionValue="value" class="w-full" showClear />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Sector</label>
                        <Dropdown v-model="form.sector" :options="sectorOptions"
                            optionLabel="label" optionValue="value" class="w-full" showClear />
                    </div>
                </div>

                <!-- Actions -->
                <div class="flex justify-content-end gap-3 pt-3" style="border-top:1px solid var(--surface-200);">
                    <Button label="Cancel" text severity="secondary"
                        @click="$router.push(`/app/projects/${route.params.id}`)" />
                    <Button label="Save Changes" icon="pi pi-check" :loading="saving"
                        style="background:#1976d2;border-color:#1976d2;" @click="save" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api/api';

const route  = useRoute();
const router = useRouter();

const loading  = ref(false);
const saving   = ref(false);
const apiError = ref('');
const errors   = ref({});

const regions         = ref([]);
const counties        = ref([]);
const subCounties     = ref([]);
const wards           = ref([]);
const loadingRegions    = ref(false);
const loadingCounties   = ref(false);
const loadingSubCounties = ref(false);
const loadingWards      = ref(false);

const form = ref({
    name: '', client_name: '', description: '',
    start_date: null, end_date: null, budget: null, progress: 0,
    status: 'planned', owner_type: '',
    region: null, county: null, sub_county: null, ward: null,
    category: '', sector: '',
});

const fieldErr = (f) => { const e = errors.value[f]; return Array.isArray(e) ? e[0] : e || ''; };

const statusOptions = [
    { label: 'Planned',     value: 'planned'     },
    { label: 'Active',      value: 'active'      },
    { label: 'In Progress', value: 'in_progress' },
    { label: 'On Hold',     value: 'on_hold'     },
    { label: 'At Risk',     value: 'at_risk'     },
    { label: 'Completed',   value: 'completed'   },
    { label: 'Cancelled',   value: 'cancelled'   },
];
const ownerTypeOptions = [
    { label: 'Government',  value: 'government'  },
    { label: 'Private',     value: 'private'     },
    { label: 'NGO',         value: 'ngo'         },
    { label: 'ppp',         value: 'ppp'         },
    { label: 'Faith-Based', value: 'faith_based' },
    { label: 'Other',       value: 'other'       },
];
const categoryOptions = [
    { label: 'Affordable Housing', value: 'affordable_housing' },
    { label: 'Infrastructure',     value: 'infrastructure'     },
    { label: 'Commercial',         value: 'commercial'         },
    { label: 'Residential',        value: 'residential'        },
    { label: 'Mixed-Use',          value: 'mixed_use'          },
    { label: 'Health',             value: 'health'             },
    { label: 'Education',          value: 'education'          },
    { label: 'Water & Sanitation', value: 'water_sanitation'   },
    { label: 'Energy',             value: 'energy'             },
    { label: 'ICT',                value: 'ict'                },
];
const sectorOptions = [
    { label: 'Housing',            value: 'housing'        },
    { label: 'Infrastructure',     value: 'infrastructure' },
    { label: 'Health',             value: 'health'         },
    { label: 'Education',          value: 'education'      },
    { label: 'Commercial',         value: 'commercial'     },
    { label: 'Water & Sanitation', value: 'water'          },
    { label: 'Energy',             value: 'energy'         },
    { label: 'Transport',          value: 'transport'      },
    {label:  'Trade',               value:   'tarade'       },
];

async function loadRegions() {
    loadingRegions.value = true;
    try {
        const res = await api.get('/api/projects/regions/');
        regions.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingRegions.value = false; }
}

async function loadCounties(regionId) {
    if (!regionId) return;
    loadingCounties.value = true;
    try {
        const res = await api.get('/api/projects/counties/', { params: { region: regionId } });
        counties.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingCounties.value = false; }
}

async function loadSubCounties(countyId) {
    if (!countyId) return;
    loadingSubCounties.value = true;
    try {
        const res = await api.get('/api/projects/subcounties/', { params: { county: countyId } });
        subCounties.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingSubCounties.value = false; }
}

async function loadWards(scId) {
    if (!scId) return;
    loadingWards.value = true;
    try {
        const res = await api.get('/api/projects/wards/', { params: { sub_county: scId } });
        wards.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingWards.value = false; }
}

async function onRegionChange() {
    form.value.county = form.value.sub_county = form.value.ward = null;
    counties.value = subCounties.value = wards.value = [];
    await loadCounties(form.value.region);
}
async function onCountyChange() {
    form.value.sub_county = form.value.ward = null;
    subCounties.value = wards.value = [];
    await loadSubCounties(form.value.county);
}
async function onSubCountyChange() {
    form.value.ward = null; wards.value = [];
    await loadWards(form.value.sub_county);
}

function parseDate(d) {
    if (!d) return null;
    if (d instanceof Date) return d;
    return new Date(d);
}
function fmtDate(d) {
    if (!d) return null;
    if (typeof d === 'string') return d;
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

async function loadProject() {
    loading.value = true;
    try {
        const res = await api.get(`/api/projects/projects/${route.params.id}/`);
        const p   = res.data;

        form.value = {
            name:        p.name        || '',
            client_name: p.client_name || p.sponsor_name || '',
            description: p.description || '',
            start_date:  parseDate(p.start_date),
            end_date:    parseDate(p.end_date),
            budget:      p.budget ? Number(p.budget) : null,
            progress:    p.progress || 0,
            status:      p.status      || 'planned',
            owner_type:  p.owner_type  || '',
            region:      p.region      || null,
            county:      p.county      || null,
            sub_county:  p.sub_county  || null,
            ward:        p.ward        || null,
            category:    p.category    || '',
            sector:      p.sector      || '',
        };

        // Load cascading dropdowns for existing values
        await loadRegions();
        if (p.region)     await loadCounties(p.region);
        if (p.county)     await loadSubCounties(p.county);
        if (p.sub_county) await loadWards(p.sub_county);

    } catch (e) {
        apiError.value = 'Failed to load project.';
    } finally {
        loading.value = false;
    }
}

async function save() {
    if (!form.value.name.trim()) { errors.value = { name: 'Required' }; return; }
    saving.value = true; apiError.value = '';
    try {
        await api.put(`/api/projects/projects/${route.params.id}/`, {
            ...form.value,
            start_date: fmtDate(form.value.start_date),
            end_date:   fmtDate(form.value.end_date),
        });
        router.push(`/app/projects/${route.params.id}`);
    } catch (e) {
        const data = e.response?.data;
        if (data && typeof data === 'object' && !data.detail) errors.value = data;
        else apiError.value = data?.detail || 'Failed to save project.';
    } finally { saving.value = false; }
}

onMounted(loadProject);
</script>