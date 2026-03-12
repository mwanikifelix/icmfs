<template>
  <FormCard
    :title="mode === 'create' ? 'Create Project' : 'Edit Project'"
    subtitle="Project details, schedule and classification"
    :loading="loading"
    @submit="submit"
    @cancel="cancel"
  >

    <!-- BASIC INFO -->
    <h5 class="section-title">Basic Information</h5>
    <Divider />

    <div class="p-fluid formgrid grid">
      <div class="field col-12 md:col-6">
        <label>Project Name *</label>
        <InputText v-model="form.title" class="w-full" />
      </div>

      <div class="field col-12 md:col-6">
        <label>Client</label>
        <InputText v-model="form.owner_name" class="w-full" />
      </div>
    </div>

    <!-- SCHEDULE -->
    <h5 class="section-title mt-4">Schedule & Budget</h5>
    <Divider />

    <div class="p-fluid formgrid grid">
      <div class="field col-12 md:col-4">
        <label>Start Date</label>
        <Calendar v-model="form.start_date" class="w-full" />
      </div>

      <div class="field col-12 md:col-4">
        <label>Expected End Date</label>
        <Calendar v-model="form.expected_end_date" class="w-full" />
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

    <!-- CLASSIFICATION -->
    <h5 class="section-title mt-4">Classification</h5>
    <Divider />

    <div class="p-fluid formgrid grid">
      <div class="field col-12 md:col-4">
        <label>Status</label>
        <Dropdown v-model="form.status" :options="statusOptions" />
      </div>

      <div class="field col-12 md:col-4">
        <label>Sector</label>
        <Dropdown v-model="form.sector" :options="sectorOptions" />
      </div>

      <div class="field col-12 md:col-4">
        <label>Owner Type</label>
        <Dropdown
          v-model="form.owner_type"
          :options="ownerTypeOptions"
          optionLabel="label"
          optionValue="value"
        />
      </div>
    </div>

    <!-- FOOTER -->
    <template #footer-actions>
      <Button
        label="Cancel"
        severity="secondary"
        outlined
        @click="cancel"
      />
      <Button
        :label="mode === 'create' ? 'Create Project' : 'Save Changes'"
        severity="success"
        icon="pi pi-save"
        @click="submit"
      />
    </template>

  </FormCard>
</template>

<script setup>
import { reactive, watch } from "vue";

import FormCard from "@/components/common/FormCard.vue";
import Divider from "primevue/divider";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Calendar from "primevue/calendar";
import Dropdown from "primevue/dropdown";
import Button from "primevue/button";

const props = defineProps({
  modelValue: Object,
  mode: String,
  loading: Boolean
});

const emit = defineEmits(["submit", "cancel", "update:modelValue"]);

const form = reactive({ ...props.modelValue });

watch(
  () => props.modelValue,
  (v) => Object.assign(form, v),
  { immediate: true }
);

const submit = () => emit("submit", form);
const cancel = () => emit("cancel");

/* OPTIONS */
const sectorOptions = ["Housing", "Infrastructure", "Health", "Education"];

const statusOptions = [
  "planned",
  "in_progress",
  "on_hold",
  "completed"
];

const ownerTypeOptions = [
  { label: "Government", value: "government" },
  { label: "Private", value: "private" },
  { label: "NGO", value: "ngo" },
  { label: "PPP", value: "ppp" }
];
</script>
