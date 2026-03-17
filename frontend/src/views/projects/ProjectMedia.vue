<template>
  <div class="card">

    <!-- HEADER -->
    <div class="flex justify-content-between align-items-center mb-4">
      <h4>Project Media</h4>

      <div class="flex gap-2">

        <!-- ✅ PROJECT SELECT (ADDED ONLY) -->
        <Dropdown
          v-model="selectedProject"
          :options="projects"
          optionLabel="name"
          optionValue="id"
          placeholder="Select Project"
        />

        <Button label="Photos" icon="pi pi-image" @click="photoInput.click()" />
        <Button label="Videos" icon="pi pi-video" @click="videoInput.click()" />
        <Button label="Docs" icon="pi pi-file" @click="docInput.click()" />
      </div>
    </div>

    <!-- INPUTS -->
    <input ref="photoInput" type="file" accept="image/*" multiple hidden @change="handleUpload($event,'photo')" />
    <input ref="videoInput" type="file" accept="video/*" multiple hidden @change="handleUpload($event,'video')" />
    <input ref="docInput" type="file" accept=".pdf,.doc,.docx,.xls,.xlsx" multiple hidden @change="handleUpload($event,'document')" />

    <!-- DROP -->
    <div class="upload-dropzone" @dragover.prevent @drop.prevent="handleDropUpload">
      Drag & Drop Files Here
    </div>

    <!-- TABS -->
    <div class="flex gap-2 mb-3">
      <Button label="Media Overview" :severity="activeTab==='overview'?'primary':'secondary'" @click="activeTab='overview'" />
      <Button label="Photos & Videos" :severity="activeTab==='media'?'primary':'secondary'" @click="activeTab='media'" />
      <Button label="Documents" :severity="activeTab==='docs'?'primary':'secondary'" @click="activeTab='docs'" />
    </div>

    <!-- OVERVIEW -->
    <div v-if="activeTab==='overview'" class="overview-card">
      <h5>Project Media Overview</h5>

      <div class="overview-stats">
        <div class="stat">
          <h3>{{ media.photos.length }}</h3>
          <p>Photos</p>
        </div>
        <div class="stat">
          <h3>{{ media.videos.length }}</h3>
          <p>Videos</p>
        </div>
        <div class="stat">
          <h3>{{ media.docs.length }}</h3>
          <p>Documents</p>
        </div>
      </div>
    </div>

    <!-- GALLERY -->
    <div class="gallery-grid">

      <div v-for="item in filteredMedia" :key="item.id" class="gallery-item">

        <div class="media-card">

          <!-- IMAGE -->
          <img
            v-if="item.media_type==='photo'"
            :src="item.file"
            class="gallery-img"
            loading="lazy"
            @click="openPreview(item.file)"
          />

          <!-- VIDEO -->
          <div v-if="item.media_type==='video'" class="video-wrapper">
            <video class="gallery-img" muted>
              <source :src="item.file" />
            </video>
            <i class="pi pi-play play-icon"></i>
          </div>

          <!-- DOC -->
          <div v-if="item.media_type==='document'" class="doc-wrapper">
            <i class="pi pi-file-pdf doc-icon"></i>
          </div>

          <!-- PROJECT LABEL -->
          <small class="project-tag">
            📁 {{ item.project_name || 'Project' }}
          </small>

          <!-- OVERLAY -->
          <div class="overlay">
            <Button icon="pi pi-eye" class="p-button-sm" @click="view(item)" />
            <Button icon="pi pi-trash" severity="danger" class="p-button-sm" @click="remove(item.id)" />
          </div>

        </div>

      </div>

    </div>

    <!-- PREVIEW -->
    <div v-if="previewImage" class="preview-overlay" @click="previewImage=null">
      <img :src="previewImage" class="preview-full" />
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import api from "@/api/api"
import Button from "primevue/button"
import Dropdown from "primevue/dropdown" // ✅ ADDED

const route = useRoute()

/* ✅ ADDED */
const selectedProject = ref(null)
const projects = ref([])

const photoInput = ref(null)
const videoInput = ref(null)
const docInput = ref(null)

const previewImage = ref(null)
const activeTab = ref("overview")

