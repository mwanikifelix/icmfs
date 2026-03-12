<script setup>
import { ref, computed } from "vue";
import { regions } from "@/components/data/locations";

const region = ref(null);
const county = ref(null);
const subCounty = ref(null);

const siteName = ref("");
const siteCode = ref("");
const status = ref("Active");

const counties = computed(() => region.value?.counties || []);
const subCounties = computed(() => county.value?.subCounties || []);

const saveSite = () => {
  if (!subCounty.value) return alert("Select SubCounty");
  alert("Site saved (prototype)");
};
</script>

<template>
  <div class="card">
    <h3>Create Site</h3>

    <div class="grid">
      <div class="col-4">
        <Dropdown v-model="region" :options="regions" optionLabel="name" placeholder="Region" />
      </div>
      <div class="col-4">
        <Dropdown v-model="county" :options="counties" optionLabel="name" placeholder="County" />
      </div>
      <div class="col-4">
        <Dropdown v-model="subCounty" :options="subCounties" optionLabel="name" placeholder="SubCounty" />
      </div>
    </div>

    <div class="grid mt-3">
      <div class="col-6">
        <InputText v-model="siteName" placeholder="Site Name" />
      </div>
      <div class="col-6">
        <InputText v-model="siteCode" placeholder="Site Code" />
      </div>
    </div>

    <Button class="mt-4" label="Save Site" @click="saveSite" />
  </div>
</template>
