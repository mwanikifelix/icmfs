
<!-- ============================================ -->
<!-- PATTERN 2: Standard Form Card Component -->
<!-- src/components/common/FormCard.vue -->
<!-- ============================================ -->
<script setup>
defineProps({
  title: String,
  subtitle: String,
  loading: { type: Boolean, default: false }
})

defineEmits(['submit', 'cancel'])
</script>

<template>
  <Card>
    <template #title>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-xl font-semibold">{{ title }}</h2>
          <p v-if="subtitle" class="text-sm text-gray-600 mt-1">{{ subtitle }}</p>
        </div>
        <slot name="header-actions" />
      </div>
    </template>

    <template #content>
      <div v-if="loading" class="flex justify-center py-8">
        <ProgressSpinner />
      </div>
      <div v-else>
        <slot />
      </div>
    </template>

    <template #footer>
      <div class="flex justify-end gap-2">
        <slot name="footer-actions">
          <Button label="Cancel" severity="secondary" @click="$emit('cancel')" />
          <Button label="Submit" @click="$emit('submit')" />
        </slot>
      </div>
    </template>
  </Card>
</template>

