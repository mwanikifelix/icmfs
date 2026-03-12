<template>
  <div class="grid">
    <div class="col-12">

      <!-- ================= PAGE HEADER ================= -->
      <div class="flex justify-content-between align-items-center mb-4">
        <div>
          <h4 class="mb-1 mt-0">Projects</h4>
          <span class="text-500 text-sm">
            Showing {{ filteredProjects.length }} of {{ projects.length }} projects
          </span>
        </div>
        <Button
          label="New Project"
          icon="pi pi-plus"
          @click="$router.push('/app/projects/create')"
        />
      </div>

      <!-- ================= STAT CARDS ================= -->
      <div class="grid mb-4">
        <div class="col-12 sm:col-6 lg:col-3">
          <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
              <div>
                <span class="text-500 font-medium text-sm block mb-2">Total Projects</span>
                <span class="text-900 font-bold text-3xl">{{ projects.length }}</span>
              </div>
              <div class="flex align-items-center justify-content-center bg-blue-100 border-round" style="width:3rem;height:3rem">
                <i class="pi pi-briefcase text-blue-500 text-xl" />
              </div>
            </div>
            <div class="mt-3 text-sm text-500">
              <span class="text-green-500 font-medium">{{ statusCount.in_progress }} active</span> right now
            </div>
          </div>
        </div>

        <div class="col-12 sm:col-6 lg:col-3">
          <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
              <div>
                <span class="text-500 font-medium text-sm block mb-2">In Progress</span>
                <span class="text-900 font-bold text-3xl">{{ statusCount.in_progress }}</span>
              </div>
              <div class="flex align-items-center justify-content-center bg-green-100 border-round" style="width:3rem;height:3rem">
                <i class="pi pi-spin pi-spinner text-green-500 text-xl" />
              </div>
            </div>
            <div class="mt-3 text-sm text-500">
              Avg progress <span class="text-green-500 font-medium">{{ avgProgress }}%</span>
            </div>
          </div>
        </div>

        <div class="col-12 sm:col-6 lg:col-3">
          <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
              <div>
                <span class="text-500 font-medium text-sm block mb-2">On Hold</span>
                <span class="text-900 font-bold text-3xl">{{ statusCount.on_hold }}</span>
              </div>
              <div class="flex align-items-center justify-content-center bg-orange-100 border-round" style="width:3rem;height:3rem">
                <i class="pi pi-pause-circle text-orange-500 text-xl" />
              </div>
            </div>
            <div class="mt-3 text-sm text-500">
              <span class="text-orange-500 font-medium">{{ statusCount.planned }} planned</span> not started
            </div>
          </div>
        </div>

        <div class="col-12 sm:col-6 lg:col-3">
          <div class="card mb-0">
            <div class="flex justify-content-between align-items-start">
              <div>
                <span class="text-500 font-medium text-sm block mb-2">Total Budget</span>
                <span class="text-900 font-bold text-3xl">KES {{ totalBudgetFormatted }}</span>
              </div>
              <div class="flex align-items-center justify-content-center bg-purple-100 border-round" style="width:3rem;height:3rem">
                <i class="pi pi-dollar text-purple-500 text-xl" />
              </div>
            </div>
            <div class="mt-3 text-sm text-500">
              <span class="text-purple-500 font-medium">{{ statusCount.completed }} completed</span> projects
            </div>
          </div>
        </div>
      </div>

      <!-- ================= FILTERS + TABLE ================= -->
      <div class="card">

        <!-- Toolbar -->
        <div class="flex flex-wrap gap-3 mb-4 align-items-center justify-content-between">

          <!-- Search -->
          <div class="p-input-icon-left" style="flex: 1; min-width: 200px; max-width: 320px;">
            <i class="pi pi-search" />
            <InputText
              v-model="searchQuery"
              placeholder="Search projects..."
              class="w-full"
            />
          </div>

          <!-- Dropdowns -->
          <div class="flex flex-wrap gap-2">
            <Dropdown
              v-model="filters.county"
              :options="countyOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="County"
              showClear
              style="min-width: 140px"
            />
            <Dropdown
              v-model="filters.status"
              :options="statusOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Status"
              showClear
              style="min-width: 140px"
            />
            <Dropdown
              v-model="filters.sector"
              :options="sectorOptions"
              placeholder="Sector"
              showClear
              style="min-width: 140px"
            />
            <Dropdown
              v-model="filters.owner"
              :options="ownerOptions"
              placeholder="Owner"
              showClear
              style="min-width: 140px"
            />
            <Button
              v-if="hasActiveFilters"
              label="Clear"
              icon="pi pi-times"
              severity="secondary"
              text
              @click="clearFilters"
            />
          </div>
        </div>

        <!-- Active filter chips -->
        <div v-if="hasActiveFilters" class="flex flex-wrap gap-2 mb-3">
          <Chip
            v-if="filters.county"
            :label="filters.county"
            removable
            @remove="filters.county = null"
          />
          <Chip
            v-if="filters.status"
            :label="formatStatus(filters.status)"
            removable
            @remove="filters.status = null"
          />
          <Chip
            v-if="filters.sector"
            :label="filters.sector"
            removable
            @remove="filters.sector = null"
          />
          <Chip
            v-if="filters.owner"
            :label="filters.owner"
            removable
            @remove="filters.owner = null"
          />
          <Chip
            v-if="searchQuery"
            :label="`&quot;${searchQuery}&quot;`"
            removable
            @remove="searchQuery = ''"
          />
        </div>

        <!-- ===== TABLE ===== -->
        <DataTable
          :value="filteredProjects"
          :paginator="true"
          :rows="10"
          :rowsPerPageOptions="[5, 10, 20, 50]"
          responsiveLayout="scroll"
          stripedRows
          removableSort
          :globalFilterFields="['title', 'county', 'sector', 'owner_type']"
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
          currentPageReportTemplate="Showing {first} to {last} of {totalRecords} projects"
          :emptyMessage="emptyMessage"
          v-model:selection="selectedProjects"
        >

          <!-- Selection -->
          <Column selectionMode="multiple" style="width: 3rem" :exportable="false" />

          <!-- Project Name -->
          <Column field="title" header="Project Name" sortable style="min-width: 220px">
            <template #body="{ data }">
              <div class="flex flex-column gap-1">
                <span class="font-semibold text-900">{{ data.title }}</span>
                <span class="text-400 text-xs">{{ data.project_id }}</span>
              </div>
            </template>
          </Column>

          <!-- County -->
          <Column field="county" header="County" sortable style="min-width: 120px">
            <template #body="{ data }">
              <div class="flex align-items-center gap-2">
                <i class="pi pi-map-marker text-400 text-sm" />
                <span>{{ data.county }}</span>
              </div>
            </template>
          </Column>

          <!-- Sector -->
          <Column field="sector" header="Sector" sortable style="min-width: 120px">
            <template #body="{ data }">
              <Tag :value="data.sector" severity="secondary" />
            </template>
          </Column>

          <!-- Owner -->
          <Column field="owner_type" header="Owner" sortable />

          <!-- Status -->
          <Column field="status" header="Status" sortable style="min-width: 130px">
            <template #body="{ data }">
              <Badge
                :value="formatStatus(data.status)"
                :severity="getStatusSeverity(data.status)"
              />
            </template>
          </Column>

          <!-- Progress -->
          <Column field="progress" header="Progress" sortable style="min-width: 160px">
            <template #body="{ data }">
              <div class="flex align-items-center gap-2">
                <ProgressBar
                  :value="data.progress"
                  :showValue="false"
                  style="flex: 1; height: 8px"
                  :class="getProgressClass(data.progress)"
                />
                <span class="text-sm font-medium w-3rem text-right">{{ data.progress }}%</span>
              </div>
            </template>
          </Column>

          <!-- Budget -->
          <Column field="budget_kes" header="Budget (KES)" sortable style="min-width: 140px">
            <template #body="{ data }">
              <span class="font-medium">{{ formatBudget(data.budget_kes) }}</span>
            </template>
          </Column>

          <!-- Actions -->
          <Column header="Actions" style="width: 120px; text-align: center" :exportable="false">
            <template #body="{ data }">
              <div class="flex gap-1 justify-content-center">
                <Button
                  icon="pi pi-eye"
                  text
                  rounded
                  size="small"
                  v-tooltip.top="'View'"
                  @click="$router.push(`/app/projects/${data.project_id}`)"
                />
                <Button
                  icon="pi pi-pencil"
                  text
                  rounded
                  size="small"
                  severity="secondary"
                  v-tooltip.top="'Edit'"
                  @click="$router.push(`/app/projects/${data.project_id}/edit`)"
                />
                <Button
                  icon="pi pi-ellipsis-v"
                  text
                  rounded
                  size="small"
                  severity="secondary"
                  v-tooltip.top="'More'"
                  @click="(e) => toggleMenu(e, data)"
                />
              </div>
            </template>
          </Column>

        </DataTable>

        <!-- Bulk actions (shown when rows selected) -->
        <Transition name="slide-up">
          <div v-if="selectedProjects.length" class="flex align-items-center gap-3 mt-3 p-3 border-round surface-100">
            <span class="text-600 text-sm font-medium">{{ selectedProjects.length }} selected</span>
            <Button label="Export Selected" icon="pi pi-download" size="small" text />
            <Button label="Deselect All" icon="pi pi-times" size="small" text severity="secondary" @click="selectedProjects = []" />
          </div>
        </Transition>
      </div>
    </div>

    <!-- Context menu -->
    <Menu ref="rowMenu" :model="rowMenuItems" popup />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

