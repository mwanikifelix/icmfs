<!-- <template>
  <div class="grid">
    <div class="col-12">

      <!-- ================= PROJECT FOUND ================= --
      <template v-if="project">

        <!-- ========= HEADER ========= --
        <div class="card mb-3">
          <h3 class="mb-2">{{ project.title }}</h3>

          <div class="flex flex-wrap gap-3 text-sm">
            <span><strong>County:</strong> {{ project.county }}</span>
            <span><strong>Sector:</strong> {{ project.sector }}</span>
            <span><strong>Category:</strong> {{ project.category }}</span>
            <span><strong>Owner:</strong> {{ project.owner_type }}</span>
            <span>
              <strong>Status:</strong>
              <Badge
                :value="formatStatus(project.status)"
                :severity="getStatusSeverity(project.status)"
              />
            </span>
          </div>
        </div>

        <!-- ========= PROJECT OVERVIEW ========= --
        <div class="card mb-3">
          <h5>Project Overview</h5>

          <div class="grid text-sm">
            <div class="col-12 md:col-4">
              <strong>Budget</strong><br />
              KES {{ project.budget_kes.toLocaleString() }}
            </div>

            <div class="col-12 md:col-4">
              <strong>Start Date</strong><br />
              {{ project.start_date }}
            </div>

            <div class="col-12 md:col-4">
              <strong>Expected Completion</strong><br />
              {{ project.expected_end_date || "—" }}
            </div>
          </div>
        </div>

        <!-- ========= LATEST SITE UPDATE ========= --
        <div class="card mb-3">
          <h5>Latest Site Update</h5>

          <template v-if="latestReport">
            <p class="mb-2">
              {{ latestReport.status_update }}
            </p>

            <div class="grid text-sm">
              <div class="col-12 md:col-4">
                <strong>Progress</strong><br />
                {{ latestReport.progress_percentage }}%
              </div>

              <div class="col-12 md:col-4">
                <strong>Total Workers</strong><br />
                {{ latestReport.workforce.total }}
              </div>

              <div class="col-12 md:col-4">
                <strong>Report Date</strong><br />
                {{ latestReport.report_date }}
              </div>
            </div>

            <div v-if="latestReport.issues?.length" class="mt-3">
              <strong>Issues / Risks</strong>
              <ul class="pl-4 mt-1">
                <li v-for="issue in latestReport.issues" :key="issue">
                  {{ issue }}
                </li>
              </ul>
            </div>
          </template>

          <div v-else class="text-gray-500">
            No site activity reports have been submitted yet.
          </div>
        </div>

      </template>

      <!-- ================= PROJECT NOT FOUND ================= --
      <div class="card" v-else>
        <p class="text-red-500">
          Project not found. Please check the link or project ID.
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

import Badge from "primevue/badge";

/* MASTER DATA */
import { counties } from "../../components/data/projects.master.js";

/* SITE ACTIVITY HELPERS */
import { getLatestReport } from "../../components/data/project.site.activity.js";


import { watchEffect } from "vue";

watchEffect(() => {
  console.log("ROUTE PARAM ID RECEIVED:", route.params.id);
});

