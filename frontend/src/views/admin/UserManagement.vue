<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-users text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">User Management</h4>
                        <span class="text-sm" style="color:#b3c8e8;">{{ users.length }} registered users</span>
                    </div>
                </div>
                <Button label="Add User" icon="pi pi-user-plus"
                    style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                    @click="openForm()" />
            </div>

            <!-- Stats -->
            <div class="grid mb-3">
                <div class="col-6 lg:col-3" v-for="s in stats" :key="s.label">
                    <div class="card mb-0 text-center">
                        <div class="font-bold text-3xl mb-1" :style="{ color: s.color }">{{ s.value }}</div>
                        <div class="text-500 text-sm">{{ s.label }}</div>
                    </div>
                </div>
            </div>

            <!-- Table card -->
            <div class="card">
                <!-- Toolbar -->
                <div class="flex flex-wrap gap-3 mb-4 align-items-center justify-content-between">
                    <div class="p-input-icon-left" style="flex:1;min-width:200px;max-width:320px;">
                        <i class="pi pi-search" />
                        <InputText v-model="search" placeholder="Search users..." class="w-full" />
                    </div>
                    <div class="flex gap-2 flex-wrap">
                        <Dropdown v-model="filterRole" :options="roleOptions" placeholder="All Roles"
                            showClear style="min-width:160px;" />
                        <Dropdown v-model="filterStatus" :options="['Active','Inactive','Pending']"
                            placeholder="All Status" showClear style="min-width:140px;" />
                        <Button icon="pi pi-download" label="Export" outlined severity="secondary" />
                    </div>
                </div>

                <DataTable :value="filteredUsers" :paginator="true" :rows="10"
                    stripedRows responsiveLayout="scroll"
                    v-model:selection="selectedUsers"
                    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                    currentPageReportTemplate="{first}–{last} of {totalRecords}">
                    <Column selectionMode="multiple" style="width:3rem" />
                    <Column header="User" sortable sortField="name" style="min-width:200px;">
                        <template #body="{ data }">
                            <div class="flex align-items-center gap-3">
                                <div class="flex align-items-center justify-content-center border-circle font-bold text-sm flex-shrink-0"
                                    style="width:2.4rem;height:2.4rem;background:#1976d2;color:#fff;">
                                    {{ initials(data.name) }}
                                </div>
                                <div>
                                    <div class="font-semibold text-900 text-sm">{{ data.name }}</div>
                                    <div class="text-400 text-xs">{{ data.email }}</div>
                                </div>
                            </div>
                        </template>
                    </Column>
                    <Column field="username" header="Username" sortable>
                        <template #body="{ data }">
                            <span class="font-mono text-sm text-600">{{ data.username }}</span>
                        </template>
                    </Column>
                    <Column header="Role" sortable sortField="role">
                        <template #body="{ data }">
                            <Tag :value="data.role" style="background:#0d2347;color:#e6a817;font-size:0.7rem;" />
                        </template>
                    </Column>
                    <Column field="department" header="Department" />
                    <Column header="Status">
                        <template #body="{ data }">
                            <Tag :value="data.status"
                                :severity="data.status==='Active'?'success':data.status==='Pending'?'warn':'danger'" />
                        </template>
                    </Column>
                    <Column field="lastLogin" header="Last Login" sortable>
                        <template #body="{ data }">
                            <span class="text-500 text-sm">{{ data.lastLogin }}</span>
                        </template>
                    </Column>
                    <Column header="Actions" style="width:110px;">
                        <template #body="{ data }">
                            <div class="flex gap-1">
                                <Button icon="pi pi-pencil" text rounded size="small"
                                    v-tooltip.top="'Edit'" @click="openForm(data)" />
                                <Button icon="pi pi-key" text rounded size="small"
                                    severity="warning" v-tooltip.top="'Reset Password'"
                                    @click="resetPassword(data)" />
                                <Button icon="pi pi-trash" text rounded size="small"
                                    severity="danger" v-tooltip.top="'Delete'"
                                    @click="confirmDelete(data)" />
                            </div>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>

        <!-- Add/Edit Dialog -->
        <Dialog v-model:visible="showForm" :header="editUser ? 'Edit User' : 'Add New User'"
            :modal="true" :style="{ width: '560px' }" :closable="true">
            <div class="grid pt-2">
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">First Name *</label>
                    <InputText v-model="form.first_name" class="w-full" placeholder="First name" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Last Name *</label>
                    <InputText v-model="form.last_name" class="w-full" placeholder="Last name" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Username *</label>
                    <InputText v-model="form.username" class="w-full" placeholder="username" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Email *</label>
                    <InputText v-model="form.email" class="w-full" placeholder="email@icmfs.co.ke" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Role *</label>
                    <Dropdown v-model="form.role" :options="roleOptions" class="w-full" placeholder="Select role" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Department</label>
                    <Dropdown v-model="form.department" :options="deptOptions" class="w-full" placeholder="Department" />
                </div>
                <div class="col-12 md:col-6 field" v-if="!editUser">
                    <label class="block font-medium mb-2 text-600">Password *</label>
                    <Password v-model="form.password" class="w-full" fluid toggleMask :feedback="false" />
                </div>
                <div class="col-12 md:col-6 field">
                    <label class="block font-medium mb-2 text-600">Phone</label>
                    <InputText v-model="form.phone" class="w-full" placeholder="+254 7XX XXX XXX" />
                </div>
                <div class="col-12 field">
                    <label class="block font-medium mb-2 text-600">Status</label>
                    <div class="flex gap-4">
                        <div v-for="s in ['Active','Inactive','Pending']" :key="s" class="flex align-items-center gap-2">
                            <RadioButton v-model="form.status" :value="s" :inputId="s" />
                            <label :for="s" class="text-600 text-sm cursor-pointer">{{ s }}</label>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" text @click="showForm = false" />
                <Button :label="editUser ? 'Save Changes' : 'Create User'" icon="pi pi-check"
                    :loading="saving"
                    style="background:#1976d2;border-color:#1976d2;"
                    @click="saveUser" />
            </template>
        </Dialog>

        <!-- Delete confirm -->
        <Dialog v-model:visible="showDeleteConfirm" header="Delete User"
            :modal="true" :style="{ width: '380px' }">
            <p class="text-600">Delete <strong>{{ deleteTarget?.name }}</strong>? This cannot be undone.</p>
            <template #footer>
                <Button label="Cancel" text @click="showDeleteConfirm = false" />
                <Button label="Delete" severity="danger" icon="pi pi-trash" @click="deleteUser" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const search        = ref('');
