<template>
<div class="grid">
<div class="col-12">

<!-- Loading -->
<div v-if="loading" class="card flex justify-content-center py-6">
<ProgressSpinner style="width:3rem;height:3rem;" />
</div>

<template v-else-if="project">

<!-- ================= HEADER ================= -->
<div class="border-round-xl mb-4 p-4"
style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">

<div class="flex align-items-start justify-content-between flex-wrap gap-3">

<div class="flex align-items-center gap-3">

<Button
icon="pi pi-arrow-left"
text
rounded
style="color:#fff;"
@click="$router.push('/app/projects')"
/>

<div>
<h4 class="mt-0 mb-1" style="color:#fff;">
{{ project.name }}
</h4>

<div class="flex flex-wrap gap-3 text-sm" style="color:#b3c8e8;">

<span>
<i class="pi pi-user mr-1" />
{{ project.sponsor_name }}
</span>

<span v-if="project.region_detail">
<i class="pi pi-map-marker mr-1" />
{{ project.region_detail.name }}
</span>

<span v-if="project.county_detail">
<i class="pi pi-map mr-1" />
{{ project.county_detail.name }}
</span>

</div>
</div>
</div>

<div class="flex gap-2">

<Tag
:value="project.status_display || project.status"
:severity="statusSeverity(project.status)"
style="font-size:0.9rem;"
/>

<Button
label="Edit"
icon="pi pi-pencil"
size="small"
style="background:#e6a817;border-color:#e6a817;color:#0d2347;"
@click="$router.push(`/app/projects/${project.id}/edit`)"
/>

</div>
</div>
</div>

<!-- ================= TAB NAV ================= -->
<div class="card mb-3 py-2">

<div class="flex gap-2 flex-wrap">

<Button
v-for="tab in tabs"
:key="tab.name"
:label="tab.label"
:icon="tab.icon"
size="small"
:outlined="activeTab !== tab.name"
:style="activeTab === tab.name
? 'background:#1976d2;border-color:#1976d2;'
: 'border-color:#1976d2;color:#1976d2;'"
@click="activeTab = tab.name"
/>

</div>
</div>

<!-- ================= OVERVIEW ================= -->
<div v-if="activeTab === 'overview'" class="grid">

<div class="col-6 lg:col-3">
<div class="card mb-0 text-center">
<div class="text-500 text-sm mb-1">Budget (KES)</div>
<div class="font-bold text-xl text-900">
{{ project.budget ? fmtBudget(project.budget) : '—' }}
</div>
</div>
</div>

<div class="col-6 lg:col-3">
<div class="card mb-0 text-center">
<div class="text-500 text-sm mb-1">Progress</div>
<div class="font-bold text-xl" style="color:#1976d2;">
{{ project.progress || 0 }}%
</div>
</div>
</div>

<div class="col-6 lg:col-3">
<div class="card mb-0 text-center">
<div class="text-500 text-sm mb-1">Start Date</div>
<div class="font-bold text-xl text-900">
{{ fmtDate(project.start_date) }}
</div>
</div>
</div>

<div class="col-6 lg:col-3">
<div class="card mb-0 text-center">
<div class="text-500 text-sm mb-1">End Date</div>
<div class="font-bold text-xl text-900">
{{ fmtDate(project.end_date) || '—' }}
</div>
</div>
</div>

<!-- Project Details -->
<div class="col-12 lg:col-8">

<div class="card">

<h5 class="mt-0 mb-4" style="color:#0d2347;">
Project Details
</h5>

<div class="mb-4">

<div class="flex justify-content-between mb-2">

<span class="text-600 text-sm font-medium">
Overall Progress
</span>

<span class="font-bold" style="color:#1976d2;">
{{ project.progress || 0 }}%
</span>

</div>

<ProgressBar
:value="project.progress || 0"
style="height:10px;"
:pt="{ value: { style: { background: progressColor(project.progress) } } }"
/>

</div>

<div class="grid text-sm">

<div class="col-6 md:col-3 mb-3">
<div class="text-500 mb-1">Category</div>
<div class="font-medium text-900">
{{ project.category_display || '—' }}
</div>
</div>

<div class="col-6 md:col-3 mb-3">
<div class="text-500 mb-1">Sector</div>
<div class="font-medium text-900">
{{ project.sector || '—' }}
</div>
</div>

<div class="col-6 md:col-3 mb-3">
<div class="text-500 mb-1">Owner Type</div>
<div class="font-medium text-900">
{{ project.owner_type_display || '—' }}
</div>
</div>

