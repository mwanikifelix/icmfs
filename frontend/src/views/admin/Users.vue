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
                        <h4 class="mt-0 mb-1" style="color:#fff;">Users</h4>
                        <span class="text-sm" style="color:#b3c8e8;">{{ filtered.length }} of {{ users.length }} users</span>
                    </div>
                </div>
                <div class="flex gap-2">
                    <Button label="Manage Users" icon="pi pi-cog" size="small" outlined
                        style="border-color:#fff;color:#fff;"
                        @click="$router.push('/app/admin/user-management')" />
                    <Button label="Add User" icon="pi pi-user-plus" size="small"
                        style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;" />
                </div>
            </div>

            <!-- Stats bar -->
            <div class="grid mb-3">
                <div class="col-6 lg:col-3" v-for="s in stats" :key="s.label">
                    <div class="card mb-0 text-center py-3">
                        <div class="font-bold text-3xl mb-1" :style="{ color: s.color }">{{ s.value }}</div>
                        <div class="text-500 text-sm">{{ s.label }}</div>
                    </div>
                </div>
            </div>

            <!-- Search + filters -->
            <div class="card mb-3">
                <div class="flex flex-wrap gap-3 align-items-center">
                    <div class="p-input-icon-left" style="flex:1;min-width:200px;max-width:320px;">
                        <i class="pi pi-search" />
                        <InputText v-model="search" placeholder="Search name, email or username..." class="w-full" />
                    </div>
                    <div class="flex gap-2 flex-wrap">
                        <div v-for="r in ['All', ...roleNames]" :key="r">
                            <Button :label="r" size="small"
                                :style="filterRole === r
                                    ? 'background:#0d2347;border-color:#0d2347;color:#e6a817;'
                                    : ''"
                                :outlined="filterRole !== r"
                                @click="filterRole = r" />
                        </div>
                    </div>
                    <SelectButton v-model="filterStatus" :options="['All','Active','Inactive','Pending']" />
                </div>
            </div>

            <!-- View toggle -->
            <div class="flex justify-content-end mb-3 gap-2">
                <Button :icon="viewMode==='grid'?'pi pi-th-large':'pi pi-list'"
                    :outlined="viewMode!=='grid'" text
                    @click="viewMode = viewMode==='grid'?'list':'grid'" />
            </div>

            <!-- ── GRID VIEW ── -->
            <div v-if="viewMode==='grid'" class="grid">
                <div class="col-12 sm:col-6 lg:col-4 xl:col-3" v-for="user in filtered" :key="user.id">
                    <div class="card mb-0 h-full text-center">
                        <!-- Avatar -->
                        <div class="flex align-items-center justify-content-center border-circle font-bold mx-auto mb-3"
                            style="width:4rem;height:4rem;font-size:1.2rem;"
                            :style="{ background: avatarColor(user.role), color: '#fff' }">
                            {{ initials(user.name) }}
                        </div>

                        <div class="font-bold text-900 mb-1">{{ user.name }}</div>
                        <div class="text-400 text-xs mb-2">@{{ user.username }}</div>
                        <div class="text-500 text-sm mb-3">{{ user.email }}</div>

                        <div class="flex justify-content-center gap-2 mb-3 flex-wrap">
                            <Tag :value="user.role" style="background:#0d2347;color:#e6a817;font-size:0.65rem;" />
                            <Tag :value="user.status"
                                :severity="user.status==='Active'?'success':user.status==='Pending'?'warn':'danger'" />
                        </div>

                        <div class="text-400 text-xs mb-3">
                            <i class="pi pi-clock mr-1" />Last login: {{ user.lastLogin }}
                        </div>

                        <Divider class="my-2" />

                        <div class="flex justify-content-center gap-1">
                            <Button icon="pi pi-eye"    text rounded size="small" v-tooltip.top="'View'"    />
                            <Button icon="pi pi-pencil" text rounded size="small" v-tooltip.top="'Edit'"    />
                            <Button icon="pi pi-key"    text rounded size="small" severity="warning" v-tooltip.top="'Reset Password'" />
                            <Button icon="pi pi-ban"    text rounded size="small" severity="danger"  v-tooltip.top="'Deactivate'"     />
                        </div>
                    </div>
                </div>
            </div>

            <!-- ── LIST VIEW ── -->
            <div v-else class="card">
                <DataTable :value="filtered" :paginator="true" :rows="10"
                    stripedRows responsiveLayout="scroll"
                    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                    currentPageReportTemplate="{first}–{last} of {totalRecords}">
                    <Column header="User" style="min-width:200px;">
                        <template #body="{ data }">
                            <div class="flex align-items-center gap-3">
                                <div class="flex align-items-center justify-content-center border-circle font-bold text-sm flex-shrink-0"
                                    style="width:2.5rem;height:2.5rem;color:#fff;"
                                    :style="{ background: avatarColor(data.role) }">
                                    {{ initials(data.name) }}
                                </div>
                                <div>
                                    <div class="font-semibold text-900 text-sm">{{ data.name }}</div>
                                    <div class="text-400 text-xs">{{ data.email }}</div>
                                </div>
                            </div>
                        </template>
                    </Column>
                    <Column field="username" header="Username">
                        <template #body="{ data }">
                            <span class="font-mono text-sm text-600">{{ data.username }}</span>
                        </template>
                    </Column>
                    <Column header="Role">
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
                    <Column field="lastLogin" header="Last Login">
                        <template #body="{ data }">
                            <span class="text-500 text-sm">{{ data.lastLogin }}</span>
                        </template>
                    </Column>
                    <Column header="Actions" style="width:120px;">
                        <template #body>
                            <div class="flex gap-1">
                                <Button icon="pi pi-pencil" text rounded size="small" v-tooltip.top="'Edit'" />
                                <Button icon="pi pi-key"    text rounded size="small" severity="warning" v-tooltip.top="'Reset Password'" />
                                <Button icon="pi pi-ban"    text rounded size="small" severity="danger"  v-tooltip.top="'Deactivate'" />
                            </div>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const search       = ref('');
