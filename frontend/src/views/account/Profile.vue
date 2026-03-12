<template>
    <div class="grid">
        <div class="col-12">

            <!-- ── HEADER BANNER ── -->
            <div class="border-round-xl mb-4 p-5 flex align-items-center gap-4 flex-wrap"
                style="background: linear-gradient(135deg, #0d2347 0%, #1976d2 100%);">
                <!-- Avatar -->
                <div class="flex align-items-center justify-content-center border-circle font-bold flex-shrink-0"
                    style="width:5rem;height:5rem;font-size:1.8rem;background:#e6a817;color:#0d2347;">
                    {{ userInitials }}
                </div>
                <div class="flex-1">
                    <h3 class="mt-0 mb-1" style="color:#ffffff;">{{ displayName }}</h3>
                    <div class="flex flex-wrap gap-3 align-items-center">
                        <Tag :value="userRole" style="background:#e6a817;color:#0d2347;font-weight:700;" />
                        <span class="text-sm" style="color:#b3c8e8;">
                            <i class="pi pi-envelope mr-1" />{{ user?.email || '—' }}
                        </span>
                        <span class="text-sm" style="color:#b3c8e8;">
                            <i class="pi pi-calendar mr-1" />Joined {{ joinedDate }}
                        </span>
                    </div>
                </div>
                <Button
                    label="Edit Profile"
                    icon="pi pi-pencil"
                    class="flex-shrink-0"
                    style="background:#e6a817;border-color:#e6a817;color:#0d2347;font-weight:700;"
                    @click="editing = true"
                />
            </div>

            <div class="grid">

                <!-- ── LEFT: Personal Info ── -->
                <div class="col-12 lg:col-8">
                    <div class="card h-full">
                        <div class="flex justify-content-between align-items-center mb-4">
                            <h5 class="mt-0 mb-0" style="color:#0d2347;">
                                <i class="pi pi-user mr-2" style="color:#1976d2;" />Personal Information
                            </h5>
                            <span v-if="saved" class="text-sm font-medium" style="color:#2ecc71;">
                                <i class="pi pi-check-circle mr-1" />Saved
                            </span>
                        </div>

                        <div class="grid">
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">First Name</label>
                                <InputText v-model="form.first_name" class="w-full" :disabled="!editing" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Last Name</label>
                                <InputText v-model="form.last_name" class="w-full" :disabled="!editing" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Username</label>
                                <InputText v-model="form.username" class="w-full" disabled />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Email Address</label>
                                <InputText v-model="form.email" class="w-full" :disabled="!editing" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Phone Number</label>
                                <InputText v-model="form.phone" class="w-full" :disabled="!editing" placeholder="+254 7XX XXX XXX" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Department</label>
                                <InputText v-model="form.department" class="w-full" :disabled="!editing" />
                            </div>
                            <div class="col-12 field">
                                <label class="block font-medium mb-2 text-600">Bio</label>
                                <Textarea v-model="form.bio" rows="3" class="w-full" :disabled="!editing"
                                    placeholder="Brief description of your role..." autoResize />
                            </div>
                        </div>

                        <div v-if="editing" class="flex gap-2 mt-2">
                            <Button label="Save Changes" icon="pi pi-check" :loading="saving"
                                style="background:#1976d2;border-color:#1976d2;"
                                @click="saveProfile" />
                            <Button label="Cancel" icon="pi pi-times" severity="secondary" text
                                @click="cancelEdit" />
                        </div>
                    </div>
                </div>

                <!-- ── RIGHT: Account Info ── -->
                <div class="col-12 lg:col-4">

                    <!-- Role & Access -->
                    <div class="card mb-3">
                        <h6 class="mt-0 mb-3 font-bold" style="color:#0d2347;">
                            <i class="pi pi-shield mr-2" style="color:#1976d2;" />Role & Access
                        </h6>
                        <div class="flex flex-column gap-3">
                            <div class="flex justify-content-between align-items-center">
                                <span class="text-600 text-sm">Role</span>
                                <Tag :value="userRole" style="background:#0d2347;color:#e6a817;" />
                            </div>
                            <Divider class="my-0" />
                            <div class="flex justify-content-between align-items-center">
                                <span class="text-600 text-sm">Status</span>
                                <Tag value="Active" severity="success" />
                            </div>
                            <Divider class="my-0" />
                            <div class="flex justify-content-between align-items-center">
                                <span class="text-600 text-sm">2FA</span>
                                <Tag value="Disabled" severity="warning" />
                            </div>
                        </div>
                    </div>

                    <!-- Quick stats -->
                    <div class="card mb-3">
                        <h6 class="mt-0 mb-3 font-bold" style="color:#0d2347;">
                            <i class="pi pi-chart-bar mr-2" style="color:#2ecc71;" />Activity
                        </h6>
                        <div class="flex flex-column gap-3">
                            <div v-for="stat in activityStats" :key="stat.label"
                                class="flex justify-content-between align-items-center">
                                <span class="text-600 text-sm">{{ stat.label }}</span>
                                <span class="font-bold" :style="{ color: stat.color }">{{ stat.value }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Danger zone -->
                    <div class="card border-1" style="border-color:#ef4444 !important;">
                        <h6 class="mt-0 mb-3 font-bold text-red-500">
                            <i class="pi pi-exclamation-triangle mr-2" />Danger Zone
                        </h6>
                        <Button label="Deactivate Account" icon="pi pi-ban"
                            severity="danger" outlined class="w-full text-sm"
                            @click="confirmDeactivate = true" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Confirm deactivate dialog -->
        <Dialog v-model:visible="confirmDeactivate" header="Deactivate Account"
            :modal="true" :style="{ width: '400px' }">
            <p class="text-600">Are you sure you want to deactivate your account? You will be logged out immediately.</p>
            <template #footer>
                <Button label="Cancel" text @click="confirmDeactivate = false" />
                <Button label="Deactivate" severity="danger" @click="confirmDeactivate = false" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { authService } from '@/service/authService';

// ── User data ─────────────────────────────────────────────────
const user = computed(() => authService.getUser());

const displayName = computed(() => {
    if (!user.value) return 'User';
    if (user.value.full_name)  return user.value.full_name;
    if (user.value.first_name) return `${user.value.first_name} ${user.value.last_name || ''}`.trim();
    return user.value.username || 'User';
});

const userInitials = computed(() =>
    displayName.value.split(' ').map((n) => n[0]).slice(0, 2).join('').toUpperCase()
);

const userRole = computed(() =>
    (localStorage.getItem('role') || user.value?.role || 'User')
        .replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
);

const joinedDate = computed(() => {
    const d = user.value?.date_joined;
    return d ? new Date(d).toLocaleDateString('en-KE', { year: 'numeric', month: 'long' }) : '—';
});

// ── Form state ────────────────────────────────────────────────
const editing = ref(false);
const saving  = ref(false);
const saved   = ref(false);
const confirmDeactivate = ref(false);

const form = ref({
    first_name:  user.value?.first_name  || '',
    last_name:   user.value?.last_name   || '',
    username:    user.value?.username    || '',
    email:       user.value?.email       || '',
    phone:       user.value?.phone       || '',
    department:  user.value?.department  || '',
    bio:         user.value?.bio         || '',
});

const original = { ...form.value };

async function saveProfile() {
    saving.value = true;
    await new Promise((r) => setTimeout(r, 800)); // replace with api.patch('/api/accounts/me/', form.value)
    const updated = { ...user.value, ...form.value };
    localStorage.setItem('user', JSON.stringify(updated));
    saving.value = false;
    editing.value = false;
    saved.value = true;
    setTimeout(() => (saved.value = false), 3000);
}

function cancelEdit() {
    Object.assign(form.value, original);
    editing.value = false;
}

// ── Activity stats (replace with real API data) ───────────────
const activityStats = [
    { label: 'Projects Managed',    value: '4',         color: '#1976d2' },
    { label: 'Reports This Month',  value: '12',        color: '#2ecc71' },
    { label: 'Last Login',          value: 'Today',     color: '#e6a817' },
    { label: 'Sessions This Week',  value: '8',         color: '#0d2347' },
];
</script>