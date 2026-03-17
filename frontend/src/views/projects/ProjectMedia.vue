<template>
  <div class="card">

    <!-- ================= HEADER ================= -->
    <div class="flex justify-content-between align-items-center mb-4">
      <h4>Project Media</h4>

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

        <Button
          icon="pi pi-file"
          label="Upload Documents"
          severity="secondary"
          @click="docInput.click()"
        />

        <Button
          label="Upload Selected Videos"
          icon="pi pi-upload"
          class="mt-3"
          @click="uploadVideos"
        />

      </div>
    </div>

    <!-- ================= FILE INPUTS ================= -->

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

    <input
      ref="docInput"
      type="file"
      accept=".pdf,.doc,.docx,.xls,.xlsx"
      multiple
      hidden
      @change="handleDocUpload"
    />

    <!-- ================= DRAG DROP ================= -->

    <div
      class="upload-dropzone"
      @dragover.prevent
      @drop.prevent="handleDropUpload"
    >
      <i class="pi pi-upload text-2xl mb-2"></i>
      <p class="text-sm">
        Drag & Drop Photos, Videos or Documents here
      </p>
      <small class="text-gray-500">
        or use the upload buttons above
      </small>
    </div>

    <!-- ================= EMPTY ================= -->

    <div
      v-if="!media.photos.length && !media.videos.length && !media.docs.length"
      class="text-gray-500 mb-4"
    >
      No media uploaded yet.
    </div>

    <!-- ================= PHOTOS ================= -->

    <template v-if="media.photos.length">

      <h5 class="mb-3">Photos</h5>

      <div class="grid">
        <div
          v-for="photo in media.photos"
          :key="photo.id"
          class="col-12 md:col-4"
        >
          <div class="media-card">

            <img
              :src="photo.file"
              class="w-full border-round"
            />

            <small class="text-gray-500">
              Uploaded: {{ photo.uploaded_at }}
            </small>

          </div>
        </div>
      </div>

    </template>

    <!-- ================= VIDEO PREVIEW ================= -->

      <template v-if="videoPreview.length">

    <h5 class="mt-4 mb-3">Video Preview</h5>

    <div class="grid">

      <div
        v-for="video in videoPreview"
        :key="video.preview"
        class="col-12 md:col-4"
      >

        <div class="video-preview-card">

          <video controls class="video-preview">
            <source :src="video.preview">
          </video>

        </div>

      </div>

    </div>

    <Button
      label="Upload Videos"
      icon="pi pi-upload"
      class="mt-3"
      @click="uploadVideos"
    />

    </template>
    <!-- ================= VIDEOS ================= -->

    <template v-if="media.videos.length">

      <h5 class="mt-4 mb-3">Videos</h5>

      <div class="grid">
        <div
          v-for="video in media.videos"
          :key="video.id"
          class="col-12 md:col-6"
        >
          <div class="media-card">

            <video controls class="w-full border-round">
              <source :src="video.file">
            </video>

            <small class="text-gray-500">
              Uploaded: {{ video.uploaded_at }}
            </small>

          </div>
        </div>
      </div>

    </template>

    <!-- ================= DOCUMENTS ================= -->

    <template v-if="media.docs.length">

      <h5 class="mt-4 mb-3">Documents</h5>

      <div class="grid">

        <div
          v-for="doc in media.docs"
          :key="doc.id"
          class="col-12 md:col-4"
        >
          <div class="media-card">

            <a :href="doc.file" target="_blank">
              📄 Download Document
            </a>

            <small class="text-gray-500 block">
              Uploaded: {{ doc.uploaded_at }}
            </small>

          </div>
        </div>

      </div>

    </template>

    <Divider class="my-4" />

    <small class="text-gray-500">
      Uploads are allowed for Site Engineers and Project Managers only.
    </small>

  </div>
</template>

<script setup>

import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import api from "@/api/api"
import imageCompression from "browser-image-compression"

import Button from "primevue/button"
import Divider from "primevue/divider"

const route = useRoute()

const photoInput = ref(null)
const videoInput = ref(null)
const docInput = ref(null)

const videoPreview = ref([])

const media = ref({
  photos: [],
  videos: [],
  docs: []
})

/* ================= LOAD MEDIA ================= */