const filterRole    = ref(null);
const filterStatus  = ref(null);
const showForm      = ref(false);
const showDeleteConfirm = ref(false);
const editUser      = ref(null);
const deleteTarget  = ref(null);
const saving        = ref(false);
const selectedUsers = ref([]);

const roleOptions = ['System Admin','Project Manager','Site Engineer','Finance Officer','QA Inspector','Viewer'];
const deptOptions = ['Management','Engineering','Finance','QA','Procurement','Safety'];

const initials = (name) => name.split(' ').map(n=>n[0]).slice(0,2).join('').toUpperCase();

const emptyForm = () => ({ first_name:'', last_name:'', username:'', email:'', role:'', department:'', phone:'', password:'', status:'Active' });
const form = ref(emptyForm());

const users = ref([
    { id:1, name:'Felix Mwaniki',   username:'felix.m',   email:'felix@icmfs.co.ke',   role:'System Admin',     department:'Management',  status:'Active',   lastLogin:'Today 08:32'      },
    { id:2, name:'Peter Kamau',     username:'peter.k',   email:'peter@icmfs.co.ke',   role:'Project Manager',  department:'Engineering', status:'Active',   lastLogin:'Today 07:55'      },
    { id:3, name:'Jane Achieng',    username:'jane.a',    email:'jane@icmfs.co.ke',    role:'Site Engineer',    department:'Engineering', status:'Active',   lastLogin:'Yesterday 17:10'  },
    { id:4, name:'David Oduya',     username:'david.o',   email:'david@icmfs.co.ke',   role:'Finance Officer',  department:'Finance',     status:'Inactive', lastLogin:'5 days ago'       },
    { id:5, name:'Mary Wanjiku',    username:'mary.w',    email:'mary@icmfs.co.ke',    role:'QA Inspector',     department:'QA',          status:'Active',   lastLogin:'Today 09:11'      },
    { id:6, name:'Samuel Mwangi',   username:'samuel.m',  email:'samuel@icmfs.co.ke',  role:'Site Engineer',    department:'Engineering', status:'Active',   lastLogin:'Yesterday'        },
    { id:7, name:'Grace Njoroge',   username:'grace.n',   email:'grace@icmfs.co.ke',   role:'Finance Officer',  department:'Finance',     status:'Pending',  lastLogin:'Never'            },
]);

const stats = computed(() => [
    { label:'Total Users',    value: users.value.length,                                            color:'#1976d2' },
    { label:'Active',         value: users.value.filter(u=>u.status==='Active').length,              color:'#2ecc71' },
    { label:'Inactive',       value: users.value.filter(u=>u.status==='Inactive').length,            color:'#ef4444' },
    { label:'Pending',        value: users.value.filter(u=>u.status==='Pending').length,             color:'#e6a817' },
]);

const filteredUsers = computed(() => users.value.filter(u => {
    const q = search.value.toLowerCase();
    return (
        (!q || u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q) || u.username.toLowerCase().includes(q)) &&
        (!filterRole.value   || u.role   === filterRole.value) &&
        (!filterStatus.value || u.status === filterStatus.value)
    );
}));

function openForm(user = null) {
    editUser.value = user;
    form.value = user ? { ...user } : emptyForm();
    showForm.value = true;
}

async function saveUser() {
    saving.value = true;
    await new Promise(r => setTimeout(r, 700));
    if (editUser.value) {
        const idx = users.value.findIndex(u => u.id === editUser.value.id);
        users.value[idx] = { ...users.value[idx], ...form.value, name: `${form.value.first_name} ${form.value.last_name}`.trim() || form.value.name };
    } else {
        users.value.unshift({ id: Date.now(), ...form.value, name: `${form.value.first_name} ${form.value.last_name}`.trim(), lastLogin: 'Never' });
    }
    saving.value = false;
    showForm.value = false;
}

function confirmDelete(user) { deleteTarget.value = user; showDeleteConfirm.value = true; }
function deleteUser() { users.value = users.value.filter(u => u.id !== deleteTarget.value.id); showDeleteConfirm.value = false; }
function resetPassword(user) { alert(`Password reset email sent to ${user.email}`); }
</script>