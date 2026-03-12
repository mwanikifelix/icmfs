<script setup>
import { ref, computed } from "vue";
import { regions } from "@/components/data/locations";
import { sites } from "@/components/data/sites";


const selectedRegion = ref(null);
const selectedCounty = ref(null);
const selectedSubCounty = ref(null);

const counties = computed(() =>
  selectedRegion.value?.counties || []
);

const subCounties = computed(() =>
  selectedCounty.value?.subCounties || []
);

const filteredSites = computed(() => {
  return sites.filter(s =>
    (!selectedRegion.value || s.regionId === selectedRegion.value.id) &&
    (!selectedCounty.value || s.countyId === selectedCounty.value.id) &&
    (!selectedSubCounty.value || s.subCountyId === selectedSubCounty.value.id)
  );
});
</script>

<template>
  <div class="card">
    <!-- Filters -->
    <div class="flex gap-3 mb-4">
      <Dropdown v-model="selectedRegion"
        :options="regions"
        optionLabel="name"
        placeholder="Select Region" />

      <Dropdown v-model="selectedCounty"
        :options="counties"
        optionLabel="name"
        placeholder="Select County" />

      <Dropdown v-model="selectedSubCounty"
        :options="subCounties"
        optionLabel="name"
        placeholder="Select SubCounty" />

      <RouterLink to="/sites/create">
        <Button label="+ New Site" />
      </RouterLink>
    </div>

    <!-- Table -->
    <DataTable :value="filteredSites">
      <Column field="code" header="Code" />
      <Column field="name" header="Site Name" />
      <Column field="status" header="Status" />
      <Column field="workers" header="Workers" />
      <Column header="Actions">
        <template #body="{ data }">
          <RouterLink :to="`/sites/${data.id}`">
            <Button label="View" size="small" />
          </RouterLink>
        </template>
      </Column>
    </DataTable>
  </div>
</template>
