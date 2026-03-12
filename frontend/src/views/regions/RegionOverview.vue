<template>
  <div class="grid">
    <div class="col-12">

      <!-- ================= REGION FOUND ================= -->
      <template v-if="region">

        <!-- ================= HEADER ================= -->
        <div class="card mb-3">
          <div class="flex align-items-center justify-content-between flex-wrap gap-2">
            <div>
              <h3 class="mb-1">{{ region.name }}</h3>
              <span class="text-500 text-sm">Region Overview</span>
            </div>
            <Button
              label="Back to Regions"
              icon="pi pi-arrow-left"
              text
              @click="router.push('/app/regions')"
            />
          </div>

          <div class="flex flex-wrap gap-4 mt-3 text-sm">
            <span><i class="pi pi-map mr-1 text-primary" /><strong>Counties:</strong> {{ region.counties.length }}</span>
            <span><i class="pi pi-briefcase mr-1 text-primary" /><strong>Projects:</strong> {{ region.projects.length }}</span>
            <span><i class="pi pi-dollar mr-1 text-primary" /><strong>Total Budget:</strong> KES {{ totalBudget.toLocaleString() }}</span>
          </div>
        </div>

        <!-- ================= STATUS SUMMARY ================= -->
        <div class="grid mb-3">
          <div class="col-12 md:col-3">
            <div class="card text-center">
              <div class="text-500 font-medium mb-2">Planned</div>
              <Badge :value="statusCount.planned" severity="info" size="large" />
            </div>
          </div>
          <div class="col-12 md:col-3">
            <div class="card text-center">
              <div class="text-500 font-medium mb-2">In Progress</div>
              <Badge :value="statusCount.in_progress" severity="success" size="large" />
            </div>
          </div>
          <div class="col-12 md:col-3">
            <div class="card text-center">
              <div class="text-500 font-medium mb-2">On Hold</div>
              <Badge :value="statusCount.on_hold" severity="warning" size="large" />
            </div>
          </div>
          <div class="col-12 md:col-3">
            <div class="card text-center">
              <div class="text-500 font-medium mb-2">Completed</div>
              <Badge :value="statusCount.completed" severity="secondary" size="large" />
            </div>
          </div>
        </div>

        <!-- ================= COUNTIES ================= -->
        <div class="card mb-3">
          <h5 class="mb-3">Counties in this Region</h5>
          <div class="flex flex-wrap gap-2">
            <Chip
              v-for="c in region.counties"
              :key="c.county_id"
              :label="`${c.name} (${c.projects.length} projects)`"
              icon="pi pi-map-marker"
            />
          </div>
        </div>

        <!-- ================= PROJECTS TABLE ================= -->
        <div class="card">
          <h5 class="mb-3">Projects in {{ region.name }}</h5>

          <DataTable
            :value="region.projects"
            :paginator="true"
            :rows="10"
            responsiveLayout="scroll"
            stripedRows
            showGridlines
          >
            <Column field="title" header="Project Name" sortable style="min-width: 200px" />

            <Column field="county" header="County" sortable />

            <Column field="sector" header="Sector" sortable />

            <Column field="owner_type" header="Owner" />

            <Column header="Status" sortable sortField="status">
              <template #body="{ data }">
                <Badge
                  :value="formatStatus(data.status)"
                  :severity="getStatusSeverity(data.status)"
                />
              </template>
            </Column>

            <Column header="Progress" style="min-width: 140px">
              <template #body="{ data }">
                <div class="flex align-items-center gap-2">
                  <ProgressBar
                    :value="data.progress"
                    style="height: 8px; flex: 1"
                    :showValue="false"
                  />
                  <span class="text-sm font-medium">{{ data.progress }}%</span>
                </div>
              </template>
            </Column>

            <Column header="Budget (KES)" sortable sortField="budget_kes">
              <template #body="{ data }">
                {{ (data.budget_kes / 1_000_000_000).toFixed(2) }}B
              </template>
            </Column>

            <Column header="Actions" style="width: 80px">
              <template #body="{ data }">
                <Button
                  icon="pi pi-eye"
                  text
                  rounded
                  v-tooltip.top="'View Project'"
                  @click="router.push(`/app/projects/${data.project_id}`)"
                />
              </template>
            </Column>
          </DataTable>
        </div>

      </template>

      <!-- ================= NOT FOUND ================= -->
      <div v-else class="card">
        <div class="text-center py-6">
          <i class="pi pi-map text-400" style="font-size: 3rem" />
          <p class="text-500 mt-3 mb-1">Region not found.</p>
          <p class="text-400 text-sm mb-4">
            Looking for: <code class="bg-primary-50 px-2 py-1 border-round">{{ $route.params.id }}</code>
          </p>
          <p class="text-400 text-sm mb-4">
            Available: <code class="bg-primary-50 px-2 py-1 border-round">{{ availableRegionSlugs.join(', ') }}</code>
          </p>
          <Button label="Back to Regions" icon="pi pi-arrow-left" @click="router.push('/app/regions')" />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { counties } from '@/components/data/projects.master.js';

const route  = useRoute();
const router = useRouter();

// ── Slugify helper ─────────────────────────────────────────────
const slugify = (text) =>
  text.toLowerCase().trim().replace(/\s+/g, '-');

// ── All unique region slugs (useful for debugging) ─────────────
const availableRegionSlugs = computed(() =>
  [...new Set(counties.map(c => slugify(c.region)))]
);

// ── Resolve region from :id param ─────────────────────────────
const region = computed(() => {
  const regionId = route.params.id;
  if (!regionId) return null;

  // Match counties whose slugified region name === the route :id
  const matchedCounties = counties.filter(
    (c) => slugify(c.region) === regionId
  );

  if (!matchedCounties.length) return null;

  const projects = matchedCounties.flatMap((c) =>
    c.projects.map((p) => ({ ...p, county: c.name }))
  );

  return {
    id:       regionId,
    name:     matchedCounties[0].region,     // original readable name e.g. "Coast"
    counties: matchedCounties,
    projects,
  };
});

// ── Aggregations ───────────────────────────────────────────────
const totalBudget = computed(() =>
  region.value
    ? region.value.projects.reduce((sum, p) => sum + (p.budget_kes || 0), 0)
    : 0
);

const statusCount = computed(() => {
  const base = { planned: 0, in_progress: 0, on_hold: 0, completed: 0 };
  region.value?.projects.forEach((p) => {
    if (base[p.status] !== undefined) base[p.status]++;
  });
  return base;
});

// ── Helpers ────────────────────────────────────────────────────
const formatStatus = (status) =>
  ({ planned: 'Planned', in_progress: 'In Progress', on_hold: 'On Hold', completed: 'Completed' }[status] || status);

const getStatusSeverity = (status) =>
  ({ planned: 'info', in_progress: 'success', on_hold: 'warning', completed: 'secondary' }[status] || 'info');
</script>