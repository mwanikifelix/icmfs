<template>
    <div class="grid">
        <div class="col-12">

            <!-- ── HEADER ── -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-users text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">User Management</h4>
                        <span class="text-sm" style="color:#b3c8e8;">
                            {{ stats.total ?? '—' }} registered users ·
                            <span style="color:#e6a817;">{{ stats.active ?? '—' }} active</span>
                        </span>
                    </div>
                </div>
                <!-- Only system_admin / admin can create users -->
                <Button
                    v-if="canCreate"
                    label="Register New User"
                    icon="pi pi-user-plus"
                    style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                    @click="openCreate"
                />
            </div>

            <!-- ── ACCESS DENIED NOTICE ── -->
            <Message v-if="!canCreate" severity="warn" :closable="false" class="mb-3">
                You have read-only access. Only System Admins can register or modify users.
            </Message>

            <!-- ── API ERROR ── -->
            <Message v-if="apiError" severity="error" :closable="true"
                class="mb-3" @close="apiError = ''">{{ apiError }}</Message>

            <!-- ── STAT CARDS ── -->
            <div class="grid mb-3">
                <div class="col-6 lg:col-3" v-for="s in statCards" :key="s.label">
                    <div class="card mb-0 text-center py-3">
                        <div v-if="statsLoading" class="flex justify-content-center">
                            <ProgressSpinner style="width:1.8rem;height:1.8rem;" />
                        </div>
                        <template v-else>
                            <div class="font-bold text-3xl mb-1" :style="{ color: s.color }">{{ s.value }}</div>
                            <div class="text-500 text-sm">{{ s.label }}</div>
                        </template>
                    </div>
                </div>
            </div>

            <!-- ── ROLE BREAKDOWN ── -->
            <div class="card mb-3" v-if="!statsLoading && stats.by_role">
                <div class="flex flex-wrap gap-3 align-items-center">
                    <span class="text-600 text-sm font-medium mr-2">Users by role:</span>
                    <div v-for="r in roleOptions" :key="r.value"
                        class="flex align-items-center gap-2 px-3 py-1 border-round"
                        style="background:var(--surface-50);">
                        <span class="font-bold text-sm" :style="{ color: r.color }">
                            {{ stats.by_role?.[r.value] ?? 0 }}
                        </span>
                        <span class="text-500 text-xs">{{ r.label }}</span>
                    </div>
                </div>
            </div>

            <!-- ── TABLE ── -->
            <div class="card">

                <!-- Toolbar -->
                <div class="flex flex-wrap gap-3 mb-4 align-items-center justify-content-between">
                    <div class="p-input-icon-left" style="flex:1;min-width:200px;max-width:320px;">
                        <i class="pi pi-search" />
                        <InputText v-model="search" placeholder="Search name, email or username..."
                            class="w-full" @input="onSearchInput" />
                    </div>
                    <div class="flex gap-2 flex-wrap">
                        <Dropdown
                            v-model="filterRole"
                            :options="roleOptions"
                            optionLabel="label" optionValue="value"
                            placeholder="All Roles" showClear style="min-width:160px;"
                            @change="loadUsers"
                        />
                        <Dropdown
                            v-model="filterStatus"
                            :options="[{label:'Active',value:'active'},{label:'Inactive',value:'inactive'}]"
                            optionLabel="label" optionValue="value"
                            placeholder="All Status" showClear style="min-width:140px;"
                            @change="loadUsers"
                        />
                        <Button icon="pi pi-refresh" outlined severity="secondary"
                            v-tooltip.top="'Refresh'" :loading="loading" @click="loadUsers" />
                    </div>
                </div>

                <DataTable
                    :value="users"
                    :loading="loading"
                    :paginator="true"
                    :rows="10"
                    :rowsPerPageOptions="[5, 10, 20, 50]"
                    stripedRows
                    responsiveLayout="scroll"
                    v-model:selection="selectedUsers"
                    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                    currentPageReportTemplate="{first}–{last} of {totalRecords} users"
                >
                    <Column selectionMode="multiple" style="width:3rem;" />

                    <!-- User -->
                    <Column header="User" sortable sortField="username" style="min-width:220px;">
                        <template #body="{ data }">
                            <div class="flex align-items-center gap-3">
                                <div class="flex align-items-center justify-content-center border-circle font-bold text-sm flex-shrink-0"
                                    style="width:2.5rem;height:2.5rem;color:#fff;"
                                    :style="{ background: roleColor(data.role) }">
                                    {{ avatarInitials(data) }}
                                </div>
                                <div>
                                    <div class="font-semibold text-900 text-sm">{{ fullName(data) }}</div>
                                    <div class="text-400 text-xs">{{ data.email }}</div>
                                </div>
                            </div>
                        </template>
                    </Column>

                    <!-- Username -->
                    <Column field="username" header="Username" sortable>
                        <template #body="{ data }">
                            <span class="font-mono text-sm text-600">@{{ data.username }}</span>
                        </template>
                    </Column>

                    <!-- Role -->
                    <Column header="Role" sortable sortField="role">
                        <template #body="{ data }">
                            <Tag :value="roleLabel(data.role)"
                                style="background:#0d2347;color:#e6a817;font-size:0.7rem;" />
                        </template>
                    </Column>

                    <!-- Phone -->
                    <Column field="phone" header="Phone">
                        <template #body="{ data }">
                            <span class="text-sm text-600">{{ data.phone || '—' }}</span>
                        </template>
                    </Column>

                    <!-- Status -->
                    <Column header="Status">
                        <template #body="{ data }">
                            <Tag
                                :value="data.is_active ? 'Active' : 'Inactive'"
                                :severity="data.is_active ? 'success' : 'danger'"
                            />
                        </template>
                    </Column>

                    <!-- Joined -->
                    <Column header="Joined" sortable sortField="date_joined">
                        <template #body="{ data }">
                            <span class="text-500 text-sm">{{ fmtDate(data.date_joined) }}</span>
                        </template>
                    </Column>

                    <!-- Last Login -->
                    <Column header="Last Login" sortable sortField="last_login">
                        <template #body="{ data }">
                            <span class="text-500 text-sm">{{ fmtDate(data.last_login) || 'Never' }}</span>
                        </template>
                    </Column>

                    <!-- Actions — hidden for non-admins -->
                    <Column v-if="canCreate" header="Actions" style="width:150px;">
                        <template #body="{ data }">
                            <div class="flex gap-1">
                                <!-- Edit -->
                                <Button icon="pi pi-pencil" text rounded size="small"
                                    v-tooltip.top="'Edit user'"
                                    @click="openEdit(data)" />

                                <!-- Activate / Deactivate — cannot do to yourself -->
                                <Button
                                    v-if="data.id !== currentUserId"
                                    :icon="data.is_active ? 'pi pi-ban' : 'pi pi-check-circle'"
                                    text rounded size="small"
                                    :severity="data.is_active ? 'warning' : 'success'"
                                    :v-tooltip="data.is_active ? 'Deactivate' : 'Activate'"
                                    @click="toggleStatus(data)"
                                />

                                <!-- Reset password -->
                                <Button icon="pi pi-key" text rounded size="small"
                                    severity="secondary"
                                    v-tooltip.top="'Reset password'"
                                    @click="openResetPassword(data)" />

                                <!-- Delete — cannot delete yourself -->
                                <Button
                                    v-if="data.id !== currentUserId"
                                    icon="pi pi-trash" text rounded size="small"
                                    severity="danger"
                                    v-tooltip.top="'Delete user'"
                                    @click="confirmDelete(data)"
                                />
                            </div>
                        </template>
                    </Column>

                    <template #empty>
                        <div class="text-center py-6 text-500">
                            <i class="pi pi-users text-4xl mb-2 block text-300" />
                            <div>No users found.</div>
                            <Button v-if="canCreate" label="Register First User" icon="pi pi-plus"
                                class="mt-3" size="small"
                                style="background:#1976d2;border-color:#1976d2;"
                                @click="openCreate" />
                        </div>
                    </template>
                </DataTable>
            </div>
        </div>

        <!-- ════════════════════════════════════════════
             REGISTER / EDIT USER DIALOG
        ════════════════════════════════════════════ -->
        <Dialog
            v-model:visible="showForm"
            :header="editTarget ? `Edit — ${fullName(editTarget)}` : 'Register New User'"
            :modal="true"
            :style="{ width: '600px' }"
            :closable="!saving"
        >
            <!-- Section: Personal details -->
            <div class="mb-3">
                <div class="flex align-items-center gap-2 mb-3 pb-2"
                    style="border-bottom:2px solid #1976d2;">
                    <i class="pi pi-user" style="color:#1976d2;" />
                    <span class="font-bold text-900">Personal Details</span>
                </div>
                <div class="grid">
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">First Name *</label>
                        <InputText v-model="form.first_name" class="w-full"
                            :class="{ 'p-invalid': errors.first_name }" placeholder="e.g. Felix" />
                        <small class="p-error">{{ Array.isArray(errors.first_name) ? errors.first_name[0] : errors.first_name }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Last Name *</label>
                        <InputText v-model="form.last_name" class="w-full"
                            :class="{ 'p-invalid': errors.last_name }" placeholder="e.g. Mwaniki" />
                        <small class="p-error">{{ Array.isArray(errors.last_name) ? errors.last_name[0] : errors.last_name }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Username *</label>
                        <InputText v-model="form.username" class="w-full"
                            :class="{ 'p-invalid': errors.username }"
                            placeholder="e.g. felix.m"
                            :disabled="!!editTarget" />
                        <small class="p-error">{{ Array.isArray(errors.username) ? errors.username[0] : errors.username }}</small>
                        <small v-if="editTarget" class="text-400">Username cannot be changed</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Email *</label>
                        <InputText v-model="form.email" class="w-full"
                            :class="{ 'p-invalid': errors.email }" placeholder="felix@icmfs.co.ke" />
                        <small class="p-error">{{ Array.isArray(errors.email) ? errors.email[0] : errors.email }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Phone</label>
                        <InputText v-model="form.phone" class="w-full" placeholder="+254 7XX XXX XXX" />
                    </div>
                </div>
            </div>

            <!-- Section: Role & Access -->
            <div class="mb-3">
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
                        <small class="p-error">{{ Array.isArray(errors.role) ? errors.role[0] : errors.role }}</small>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label class="block font-medium mb-2 text-600">Account Status</label>
                        <div class="flex gap-4 mt-2">
                            <div class="flex align-items-center gap-2">
                                <RadioButton v-model="form.is_active" :value="true" inputId="st_active" />
                                <label for="st_active" class="text-sm cursor-pointer text-900 font-medium">Active</label>
                            </div>
                            <div class="flex align-items-center gap-2">
                                <RadioButton v-model="form.is_active" :value="false" inputId="st_inactive" />
                                <label for="st_inactive" class="text-sm cursor-pointer text-600">Inactive</label>
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

            <!-- Section: Password (create only) -->
            <div v-if="!editTarget" class="mb-2">
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
                        <small class="p-error">{{ Array.isArray(errors.password) ? errors.password[0] : errors.password }}</small>
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
                <Button label="Cancel" text @click="showForm = false" :disabled="saving" />
                <Button
                    :label="editTarget ? 'Save Changes' : 'Register User'"
                    :icon="editTarget ? 'pi pi-check' : 'pi pi-user-plus'"
                    :loading="saving"
                    style="background:#1976d2;border-color:#1976d2;"
                    @click="saveUser"
                />
            </template>
        </Dialog>

        <!-- ── RESET PASSWORD DIALOG ── -->
        <Dialog v-model:visible="showResetPwd" header="Reset Password"
            :modal="true" :style="{ width: '420px' }">
            <div class="flex align-items-center gap-3 mb-4 p-3 border-round-lg"
                style="background:var(--surface-50);">
                <div class="flex align-items-center justify-content-center border-circle font-bold flex-shrink-0"
                    style="width:2.5rem;height:2.5rem;background:#1976d2;color:#fff;">
                    {{ avatarInitials(resetTarget) }}
                </div>
                <div>
                    <div class="font-bold text-900">{{ fullName(resetTarget) }}</div>
                    <div class="text-500 text-xs">@{{ resetTarget?.username }}</div>
                </div>
            </div>
            <div class="field mb-3">
                <label class="block font-medium mb-2 text-600">New Password * (min 8 chars)</label>
                <Password v-model="newPassword" class="w-full" fluid toggleMask :feedback="true" />
            </div>
            <template #footer>
                <Button label="Cancel" text @click="showResetPwd = false" :disabled="saving" />
                <Button label="Reset Password" icon="pi pi-key"
                    :loading="saving" :disabled="!newPassword || newPassword.length < 8"
                    style="background:#1976d2;border-color:#1976d2;"
                    @click="submitResetPassword" />
            </template>
        </Dialog>

        <!-- ── DELETE CONFIRM ── -->
        <Dialog v-model:visible="showDeleteConfirm" header="Delete User"
            :modal="true" :style="{ width: '400px' }">
            <div class="flex align-items-center gap-3 mb-3">
                <div class="flex align-items-center justify-content-center border-round flex-shrink-0"
                    style="width:3rem;height:3rem;background:#fde8e8;">
                    <i class="pi pi-exclamation-triangle text-xl" style="color:#ef4444;" />
                </div>
                <div>
                    <div class="font-bold text-900">Delete {{ fullName(deleteTarget) }}?</div>
                    <div class="text-500 text-sm">@{{ deleteTarget?.username }} · {{ roleLabel(deleteTarget?.role) }}</div>
                </div>
            </div>
            <p class="text-600 text-sm">
                This will permanently remove the user and all their associated data.
                This action <strong>cannot be undone</strong>.
            </p>
            <template #footer>
                <Button label="Cancel" text @click="showDeleteConfirm = false" :disabled="saving" />
                <Button label="Delete Permanently" severity="danger" icon="pi pi-trash"
                    :loading="saving" @click="deleteUser" />
            </template>
        </Dialog>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/api/api';
import { authService } from '@/service/authService';

// ── Current logged-in user ────────────────────────────────────
const currentUser   = authService.getUser();
const currentUserId = currentUser?.id;
const currentRole   = authService.getRole();

// Who can create/edit/delete users
const canCreate = computed(() =>
    ['system_admin', 'admin'].includes(currentRole)
);

// ── Role config — matches Django ROLE_CHOICES exactly ─────────
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

const roleLabel       = (v)  => roleOptions.find((r) => r.value === v)?.label || v;
const roleColor       = (v)  => roleOptions.find((r) => r.value === v)?.color || '#1976d2';
const roleDescription = (v)  => roleDescriptions[v] || '';

// ── State ─────────────────────────────────────────────────────
const users         = ref([]);
const stats         = ref({});
const loading       = ref(false);
const statsLoading  = ref(false);
const saving        = ref(false);
const apiError      = ref('');
const search        = ref('');
const filterRole    = ref(null);
const filterStatus  = ref(null);
const selectedUsers = ref([]);

const showForm          = ref(false);
const showDeleteConfirm = ref(false);
const showResetPwd      = ref(false);
const editTarget        = ref(null);
const deleteTarget      = ref(null);
const resetTarget       = ref(null);
const newPassword       = ref('');
const errors            = ref({});

const emptyForm = () => ({
    first_name:      '',
    last_name:       '',
    username:        '',
    email:           '',
    phone:           '',
    role:            'client',
    is_active:       true,
    password:        '',
    confirmPassword: '',
});
const form = ref(emptyForm());

// ── Stat cards ────────────────────────────────────────────────
const statCards = computed(() => [
    { label: 'Total Users',   value: stats.value.total    ?? 0, color: '#1976d2' },
    { label: 'Active',        value: stats.value.active   ?? 0, color: '#2ecc71' },
    { label: 'Inactive',      value: stats.value.inactive ?? 0, color: '#ef4444' },
    { label: 'Roles Defined', value: roleOptions.length,        color: '#e6a817' },
]);

// ── Helpers ───────────────────────────────────────────────────
const fullName = (u) =>
    [u?.first_name, u?.last_name].filter(Boolean).join(' ') || u?.username || '—';

const avatarInitials = (u) =>
    fullName(u).split(' ').map((n) => n[0]).slice(0, 2).join('').toUpperCase();

const fmtDate = (d) => {
    if (!d) return null;
    return new Date(d).toLocaleDateString('en-KE', {
        day: '2-digit', month: 'short', year: 'numeric',
    });
};

// ── API: load users ───────────────────────────────────────────
async function loadUsers() {
    loading.value  = true;
    apiError.value = '';
    try {
        const params = {};
        if (filterRole.value)   params.role   = filterRole.value;
        if (filterStatus.value) params.status = filterStatus.value;
        if (search.value)       params.search = search.value;

        const res = await api.get('/api/admin/users/', { params });
        users.value = Array.isArray(res.data)
            ? res.data
            : (res.data.results ?? []);
    } catch (e) {
        apiError.value = e.response?.data?.detail || 'Failed to load users.';
    } finally {
        loading.value = false;
    }
}

// ── API: load stats ───────────────────────────────────────────
async function loadStats() {
    statsLoading.value = true;
    try {
        const res = await api.get('/api/admin/users/stats/');
        stats.value = res.data;
    } catch { /* non-critical */ } finally {
        statsLoading.value = false;
    }
}

// ── Search debounce ───────────────────────────────────────────
let searchTimer = null;
function onSearchInput() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadUsers, 400);
}

// ── Open dialogs ──────────────────────────────────────────────
function openCreate() {
    editTarget.value = null;
    errors.value     = {};
    form.value       = emptyForm();
    showForm.value   = true;
}

function openEdit(user) {
    editTarget.value = user;
    errors.value     = {};
    form.value = {
        first_name:      user.first_name || '',
        last_name:       user.last_name  || '',
        username:        user.username   || '',
        email:           user.email      || '',
        phone:           user.phone      || '',
        role:            user.role       || 'client',
        is_active:       user.is_active  ?? true,
        password:        '',
        confirmPassword: '',
    };
    showForm.value = true;
}

function openResetPassword(user) {
    resetTarget.value = user;
    newPassword.value = '';
    showResetPwd.value = true;
}

function confirmDelete(user) {
    deleteTarget.value      = user;
    showDeleteConfirm.value = true;
}

// ── Validate ──────────────────────────────────────────────────
function validate() {
    const e = {};
    if (!form.value.first_name.trim()) e.first_name = 'Required';
    if (!form.value.last_name.trim())  e.last_name  = 'Required';
    if (!form.value.username.trim())   e.username   = 'Required';
    if (!form.value.email.trim())      e.email      = 'Required';
    if (!form.value.role)              e.role       = 'Required';

    if (!editTarget.value) {
        if (!form.value.password)               e.password        = 'Required';
        else if (form.value.password.length < 8) e.password       = 'Minimum 8 characters';
        if (form.value.password !== form.value.confirmPassword)
                                                  e.confirmPassword = 'Passwords do not match';
    }
    errors.value = e;
    return Object.keys(e).length === 0;
}

// ── API: create or update ─────────────────────────────────────
async function saveUser() {
    if (!validate()) return;

    saving.value   = true;
    apiError.value = '';

    try {
        const payload = { ...form.value };
        delete payload.confirmPassword;

        if (editTarget.value) {
            // PUT — partial update (username disabled so not sent)
            if (!payload.password) delete payload.password;
            await api.put(`/api/admin/users/${editTarget.value.id}/`, payload);
        } else {
            // POST — register new user with role
            await api.post('/api/admin/users/', payload);
        }

        showForm.value = false;
        await Promise.all([loadUsers(), loadStats()]);

    } catch (e) {
        const data = e.response?.data;
        if (data && typeof data === 'object' && !data.detail) {
            // DRF field-level errors: { username: ["already exists"] }
            errors.value = data;
        } else {
            apiError.value = data?.detail || 'Failed to save user. Please try again.';
        }
    } finally {
        saving.value = false;
    }
}

// ── API: toggle active / inactive ────────────────────────────
async function toggleStatus(user) {
    try {
        const res = await api.post(`/api/admin/users/${user.id}/toggle-status/`);
        user.is_active = res.data.is_active;   // mutate in-place
        await loadStats();
    } catch (e) {
        apiError.value = e.response?.data?.detail || 'Failed to update status.';
    }
}

// ── API: reset password ───────────────────────────────────────
async function submitResetPassword() {
    if (!newPassword.value || newPassword.value.length < 8) return;
    saving.value = true;
    try {
        await api.post(
            `/api/admin/users/${resetTarget.value.id}/reset-password/`,
            { new_password: newPassword.value }
        );
        showResetPwd.value = false;
    } catch (e) {
        apiError.value = e.response?.data?.detail || 'Failed to reset password.';
    } finally {
        saving.value = false;
    }
}

// ── API: delete user ──────────────────────────────────────────
async function deleteUser() {
    saving.value = true;
    try {
        await api.delete(`/api/admin/users/${deleteTarget.value.id}/`);
        showDeleteConfirm.value = false;
        await Promise.all([loadUsers(), loadStats()]);
    } catch (e) {
        apiError.value = e.response?.data?.detail || 'Failed to delete user.';
    } finally {
        saving.value = false;
    }
}

// ── Init ──────────────────────────────────────────────────────
onMounted(() => {
    loadUsers();
    loadStats();
});
</script>