<div class="col-6 md:col-3 mb-3">
<div class="text-500 mb-1">Created By</div>
<div class="font-medium text-900">
{{ project.created_by_name || '—' }}
</div>
</div>

</div>

<div v-if="project.description" class="mt-2">

<div class="text-500 font-medium mb-2 text-sm">
Description
</div>

<p class="text-700 line-height-3 m-0">
{{ project.description }}
</p>

</div>

</div>
</div>

<!-- Sites -->
<div class="col-12 lg:col-4">

<div class="card">

<div class="flex justify-content-between align-items-center mb-3">
<h5 class="mt-0 mb-0" style="color:#0d2347;">
Project Sites
</h5>

<Tag :value="`${project.sites?.length || 0}`" severity="info" />

</div>

<div v-if="project.sites?.length" class="flex flex-column gap-2">

<div
v-for="site in project.sites"
:key="site.id"
class="p-3 border-round-lg"
style="background:var(--surface-50);"
>

<div class="font-semibold text-sm text-900">
{{ site.site_name }}
</div>

<div class="text-500 text-xs mt-1">
{{ site.county_name_display }}
<span v-if="site.town"> · {{ site.town }}</span>
</div>

</div>
</div>

<div v-else class="text-500 text-sm text-center py-3">
No sites added yet.
</div>

</div>
</div>

</div>

<!-- ================= TIMELINE ================= -->
<div v-if="activeTab === 'timeline'" class="card">

<h5 style="color:#0d2347;">Timeline / WBS</h5>

<DataTable :value="project.wbs_items || []" size="small" stripedRows>

<Column field="wbs_code" header="WBS Code" style="width:120px;" />

<Column field="wbs_name" header="Name" />

<Column header="Planned Cost">
<template #body="{ data }">
KES {{ Number(data.planned_cost).toLocaleString('en-KE') }}
</template>
</Column>

<Column field="planned_start" header="Start" />
<Column field="planned_end" header="End" />

</DataTable>

</div>

<!-- ================= MEDIA ================= -->
<div v-if="activeTab === 'media'">
<ProjectMedia />
</div>

<!-- ================= RISKS ================= -->
<div v-if="activeTab === 'risks'" class="card">
<h5 style="color:#0d2347;">Risks</h5>
<p class="text-500">Risk register — coming soon.</p>
</div>

<!-- ================= REPORTS ================= -->
<div v-if="activeTab === 'reports'" class="card">
<h5 style="color:#0d2347;">Reports</h5>
<p class="text-500">Project reports — coming soon.</p>
</div>

</template>

</div>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/api/api";

/* MEDIA COMPONENT */
import ProjectMedia from "@/views/projects/ProjectMedia.vue";

const route = useRoute();

const project = ref(null);
const loading = ref(false);

const activeTab = ref("overview");

const tabs = [
{ name: "overview", label: "Overview", icon: "pi pi-eye" },
{ name: "timeline", label: "Timeline", icon: "pi pi-calendar" },
{ name: "media", label: "Media", icon: "pi pi-images" },
{ name: "risks", label: "Risks", icon: "pi pi-exclamation-triangle" },
{ name: "reports", label: "Reports", icon: "pi pi-file-pdf" }
];

const fmtDate = (d) => {
if (!d) return null;
return new Date(d).toLocaleDateString("en-KE", {
day: "2-digit",
month: "short",
year: "numeric"
});
};

const fmtBudget = (v) => {
const n = Number(v);
if (n >= 1e9) return `KES ${(n / 1e9).toFixed(2)}B`;
if (n >= 1e6) return `KES ${(n / 1e6).toFixed(1)}M`;
return `KES ${n.toLocaleString("en-KE")}`;
};

const statusSeverity = (s) =>
({
planned: "info",
active: "success",
in_progress: "success",
on_hold: "warn",
at_risk: "danger",
completed: "secondary",
cancelled: "danger"
}[s] || "info");

const progressColor = (p) =>
(p || 0) >= 80 ? "#2ecc71" :
(p || 0) >= 40 ? "#e6a817" :
"#1976d2";

async function loadProject() {
loading.value = true;

try {
const res = await api.get(`/api/projects/projects/${route.params.id}/`);
project.value = res.data;
} catch {
project.value = null;
} finally {
loading.value = false;
}
}

onMounted(loadProject);
</script>