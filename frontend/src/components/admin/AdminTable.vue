<script setup>
defineProps({
  columns: Array,
  rows: Array,
});
</script>

<template>
  <table border="1" width="100%">
    <thead>
      <tr>
        <th v-for="col in columns" :key="col">{{ col }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in rows" :key="row.id">
        <td v-for="col in columns" :key="col">
          {{ row[col] }}
        </td>
      </tr>
    </tbody>
  </table>
</template>
