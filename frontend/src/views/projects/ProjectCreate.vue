<template>
  <PageWrapper
    title="Create New Project"
    subtitle="Fill in the details to create a new construction project"
    :breadcrumbItems="breadcrumbItems"
  >
    <FormCard
      title="Project Information"
      subtitle="Basic project details, schedule, and classification"
      :loading="loading"
      @submit="createProject"
      @cancel="handleCancel"
    >

      <!-- INFO CALLOUT -->
      <Message severity="info" icon="pi pi-info-circle" class="mb-4">
        You can save this project as a draft and complete remaining details later.
      </Message>

      <!-- ================= BASIC INFORMATION ================= -->
      <h5 class="section-title">Basic Information</h5>
      <Divider />

      <div class="p-fluid formgrid grid">
        <!-- Project Name -->
        <div class="field col-12 md:col-6">
          <label class="font-semibold">
            Project Name <span class="text-red-500">*</span>
          </label>
          <span class="p-input-icon-left w-full">
            <i class="pi pi-briefcase" />
            <InputText
              v-model="project.name"
              placeholder="Enter project name"
              class="w-full"
              :class="{ 'p-invalid': submitted && !project.name }"
            />
          </span>
          <small v-if="submitted && !project.name" class="p-error">
            Project name is required
          </small>
        </div>

        <!-- Client -->
        <div class="field col-12 md:col-6">
          <label class="font-semibold">
            Client <span class="text-red-500">*</span>
          </label>
          <span class="p-input-icon-left w-full">
            <i class="pi pi-building" />
            <InputText
              v-model="project.client"
              placeholder="Enter client name"
              class="w-full"
              :class="{ 'p-invalid': submitted && !project.client }"
            />
          </span>
          <small v-if="submitted && !project.client" class="p-error">
            Client name is required
          </small>
        </div>
      </div>

      <!-- ================= SCHEDULE & BUDGET ================= -->
      <h5 class="section-title mt-4">Schedule & Budget</h5>
      <Divider />

      <div class="p-fluid formgrid grid">
        <!-- Start Date -->
        <div class="field col-12 md:col-4">
          <label class="font-semibold">
            Start Date <span class="text-red-500">*</span>
          </label>
          <Calendar
            v-model="project.startDate"
            dateFormat="yy-mm-dd"
            showIcon
            class="w-full"
            :class="{ 'p-invalid': submitted && !project.startDate }"
          />
        </div>

        <!-- End Date -->
        <div class="field col-12 md:col-4">
          <label class="font-semibold">
            Expected End Date <span class="text-red-500">*</span>
          </label>
          <Calendar
            v-model="project.endDate"
            dateFormat="yy-mm-dd"
            showIcon
            class="w-full"
            :minDate="project.startDate"
            :class="{ 'p-invalid': submitted && !project.endDate }"
          />
        </div>

        <!-- Budget -->
        <div class="field col-12 md:col-4">
          <label class="font-semibold">
            Budget (KES) <span class="text-red-500">*</span>
          </label>
          <InputNumber
            v-model="project.budget"
            mode="currency"
            currency="KES"
            locale="en-KE"
            class="w-full"
            :class="{ 'p-invalid': submitted && project.budget <= 0 }"
          />
        </div>
                    <!-- Owner Type -->
          <div class="field col-12 md:col-4">
            <label class="font-semibold">
              Owner Type <span class="text-red-500">*</span>
            </label>

            <Select
              v-model="project.owner_type"
              :options="ownerTypes"
              optionLabel="label"
              optionValue="value"
              placeholder="Select Owner Type"
              class="w-full"
              :class="{ 'p-invalid': submitted && !project.owner_type }"
            />

            <small v-if="submitted && !project.owner_type" class="p-error">
              Owner type is required
            </small>
          </div>

      </div>

      <!-- ================= CLASSIFICATION ================= -->
      <h5 class="section-title mt-4">Classification</h5>
      <Divider />

      <div class="p-fluid formgrid grid">
        <!-- Status -->
        <div class="field col-12 md:col-4">
          <label class="font-semibold">
            Status <span class="text-red-500">*</span>
          </label>
          <Select
            v-model="project.status"
            :options="statuses"
            optionLabel="label"
            optionValue="value"
            placeholder="Select Status"
            class="w-full"
            :class="{ 'p-invalid': submitted && !project.status }"
          />
        </div>

        <!-- Region -->
        <div class="field col-12 md:col-4">
          <label class="font-semibold">
            Region <span class="text-red-500">*</span>
          </label>
          <Select
            v-model="project.region"
            :options="regions"
            optionLabel="name"
            optionValue="value"
            placeholder="Select Region"
            class="w-full"
            :class="{ 'p-invalid': submitted && !project.region }"
          />
        </div>

        <!-- Category -->
        <div class="field col-12 md:col-4">
          <label class="font-semibold">Category</label>
          <Select
            v-model="project.category"
            :options="categories"
            placeholder="Select Category"
            class="w-full"
          />
        </div>
      </div>

      <!-- ================= DESCRIPTION ================= -->
      <h5 class="section-title mt-4">Description</h5>
      <Divider />

      <div class="p-fluid formgrid grid">
        <div class="field col-12">
          <Textarea
            v-model="project.description"
            rows="5"
            placeholder="Enter project description, objectives, and key details..."
            class="w-full"
          />
        </div>
      </div>

      <!-- ================= FOOTER ACTIONS ================= -->
      <template #footer-actions>
        <Button
          label="Cancel"
          icon="pi pi-times"
          severity="secondary"
          outlined
          @click="handleCancel"
        />
        <Button
          label="Save as Draft"
          icon="pi pi-save"
          severity="info"
          outlined
          @click="saveDraft"
        />
        <Button
          label="Create Project"
          icon="pi pi-check"
          severity="success"
          class="p-button-lg"
          @click="createProject"
        />
      </template>

    </FormCard>
  </PageWrapper>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "primevue/usetoast";

