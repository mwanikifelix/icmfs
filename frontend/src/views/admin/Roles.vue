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
                        <h4 class="mt-0 mb-1" style="color:#fff;">Roles Overview</h4>
                        <span class="text-sm" style="color:#b3c8e8;">All system roles and their assigned users</span>
                    </div>
                </div>
                <Button label="Manage Permissions" icon="pi pi-cog" size="small"
                    style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                    @click="$router.push('/app/admin/role-management')" />
            </div>

            <!-- Role cards grid -->
            <div class="grid mb-4">
                <div class="col-12 md:col-6 lg:col-4" v-for="role in roles" :key="role.id">
                    <div class="card mb-0 h-full" style="cursor:default;">
                        <!-- Card header -->
                        <div class="flex align-items-center justify-content-between mb-3">
                            <div class="flex align-items-center gap-3">
                                <div class="flex align-items-center justify-content-center border-round"
                                    style="width:2.5rem;height:2.5rem;" :style="{ background: role.bg }">
                                    <i :class="role.icon" :style="{ color: role.color }" />
                                </div>
                                <div>
                                    <div class="font-bold text-900">{{ role.name }}</div>
                                    <div class="text-400 text-xs">{{ role.userCount }} users</div>
                                </div>
                            </div>
                            <Tag v-if="role.protected" value="System" severity="secondary" style="font-size:0.65rem;" />
                        </div>

                        <p class="text-500 text-sm mt-0 mb-3">{{ role.description }}</p>

                        <!-- Access level badge -->
                        <div class="flex align-items-center gap-2 mb-3">
                            <span class="text-xs text-400">Access:</span>
                            <Tag :value="role.accessLevel"
                                :style="accessStyle(role.accessLevel)" style="font-size:0.7rem;" />
                        </div>

                        <!-- Module access dots -->
                        <div class="mb-3">
                            <div class="text-xs text-400 mb-2">Module access</div>
                            <div class="flex flex-wrap gap-1">
                                <span v-for="m in role.modules" :key="m"
                                    class="text-xs px-2 py-1 border-round"
                                    style="background:var(--surface-100);color:var(--text-color-secondary);">
                                    {{ m }}
                                </span>
                                <span v-if="role.allModules" class="text-xs px-2 py-1 border-round"
                                    style="background:#e8f0fe;color:#1976d2;">+ All</span>
                            </div>
                        </div>

                        <Divider class="my-2" />

                        <!-- Assigned users avatars -->
                        <div class="flex align-items-center justify-content-between">
                            <div class="flex align-items-center">
                                <div v-for="(user, idx) in role.users.slice(0,4)" :key="user"
                                    class="flex align-items-center justify-content-center border-circle text-xs font-bold border-2"
                                    style="width:2rem;height:2rem;background:#1976d2;color:#fff;border-color:var(--surface-card);"
                                    :style="{ marginLeft: idx > 0 ? '-0.5rem' : '0' }"
                                    v-tooltip.top="user">
                                    {{ user.split(' ').map(n=>n[0]).join('') }}
                                </div>
                                <span v-if="role.users.length > 4"
                                    class="text-400 text-xs ml-2">+{{ role.users.length - 4 }} more</span>
                            </div>
                            <Button label="Assign" icon="pi pi-user-plus" text size="small"
                                style="color:#1976d2;" @click="openAssign(role)" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Users per role table -->
            <div class="card">
                <h5 class="mt-0 mb-4" style="color:#0d2347;">
                    <i class="pi pi-table mr-2" style="color:#1976d2;" />User–Role Assignment Table
                </h5>
                <DataTable :value="userRoleRows" stripedRows size="small"
                    :paginator="true" :rows="10">
                    <Column header="User" sortable sortField="name">
                        <template #body="{ data }">
                            <div class="flex align-items-center gap-2">
                                <div class="flex align-items-center justify-content-center border-circle text-xs font-bold"
                                    style="width:2rem;height:2rem;background:#1976d2;color:#fff;">
                                    {{ data.name.split(' ').map(n=>n[0]).join('') }}
                                </div>
                                <div>
                                    <div class="text-sm font-medium text-900">{{ data.name }}</div>
                                    <div class="text-400 text-xs">{{ data.email }}</div>
                                </div>
                            </div>
                        </template>
                    </Column>
                    <Column header="Current Role">
                        <template #body="{ data }">
                            <Tag :value="data.role" style="background:#0d2347;color:#e6a817;font-size:0.7rem;" />
                        </template>
                    </Column>
                    <Column field="department" header="Department" />
                    <Column header="Change Role" style="min-width:200px;">
                        <template #body="{ data }">
                            <Dropdown v-model="data.newRole" :options="roleNames"
                                class="w-full" size="small" :placeholder="data.role"
                                @change="onRoleChange(data)" />
                        </template>
                    </Column>
                    <Column header="Status">
                        <template #body="{ data }">
                            <Tag :value="data.status"
                                :severity="data.status==='Active'?'success':data.status==='Pending'?'warn':'danger'" />
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>

        <!-- Assign user dialog -->
        <Dialog v-model:visible="showAssign" :header="`Assign Users — ${assignRole?.name}`"
            :modal="true" :style="{ width: '480px' }">
            <div class="pt-2">
                <div class="p-input-icon-left mb-3">
                    <i class="pi pi-search" />
                    <InputText v-model="assignSearch" placeholder="Search users..." class="w-full" />
                </div>
                <div class="flex flex-column gap-2" style="max-height:300px;overflow-y:auto;">
                    <div v-for="user in filteredAssignUsers" :key="user.id"
                        class="flex align-items-center justify-content-between p-2 border-round hover:surface-100 cursor-pointer">
                        <div class="flex align-items-center gap-2">
                            <Checkbox v-model="assignSelected" :value="user.name" binary />
                            <div class="flex align-items-center justify-content-center border-circle text-xs font-bold"
                                style="width:1.8rem;height:1.8rem;background:#1976d2;color:#fff;">
                                {{ user.name.split(' ').map(n=>n[0]).join('') }}
                            </div>
                            <div>
                                <div class="text-sm font-medium">{{ user.name }}</div>
                                <div class="text-400 text-xs">{{ user.email }}</div>
                            </div>
                        </div>
                        <Tag :value="user.role" severity="secondary" style="font-size:0.65rem;" />
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" text @click="showAssign = false" />
                <Button label="Assign Role" icon="pi pi-check"
                    style="background:#1976d2;border-color:#1976d2;"
                    @click="showAssign = false" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const showAssign    = ref(false);