const filterRole   = ref('All');
const filterStatus = ref('All');
const viewMode     = ref('grid');

const roleNames = ['System Admin','Project Manager','Site Engineer','Finance Officer','QA Inspector','Viewer'];

const roleColors = {
    'System Admin':    '#0d2347',
    'Project Manager': '#1976d2',
    'Site Engineer':   '#2ecc71',
    'Finance Officer': '#e6a817',
    'QA Inspector':    '#a855f7',
    'Viewer':          '#9ca3af',
};

const initials    = (name) => name.split(' ').map(n=>n[0]).slice(0,2).join('').toUpperCase();
const avatarColor = (role) => roleColors[role] || '#1976d2';

const users = ref([
    { id:1, name:'Felix Mwaniki',  username:'felix.m',  email:'felix@icmfs.co.ke',   role:'System Admin',    department:'Management',  status:'Active',   lastLogin:'Today 08:32'    },
    { id:2, name:'Peter Kamau',    username:'peter.k',  email:'peter@icmfs.co.ke',   role:'Project Manager', department:'Engineering', status:'Active',   lastLogin:'Today 07:55'    },
    { id:3, name:'Jane Achieng',   username:'jane.a',   email:'jane@icmfs.co.ke',    role:'Site Engineer',   department:'Engineering', status:'Active',   lastLogin:'Yesterday 17:10'},
    { id:4, name:'David Oduya',    username:'david.o',  email:'david@icmfs.co.ke',   role:'Finance Officer', department:'Finance',     status:'Inactive', lastLogin:'5 days ago'     },
    { id:5, name:'Mary Wanjiku',   username:'mary.w',   email:'mary@icmfs.co.ke',    role:'QA Inspector',    department:'QA',          status:'Active',   lastLogin:'Today 09:11'    },
    { id:6, name:'Samuel Mwangi',  username:'samuel.m', email:'samuel@icmfs.co.ke',  role:'Site Engineer',   department:'Engineering', status:'Active',   lastLogin:'Yesterday'      },
    { id:7, name:'Grace Njoroge',  username:'grace.n',  email:'grace@icmfs.co.ke',   role:'Finance Officer', department:'Finance',     status:'Pending',  lastLogin:'Never'          },
    { id:8, name:'Hassan Ali',     username:'hassan.a', email:'hassan@icmfs.co.ke',  role:'QA Inspector',    department:'QA',          status:'Active',   lastLogin:'2 days ago'     },
    { id:9, name:'Dr. Kariuki',    username:'kariuki',  email:'kariuki@tum.ac.ke',   role:'Viewer',          department:'Management',  status:'Active',   lastLogin:'1 week ago'     },
]);

const stats = computed(() => [
    { label:'Total',    value: users.value.length,                                              color:'#1976d2' },
    { label:'Active',   value: users.value.filter(u=>u.status==='Active').length,               color:'#2ecc71' },
    { label:'Inactive', value: users.value.filter(u=>u.status==='Inactive').length,             color:'#ef4444' },
    { label:'Pending',  value: users.value.filter(u=>u.status==='Pending').length,              color:'#e6a817' },
]);

const filtered = computed(() => users.value.filter(u => {
    const q = search.value.toLowerCase();
    return (
        (!q || u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q) || u.username.toLowerCase().includes(q)) &&
        (filterRole.value   === 'All' || u.role   === filterRole.value) &&
        (filterStatus.value === 'All' || u.status === filterStatus.value)
    );
}));
</script>