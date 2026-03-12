<script setup>
const workers = [
  { id: 1, name: "John K", role: "Supervisor", status: "Present" }
];
</script>

<template>
  <DataTable :value="workers">
    <Column field="name" header="Name" />
    <Column field="role" header="Role" />
    <Column field="status" header="Status" />
  </DataTable>
</template>
