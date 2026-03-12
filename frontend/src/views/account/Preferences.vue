<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center justify-content-center border-round-lg"
                    style="width:3rem;height:3rem;background:#e6a817;">
                    <i class="pi pi-sliders-h text-xl" style="color:#0d2347;" />
                </div>
                <div>
                    <h4 class="mt-0 mb-1" style="color:#fff;">Preferences</h4>
                    <span class="text-sm" style="color:#b3c8e8;">Manage your display, notification and system preferences</span>
                </div>
            </div>

            <div class="grid">

                <!-- ── LEFT column ── -->
                <div class="col-12 lg:col-6">

                    <!-- Appearance -->
                    <div class="card mb-3">
                        <h5 class="mt-0 mb-4 flex align-items-center gap-2" style="color:#0d2347;">
                            <i class="pi pi-palette" style="color:#1976d2;" /> Appearance
                        </h5>

                        <div class="field mb-4">
                            <label class="block font-medium mb-2 text-600">Theme Mode</label>
                            <div class="flex gap-3">
                                <div v-for="mode in themeModes" :key="mode.value"
                                    class="flex-1 border-round-lg p-3 text-center cursor-pointer border-2 transition-all transition-duration-200"
                                    :style="prefs.theme === mode.value
                                        ? 'border-color:#1976d2;background:#e8f0fe;'
                                        : 'border-color:var(--surface-border);'"
                                    @click="prefs.theme = mode.value">
                                    <i :class="mode.icon" class="text-2xl mb-2 block"
                                        :style="prefs.theme === mode.value ? 'color:#1976d2' : 'color:var(--text-color-secondary)'" />
                                    <span class="text-sm font-medium">{{ mode.label }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="field mb-4">
                            <label class="block font-medium mb-2 text-600">Language</label>
                            <Dropdown v-model="prefs.language" :options="languageOptions"
                                optionLabel="label" optionValue="value" class="w-full" />
                        </div>

                        <div class="field mb-0">
                            <label class="block font-medium mb-2 text-600">Date Format</label>
                            <Dropdown v-model="prefs.dateFormat" :options="dateFormats"
                                optionLabel="label" optionValue="value" class="w-full" />
                        </div>
                    </div>

                    <!-- Dashboard Layout -->
                    <div class="card">
                        <h5 class="mt-0 mb-4 flex align-items-center gap-2" style="color:#0d2347;">
                            <i class="pi pi-th-large" style="color:#2ecc71;" /> Dashboard Layout
                        </h5>

                        <div class="field mb-4">
                            <label class="block font-medium mb-2 text-600">Default Landing Page</label>
                            <Dropdown v-model="prefs.landingPage" :options="landingOptions"
                                optionLabel="label" optionValue="value" class="w-full" />
                        </div>

                        <div class="field mb-4">
                            <label class="block font-medium mb-2 text-600">Items Per Page (tables)</label>
                            <Dropdown v-model="prefs.rowsPerPage" :options="[5,10,20,50]" class="w-full" />
                        </div>

                        <div class="flex align-items-center justify-content-between mb-3">
                            <div>
                                <div class="font-medium text-900">Show Progress Bars</div>
                                <div class="text-500 text-sm">Display progress in project tables</div>
                            </div>
                            <ToggleSwitch v-model="prefs.showProgress" />
                        </div>
                        <div class="flex align-items-center justify-content-between">
                            <div>
                                <div class="font-medium text-900">Compact View</div>
                                <div class="text-500 text-sm">Reduce spacing in tables and lists</div>
                            </div>
                            <ToggleSwitch v-model="prefs.compactView" />
                        </div>
                    </div>
                </div>

                <!-- ── RIGHT column ── -->
                <div class="col-12 lg:col-6">

                    <!-- Notifications -->
                    <div class="card mb-3">
                        <h5 class="mt-0 mb-4 flex align-items-center gap-2" style="color:#0d2347;">
                            <i class="pi pi-bell" style="color:#e6a817;" /> Notifications
                        </h5>

                        <div class="flex flex-column gap-4">
                            <div v-for="n in notificationSettings" :key="n.key"
                                class="flex align-items-center justify-content-between p-3 border-round-lg"
                                style="background:var(--surface-50);">
                                <div class="flex align-items-center gap-3">
                                    <div class="flex align-items-center justify-content-center border-round"
                                        style="width:2.2rem;height:2.2rem;" :style="{ background: n.bg }">
                                        <i :class="n.icon" style="font-size:0.9rem;" :style="{ color: n.color }" />
                                    </div>
                                    <div>
                                        <div class="font-medium text-900 text-sm">{{ n.label }}</div>
                                        <div class="text-500 text-xs">{{ n.description }}</div>
                                    </div>
                                </div>
                                <ToggleSwitch v-model="prefs.notifications[n.key]" />
                            </div>
                        </div>
                    </div>

                    <!-- Currency & Units -->
                    <div class="card mb-3">
                        <h5 class="mt-0 mb-4 flex align-items-center gap-2" style="color:#0d2347;">
                            <i class="pi pi-dollar" style="color:#2ecc71;" /> Regional & Units
                        </h5>

                        <div class="field mb-4">
                            <label class="block font-medium mb-2 text-600">Currency</label>
                            <Dropdown v-model="prefs.currency" :options="currencyOptions"
                                optionLabel="label" optionValue="value" class="w-full" />
                        </div>

                        <div class="field mb-0">
                            <label class="block font-medium mb-2 text-600">Budget Display</label>
                            <SelectButton v-model="prefs.budgetDisplay" :options="budgetDisplayOpts"
                                optionLabel="label" optionValue="value" />
                        </div>
                    </div>

                    <!-- Save -->
                    <div class="card">
                        <div class="flex gap-2">
                            <Button label="Save Preferences" icon="pi pi-check" class="flex-1"
                                :loading="saving"
                                style="background:#1976d2;border-color:#1976d2;"
                                @click="savePreferences" />
                            <Button label="Reset" icon="pi pi-refresh" severity="secondary" outlined
                                @click="resetPreferences" />
                        </div>
                        <p v-if="saved" class="text-center mt-3 mb-0 text-sm font-medium"
                            style="color:#2ecc71;">
                            <i class="pi pi-check-circle mr-1" />Preferences saved successfully
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const saving = ref(false);
const saved  = ref(false);

const prefs = ref({
    theme:        'light',
    language:     'en',
    dateFormat:   'DD/MM/YYYY',
    landingPage:  '/app/dashboard',
    rowsPerPage:  10,
    showProgress: true,
    compactView:  false,
    currency:     'KES',
    budgetDisplay:'billions',
    notifications: {
        project_updates: true,
        payment_alerts:  true,
        qa_issues:       true,
        system:          false,
        weekly_report:   true,
    },
});

const themeModes = [
    { label: 'Light',  value: 'light',  icon: 'pi pi-sun'    },
    { label: 'Dark',   value: 'dark',   icon: 'pi pi-moon'   },
    { label: 'System', value: 'system', icon: 'pi pi-desktop' },
];

const languageOptions = [
    { label: 'English (Kenya)', value: 'en' },
    { label: 'Swahili',         value: 'sw' },
];

const dateFormats = [
    { label: 'DD/MM/YYYY (31/01/2025)',  value: 'DD/MM/YYYY' },
    { label: 'MM/DD/YYYY (01/31/2025)',  value: 'MM/DD/YYYY' },
    { label: 'YYYY-MM-DD (2025-01-31)',  value: 'YYYY-MM-DD' },
];

const landingOptions = [
    { label: 'Dashboard',   value: '/app/dashboard'   },
    { label: 'Projects',    value: '/app/projects'    },
    { label: 'Finance',     value: '/app/finance/dashboard' },
    { label: 'Progress',    value: '/app/progress/progress-overview' },
];

const currencyOptions = [
    { label: 'KES — Kenyan Shilling', value: 'KES' },
    { label: 'USD — US Dollar',       value: 'USD' },
    { label: 'EUR — Euro',            value: 'EUR' },
];

const budgetDisplayOpts = [
    { label: 'Billions (6.5B)', value: 'billions' },
    { label: 'Millions (6,500M)', value: 'millions' },
    { label: 'Full (6,500,000,000)', value: 'full' },
];

const notificationSettings = [
    { key: 'project_updates', label: 'Project Updates',   description: 'Status changes and milestones',   icon: 'pi pi-briefcase', color: '#1976d2', bg: '#e8f0fe' },
    { key: 'payment_alerts',  label: 'Payment Alerts',    description: 'Approvals and overdue invoices',  icon: 'pi pi-dollar',    color: '#e6a817', bg: '#fef9e7' },
    { key: 'qa_issues',       label: 'QA Issues & NCRs',  description: 'New non-conformance reports',     icon: 'pi pi-exclamation-triangle', color: '#ef4444', bg: '#fde8e8' },
    { key: 'system',          label: 'System Alerts',     description: 'Maintenance and system messages', icon: 'pi pi-cog',       color: '#6b7280', bg: '#f3f4f6' },
    { key: 'weekly_report',   label: 'Weekly Summary',    description: 'Email digest every Monday',       icon: 'pi pi-envelope',  color: '#2ecc71', bg: '#e8fdf0' },
];

const defaults = JSON.parse(JSON.stringify(prefs.value));

async function savePreferences() {
    saving.value = true;
    await new Promise((r) => setTimeout(r, 700));
    localStorage.setItem('icmfs_prefs', JSON.stringify(prefs.value));
    saving.value = false;
    saved.value  = true;
    setTimeout(() => (saved.value = false), 3000);
}

function resetPreferences() {
    Object.assign(prefs.value, defaults);
}
</script>