import DataTable  from 'primevue/datatable';
import Column     from 'primevue/column';
import Button     from 'primevue/button';
import Badge      from 'primevue/badge';
import Tag        from 'primevue/tag';
import ProgressBar from 'primevue/progressbar';
import Dropdown   from 'primevue/dropdown';
import InputText  from 'primevue/inputtext';
import Chip       from 'primevue/chip';
import Menu       from 'primevue/menu';

import { counties } from '@/components/data/projects.master.js';

const router = useRouter();

// ── Flatten all projects ──────────────────────────────────────
const projects = computed(() =>
  counties.flatMap((county) =>
    county.projects.map((p) => ({ ...p, county: county.name }))
  )
);

// ── Filters & search ──────────────────────────────────────────
const searchQuery = ref('');
const filters = ref({ county: null, status: null, sector: null, owner: null });
const selectedProjects = ref([]);

const hasActiveFilters = computed(() =>
  searchQuery.value || Object.values(filters.value).some(Boolean)
);

function clearFilters() {
  searchQuery.value = '';
  filters.value = { county: null, status: null, sector: null, owner: null };
}

const filteredProjects = computed(() => {
  const q = searchQuery.value.toLowerCase();
  return projects.value.filter((p) => {
    const matchesSearch =
      !q ||
      p.title.toLowerCase().includes(q) ||
      p.county.toLowerCase().includes(q) ||
      p.sector?.toLowerCase().includes(q) ||
      p.project_id.toLowerCase().includes(q);

    return (
      matchesSearch &&
      (!filters.value.county || p.county        === filters.value.county) &&
      (!filters.value.status || p.status        === filters.value.status) &&
      (!filters.value.sector || p.sector        === filters.value.sector) &&
      (!filters.value.owner  || p.owner_type    === filters.value.owner)
    );
  });
});

