<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg flex-shrink-0"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-shield text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">Admin Dashboard</h4>
                        <span class="text-sm" style="color:#b3c8e8;">System overview · {{ today }}</span>
                    </div>
                </div>
                <div class="flex gap-2">
                    <Button label="System Health" icon="pi pi-heart" size="small"
                        style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                        @click="$router.push('/app/admin/settings')" />
                    <Button label="Audit Logs" icon="pi pi-list" size="small" outlined
                        style="border-color:#fff;color:#fff;"
                        @click="$router.push('/app/admin/audit')" />
                </div>
            </div>

            <!-- KPI Cards -->
            <div class="grid mb-3">
                <div class="col-12 sm:col-6 lg:col-3" v-for="kpi in kpis" :key="kpi.label">
                    <div class="card mb-0 h-full">
                        <div class="flex justify-content-between align-items-start">
                            <div>
                                <span class="text-500 font-medium text-sm block mb-2">{{ kpi.label }}</span>
                                <span class="font-bold text-3xl text-900">{{ kpi.value }}</span>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round flex-shrink-0"
                                style="width:3rem;height:3rem;"
                                :style="{ background: kpi.bg }">
                                <i :class="kpi.icon" class="text-xl" :style="{ color: kpi.color }" />
                            </div>
                        </div>
                        <div class="mt-3 text-sm">
                            <span :style="{ color: kpi.trendColor }" class="font-medium">{{ kpi.trend }}</span>
                            <span class="text-500"> {{ kpi.trendLabel }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid">
                <!-- Recent Users -->
                <div class="col-12 lg:col-6">
                    <div class="card h-full">
                        <div class="flex justify-content-between align-items-center mb-4">
                            <h5 class="mt-0 mb-0" style="color:#0d2347;">
                                <i class="pi pi-users mr-2" style="color:#1976d2;" />Recent Users
                            </h5>
                            <Button label="View All" icon="pi pi-arrow-right" iconPos="right"
                                text size="small" @click="$router.push('/app/admin/users')" />
                        </div>
                        <DataTable :value="recentUsers" size="small" stripedRows>
                            <Column header="User">
                                <template #body="{ data }">
                                    <div class="flex align-items-center gap-2">
                                        <div class="flex align-items-center justify-content-center border-circle font-bold text-xs flex-shrink-0"
                                            style="width:2rem;height:2rem;background:#1976d2;color:#fff;">
                                            {{ initials(data.name) }}
                                        </div>
                                        <div>
                                            <div class="font-medium text-sm text-900">{{ data.name }}</div>
                                            <div class="text-400 text-xs">{{ data.email }}</div>
                                        </div>
                                    </div>
                                </template>
                            </Column>
                            <Column header="Role">
                                <template #body="{ data }">
                                    <Tag :value="data.role" style="background:#0d2347;color:#e6a817;font-size:0.7rem;" />
                                </template>
                            </Column>
                            <Column header="Status">
                                <template #body="{ data }">
                                    <Tag :value="data.status"
                                        :severity="data.status === 'Active' ? 'success' : 'warning'" />
                                </template>
                            </Column>
                            <Column header="Joined">
                                <template #body="{ data }">
                                    <span class="text-500 text-xs">{{ data.joined }}</span>
                                </template>
                            </Column>
                        </DataTable>
                    </div>
                </div>

                <!-- Recent Audit Events -->
                <div class="col-12 lg:col-6">
                    <div class="card h-full">
                        <div class="flex justify-content-between align-items-center mb-4">
                            <h5 class="mt-0 mb-0" style="color:#0d2347;">
                                <i class="pi pi-history mr-2" style="color:#e6a817;" />Recent Audit Events
                            </h5>
                            <Button label="View All" icon="pi pi-arrow-right" iconPos="right"
                                text size="small" @click="$router.push('/app/admin/audit')" />
                        </div>
                        <div class="flex flex-column gap-3">
                            <div v-for="event in auditEvents" :key="event.id"
                                class="flex align-items-start gap-3 p-3 border-round-lg"
                                style="background:var(--surface-50);">
                                <div class="flex align-items-center justify-content-center border-round flex-shrink-0 mt-1"
                                    style="width:2rem;height:2rem;" :style="{ background: event.bg }">
                                    <i :class="event.icon" style="font-size:0.75rem;" :style="{ color: event.color }" />
                                </div>
                                <div class="flex-1">
                                    <div class="text-900 text-sm font-medium">{{ event.action }}</div>
                                    <div class="text-500 text-xs">{{ event.user }} · {{ event.time }}</div>
                                </div>
                                <Tag :value="event.module" severity="secondary" style="font-size:0.65rem;" />
                            </div>
                        </div>
                    </div>
                </div>

                <!-- System Health -->
                <div class="col-12 lg:col-6">
                    <div class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-server mr-2" style="color:#2ecc71;" />System Health
                        </h5>
                        <div class="flex flex-column gap-3">
                            <div v-for="s in systemHealth" :key="s.label">
                                <div class="flex justify-content-between align-items-center mb-2">
                                    <span class="text-600 text-sm font-medium">{{ s.label }}</span>
                                    <span class="font-bold text-sm" :style="{ color: s.color }">{{ s.value }}</span>
                                </div>
                                <ProgressBar :value="s.pct" :showValue="false" style="height:8px;"
                                    :pt="{ value: { style: { background: s.color } } }" />
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Role Distribution -->
                <div class="col-12 lg:col-6">
                    <div class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-chart-pie mr-2" style="color:#1976d2;" />Users by Role
                        </h5>
                        <div class="flex flex-column gap-3">
                            <div v-for="r in roleDistribution" :key="r.role">
                                <div class="flex justify-content-between align-items-center mb-1">
                                    <span class="text-600 text-sm">{{ r.role }}</span>
                                    <span class="font-bold text-sm text-900">{{ r.count }}</span>
                                </div>
                                <ProgressBar :value="r.pct" :showValue="false" style="height:6px;"
                                    :pt="{ value: { style: { background: r.color } } }" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
const today = new Date().toLocaleDateString('en-KE', { weekday:'long', year:'numeric', month:'long', day:'numeric' });

const initials = (name) => name.split(' ').map(n=>n[0]).slice(0,2).join('').toUpperCase();

const kpis = [
    { label:'Total Users',      value:'24',   icon:'pi pi-users',      color:'#1976d2', bg:'#e8f0fe', trend:'+3',      trendColor:'#2ecc71', trendLabel:'this month'   },
    { label:'Active Sessions',  value:'8',    icon:'pi pi-desktop',    color:'#2ecc71', bg:'#e8fdf0', trend:'4 online', trendColor:'#2ecc71', trendLabel:'right now'    },
    { label:'Roles Defined',    value:'6',    icon:'pi pi-id-card',    color:'#e6a817', bg:'#fef9e7', trend:'2',        trendColor:'#e6a817', trendLabel:'with open access' },
    { label:'Audit Events Today',value:'37',  icon:'pi pi-list',       color:'#0d2347', bg:'#e8ecf4', trend:'12',       trendColor:'#ef4444', trendLabel:'warnings'     },
];

const recentUsers = ref([
    { name:'Felix Mwaniki',    email:'felix@icmfs.co.ke',   role:'Admin',          status:'Active',   joined:'Today'     },
    { name:'Peter Kamau',      email:'peter@icmfs.co.ke',   role:'Project Manager',status:'Active',   joined:'2 days ago'},
    { name:'Jane Achieng',     email:'jane@icmfs.co.ke',    role:'Site Engineer',  status:'Active',   joined:'5 days ago'},
    { name:'David Oduya',      email:'david@icmfs.co.ke',   role:'Finance Officer',status:'Inactive', joined:'1 week ago'},
    { name:'Mary Wanjiku',     email:'mary@icmfs.co.ke',    role:'QA Inspector',   status:'Active',   joined:'2 weeks ago'},
]);

const auditEvents = ref([
    { id:1, action:'User login',             user:'Felix Mwaniki',  time:'2 min ago',  module:'Auth',     icon:'pi pi-sign-in',   color:'#2ecc71', bg:'#e8fdf0' },
    { id:2, action:'Role updated — PM',      user:'Admin',          time:'1 hr ago',   module:'Roles',    icon:'pi pi-id-card',   color:'#1976d2', bg:'#e8f0fe' },
    { id:3, action:'New user registered',    user:'System',         time:'3 hrs ago',  module:'Users',    icon:'pi pi-user-plus', color:'#e6a817', bg:'#fef9e7' },
    { id:4, action:'Settings changed',       user:'Felix Mwaniki',  time:'Yesterday',  module:'Settings', icon:'pi pi-cog',       color:'#6b7280', bg:'#f3f4f6' },
    { id:5, action:'Failed login attempt',   user:'Unknown',        time:'Yesterday',  module:'Auth',     icon:'pi pi-ban',       color:'#ef4444', bg:'#fde8e8' },
]);

const systemHealth = ref([
    { label:'Database',        value:'Healthy', pct:98, color:'#2ecc71' },
    { label:'API Response',    value:'42ms',    pct:92, color:'#1976d2' },
    { label:'Storage Used',    value:'34%',     pct:34, color:'#e6a817' },
    { label:'CPU Usage',       value:'18%',     pct:18, color:'#2ecc71' },
    { label:'Memory Usage',    value:'61%',     pct:61, color:'#e6a817' },
]);

const roleDistribution = ref([
    { role:'System Admin',     count:2,  pct:8,  color:'#0d2347' },
    { role:'Project Manager',  count:5,  pct:21, color:'#1976d2' },
    { role:'Site Engineer',    count:8,  pct:33, color:'#2ecc71' },
    { role:'Finance Officer',  count:4,  pct:17, color:'#e6a817' },
    { role:'QA Inspector',     count:3,  pct:13, color:'#a855f7' },
    { role:'Viewer',           count:2,  pct:8,  color:'#9ca3af' },
]);
</script>