const loadMedia = async () => {

  const res = await api.get("/api/projects/media/", {
    params: { project: route.params.id }
  })

  const files = res.data.results ?? res.data

  media.value.photos = files.filter(f => f.media_type === "photo")
  media.value.videos = files.filter(f => f.media_type === "video")
  media.value.docs = files.filter(f => f.media_type === "document")

}

/* ================= PHOTO UPLOAD ================= */

/* const handlePhotoUpload = async (event) => {

  const files = event.target.files

  for (let file of files) {

    const compressed = await imageCompression(file,{
      maxSizeMB:1,
      maxWidthOrHeight:1920
    })

    const formData = new FormData()

    formData.append("file",compressed)
    formData.append("media_type","photo")
    formData.append("project",route.params.id)

    await api.post("/api/projects/media/",formData,{
      headers:{ "Content-Type":"multipart/form-data"}
    })

  }

  loadMedia()

} */


const handlePhotoUpload = async (event) => {

  const files = event.target.files
  if (!files.length) return

  for (let file of files) {

    const formData = new FormData()

    formData.append("file", file)
    formData.append("project", route.params.id)
    formData.append("media_type", "photo")

    await api.post("/api/projects/media/", formData)

  }

}

/* ================= VIDEO SELECT ================= */

const handleVideoUpload = (event)=>{

  const files = event.target.files

  videoPreview.value = []

  for(let file of files){

    videoPreview.value.push({
      file,
      preview:URL.createObjectURL(file)
    })

  }

}

/* ================= VIDEO UPLOAD ================= */

/* const uploadVideos = async ()=>{

  for(let v of videoPreview.value){

    const formData = new FormData()

    formData.append("file",v.file)
    formData.append("media_type","video")
    formData.append("project",route.params.id)

    await api.post("/api/projects/media/",formData,{
      headers:{ "Content-Type":"multipart/form-data"}
    })

  }

  videoPreview.value = []

  loadMedia()

}
 */

 const uploadVideos = async () => {

  for (let v of videoPreview.value) {

    const formData = new FormData()

    formData.append("file", v.file)
    formData.append("project", route.params.id)
    formData.append("media_type", "video")

    await api.post("/api/projects/media/", formData)

  }

}
/* ================= DOCUMENT UPLOAD ================= */

/* const handleDocUpload = async(event)=>{

  const files = event.target.files

  for(let file of files){

    const formData = new FormData()

    formData.append("file",file)
    formData.append("media_type","document")
    formData.append("project",route.params.id)

    await api.post("/api/projects/media/",formData,{
      headers:{ "Content-Type":"multipart/form-data"}
    })

  }

  loadMedia()

} */

const handleDocUpload = async (event) => {

  const files = event.target.files
  if (!files.length) return

  for (let file of files) {

    const formData = new FormData()

    formData.append("file", file)
    formData.append("project", route.params.id)
    formData.append("media_type", "document")

    await api.post("/api/projects/media/", formData)

  }

}

/* ================= DRAG DROP ================= */

const handleDropUpload = async(event)=>{

  const files = event.dataTransfer.files

  for(let file of files){

    let type = "document"

    if(file.type.startsWith("image")) type="photo"
    if(file.type.startsWith("video")) type="video"

    const formData = new FormData()

    formData.append("file",file)
    formData.append("media_type",type)
    formData.append("project",route.params.id)

    await api.post("/api/projects/media/",formData,{
      headers:{ "Content-Type":"multipart/form-data"}
    })

  }

  loadMedia()

}

onMounted(loadMedia)

</script>

<style scoped>

.media-card{
background:#fff;
padding:.75rem;
border-radius:12px;
box-shadow:0 4px 10px rgba(0,0,0,.06);
}

.upload-dropzone{
border:2px dashed #cbd5e1;
border-radius:10px;
padding:2rem;
text-align:center;
background:#f8fafc;
cursor:pointer;
transition:all .2s;
margin-bottom:1.5rem;
}

.upload-dropzone:hover{
border-color:#1976d2;
background:#eef5ff;
}



.video-preview-card{
  background:#fff;
  padding:0.5rem;
  border-radius:10px;
  box-shadow:0 4px 10px rgba(0,0,0,0.05);
}

.video-preview{
  width:100%;
  max-height:200px;
  object-fit:cover;
  border-radius:8px;
}
</style>