const media = reactive({
  photos: [],
  videos: [],
  docs: []
})

const filteredMedia = computed(() => {
  if (activeTab.value === "media") {
    return [...media.photos, ...media.videos]
  }
  if (activeTab.value === "docs") {
    return media.docs
  }
  return [...media.photos, ...media.videos, ...media.docs]
})

const openPreview = (src)=> previewImage.value = src

const view = (item)=>{
  if(item.media_type==='photo') openPreview(item.file)
  else window.open(item.file,"_blank")
}

const remove = async(id)=>{
  await api.delete(`/api/projects/media/${id}/`)
  loadMedia()
}

/* ✅ LOAD PROJECTS (ADDED) */
const loadProjects = async () => {
  const res = await api.get("/api/projects/projects/")
  projects.value = res.data.results ?? res.data
}

/* ✅ GET PROJECT ID (SMART LOGIC) */
const getProjectId = () => selectedProject.value || route.params.id

const loadMedia = async ()=>{
  const projectId = getProjectId()
  if (!projectId) return

  const res = await api.get("/api/projects/media/",{
    params:{ project: projectId }
  })

  const data = res.data.results ?? res.data

  media.photos = data.filter(x=>x.media_type==='photo')
  media.videos = data.filter(x=>x.media_type==='video')
  media.docs = data.filter(x=>x.media_type==='document')
}

const handleUpload = async (e,type)=>{

  const projectId = getProjectId()

  if (!projectId) {
    alert("Select a project first")
    return
  }

  for(let file of e.target.files){
    const fd = new FormData()
    fd.append("file",file)
    fd.append("project",projectId)
    fd.append("media_type",type)
    await api.post("/api/projects/media/",fd)
  }

  loadMedia()
}

const handleDropUpload = async (e)=>{

  const projectId = getProjectId()

  if (!projectId) {
    alert("Select a project first")
    return
  }

  for(let file of e.dataTransfer.files){

    let type="document"
    if(file.type.startsWith("image")) type="photo"
    if(file.type.startsWith("video")) type="video"

    const fd = new FormData()
    fd.append("file",file)
    fd.append("project",projectId)
    fd.append("media_type",type)

    await api.post("/api/projects/media/",fd)
  }

  loadMedia()
}

/* ✅ UPDATED */
onMounted(()=>{
  loadProjects()
  loadMedia()
})
</script>

<style scoped>

/* (UNCHANGED — exactly your styles) */

.gallery-grid{
  display:flex;
  flex-wrap:wrap;
  gap:12px;
}
.gallery-item{
  width:calc(33.33% - 12px);
}

.media-card{
  position:relative;
  overflow:hidden;
  border-radius:12px;
}

.gallery-img{
  width:100%;
  height:200px;
  object-fit:cover;
}

.video-wrapper{ position:relative; }
.play-icon{
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  color:white;
  font-size:30px;
}

.doc-wrapper{
  height:200px;
  display:flex;
  justify-content:center;
  align-items:center;
  background:#f1f5f9;
}

.project-tag{
  position:absolute;
  bottom:6px;
  left:6px;
  background:rgba(0,0,0,0.6);
  color:white;
  font-size:11px;
  padding:3px 6px;
  border-radius:6px;
}

.overlay{
  position:absolute;
  inset:0;
  background:rgba(0,0,0,0.5);
  display:flex;
  justify-content:center;
  align-items:center;
  gap:10px;
  opacity:0;
  transition:0.3s;
}
.media-card:hover .overlay{
  opacity:1;
}

.preview-overlay{
  position:fixed;
  inset:0;
  background:rgba(0,0,0,0.85);
  display:flex;
  justify-content:center;
  align-items:center;
}
.preview-full{
  max-width:90%;
  max-height:90%;
}

.overview-card{
  background:#f8fafc;
  padding:1rem;
  border-radius:12px;
  margin-bottom:1rem;
}
.overview-stats{
  display:flex;
  gap:20px;
}
.stat{
  flex:1;
  text-align:center;
}

.upload-dropzone{
  border:2px dashed #ccc;
  padding:1rem;
  text-align:center;
  margin-bottom:1rem;
}

</style>