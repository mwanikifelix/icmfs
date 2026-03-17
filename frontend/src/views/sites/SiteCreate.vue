<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <Button icon="pi pi-arrow-left" text rounded style="color:#fff;"
                    @click="$router.push('/app/sites')" />
                <div>
                    <h4 class="mt-0 mb-1" style="color:#fff;">Create New Site</h4>
                    <span class="text-sm" style="color:#b3c8e8;">Add a project site with location details</span>
                </div>
            </div>

            <Message v-if="apiError" severity="error" :closable="true" class="mb-3"
                @close="apiError = ''">{{ apiError }}</Message>

            <div class="card">

                <!-- ── SITE DETAILS ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #1976d2;">
                    <i class="pi pi-map-marker" style="color:#1976d2;" />
                    <span class="font-bold text-900">Site Details</span>
                </div>
                <div class="grid mb-4">
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Site Name <span class="text-red-500">*</span></label>
                        <InputText v-model="form.site_name" class="w-full"
                            placeholder="e.g. Changamwe Block A"
                            :class="{ 'p-invalid': errors.site_name }" />
                        <small class="p-error">{{ fieldErr('site_name') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Project <span class="text-red-500">*</span></label>
                        <Dropdown v-model="form.project" :options="projects"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select project" :loading="loadingProjects"
                            :class="{ 'p-invalid': errors.project }"
                            emptyMessage="No projects found" />
                        <small class="p-error">{{ fieldErr('project') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Town / Area</label>
                        <InputText v-model="form.town" class="w-full"
                            placeholder="e.g. Changamwe" />
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Status</label>
                        <Dropdown v-model="form.status" :options="statusOptions"
                            optionLabel="label" optionValue="value" class="w-full" />
                    </div>
                </div>

                <!-- ── LOCATION ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #2ecc71;">
                    <i class="pi pi-map" style="color:#2ecc71;" />
                    <span class="font-bold text-900">Location</span>
                    <span class="text-500 text-sm ml-1">— select from top to bottom</span>
                </div>
                <div class="grid mb-4">
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">County <span class="text-red-500">*</span></label>
                        <Dropdown v-model="form.county" :options="counties"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select county" :loading="loadingCounties"
                            :class="{ 'p-invalid': errors.county }"
                            emptyMessage="No available options"
                            @change="onCountyChange" />
                        <small class="p-error">{{ fieldErr('county') }}</small>
                    </div>
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">Sub-County</label>
                        <Dropdown v-model="form.sub_county" :options="subCounties"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select sub-county" :loading="loadingSubCounties"
                            :disabled="!form.county" showClear
                            emptyMessage="No available options — select a county first"
                            @change="onSubCountyChange" />
                    </div>
                    <div class="col-12 md:col-3 field">
                        <label class="block font-medium mb-2 text-600">Ward</label>
                        <Dropdown v-model="form.ward" :options="wards"
                            optionLabel="name" optionValue="id" class="w-full"
                            placeholder="Select ward" :loading="loadingWards"
                            :disabled="!form.sub_county" showClear
                            emptyMessage="No available options — select a sub-county first" />
                    </div>
                </div>

                <!-- ── GPS ── -->
                <div class="flex align-items-center gap-2 mb-3 pb-2" style="border-bottom:2px solid #e6a817;">
                    <i class="pi pi-compass" style="color:#e6a817;" />
                    <span class="font-bold text-900">GPS Coordinates</span>
                    <span class="text-500 text-sm ml-1">— optional</span>
                </div>
                <div class="grid mb-4">
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Latitude</label>
                        <InputNumber v-model="form.gps_latitude" class="w-full"
                            :minFractionDigits="6" :maxFractionDigits="6"
                            placeholder="e.g. -4.043477" />
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Longitude</label>
                        <InputNumber v-model="form.gps_longitude" class="w-full"
                            :minFractionDigits="6" :maxFractionDigits="6"
                            placeholder="e.g. 39.668206" />
                    </div>
                </div>

                <!-- Actions -->
                <div class="flex justify-content-end gap-3 pt-3"
                    style="border-top:1px solid var(--surface-200);">
                    <Button label="Cancel" text severity="secondary"
                        @click="$router.push('/app/sites')" />
                    <Button label="Create Site" icon="pi pi-check" :loading="saving"
                        style="background:#1976d2;border-color:#1976d2;"
                        @click="submit" />
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

const projects        = ref([]);
const counties        = ref([]);
const subCounties     = ref([]);
const wards           = ref([]);
const loadingProjects    = ref(false);
const loadingCounties    = ref(false);
const loadingSubCounties = ref(false);
const loadingWards       = ref(false);

const form = ref({
    site_name:    '',
    project:      null,
    town:         '',
    status:       'active',
    county:       null,
    sub_county:   null,
    ward:         null,
    gps_latitude: null,
    gps_longitude: null,
});

const fieldErr = (f) => { const e = errors.value[f]; return Array.isArray(e) ? e[0] : e || ''; };

const statusOptions = [
    { label: 'Active',    value: 'active'    },
    { label: 'On Hold',   value: 'on_hold'   },
    { label: 'Completed', value: 'completed' },
    { label: 'Inactive',  value: 'inactive'  },
];

async function loadProjects() {
    loadingProjects.value = true;
    try {
        const res = await api.get('/api/projects/projects/', { params: { ordering: 'name' } });
        projects.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingProjects.value = false; }
}

async function loadCounties() {
    loadingCounties.value = true;
    try {
        const res = await api.get('/api/projects/counties/');
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
    form.value.ward = null; wards.value = [];
    if (!form.value.sub_county) return;
    loadingWards.value = true;
    try {
        const res = await api.get('/api/projects/wards/', { params: { sub_county: form.value.sub_county } });
        wards.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } finally { loadingWards.value = false; }
}

function validate() {
    const e = {};
    if (!form.value.site_name.trim()) e.site_name = 'Required';
    if (!form.value.project)          e.project   = 'Required';
    if (!form.value.county)           e.county    = 'Required';
    errors.value = e;
    return !Object.keys(e).length;
}

async function submit() {
    if (!validate()) return;
    saving.value = true; apiError.value = '';
    try {
        const res = await api.post('/api/projects/sites/', form.value);
        router.push(`/app/sites/${res.data.id}`);
    } catch (e) {
        const data = e.response?.data;
        if (data && typeof data === 'object' && !data.detail) errors.value = data;
        else apiError.value = data?.detail || 'Failed to create site.';
    } finally { saving.value = false; }
}

onMounted(() => { loadProjects(); loadCounties(); });
</script>