const assignRole    = ref(null);
const assignSearch  = ref('');
const assignSelected = ref([]);

const roleNames = ['System Admin','Project Manager','Site Engineer','Finance Officer','QA Inspector','Viewer'];

const accessStyle = (level) => {
    const map = {
        'Full Access': 'background:#fde8e8;color:#ef4444;',
        'Read/Write':  'background:#e8f0fe;color:#1976d2;',
        'Limited':     'background:#fef9e7;color:#e6a817;',
        'Read Only':   'background:#f3f4f6;color:#6b7280;',
    };
    return map[level] || '';
};

const roles = ref([
    {
        id:1, name:'System Admin', icon:'pi pi-shield', color:'#fff', bg:'#0d2347', protected:true,
        description:'Full system access. Can manage users, roles, settings and all modules.',
        accessLevel:'Full Access', allModules:true, modules:[], userCount:2,
        users:['Felix Mwaniki','Admin User'],
    },
    {
        id:2, name:'Project Manager', icon:'pi pi-briefcase', color:'#1976d2', bg:'#e8f0fe', protected:false,
        description:'Manages projects, approves payments and monitors progress across all sites.',
        accessLevel:'Read/Write', allModules:false, modules:['Projects','Finance','Progress','Payments','QA'], userCount:5,
        users:['Peter Kamau','Alice Mutua','James Opiyo','Sarah Ndungu','Tom Kariuki'],
    },
    {
        id:3, name:'Site Engineer', icon:'pi pi-hammer', color:'#2ecc71', bg:'#e8fdf0', protected:false,
        description:'Field engineer responsible for daily progress reports, safety and QA inspections.',
        accessLevel:'Limited', allModules:false, modules:['Projects','Progress','QA','Safety'], userCount:8,
        users:['Jane Achieng','Samuel Mwangi','Brian Otieno','Lucy Kamau'],
    },
    {
        id:4, name:'Finance Officer', icon:'pi pi-dollar', color:'#e6a817', bg:'#fef9e7', protected:false,
        description:'Manages budgets, expenses, invoices and financial reporting.',
        accessLevel:'Limited', allModules:false, modules:['Finance','Payments','Procurement','Suppliers'], userCount:4,
        users:['David Oduya','Grace Njoroge','Mark Mugo'],
    },
    {
        id:5, name:'QA Inspector', icon:'pi pi-verified', color:'#a855f7', bg:'#f3e8ff', protected:false,
        description:'Conducts quality audits, raises NCRs and certifies work at various stages.',
        accessLevel:'Limited', allModules:false, modules:['QA','Safety','Projects'], userCount:3,
        users:['Mary Wanjiku','Hassan Ali'],
    },
    {
        id:6, name:'Viewer', icon:'pi pi-eye', color:'#9ca3af', bg:'#f3f4f6', protected:false,
        description:'Read-only access to dashboard and project reports. No edit rights.',
        accessLevel:'Read Only', allModules:false, modules:['Dashboard','Projects','Reports'], userCount:2,
        users:['Dr. Kariuki','Auditor'],
    },
]);

const userRoleRows = ref([
    { id:1, name:'Felix Mwaniki',  email:'felix@icmfs.co.ke',   role:'System Admin',    department:'Management',  status:'Active',   newRole:null },
    { id:2, name:'Peter Kamau',    email:'peter@icmfs.co.ke',   role:'Project Manager', department:'Engineering', status:'Active',   newRole:null },
    { id:3, name:'Jane Achieng',   email:'jane@icmfs.co.ke',    role:'Site Engineer',   department:'Engineering', status:'Active',   newRole:null },
    { id:4, name:'David Oduya',    email:'david@icmfs.co.ke',   role:'Finance Officer', department:'Finance',     status:'Inactive', newRole:null },
    { id:5, name:'Mary Wanjiku',   email:'mary@icmfs.co.ke',    role:'QA Inspector',    department:'QA',          status:'Active',   newRole:null },
    { id:6, name:'Samuel Mwangi',  email:'samuel@icmfs.co.ke',  role:'Site Engineer',   department:'Engineering', status:'Active',   newRole:null },
    { id:7, name:'Grace Njoroge',  email:'grace@icmfs.co.ke',   role:'Finance Officer', department:'Finance',     status:'Pending',  newRole:null },
]);

const allUsers = userRoleRows.value;

const filteredAssignUsers = computed(() =>
    allUsers.filter(u =>
        !assignSearch.value ||
        u.name.toLowerCase().includes(assignSearch.value.toLowerCase())
    )
);

function openAssign(role) {
    assignRole.value    = role;
    assignSelected.value = [...role.users];
    assignSearch.value  = '';
    showAssign.value    = true;
}

function onRoleChange(row) {
    if (row.newRole) row.role = row.newRole;
}
</script>