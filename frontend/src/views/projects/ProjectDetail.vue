<template>
<div class="grid">
<div class="col-12">

<!-- Loading -->
<div v-if="loading" class="card flex justify-content-center py-6">
<ProgressSpinner style="width:3rem;height:3rem;" />
</div>

<template v-else-if="project">

<!-- ================= HEADER ================= -->
<div class="border-round-xl mb-4 p-4 header-gradient">

<div class="flex align-items-start justify-content-between flex-wrap gap-3">

<div class="flex align-items-center gap-3">

<Button
icon="pi pi-arrow-left"
text
rounded
class="header-back-btn"
@click="$router.push('/app/projects')"
/>

<div>
<h4 class="mt-0 mb-1 text-white">
{{ project.name }}
</h4>

<div class="flex flex-wrap gap-3 text-sm text-light">

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
class="status-tag"
/>

<Button
label="Edit"
icon="pi pi-pencil"
size="small"
class="edit-btn"
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
:class="activeTab === tab.name ? 'tab-active' : 'tab-inactive'"
@click="activeTab = tab.name"
/>

</div>
</div>

<!-- ================= OVERVIEW ================= -->
<div v-if="activeTab === 'overview'" class="grid">

<div class="col-6 lg:col-3">
<div class="card stat-card">
<div class="text-500 text-sm mb-1">Budget (KES)</div>
<div class="font-bold text-xl">
{{ project.budget ? fmtBudget(project.budget) : '—' }}
</div>
</div>
</div>

<div class="col-6 lg:col-3">
<div class="card stat-card">
<div class="text-500 text-sm mb-1">Progress</div>
<div class="font-bold text-xl text-primary">
{{ project.progress || 0 }}%
</div>
</div>
</div>

<div class="col-6 lg:col-3">
<div class="card stat-card">
<div class="text-500 text-sm mb-1">Start Date</div>
<div class="font-bold text-xl">
{{ fmtDate(project.start_date) }}
</div>
</div>
</div>

<div class="col-6 lg:col-3">
<div class="card stat-card">
<div class="text-500 text-sm mb-1">End Date</div>
<div class="font-bold text-xl">
{{ fmtDate(project.end_date) || '—' }}
</div>
</div>
</div>

<!-- DETAILS -->
<div class="col-12 lg:col-8">
<div class="card">

<h5 class="section-title">Project Details</h5>

<div class="mb-4">
<div class="flex justify-content-between mb-2">
<span class="text-600 text-sm">Overall Progress</span>
<span class="font-bold text-primary">
{{ project.progress || 0 }}%
</span>
</div>

<ProgressBar
:value="project.progress || 0"
class="progress-bar"
/>

</div>

<div class="grid text-sm">

<div class="col-6 md:col-3 mb-3">
<div class="text-500 mb-1">Category</div>
<div class="font-medium">
{{ project.category_display || '—' }}
</div>
</div>

<div class="col-6 md:col-3 mb-3">
<div class="text-500 mb-1">Sector</div>
<div class="font-medium">
{{ project.sector || '—' }}
</div>
</div>

<div class="col-6 md:col-3 mb-3">
<div class="text-500 mb-1">Owner Type</div>
<div class="font-medium">
{{ project.owner_type_display || '—' }}
</div>
</div>

<div class="col-6 md:col-3 mb-3">
<div class="text-500 mb-1">Created By</div>
<div class="font-medium">
{{ project.created_by_name || '—' }}
</div>
</div>

</div>

<div v-if="project.description" class="mt-2">
<div class="text-500 mb-2 text-sm">Description</div>
<p class="text-700 line-height-3 m-0">
{{ project.description }}
</p>
</div>

</div>
</div>

<!-- SITES -->
<div class="col-12 lg:col-4">
<div class="card">

<div class="flex justify-content-between align-items-center mb-3">
<h5 class="section-title">Project Sites</h5>
<Tag :value="`${project.sites?.length || 0}`" severity="info" />
</div>

<div v-if="project.sites?.length" class="flex flex-column gap-2">

<div
v-for="site in project.sites"
:key="site.id"
class="site-card"
>

<div class="font-semibold">
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

<!-- ================= MEDIA ================= -->
<div v-if="activeTab === 'media' && project">
<ProjectMedia :projectId="project.id" />
</div>

<!-- OTHER TABS -->
<div v-if="activeTab === 'timeline'" class="card">
<h5>Timeline / WBS</h5>
</div>

<div v-if="activeTab === 'risks'" class="card">
<h5>Risks</h5>
</div>

<div v-if="activeTab === 'reports'" class="card">
<h5>Reports</h5>
</div>

</template>

</div>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/api/api";
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

const fmtDate = (d) =>
d ? new Date(d).toLocaleDateString("en-KE") : null;

const fmtBudget = (v) =>
`KES ${Number(v).toLocaleString("en-KE")}`;

const statusSeverity = (s) =>
({ planned:"info", active:"success", completed:"secondary" }[s] || "info");

async function loadProject() {
loading.value = true;
try {
const res = await api.get(`/api/projects/projects/${route.params.id}/`);
project.value = res.data;
} finally {
loading.value = false;
}
}

onMounted(loadProject);
</script>

<style scoped>

/* HEADER */
.header-gradient{
background:linear-gradient(135deg,#0d2347,#1976d2);
}
.header-back-btn{ color:#fff; }
.text-light{ color:#cfe3ff; }

/* BUTTONS */
.tab-active{
background:#1976d2 !important;
color:#fff !important;
}
.tab-inactive{
border-color:#1976d2;
color:#1976d2;
}

/* STATS */
.stat-card{
border-left:4px solid #1976d2;
}

/* TEXT */
.section-title{
color:#0d2347;
}

/* PROGRESS */
.progress-bar .p-progressbar-value{
background:#1976d2;
}

/* SITE */
.site-card{
background:#f4f7fb;
padding:10px;
border-radius:8px;
}

.edit-btn{
background:#ffc107;
border:none;
color:#0d2347;
}

</style>