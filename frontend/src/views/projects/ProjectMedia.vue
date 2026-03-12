<template>
  <div class="card">

    <!-- ================= HEADER ================= -->
    <div class="flex justify-content-between align-items-center mb-4">
      <h4>Project Media</h4>

      <!-- Upload Actions -->
      <div class="flex gap-2">
        <Button
          icon="pi pi-image"
          label="Upload Photos"
          severity="secondary"
          @click="photoInput.click()"
        />
        <Button
          icon="pi pi-video"
          label="Upload Videos"
          severity="secondary"
          @click="videoInput.click()"
        />
      </div>
    </div>

    <!-- ================= HIDDEN FILE INPUTS ================= -->
    <input
      ref="photoInput"
      type="file"
      accept="image/*"
      multiple
      hidden
      @change="handlePhotoUpload"
    />

    <input
      ref="videoInput"
      type="file"
      accept="video/*"
      multiple
      hidden
      @change="handleVideoUpload"
    />

    <!-- ================= EMPTY STATE ================= -->
    <div
      v-if="!media.photos.length && !media.videos.length"
      class="text-gray-500 mb-4"
    >
      No photos or videos have been uploaded for this project yet.
    </div>

    <!-- ================= PHOTOS ================= -->
    <template v-if="media.photos.length">
      <h5 class="mb-3">Photos</h5>

      <div class="grid">
        <div
          v-for="photo in media.photos"
          :key="photo.file_id"
          class="col-12 md:col-4"
        >
          <div class="media-card">
            <img
              :src="photo.url"
              class="w-full border-round"
              alt="Project Photo"
            />
            <p class="text-sm mt-2">{{ photo.caption }}</p>
            <small class="text-gray-500">
              Uploaded: {{ photo.uploaded_at }}
            </small>
          </div>
        </div>
      </div>
    </template>

    <!-- ================= VIDEOS ================= -->
    <template v-if="media.videos.length">
      <h5 class="mt-4 mb-3">Videos</h5>

      <div class="grid">
        <div
          v-for="video in media.videos"
          :key="video.file_id"
          class="col-12 md:col-6"
        >
          <div class="media-card">
            <video controls class="w-full border-round">
              <source :src="video.url" type="video/mp4" />
              Your browser does not support video playback.
            </video>
            <small class="text-gray-500">
              Duration: {{ video.duration_seconds }} seconds
            </small>
          </div>
        </div>
      </div>
    </template>

    <!-- ================= INFO ================= -->
    <Divider class="my-4" />
    <small class="text-gray-500">
      Uploads are allowed for Site Engineers and Project Managers only.
    </small>

  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";

/* PrimeVue */
import Button from "primevue/button";
import Divider from "primevue/divider";

/* Data */
import { getProjectActivityById } from "../../components/data/project.site.activity.js";

const route = useRoute();

/* -----------------------------------
   Media from latest report
----------------------------------- */
const media = computed(() => {
  const activity = getProjectActivityById(route.params.id);
  const latestReport = activity?.reports?.at(-1);

  return {
    photos: latestReport?.media?.photos || [],
    videos: latestReport?.media?.videos || []
  };
});

/* -----------------------------------
   Upload refs
----------------------------------- */
const photoInput = ref(null);
const videoInput = ref(null);

/* -----------------------------------
   Upload handlers (DUMMY)
----------------------------------- */
const handlePhotoUpload = (event) => {
  const files = event.target.files;
  if (!files.length) return;

  console.log("PHOTO FILES SELECTED:", files);

  // 🔔 FUTURE:
  // - upload to backend
  // - save URL
  // - refresh media
};

const handleVideoUpload = (event) => {
  const files = event.target.files;
  if (!files.length) return;

  console.log("VIDEO FILES SELECTED:", files);

  // 🔔 FUTURE:
  // - upload to backend
  // - save URL
  // - refresh media
};
</script>

<style scoped>
.media-card {
  background: #ffffff;
  padding: 0.75rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
}
</style>
