<template>
    <div class="grid">
        <div class="col-12">

            <!-- ── HEADER ── -->
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

            <!-- ── USERS SUMMARY CARD ── -->
            <div class="card mb-4" style="border-left:4px solid #1976d2;">
                <div class="flex align-items-center justify-content-between flex-wrap gap-3">
                    <div class="flex align-items-center gap-3">
                        <div class="flex align-items-center justify-content-center border-round-lg flex-shrink-0"
                            style="width:3rem;height:3rem;background:#e8f0fe;">
                            <i class="pi pi-users text-xl" style="color:#1976d2;" />
                        </div>
                        <div>
                            <div class="font-bold text-900 text-xl">Users</div>
                            <div class="text-500 text-sm" v-if="!statsLoading">
                                <span class="font-semibold" style="color:#1976d2;">{{ userStats.active ?? 0 }}</span>
                                active ·
                                <span class="font-semibold text-900">{{ userStats.total ?? 0 }}</span>
                                total
                            </div>
                            <div v-else class="text-500 text-sm">Loading...</div>
                        </div>
                    </div>
                    <div class="flex gap-2">
                        <Button label="Manage Users" icon="pi pi-cog" size="small"
                            outlined style="border-color:#1976d2;color:#1976d2;"
                            @click="$router.push('/app/admin/user-management')" />
                        <Button label="Add User" icon="pi pi-user-plus" size="small"
                            style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                            @click="openAddUser" />
                    </div>
                </div>

                <!-- Role breakdown chips -->
                <div class="flex flex-wrap gap-2 mt-3" v-if="!statsLoading && userStats.by_role">
                    <div v-for="r in roleOptions" :key="r.value"
                        class="flex align-items-center gap-1 px-2 py-1 border-round text-xs"
                        style="background:var(--surface-100);">
                        <span class="font-bold" :style="{ color: r.color }">
                            {{ userStats.by_role[r.value] ?? 0 }}
                        </span>
                        <span class="text-500">{{ r.label }}</span>
                    </div>
                </div>
            </div>

            <!-- ── KPI CARDS ── -->
            <div class="grid mb-3">
                <div class="col-12 sm:col-6 lg:col-3" v-for="kpi in kpis" :key="kpi.label">
                    <div class="card mb-0 h-full">
                        <div class="flex justify-content-between align-items-start">
                            <div>
                                <span class="text-500 font-medium text-sm block mb-2">{{ kpi.label }}</span>
                                <span class="font-bold text-3xl text-900">{{ kpi.value }}</span>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round flex-shrink-0"
                                style="width:3rem;height:3rem;" :style="{ background: kpi.bg }">
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
                <!-- ── Recent Users ── -->
                <div class="col-12 lg:col-6">
                    <div class="card h-full">
                        <div class="flex justify-content-between align-items-center mb-4">
                            <h5 class="mt-0 mb-0" style="color:#0d2347;">
                                <i class="pi pi-users mr-2" style="color:#1976d2;" />Recent Users
                            </h5>
                            <div class="flex gap-2">
                                <Button label="Add" icon="pi pi-plus" text size="small"
                                    style="color:#1976d2;" @click="openAddUser" />
                                <Button label="View All" icon="pi pi-arrow-right" iconPos="right"
                                    text size="small" @click="$router.push('/app/admin/user-management')" />
                            </div>
                        </div>

                        <div v-if="usersLoading" class="flex justify-content-center py-4">
                            <ProgressSpinner style="width:2rem;height:2rem;" />
                        </div>
                        <DataTable v-else :value="recentUsers" size="small" stripedRows>
                            <Column header="User" style="min-width:160px;">
                                <template #body="{ data }">
                                    <div class="flex align-items-center gap-2">
                                        <div class="flex align-items-center justify-content-center border-circle font-bold text-xs flex-shrink-0"
                                            style="width:2rem;height:2rem;color:#fff;"
                                            :style="{ background: roleColor(data.role) }">
                                            {{ initials(data) }}
                                        </div>
                                        <div>
                                            <div class="font-medium text-sm text-900">{{ fullName(data) }}</div>
                                            <div class="text-400 text-xs">{{ data.email }}</div>
                                        </div>
                                    </div>
                                </template>
                            </Column>
                            <Column header="Role">
                                <template #body="{ data }">
                                    <Tag :value="roleLabel(data.role)"
                                        style="background:#0d2347;color:#e6a817;font-size:0.7rem;" />
                                </template>
                            </Column>
                            <Column header="Status">
                                <template #body="{ data }">
                                    <Tag :value="data.is_active ? 'Active' : 'Inactive'"
                                        :severity="data.is_active ? 'success' : 'danger'" />
                                </template>
                            </Column>
                            <Column header="Joined">
                                <template #body="{ data }">
                                    <span class="text-500 text-xs">{{ fmtDate(data.date_joined) }}</span>
                                </template>
                            </Column>
                            <template #empty>
                                <div class="text-center py-3 text-500 text-sm">No users yet.</div>
                            </template>
                        </DataTable>
                    </div>
                </div>

                <!-- ── Recent Audit Events ── -->
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

                <!-- ── System Health ── -->
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

                <!-- ── Role Distribution ── -->
                <div class="col-12 lg:col-6">
                    <div class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-chart-pie mr-2" style="color:#1976d2;" />Users by Role
                        </h5>
                        <div class="flex flex-column gap-3" v-if="!statsLoading">
                            <div v-for="r in roleOptions" :key="r.value">
                                <div class="flex justify-content-between align-items-center mb-1">
                                    <span class="text-600 text-sm">{{ r.label }}</span>
                                    <span class="font-bold text-sm text-900">
                                        {{ userStats.by_role?.[r.value] ?? 0 }}
                                    </span>
                                </div>
                                <ProgressBar
                                    :value="rolePct(r.value)"
                                    :showValue="false" style="height:6px;"
                                    :pt="{ value: { style: { background: r.color } } }" />
                            </div>
                        </div>
                        <div v-else class="flex justify-content-center py-4">
                            <ProgressSpinner style="width:2rem;height:2rem;" />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ══════════════════════════════════════════════
             ADD USER DIALOG — wired to POST /api/admin/users/
        ══════════════════════════════════════════════ -->
        <Dialog v-model:visible="showAddUser"
            header="Register New User"
            :modal="true"
            :style="{ width: '600px' }"
            :closable="!saving">

            <!-- API error inside dialog -->
            <Message v-if="apiError" severity="error" :closable="true"
                class="mb-3" @close="apiError = ''">{{ apiError }}</Message>

            <!-- Section: Personal -->
            <div class="mb-4">
                <div class="flex align-items-center gap-2 mb-3 pb-2"
                    style="border-bottom:2px solid #1976d2;">
                    <i class="pi pi-user" style="color:#1976d2;" />
                    <span class="font-bold text-900">Personal Details</span>
                </div>
                <div class="grid">
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">First Name *</label>
                        <InputText v-model="form.first_name" class="w-full"
                            :class="{ 'p-invalid': errors.first_name }"
                            placeholder="e.g. Felix" />
                        <small class="p-error">{{ fieldError('first_name') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Last Name *</label>
                        <InputText v-model="form.last_name" class="w-full"
                            :class="{ 'p-invalid': errors.last_name }"
                            placeholder="e.g. Mwaniki" />
                        <small class="p-error">{{ fieldError('last_name') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Username *</label>
                        <InputText v-model="form.username" class="w-full"
                            :class="{ 'p-invalid': errors.username }"
                            placeholder="e.g. felix.m" />
                        <small class="p-error">{{ fieldError('username') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Email *</label>
                        <InputText v-model="form.email" class="w-full"
                            :class="{ 'p-invalid': errors.email }"
                            placeholder="felix@icmfs.co.ke" />
                        <small class="p-error">{{ fieldError('email') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Phone</label>
                        <InputText v-model="form.phone" class="w-full"
                            placeholder="+254 7XX XXX XXX" />
                    </div>
                </div>
            </div>

            <!-- Section: Role & Access -->
            <div class="mb-4">
                <div class="flex align-items-center gap-2 mb-3 pb-2"
                    style="border-bottom:2px solid #e6a817;">
                    <i class="pi pi-id-card" style="color:#e6a817;" />
                    <span class="font-bold text-900">Role & Access</span>
                </div>
                <div class="grid">
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Role *</label>
                        <Dropdown v-model="form.role" :options="roleOptions"
                            optionLabel="label" optionValue="value"
                            class="w-full" placeholder="Select a role"
                            :class="{ 'p-invalid': errors.role }" />
                        <small class="p-error">{{ fieldError('role') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Account Status</label>
                        <div class="flex gap-4 mt-2">
                            <div class="flex align-items-center gap-2">
                                <RadioButton v-model="form.is_active" :value="true" inputId="u_active" />
                                <label for="u_active" class="text-sm cursor-pointer font-medium">Active</label>
                            </div>
                            <div class="flex align-items-center gap-2">
                                <RadioButton v-model="form.is_active" :value="false" inputId="u_inactive" />
                                <label for="u_inactive" class="text-sm cursor-pointer text-600">Inactive</label>
                            </div>
                        </div>
                    </div>
                    <!-- Role description hint -->
                    <div class="col-12" v-if="form.role">
                        <div class="flex align-items-start gap-2 p-3 border-round-lg"
                            style="background:var(--surface-50);">
                            <i class="pi pi-info-circle mt-1 flex-shrink-0"
                                :style="{ color: roleColor(form.role) }" />
                            <span class="text-sm text-600">{{ roleDescription(form.role) }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Section: Password -->
            <div class="mb-2">
                <div class="flex align-items-center gap-2 mb-3 pb-2"
                    style="border-bottom:2px solid #2ecc71;">
                    <i class="pi pi-lock" style="color:#2ecc71;" />
                    <span class="font-bold text-900">Password</span>
                </div>
                <div class="grid">
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Password * (min 8 chars)</label>
                        <Password v-model="form.password" class="w-full" fluid
                            toggleMask :feedback="true"
                            :class="{ 'p-invalid': errors.password }" />
                        <small class="p-error">{{ fieldError('password') }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Confirm Password *</label>
                        <Password v-model="form.confirmPassword" class="w-full" fluid
                            toggleMask :feedback="false"
                            :class="{ 'p-invalid': errors.confirmPassword }" />
                        <small class="p-error">{{ errors.confirmPassword }}</small>
                    </div>
                </div>
            </div>

            <template #footer>
                <Button label="Cancel" text @click="showAddUser = false" :disabled="saving" />
                <Button label="Register User" icon="pi pi-user-plus"
                    :loading="saving"
                    style="background:#1976d2;border-color:#1976d2;"
                    @click="submitAddUser" />
            </template>
        </Dialog>

        <!-- ── SUCCESS TOAST (using inline message) ── -->
        <Dialog v-model:visible="showSuccess"
            header="User Registered"
            :modal="true" :style="{ width: '380px' }">
            <div class="flex align-items-center gap-3 py-2">
                <div class="flex align-items-center justify-content-center border-circle flex-shrink-0"
                    style="width:3rem;height:3rem;background:#e8fdf0;">
                    <i class="pi pi-check-circle text-2xl" style="color:#2ecc71;" />
                </div>
                <div>
                    <div class="font-bold text-900">{{ createdUser?.full_name || createdUser?.username }} registered!</div>
                    <div class="text-500 text-sm">
                        Role: <strong>{{ roleLabel(createdUser?.role) }}</strong> ·
                        <span :style="{ color: createdUser?.is_active ? '#2ecc71' : '#ef4444' }">
                            {{ createdUser?.is_active ? 'Active' : 'Inactive' }}
                        </span>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Add Another" icon="pi pi-user-plus" text
                    @click="showSuccess = false; openAddUser()" />
                <Button label="Manage Users" icon="pi pi-cog"
                    style="background:#1976d2;border-color:#1976d2;"
                    @click="showSuccess = false; $router.push('/app/admin/user-management')" />
            </template>
        </Dialog>

    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api/api';

const today = new Date().toLocaleDateString('en-KE', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
});

// ── Role config ───────────────────────────────────────────────
const roleOptions = [
    { label: 'System Admin',    value: 'system_admin', color: '#0d2347' },
    { label: 'Admin',           value: 'admin',        color: '#1976d2' },
    { label: 'Project Manager', value: 'manager',      color: '#2ecc71' },
    { label: 'Engineer',        value: 'engineer',     color: '#e6a817' },
    { label: 'QA / QC',         value: 'qa',           color: '#a855f7' },
    { label: 'Finance',         value: 'finance',      color: '#ef4444' },
    { label: 'Client',          value: 'client',       color: '#9ca3af' },
];

const roleDescriptions = {
    system_admin: 'Full system access. Can manage all users, roles, settings and every module.',
    admin:        'Administrative access. Can manage users and most modules except system settings.',
    manager:      'Manages projects, approves payments and monitors progress across all sites.',
    engineer:     'Field access. Daily logs, progress reports, QA inspections and safety.',
    qa:           'Quality assurance. Conducts inspections, raises NCRs and certifies work.',
    finance:      'Financial access. Manages budgets, invoices, payments and financial reports.',
    client:       'Read-only view of assigned projects and reports.',
};

const roleLabel       = (v) => roleOptions.find((r) => r.value === v)?.label || v;
const roleColor       = (v) => roleOptions.find((r) => r.value === v)?.color || '#1976d2';
const roleDescription = (v) => roleDescriptions[v] || '';

// ── Helpers ───────────────────────────────────────────────────
const fullName = (u) =>
    [u?.first_name, u?.last_name].filter(Boolean).join(' ') || u?.username || '—';
const initials = (u) =>
    fullName(u).split(' ').map((n) => n[0]).slice(0, 2).join('').toUpperCase();
const fmtDate = (d) => {
    if (!d) return '—';
    return new Date(d).toLocaleDateString('en-KE', {
        day: '2-digit', month: 'short', year: 'numeric'
    });
};

// ── Live data state ───────────────────────────────────────────
const userStats    = ref({});
const recentUsers  = ref([]);
const statsLoading = ref(false);
const usersLoading = ref(false);

// ── Add User dialog state ─────────────────────────────────────
const showAddUser  = ref(false);
const showSuccess  = ref(false);
const saving       = ref(false);
const apiError     = ref('');
const errors       = ref({});
const createdUser  = ref(null);

const emptyForm = () => ({
    first_name: '', last_name: '', username: '',
    email: '', phone: '', role: 'client',
    is_active: true, password: '', confirmPassword: '',
});
const form = ref(emptyForm());

const fieldError = (f) => {
    const e = errors.value[f];
    return Array.isArray(e) ? e[0] : e || '';
};

// ── Role % for progress bars ──────────────────────────────────
const rolePct = (role) => {
    const total = userStats.value.total || 1;
    return Math.round(((userStats.value.by_role?.[role] ?? 0) / total) * 100);
};

// ── API: fetch stats + recent users ──────────────────────────
async function loadStats() {
    statsLoading.value = true;
    try {
        const res = await api.get('/api/admin/users/stats/');
        userStats.value = res.data;
    } catch { /* non-critical */ } finally {
        statsLoading.value = false;
    }
}

async function loadRecentUsers() {
    usersLoading.value = true;
    try {
        const res = await api.get('/api/admin/users/?ordering=-date_joined');
        const all = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
        recentUsers.value = all.slice(0, 6);   // show last 6 joined
    } catch { /* non-critical */ } finally {
        usersLoading.value = false;
    }
}

// ── Open Add User ─────────────────────────────────────────────
function openAddUser() {
    form.value   = emptyForm();
    errors.value = {};
    apiError.value = '';
    showAddUser.value = true;
}

// ── Validate ──────────────────────────────────────────────────
function validate() {
    const e = {};
    if (!form.value.first_name.trim()) e.first_name = 'Required';
    if (!form.value.last_name.trim())  e.last_name  = 'Required';
    if (!form.value.username.trim())   e.username   = 'Required';
    if (!form.value.email.trim())      e.email      = 'Required';
    if (!form.value.role)              e.role       = 'Required';
    if (!form.value.password)          e.password   = 'Required';
    else if (form.value.password.length < 8)
                                       e.password   = 'Minimum 8 characters';
    if (form.value.password !== form.value.confirmPassword)
                                       e.confirmPassword = 'Passwords do not match';
    errors.value = e;
    return Object.keys(e).length === 0;
}

// ── Submit → POST /api/admin/users/ ──────────────────────────
async function submitAddUser() {
    if (!validate()) return;

    saving.value   = true;
    apiError.value = '';

    try {
        const payload = { ...form.value };
        delete payload.confirmPassword;

        const res = await api.post('/api/admin/users/', payload);

        createdUser.value   = res.data;
        showAddUser.value   = false;
        showSuccess.value   = true;

        // Refresh dashboard data
        await Promise.all([loadStats(), loadRecentUsers()]);

    } catch (e) {
        const data = e.response?.data;
        if (data && typeof data === 'object' && !data.detail) {
            // DRF field-level errors → show under each field
            errors.value = data;
        } else {
            apiError.value = data?.detail || 'Registration failed. Please try again.';
        }
    } finally {
        saving.value = false;
    }
}

// ── Static data (kept as fallback until real endpoints exist) ─
const kpis = ref([
    { label: 'Total Users',       value: '—',  icon: 'pi pi-users',   color: '#1976d2', bg: '#e8f0fe', trend: '',  trendColor: '#2ecc71', trendLabel: '' },
    { label: 'Active Sessions',   value: '—',  icon: 'pi pi-desktop', color: '#2ecc71', bg: '#e8fdf0', trend: '',  trendColor: '#2ecc71', trendLabel: 'right now' },
    { label: 'Roles Defined',     value: '7',  icon: 'pi pi-id-card', color: '#e6a817', bg: '#fef9e7', trend: '',  trendColor: '#e6a817', trendLabel: '' },
    { label: 'Audit Events Today',value: '—',  icon: 'pi pi-list',    color: '#0d2347', bg: '#e8ecf4', trend: '',  trendColor: '#ef4444', trendLabel: '' },
]);

const auditEvents = ref([
    { id:1, action:'User login',           user:'Felix Mwaniki', time:'2 min ago', module:'Auth',     icon:'pi pi-sign-in',   color:'#2ecc71', bg:'#e8fdf0' },
    { id:2, action:'Role updated — PM',    user:'Admin',         time:'1 hr ago',  module:'Roles',    icon:'pi pi-id-card',   color:'#1976d2', bg:'#e8f0fe' },
    { id:3, action:'New user registered',  user:'System',        time:'3 hrs ago', module:'Users',    icon:'pi pi-user-plus', color:'#e6a817', bg:'#fef9e7' },
    { id:4, action:'Settings changed',     user:'Felix Mwaniki', time:'Yesterday', module:'Settings', icon:'pi pi-cog',       color:'#6b7280', bg:'#f3f4f6' },
    { id:5, action:'Failed login attempt', user:'Unknown',       time:'Yesterday', module:'Auth',     icon:'pi pi-ban',       color:'#ef4444', bg:'#fde8e8' },
]);

const systemHealth = ref([
    { label: 'Database',     value: 'Healthy', pct: 98, color: '#2ecc71' },
    { label: 'API Response', value: '42ms',    pct: 92, color: '#1976d2' },
    { label: 'Storage Used', value: '34%',     pct: 34, color: '#e6a817' },
    { label: 'CPU Usage',    value: '18%',     pct: 18, color: '#2ecc71' },
    { label: 'Memory Usage', value: '61%',     pct: 61, color: '#e6a817' },
]);

// ── Init ──────────────────────────────────────────────────────
onMounted(async () => {
    await Promise.all([loadStats(), loadRecentUsers()]);
    // Update KPI total users from real data
    kpis.value[0].value = userStats.value.total ?? '—';
});
</script>