const emptyMessage = computed(() =>
  hasActiveFilters.value
    ? 'No projects match your current filters.'
    : 'No projects found.'
);

// ── Stat cards ────────────────────────────────────────────────
const statusCount = computed(() => {
  const base = { planned: 0, in_progress: 0, on_hold: 0, completed: 0, cancelled: 0 };
  projects.value.forEach((p) => { if (base[p.status] !== undefined) base[p.status]++; });
  return base;
});

const avgProgress = computed(() => {
  const active = projects.value.filter((p) => p.status === 'in_progress');
  if (!active.length) return 0;
  return Math.round(active.reduce((s, p) => s + p.progress, 0) / active.length);
});

const totalBudgetFormatted = computed(() => {
  const total = projects.value.reduce((s, p) => s + (p.budget_kes || 0), 0);
  return formatBudget(total);
});

// ── Dropdown options ──────────────────────────────────────────
const countyOptions = counties.map((c) => ({ label: c.name, value: c.name }));

const statusOptions = [
  { label: 'Planned',     value: 'planned'     },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'On Hold',     value: 'on_hold'     },
  { label: 'Completed',   value: 'completed'   },
  { label: 'Cancelled',   value: 'cancelled'   },
];

const sectorOptions = ['Housing', 'Infrastructure', 'Health', 'Education'];
const ownerOptions  = ['Government', 'Private', 'NGO'];

// ── Helpers ───────────────────────────────────────────────────
const formatStatus = (s) =>
  ({ planned: 'Planned', in_progress: 'In Progress', on_hold: 'On Hold',
     completed: 'Completed', cancelled: 'Cancelled' }[s] || s);

const getStatusSeverity = (s) =>
  ({ planned: 'info', in_progress: 'success', on_hold: 'warn',
     completed: 'secondary', cancelled: 'danger' }[s] || 'info');

const getProgressClass = (val) =>
  val >= 75 ? 'progress-success' : val >= 40 ? 'progress-warn' : 'progress-danger';

const formatBudget = (val) => {
  if (!val) return '—';
  if (val >= 1_000_000_000) return `${(val / 1_000_000_000).toFixed(2)}B`;
  if (val >= 1_000_000)     return `${(val / 1_000_000).toFixed(1)}M`;
  return val.toLocaleString();
};

// ── Row context menu ──────────────────────────────────────────
const rowMenu   = ref();
const activeRow = ref(null);

const rowMenuItems = computed(() => [
  {
    label: 'View Details',
    icon: 'pi pi-eye',
    command: () => router.push(`/app/projects/${activeRow.value?.project_id}`),
  },
  {
    label: 'Edit',
    icon: 'pi pi-pencil',
    command: () => router.push(`/app/projects/${activeRow.value?.project_id}/edit`),
  },
  { separator: true },
  {
    label: 'View Timeline',
    icon: 'pi pi-calendar',
    command: () => router.push(`/app/projects/${activeRow.value?.project_id}/timeline`),
  },
  {
    label: 'View Reports',
    icon: 'pi pi-chart-bar',
    command: () => router.push(`/app/projects/${activeRow.value?.project_id}/reports`),
  },
]);

function toggleMenu(event, row) {
  activeRow.value = row;
  rowMenu.value.toggle(event);
}
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>