/* Layout */
import PageWrapper from "@/components/common/PageWrapper.vue";
import FormCard from "@/components/common/FormCard.vue";

/* PrimeVue */
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Calendar from "primevue/calendar";
import Select from "primevue/select";
import Textarea from "primevue/textarea";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Message from "primevue/message";

const router = useRouter();
const toast = useToast();

/* Breadcrumb */
const breadcrumbItems = ref([
  { label: "Projects", to: "/app/projects" },
  { label: "Create Project" }
]);

/* State */
const loading = ref(false);
const submitted = ref(false);

/* Form model */
const project = ref({
  name: "",
  client: "",
  startDate: null,
  endDate: null,
  budget: 0,
  status: "",
  region: "",
  category: "",
 owner_type: "", 
  description: ""

});

/* Options */
const statuses = ref([
  { label: "Planned", value: "planned" },
  { label: "In Progress", value: "in_progress" },
  { label: "On Hold", value: "on_hold" },
  { label: "Completed", value: "completed" }
]);

const regions = ref([
  { name: "Nairobi Region", value: "nairobi" },
  { name: "Coast Region", value: "coast" },
  { name: "Rift Valley", value: "rift_valley" },
  { name: "Western Region", value: "western" },
  { name: "Nyanza Region", value: "nyanza" },
  { name: "Central Region", value: "central" }
]);

const ownerTypes = ref([
  { label: "Government", value: "government" },
  { label: "Private", value: "private" },
  { label: "NGO", value: "ngo" },
  { label: "Public–Private Partnership (PPP)", value: "ppp" },
  { label: "Faith-Based / CBO", value: "faith_based" },
  { label: "Other", value: "other" }
]);

const categories = ref([
  "Affordable Housing",
  "Infrastructure",
  "Commercial",
  "Residential",
  "Mixed-Use"
]);

/* Validation */
const validateForm = () => {
  submitted.value = true;
  return (
    project.value.name &&
    project.value.client &&
    project.value.startDate &&
    project.value.endDate &&
    project.value.budget > 0 &&
    project.value.status &&
    project.value.region
   
  );
};

/* Actions */
const createProject = async () => {
  if (!validateForm()) {
    toast.add({
      severity: "error",
      summary: "Validation Error",
      detail: "Please fill in all required fields",
      life: 3000
    });
    return;
  }

  loading.value = true;

  try {
    await new Promise(r => setTimeout(r, 1000));

    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Project created successfully",
      life: 3000
    });

    router.push("/app/projects");
  } finally {
    loading.value = false;
  }
};

const saveDraft = async () => {
  loading.value = true;
  await new Promise(r => setTimeout(r, 800));
  toast.add({
    severity: "info",
    summary: "Draft Saved",
    detail: "Project saved as draft",
    life: 3000
  });
  router.push("/app/projects");
};

const handleCancel = () => {
  router.push("/app/projects");
};
</script>

<style scoped>
.section-title {
  font-weight: 600;
  font-size: 1.1rem;
}

.p-invalid {
  border-color: #e24c4c;
}

.p-error {
  color: #e24c4c;
  font-size: 0.875rem;
}
</style>
