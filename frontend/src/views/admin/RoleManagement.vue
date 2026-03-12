<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-id-card text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">Role Management</h4>
                        <span class="text-sm" style="color:#b3c8e8;">Define roles and module-level permissions</span>
                    </div>
                </div>
                <Button label="Create Role" icon="pi pi-plus"
                    style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                    @click="openForm()" />
            </div>

            <div class="grid">
                <!-- Role cards -->
                <div class="col-12 lg:col-4">
                    <div class="card h-full">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-list mr-2" style="color:#1976d2;" />Defined Roles
                        </h5>
                        <div class="flex flex-column gap-2">
                            <div v-for="role in roles" :key="role.id"
                                class="flex align-items-center justify-content-between p-3 border-round-lg cursor-pointer border-2 transition-all transition-duration-200"
                                :style="selectedRole?.id === role.id
                                    ? 'border-color:#1976d2;background:#e8f0fe;'
                                    : 'border-color:var(--surface-border);background:var(--surface-50);'"
                                @click="selectedRole = role">
                                <div class="flex align-items-center gap-3">
                                    <div class="flex align-items-center justify-content-center border-round"
                                        style="width:2.2rem;height:2.2rem;" :style="{ background: role.bg }">
                                        <i :class="role.icon" :style="{ color: role.color }" />
                                    </div>
                                    <div>
                                        <div class="font-semibold text-900 text-sm">{{ role.name }}</div>
                                        <div class="text-400 text-xs">{{ role.userCount }} users</div>
                                    </div>
                                </div>
                                <div class="flex gap-1">
                                    <Button icon="pi pi-pencil" text rounded size="small"
                                        v-tooltip.top="'Edit'" @click.stop="openForm(role)" />
                                    <Button icon="pi pi-trash" text rounded size="small"
                                        severity="danger" v-tooltip.top="'Delete'"
                                        :disabled="role.protected" @click.stop="confirmDelete(role)" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Permissions matrix -->
                <div class="col-12 lg:col-8">
                    <div class="card h-full">
                        <div v-if="selectedRole">
                            <div class="flex justify-content-between align-items-center mb-4">
                                <h5 class="mt-0 mb-0" style="color:#0d2347;">
                                    Permissions — <span style="color:#1976d2;">{{ selectedRole.name }}</span>
                                </h5>
                                <Button label="Save Permissions" icon="pi pi-check" size="small"
                                    :loading="saving"
                                    style="background:#1976d2;border-color:#1976d2;"
                                    @click="savePermissions" />
                            </div>

                            <DataTable :value="modules" size="small" stripedRows>
                                <Column field="label" header="Module" style="min-width:160px;">
                                    <template #body="{ data }">
                                        <div class="flex align-items-center gap-2">
                                            <i :class="data.icon" class="text-400" />
                                            <span class="font-medium text-sm">{{ data.label }}</span>
                                        </div>
                                    </template>
                                </Column>
                                <Column v-for="perm in permTypes" :key="perm.key" :header="perm.label" style="width:100px;text-align:center;">
                                    <template #body="{ data }">
                                        <div class="flex justify-content-center">
                                            <Checkbox
                                                v-model="selectedRole.permissions[data.key]"
                                                :binary="false"
                                                :value="perm.key"
                                                :disabled="selectedRole.protected && perm.key === 'view'"
                                            />
                                        </div>
                                    </template>
                                </Column>
                            </DataTable>
                        </div>
                        <div v-else class="flex align-items-center justify-content-center h-full py-8">
                            <div class="text-center text-500">
                                <i class="pi pi-id-card text-4xl mb-3 block text-300" />
                                Select a role to manage its permissions
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Role form dialog -->
        <Dialog v-model:visible="showForm" :header="editRole ? 'Edit Role' : 'Create Role'"
            :modal="true" :style="{ width: '440px' }">
            <div class="flex flex-column gap-3 pt-2">
                <div class="field">
                    <label class="block font-medium mb-2 text-600">Role Name *</label>
                    <InputText v-model="form.name" class="w-full" placeholder="e.g. Finance Officer" />
                </div>
                <div class="field">
                    <label class="block font-medium mb-2 text-600">Description</label>
                    <Textarea v-model="form.description" rows="2" class="w-full" autoResize />
                </div>
                <div class="field">
                    <label class="block font-medium mb-2 text-600">Access Level</label>
                    <div class="flex flex-column gap-2">
                        <div v-for="lvl in accessLevels" :key="lvl.value" class="flex align-items-center gap-2">
                            <RadioButton v-model="form.accessLevel" :value="lvl.value" :inputId="lvl.value" />
                            <label :for="lvl.value" class="text-sm text-600 cursor-pointer">
                                <span class="font-medium text-900">{{ lvl.label }}</span> — {{ lvl.desc }}
                            </label>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" text @click="showForm = false" />
                <Button :label="editRole ? 'Save' : 'Create'" icon="pi pi-check"
                    style="background:#1976d2;border-color:#1976d2;" @click="saveRole" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const selectedRole = ref(null);
const showForm     = ref(false);
const editRole     = ref(null);
const saving       = ref(false);
const form         = ref({ name:'', description:'', accessLevel:'limited' });

