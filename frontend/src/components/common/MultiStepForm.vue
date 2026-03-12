
<!-- ============================================ -->
<!-- PATTERN 4: File Upload Form Pattern -->
<!-- src/views/sites/DailyReports.vue -->
<!-- ============================================ -->
<script setup>
import { ref } from 'vue'
import PageWrapper from '@/components/common/PageWrapper.vue'
import FormCard from '@/components/common/FormCard.vue'

const reportData = ref({
  date: new Date(),
  activities: '',
  workforce: null,
  materials: [],
  photos: []
})

const onFileUpload = (event) => {
  reportData.value.photos = event.files
}

const handleSubmit = async () => {
  const formData = new FormData()
  formData.append('date', reportData.value.date)
  formData.append('activities', reportData.value.activities)
  
  // Append files
  reportData.value.photos.forEach((file, index) => {
    formData.append(`photos[${index}]`, file)
  })
  
  // API call with formData
}
</script>

<template>
  <PageWrapper title="Daily Site Report">
    <FormCard
      title="Report Details"
      @submit="handleSubmit"
    >
      <div class="grid gap-4">
        <div class="field">
          <label>Report Date</label>
          <Calendar v-model="reportData.date" class="w-full" />
        </div>

        <div class="field">
          <label>Activities Performed</label>
          <Textarea v-model="reportData.activities" rows="5" class="w-full" />
        </div>

        <div class="field">
          <label>Workforce Count</label>
          <InputNumber v-model="reportData.workforce" class="w-full" />
        </div>

        <!-- File Upload -->
        <div class="field">
          <label>Site Photos</label>
          <FileUpload
            mode="basic"
            multiple
            accept="image/*"
            :maxFileSize="5000000"
            @select="onFileUpload"
            chooseLabel="Upload Photos"
          />
          <small class="text-gray-600">Max 5MB per file</small>
        </div>
      </div>
    </FormCard>
  </PageWrapper>
</template>


<!-- ============================================ -->
<!-- PATTERN 5: Multi-Step Form Pattern -->
<!-- src/components/common/MultiStepForm.vue -->
<!-- ============================================ -->
<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  steps: Array // ['Basic Info', 'Details', 'Review']
})

const activeStep = ref(0)

const isFirstStep = computed(() => activeStep.value === 0)
const isLastStep = computed(() => activeStep.value === props.steps.length - 1)

const nextStep = () => {
  if (!isLastStep.value) activeStep.value++
}

const prevStep = () => {
  if (!isFirstStep.value) activeStep.value--
}

defineExpose({ nextStep, prevStep, activeStep })
</script>

<template>
  <Card>
    <template #title>
      <Steps :model="steps" :activeStep="activeStep" :readonly="false" />
    </template>

    <template #content>
      <slot :name="`step-${activeStep}`" />
    </template>

    <template #footer>
      <div class="flex justify-between">
        <Button 
          label="Previous" 
          :disabled="isFirstStep"
          @click="prevStep"
          severity="secondary"
        />
        <Button 
          :label="isLastStep ? 'Submit' : 'Next'"
          @click="isLastStep ? $emit('submit') : nextStep()"
        />
      </div>
    </template>
  </Card>
</template>


<!-- ============================================ -->
<!-- HOW TO ADOPT ACROSS ALL FORMS -->
<!-- ============================================ -->

/*
✅ ADOPTION STRATEGY:

1. CREATE REUSABLE COMPONENTS (One Time Setup):
   - PageWrapper.vue → Consistent page structure
   - FormCard.vue → Standardized form cards
   - MultiStepForm.vue → For complex forms

2. UPDATE EXISTING FORMS (Gradually):
   Replace this:
   ```vue
   <template>
     <div>
       <h1>Create Project</h1>
       <form>...</form>
     </div>
   </template>
   ```

   With this:
   ```vue
   <template>
     <PageWrapper title="Create Project">
       <FormCard @submit="handleSubmit">
         <!-- form fields -->
       </FormCard>
     </PageWrapper>
   </template>
   ```
