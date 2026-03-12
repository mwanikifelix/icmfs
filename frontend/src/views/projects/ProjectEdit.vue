<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">

        <!-- ================= PROJECT FOUND ================= -->
        <template v-if="project">

          <h4 class="mb-4">Edit Project</h4>

          <!-- ================= BASIC INFORMATION ================= -->
          <h5 class="section-title">Basic Information</h5>
          <Divider />

          <div class="p-fluid formgrid grid">
            <div class="field col-12 md:col-6">
              <label class="font-semibold">Project Name *</label>
              <InputText v-model="form.title" class="w-full" />
            </div>

            <div class="field col-12 md:col-6">
              <label class="font-semibold">Client / Owner Name</label>
              <InputText v-model="form.owner_name" class="w-full" />
            </div>
          </div>

          <!-- ================= SCHEDULE & BUDGET ================= -->
          <h5 class="section-title mt-4">Schedule & Budget</h5>
          <Divider />

          <div class="p-fluid formgrid grid">
            <div class="field col-12 md:col-4">
              <label>Start Date</label>
              <Calendar v-model="form.start_date" class="w-full" dateFormat="yy-mm-dd" />
            </div>

            <div class="field col-12 md:col-4">
              <label>Expected End Date</label>
              <Calendar v-model="form.expected_end_date" class="w-full" dateFormat="yy-mm-dd" />
            </div>

            <div class="field col-12 md:col-4">
              <label>Budget (KES)</label>
              <InputNumber
                v-model="form.budget_kes"
                mode="currency"
                currency="KES"
                locale="en-KE"
                class="w-full"
              />
            </div>
          </div>

          <!-- ================= CLASSIFICATION ================= -->
          <h5 class="section-title mt-4">Classification</h5>
          <Divider />

          <div class="p-fluid formgrid grid">
            <div class="field col-12 md:col-4">
              <label>Status</label>
              <Dropdown
                v-model="form.status"
                :options="statusOptions"
                optionLabel="label"
                optionValue="value"
                class="w-full"
              />
            </div>

            <div class="field col-12 md:col-4">
              <label>Sector</label>
              <Dropdown
                v-model="form.sector"
                :options="sectorOptions"
                class="w-full"
              />
            </div>

            <div class="field col-12 md:col-4">
              <label>Category</label>
              <Dropdown
                v-model="form.category"
                :options="categoryOptions"
                class="w-full"
              />
            </div>

            <div class="field col-12 md:col-4">
              <label>Owner Type</label>
              <Dropdown
                v-model="form.owner_type"
                :options="ownerTypeOptions"
                optionLabel="label"
                optionValue="value"
                class="w-full"
              />
            </div>

            <div class="field col-12 md:col-4">
              <label>Region</label>
              <Dropdown
                v-model="form.region"
                :options="regionOptions"
                class="w-full"
              />
            </div>

            <div class="field col-12 md:col-4">
              <label>County</label>
              <Dropdown
                v-model="form.county"
                :options="countyOptions"
                class="w-full"
              />
            </div>

            <div class="field col-12 md:col-4">
              <label>Sub-County</label>
              <Dropdown
                v-model="form.sub_county"
                :options="subCountyOptions"
                class="w-full"
              />
            </div>
          </div>

          <!-- ================= ACTIONS ================= -->
          <div class="flex justify-content-end gap-2 mt-4">
            <Button
              label="Cancel"
              icon="pi pi-times"
              severity="secondary"
              outlined
              @click="goBack"
            />
            <Button
              label="Save Changes"
              icon="pi pi-save"
              severity="success"
              @click="save"
            />
          </div>

        </template>

        <!-- ================= NOT FOUND ================= -->
        <div v-else class="text-red-500">
          Project not found.
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

/* PrimeVue */
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Dropdown from "primevue/dropdown";
import Calendar from "primevue/calendar";
import Button from "primevue/button";
import Divider from "primevue/divider";

/* Data */
import { counties } from "../../components/data/projects.master.js";

const route = useRoute();
const router = useRouter();

/* -----------------------------------
   Find project
----------------------------------- */
const project = computed(() =>
  counties.flatMap(c => c.projects).find(p => p.project_id === route.params.id) || null
);

/* -----------------------------------
   Editable form (EMPTY INIT)
----------------------------------- */
const form = reactive({
  title: "",
  owner_name: "",
  sector: "",
  category: "",
  owner_type: "",
  status: "",
  region: "",
  county: "",
  sub_county: "",
  budget_kes: 0,
  start_date: null,
  expected_end_date: null
});

/* -----------------------------------
   🔥 Populate form when project loads
----------------------------------- */
watch(project, p => {
  if (!p) return;

  form.title = p.title;
  form.owner_name = p.owner_name || "";
  form.sector = p.sector;
  form.category = p.category;
  form.owner_type = p.owner_type;
  form.status = p.status;
  form.region = p.region || "";
  form.county = p.county || "";
  form.sub_county = p.site?.sub_county || "";
  form.budget_kes = p.budget_kes;
  form.start_date = p.start_date;
  form.expected_end_date = p.expected_end_date || null;
}, { immediate: true });

/* -----------------------------------
   Options (MATCH CREATE)
----------------------------------- */
const sectorOptions = ["Housing", "Infrastructure", "Health", "Education"];

const categoryOptions = [
  "Affordable Housing",
  "Infrastructure",
  "Commercial",
  "Residential",
  "Mixed-Use"
];

const ownerTypeOptions = [
  { label: "Government", value: "government" },
  { label: "Private", value: "private" },
  { label: "NGO", value: "ngo" },
  { label: "PPP", value: "ppp" },
  { label: "Other", value: "other" }
];

const statusOptions = [
  { label: "Planned", value: "planned" },
  { label: "In Progress", value: "in_progress" },
  { label: "On Hold", value: "on_hold" },
  { label: "Completed", value: "completed" }
];

const regionOptions = ["Coast", "Nairobi Metropolitan", "Rift Valley"];
const countyOptions = ["Mombasa", "Nairobi", "Kilifi"];
const subCountyOptions = ["Mvita", "Likoni", "Changamwe", "Kisauni"];

/* -----------------------------------
   Actions
----------------------------------- */
const goBack = () => {
  router.push(`/app/projects/${route.params.id}`);
};

const save = () => {
  console.log("UPDATED PROJECT DATA:", { ...form });

  // 🔔 Future:
  // api.updateProject(route.params.id, form)

  router.push(`/app/projects/${route.params.id}`);
};
</script>