const accessLevels = [
    { value:'full',     label:'Full Access',    desc:'Can view, create, edit and delete'  },
    { value:'write',    label:'Read/Write',     desc:'Can view and create, no delete'     },
    { value:'limited',  label:'Limited',        desc:'Custom per-module permissions'      },
    { value:'readonly', label:'Read Only',      desc:'View access to assigned modules'    },
];

const permTypes = [
    { key:'view',   label:'View'   },
    { key:'create', label:'Create' },
    { key:'edit',   label:'Edit'   },
    { key:'delete', label:'Delete' },
    { key:'approve',label:'Approve'},
];

const modules = [
    { key:'dashboard',   label:'Dashboard',   icon:'pi pi-home'         },
    { key:'projects',    label:'Projects',    icon:'pi pi-briefcase'    },
    { key:'finance',     label:'Finance',     icon:'pi pi-dollar'       },
    { key:'payments',    label:'Payments',    icon:'pi pi-credit-card'  },
    { key:'progress',    label:'Progress',    icon:'pi pi-chart-line'   },
    { key:'procurement', label:'Procurement', icon:'pi pi-shopping-cart'},
    { key:'suppliers',   label:'Suppliers',   icon:'pi pi-truck'        },
    { key:'qa',          label:'QA',          icon:'pi pi-verified'     },
    { key:'safety',      label:'Safety',      icon:'pi pi-shield'       },
    { key:'reports',     label:'Reports',     icon:'pi pi-file'         },
    { key:'admin',       label:'Admin',       icon:'pi pi-cog'          },
];

const roles = ref([
    { id:1, name:'System Admin',    icon:'pi pi-shield',      color:'#fff',    bg:'#0d2347', userCount:2, protected:true,  permissions:{ dashboard:['view','create','edit','delete','approve'], projects:['view','create','edit','delete','approve'], finance:['view','create','edit','delete','approve'], payments:['view','approve'], progress:['view','create','edit','delete'], procurement:['view','create','edit','delete','approve'], suppliers:['view','create','edit','delete'], qa:['view','create','edit','delete'], safety:['view','create','edit','delete'], reports:['view','create','edit','delete'], admin:['view','create','edit','delete','approve'] } },
    { id:2, name:'Project Manager', icon:'pi pi-briefcase',   color:'#1976d2', bg:'#e8f0fe', userCount:5, protected:false, permissions:{ dashboard:['view'], projects:['view','create','edit'], finance:['view'], payments:['view','approve'], progress:['view','create','edit'], procurement:['view','create'], suppliers:['view'], qa:['view','create'], safety:['view','create'], reports:['view','create'], admin:[] } },
    { id:3, name:'Site Engineer',   icon:'pi pi-hammer',      color:'#2ecc71', bg:'#e8fdf0', userCount:8, protected:false, permissions:{ dashboard:['view'], projects:['view'], finance:[], payments:[], progress:['view','create','edit'], procurement:['view'], suppliers:['view'], qa:['view','create','edit'], safety:['view','create','edit'], reports:['view'], admin:[] } },
    { id:4, name:'Finance Officer', icon:'pi pi-dollar',      color:'#e6a817', bg:'#fef9e7', userCount:4, protected:false, permissions:{ dashboard:['view'], projects:['view'], finance:['view','create','edit'], payments:['view','create','edit','approve'], progress:['view'], procurement:['view','create'], suppliers:['view','create','edit'], qa:[], safety:[], reports:['view','create'], admin:[] } },
    { id:5, name:'QA Inspector',    icon:'pi pi-verified',    color:'#a855f7', bg:'#f3e8ff', userCount:3, protected:false, permissions:{ dashboard:['view'], projects:['view'], finance:[], payments:[], progress:['view'], procurement:['view'], suppliers:['view'], qa:['view','create','edit','delete'], safety:['view'], reports:['view','create'], admin:[] } },
    { id:6, name:'Viewer',          icon:'pi pi-eye',         color:'#9ca3af', bg:'#f3f4f6', userCount:2, protected:false, permissions:{ dashboard:['view'], projects:['view'], finance:['view'], payments:[], progress:['view'], procurement:['view'], suppliers:['view'], qa:['view'], safety:['view'], reports:['view'], admin:[] } },
]);

function openForm(role = null) {
    editRole.value = role;
    form.value = role ? { ...role } : { name:'', description:'', accessLevel:'limited' };
    showForm.value = true;
}

function saveRole() {
    if (!form.value.name) return;
    if (editRole.value) {
        const idx = roles.value.findIndex(r => r.id === editRole.value.id);
        roles.value[idx] = { ...roles.value[idx], ...form.value };
    } else {
        roles.value.push({ id: Date.now(), ...form.value, icon:'pi pi-id-card', color:'#1976d2', bg:'#e8f0fe', userCount:0, protected:false, permissions:{} });
    }
    showForm.value = false;
}

function confirmDelete(role) {
    if (confirm(`Delete role "${role.name}"?`)) {
        roles.value = roles.value.filter(r => r.id !== role.id);
        if (selectedRole.value?.id === role.id) selectedRole.value = null;
    }
}

async function savePermissions() {
    saving.value = true;
    await new Promise(r => setTimeout(r, 700));
    saving.value = false;
}
</script>