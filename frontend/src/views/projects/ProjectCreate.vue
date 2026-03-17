<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <Button icon="pi pi-arrow-left" text rounded style="color:#fff;"
                        @click="$router.push('/app/projects')" />
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">Create New Project</h4>
                        <span class="text-sm" style="color:#b3c8e8;">Fill in the details to register a new project</span>
                    </div>
                </div>
            </div>

            <Message v-if="apiError" severity="error" :closable="true" class="mb-3"
                @close="apiError = ''">{{ apiError }}</Message>

            <div class="card">
                <Message severity="info" :closable="false" class="mb-4">
                    You can save this project as a draft and complete remaining details later.
                </Message>

                <!-- ── BASIC INFORMATION ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #1976d2;">
                    <i class="pi pi-briefcase" style="color:#1976d2;" />
                    <span class="font-bold text-900">Basic Information</span>
                </div>
                <div class="grid mb-4">
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Project Name <span class="text-red-500">*</span></label>
                        <InputText v-model="form.name" class="w-full"
                            placeholder="e.g. Mombasa Affordable Housing Phase 1"
                            :class="{ 'p-invalid': errors.name }" />
                        <small class="p-error">{{ fieldErr('name') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Client / Sponsor <span class="text-red-500">*</span></label>
                        <InputText v-model="form.client_name" class="w-full"
                            placeholder="e.g. Ministry of Housing"
                            :class="{ 'p-invalid': errors.client_name }" />
                        <small class="p-error">{{ fieldErr('client_name') }}</small>
                    </div>
                    <div class="col-12 field">
                        <label class="block font-medium mb-2 text-600">Description</label>
                        <Textarea v-model="form.description" rows="4" class="w-full"
                            placeholder="Project objectives, scope and key deliverables..." />
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
                        <small class="p-error">{{ fieldErr('start_date') }}</small>
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Expected End Date</label>
                        <Calendar v-model="form.end_date" dateFormat="yy-mm-dd" showIcon class="w-full"
                            :minDate="form.start_date" />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Budget (KES)</label>
                        <InputNumber v-model="form.budget" mode="decimal" :useGrouping="true"
                            class="w-full" placeholder="e.g. 50000000" />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Status <span class="text-red-500">*</span></label>
                        <Dropdown v-model="form.status" :options="statusOptions"
                            optionLabel="label" optionValue="value" class="w-full"
                            placeholder="Select status"
                            :class="{ 'p-invalid': errors.status }" />
                        <small class="p-error">{{ fieldErr('status') }}</small>
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Owner Type</label>
                        <Dropdown v-model="form.owner_type" :options="ownerTypeOptions"
                            optionLabel="label" optionValue="value" class="w-full"
                            placeholder="Select owner type" showClear />
                    </div>
                </div>

                <!-- ── LOCATION ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #2ecc71;">
                    <i class="pi pi-map-marker" style="color:#2ecc71;" />
                    <span class="font-bold text-900">Location</span>
                    <span class="text-500 text-sm ml-1">— select from top to bottom</span>
                </div>
                <div class="grid mb-4">
                    <!-- Region -->
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">Region <span class="text-red-500">*</span></label>
                        <Dropdown v-model="form.region" :options="regions"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select region" :loading="loadingRegions"
                            :class="{ 'p-invalid': errors.region }"
                            @change="onRegionChange" />
                        <small class="p-error">{{ fieldErr('region') }}</small>
                    </div>

                    <!-- County -->
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">County</label>
                        <Dropdown v-model="form.county" :options="counties"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select county" :loading="loadingCounties"
                            :disabled="!form.region" showClear
                            emptyMessage="No available options — select a region first"
                            @change="onCountyChange" />
                    </div>

                    <!-- Sub-County -->
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">Sub-County</label>
                        <Dropdown v-model="form.sub_county" :options="subCounties"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select sub-county" :loading="loadingSubCounties"
                            :disabled="!form.county" showClear
                            emptyMessage="No available options — select a county first"
                            @change="onSubCountyChange" />
                    </div>

                    <!-- Ward -->
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">Ward</label>
                        <Dropdown v-model="form.ward" :options="wards"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select ward" :loading="loadingWards"
                            :disabled="!form.sub_county" showClear
                            emptyMessage="No available options — select a sub-county first" />
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
                            optionLabel="label" optionValue="value" class="w-full"
                            placeholder="Select category" showClear />
                    </div>
                    <div class="col-12 md:col-4 field">
                        <label class="block font-medium mb-2 text-600">Sector</label>
                        <Dropdown v-model="form.sector" :options="sectorOptions"
                            optionLabel="label" optionValue="value" class="w-full"
                            placeholder="Select sector" showClear />
                    </div>
                </div>

                <!-- Actions -->
                <div class="flex justify-content-end gap-3 pt-3" style="border-top:1px solid var(--surface-200);">
                    <Button label="Cancel" text severity="secondary"
                        @click="$router.push('/app/projects')" />
                    <Button label="Save as Draft" icon="pi pi-save" outlined
                        :loading="saving" @click="submit('planned')" />
                    <Button label="Create Project" icon="pi pi-check" :loading="saving"
                        style="background:#1976d2;border-color:#1976d2;"
                        @click="submit(null)" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api/api';

const router   = useRouter();
const saving   = ref(false);
const apiError = ref('');
const errors   = ref({});

// ── Location cascading state ───────────────────────────────────
const regions          = ref([]);
const counties         = ref([]);
const subCounties      = ref([]);
const wards            = ref([]);
const loadingRegions    = ref(false);
const loadingCounties   = ref(false);
const loadingSubCounties = ref(false);
const loadingWards      = ref(false);

// ── Form ──────────────────────────────────────────────────────
const form = ref({
    name: '', client_name: '', description: '',
    start_date: null, end_date: null, budget: null,
    status: 'planned', owner_type: '',
    region: null, county: null, sub_county: null, ward: null,
    category: '', sector: '', progress: 0,
});

const fieldErr = (f) => { const e = errors.value[f]; return Array.isArray(e) ? e[0] : e || ''; };

// ── Dropdown options ──────────────────────────────────────────
const statusOptions = [
    { label: 'Planned',     value: 'planned'     },
    { label: 'Active',      value: 'active'      },
    { label: 'In Progress', value: 'in_progress' },
    { label: 'On Hold',     value: 'on_hold'     },
    { label: 'Completed',   value: 'completed'   },
];
const ownerTypeOptions = [
    { label: 'Government',  value: 'government'  },
    { label: 'Private',     value: 'private'     },
    { label: 'NGO',         value: 'ngo'         },
    { label: 'PPP',         value: 'ppp'         },
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
];

// ── API loaders ───────────────────────────────────────────────
async function loadRegions() {
    loadingRegions.value = true;
    try {
        const res = await api.get('/api/projects/regions/');
        regions.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } catch { apiError.value = 'Failed to load regions.'; }
    finally  { loadingRegions.value = false; }
}

async function onRegionChange() {
    form.value.county = form.value.sub_county = form.value.ward = null;
    counties.value = subCounties.value = wards.value = [];
    if (!form.value.region) return;
    loadingCounties.value = true;
    try {
        const res = await api.get('/api/projects/counties/', { params: { region: form.value.region } });
        counties.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingCounties.value = false; }
}

async function onCountyChange() {
    form.value.sub_county = form.value.ward = null;
    subCounties.value = wards.value = [];
    if (!form.value.county) return;
    loadingSubCounties.value = true;
    try {
        const res = await api.get('/api/projects/subcounties/', { params: { county: form.value.county } });
        subCounties.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingSubCounties.value = false; }
}

async function onSubCountyChange() {
    form.value.ward = null;
    wards.value = [];
    if (!form.value.sub_county) return;
    loadingWards.value = true;
    try {
        const res = await api.get('/api/projects/wards/', { params: { sub_county: form.value.sub_county } });
        wards.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingWards.value = false; }
}

// ── Validate ──────────────────────────────────────────────────
function validate() {
    const e = {};
    if (!form.value.name.trim())        e.name        = 'Required';
    if (!form.value.client_name.trim()) e.client_name = 'Required';
    if (!form.value.start_date)         e.start_date  = 'Required';
    if (!form.value.status)             e.status      = 'Required';
    if (!form.value.region)             e.region      = 'Required';
    errors.value = e;
    return !Object.keys(e).length;
}

function fmtDate(d) {
    if (!d) return null;
    if (typeof d === 'string') return d;
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

// ── Submit ────────────────────────────────────────────────────
async function submit(forceStatus) {
    if (!validate()) return;
    saving.value = true; apiError.value = '';
    try {
        const res = await api.post('/api/projects/projects/', {
            ...form.value,
            status:     forceStatus || form.value.status,
            start_date: fmtDate(form.value.start_date),
            end_date:   fmtDate(form.value.end_date),
        });
        router.push(`/app/projects/${res.data.id}`);
    } catch (e) {
        const data = e.response?.data;
        if (data && typeof data === 'object' && !data.detail) errors.value = data;
        else apiError.value = data?.detail || 'Failed to create project.';
    } finally { saving.value = false; }
}

onMounted(loadRegions);
</script>