/* -----------------------------------
   Route
----------------------------------- *
const route = useRoute();

/* -----------------------------------
   Project (flatten counties)
----------------------------------- *
const project = computed(() => {
  const id = route.params.id;
  if (!id) return null;

  return counties
    .flatMap(c =>
      c.projects.map(p => ({
        ...p,
        county: c.name
      }))
    )
    .find(p => p.project_id === id);
});

/* -----------------------------------
   Latest site report
----------------------------------- *
const latestReport = computed(() => {
  if (!project.value) return null;
  return getLatestReport(project.value.project_id);
});

/* -----------------------------------
   Helpers
----------------------------------- *
const getStatusSeverity = status => {
  const map = {
    planned: "info",
    pending: "warning",
    in_progress: "success",
    on_hold: "warning",
    completed: "secondary",
    cancelled: "danger"
  };
  return map[status] || "info";
};

const formatStatus = status => {
  const map = {
    planned: "Planned",
    pending: "Pending",
    in_progress: "In Progress / Ongoing",
    on_hold: "On Hold",
    completed: "Completed",
    cancelled: "Cancelled"
  };
  return map[status] || status;
};
</script>
 -->








 <template>
  <div class="grid">
    <div class="col-12">

      <!-- ================= PROJECT FOUND ================= -->
      <template v-if="project">

        <!-- ========= HEADER ========= -->
        <div class="card mb-3">
          <h3 class="mb-2">{{ project.title }}</h3>

          <div class="flex flex-wrap gap-3 text-sm">
            <span><strong>County:</strong> {{ project.county }}</span>
            <span><strong>Sector:</strong> {{ project.sector }}</span>
            <span><strong>Category:</strong> {{ project.category }}</span>
            <span><strong>Owner:</strong> {{ project.owner_type }}</span>
            <span>
              <strong>Status:</strong>
              <Badge
                :value="formatStatus(project.status)"
                :severity="getStatusSeverity(project.status)"
              />
            </span>
          </div>
        </div>

        <!-- ========= PROJECT TABS ========= -->
        <div class="card mb-3">
          <div class="flex gap-3 flex-wrap">

            <Button label="Overview" icon="pi pi-eye"
              :outlined="!isActive('project-detail')"
              @click="go('project-detail')" />

            <Button label="Timeline" icon="pi pi-calendar"
              :outlined="!isActive('project-timeline')"
              @click="go('project-timeline')" />

            <Button label="Media" icon="pi pi-images"
              :outlined="!isActive('project-media')"
              @click="go('project-media')" />

            <Button label="Risks" icon="pi pi-exclamation-triangle"
              :outlined="!isActive('project-risks')"
              @click="go('project-risks')" />

            <Button label="Reports" icon="pi pi-file-pdf"
              :outlined="!isActive('project-reports')"
              @click="go('project-reports')" />

            <Button label="Edit" icon="pi pi-pencil"
              severity="secondary"
              :outlined="!isActive('project-edit')"
              @click="go('project-edit')" />
          </div>
        </div>

        <!-- ========= TAB CONTENT ========= -->
        <router-view
          :project="project"
          :latestReport="latestReport"
        />

      </template>

      <!-- ================= PROJECT NOT FOUND ================= -->
      <div class="card" v-else>
        <p class="text-red-500">
          Project not found. Please check the link or project ID.
        </p>
      </div>

    </div>
  </div>
</template>
<script setup>
import { computed, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";
import Badge from "primevue/badge";
import Button from "primevue/button";

/* MASTER DATA */
import { counties } from "../../components/data/projects.master.js";

/* SITE ACTIVITY */
import { getLatestReport } from "../../components/data/project.site.activity.js";

const route = useRoute();
const router = useRouter();

/* -----------------------------------
   DEBUG (safe to remove later)
----------------------------------- */
watchEffect(() => {
  console.log("ROUTE PARAM ID:", route.params.id);
});

/* -----------------------------------
   Project lookup
----------------------------------- */
const project = computed(() => {
  const id = route.params.id;
  if (!id) return null;

  return counties
    .flatMap(c =>
      c.projects.map(p => ({
        ...p,
        county: c.name
      }))
    )
    .find(p => p.project_id === id) || null;
});

/* -----------------------------------
   Latest site report
----------------------------------- */
const latestReport = computed(() => {
  if (!project.value) return null;
  return getLatestReport(project.value.project_id);
});

/* -----------------------------------
   Navigation helpers
----------------------------------- */
const go = (name) => {
  router.push({ name, params: { id: project.value.project_id } });
};

const isActive = (name) => route.name === name;

/* -----------------------------------
   Helpers
----------------------------------- */
const getStatusSeverity = status => ({
  planned: "info",
  pending: "warning",
  in_progress: "success",
  on_hold: "warning",
  completed: "secondary",
  cancelled: "danger"
}[status] || "info");

const formatStatus = status => ({
  planned: "Planned",
  pending: "Pending",
  in_progress: "In Progress / Ongoing",
  on_hold: "On Hold",
  completed: "Completed",
  cancelled: "Cancelled"
}[status] || status);
</script>
