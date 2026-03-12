<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center justify-content-center border-round-lg"
                    style="width:3rem;height:3rem;background:#e6a817;">
                    <i class="pi pi-lock text-xl" style="color:#0d2347;" />
                </div>
                <div>
                    <h4 class="mt-0 mb-1" style="color:#fff;">Security Settings</h4>
                    <span class="text-sm" style="color:#b3c8e8;">Manage your password, two-factor authentication and active sessions</span>
                </div>
            </div>

            <div class="grid">

                <!-- ── LEFT ── -->
                <div class="col-12 lg:col-6">

                    <!-- Change Password -->
                    <div class="card mb-3">
                        <h5 class="mt-0 mb-4 flex align-items-center gap-2" style="color:#0d2347;">
                            <i class="pi pi-key" style="color:#1976d2;" /> Change Password
                        </h5>

                        <Message v-if="passwordError" severity="error" class="mb-3" :closable="false">
                            {{ passwordError }}
                        </Message>
                        <Message v-if="passwordSuccess" severity="success" class="mb-3" :closable="false">
                            Password updated successfully.
                        </Message>

                        <div class="field mb-3">
                            <label class="block font-medium mb-2 text-600">Current Password</label>
                            <Password v-model="passwordForm.current" class="w-full" :feedback="false"
                                toggleMask fluid placeholder="Enter current password" />
                        </div>
                        <div class="field mb-3">
                            <label class="block font-medium mb-2 text-600">New Password</label>
                            <Password v-model="passwordForm.new" class="w-full" toggleMask fluid
                                placeholder="Min 8 characters" />
                        </div>
                        <div class="field mb-4">
                            <label class="block font-medium mb-2 text-600">Confirm New Password</label>
                            <Password v-model="passwordForm.confirm" class="w-full" :feedback="false"
                                toggleMask fluid placeholder="Repeat new password" />
                        </div>

                        <!-- Password strength indicator -->
                        <div v-if="passwordForm.new" class="mb-4">
                            <div class="flex justify-content-between mb-1">
                                <span class="text-sm text-600">Password Strength</span>
                                <span class="text-sm font-medium" :style="{ color: strengthColor }">
                                    {{ strengthLabel }}
                                </span>
                            </div>
                            <ProgressBar :value="strengthScore" :showValue="false"
                                style="height:6px;"
                                :pt="{ value: { style: { background: strengthColor } } }" />
                        </div>

                        <Button label="Update Password" icon="pi pi-check"
                            :loading="savingPassword"
                            class="w-full"
                            style="background:#1976d2;border-color:#1976d2;"
                            @click="changePassword" />
                    </div>

                    <!-- Two-Factor Auth -->
                    <div class="card">
                        <h5 class="mt-0 mb-4 flex align-items-center gap-2" style="color:#0d2347;">
                            <i class="pi pi-mobile" style="color:#2ecc71;" /> Two-Factor Authentication
                        </h5>

                        <div class="flex align-items-start gap-3 p-3 border-round-lg mb-4"
                            style="background:var(--surface-50);">
                            <div class="flex align-items-center justify-content-center border-round flex-shrink-0 mt-1"
                                style="width:2.5rem;height:2.5rem;background:#fef9e7;">
                                <i class="pi pi-exclamation-triangle" style="color:#e6a817;" />
                            </div>
                            <div>
                                <div class="font-semibold text-900 mb-1">2FA is currently disabled</div>
                                <div class="text-500 text-sm">Enable two-factor authentication to add an extra layer of security to your account.</div>
                            </div>
                        </div>

                        <div class="flex flex-column gap-3 mb-4">
                            <div v-for="method in twoFAMethods" :key="method.label"
                                class="flex align-items-center gap-3 p-3 border-round-lg border-1 cursor-pointer transition-all transition-duration-200"
                                :style="selected2FA === method.value
                                    ? 'border-color:#1976d2;background:#e8f0fe;'
                                    : 'border-color:var(--surface-border);'"
                                @click="selected2FA = method.value">
                                <RadioButton v-model="selected2FA" :value="method.value" />
                                <div class="flex align-items-center justify-content-center border-round"
                                    style="width:2rem;height:2rem;" :style="{ background: method.bg }">
                                    <i :class="method.icon" :style="{ color: method.color }" />
                                </div>
                                <div>
                                    <div class="font-medium text-900 text-sm">{{ method.label }}</div>
                                    <div class="text-500 text-xs">{{ method.description }}</div>
                                </div>
                            </div>
                        </div>

                        <Button label="Enable 2FA" icon="pi pi-shield"
                            style="background:#2ecc71;border-color:#2ecc71;color:#0d2347;font-weight:700;"
                            class="w-full" />
                    </div>
                </div>

                <!-- ── RIGHT ── -->
                <div class="col-12 lg:col-6">

                    <!-- Active Sessions -->
                    <div class="card mb-3">
                        <div class="flex justify-content-between align-items-center mb-4">
                            <h5 class="mt-0 mb-0 flex align-items-center gap-2" style="color:#0d2347;">
                                <i class="pi pi-desktop" style="color:#e6a817;" /> Active Sessions
                            </h5>
                            <Button label="Revoke All" icon="pi pi-times" severity="danger"
                                size="small" text @click="confirmRevokeAll = true" />
                        </div>

                        <div class="flex flex-column gap-3">
                            <div v-for="session in sessions" :key="session.id"
                                class="flex align-items-center gap-3 p-3 border-round-lg border-1"
                                :style="session.current
                                    ? 'border-color:#2ecc71;background:#e8fdf0;'
                                    : 'border-color:var(--surface-border);'">
                                <div class="flex align-items-center justify-content-center border-round flex-shrink-0"
                                    style="width:2.5rem;height:2.5rem;background:var(--surface-100);">
                                    <i :class="session.icon" class="text-lg text-600" />
                                </div>
                                <div class="flex-1">
                                    <div class="font-semibold text-900 text-sm flex align-items-center gap-2">
                                        {{ session.device }}
                                        <Tag v-if="session.current" value="Current" severity="success" style="font-size:0.65rem;" />
                                    </div>
                                    <div class="text-500 text-xs mt-1">
                                        {{ session.location }} · {{ session.lastActive }}
                                    </div>
                                    <div class="text-400 text-xs">{{ session.browser }}</div>
                                </div>
                                <Button v-if="!session.current" icon="pi pi-times" text rounded
                                    size="small" severity="danger"
                                    v-tooltip.top="'Revoke session'"
                                    @click="revokeSession(session.id)" />
                            </div>
                        </div>
                    </div>

                    <!-- Login History -->
                    <div class="card mb-3">
                        <h5 class="mt-0 mb-4 flex align-items-center gap-2" style="color:#0d2347;">
                            <i class="pi pi-history" style="color:#1976d2;" /> Recent Login History
                        </h5>

                        <DataTable :value="loginHistory" :rows="5" :paginator="loginHistory.length > 5"
                            size="small" stripedRows>
                            <Column header="Date/Time">
                                <template #body="{ data }">
                                    <span class="text-sm">{{ data.time }}</span>
                                </template>
                            </Column>
                            <Column header="Location">
                                <template #body="{ data }">
                                    <span class="text-sm text-600">{{ data.location }}</span>
                                </template>
                            </Column>
                            <Column header="Status">
                                <template #body="{ data }">
                                    <Tag :value="data.status"
                                        :severity="data.status === 'Success' ? 'success' : 'danger'"
                                        style="font-size:0.7rem;" />
                                </template>
                            </Column>
                        </DataTable>
                    </div>

                    <!-- Security checklist -->
                    <div class="card">
                        <h5 class="mt-0 mb-4 flex align-items-center gap-2" style="color:#0d2347;">
                            <i class="pi pi-shield" style="color:#2ecc71;" /> Security Score
                        </h5>

                        <div class="flex align-items-center gap-3 mb-4">
                            <div class="text-4xl font-bold" style="color:#1976d2;">60%</div>
                            <div class="flex-1">
                                <ProgressBar :value="60" :showValue="false" style="height:10px;"
                                    :pt="{ value: { style: { background: '#1976d2' } } }" />
                                <div class="text-500 text-xs mt-1">Moderate — enable 2FA to improve</div>
                            </div>
                        </div>

                        <div class="flex flex-column gap-2">
                            <div v-for="check in securityChecks" :key="check.label"
                                class="flex align-items-center gap-2">
                                <i :class="check.done ? 'pi pi-check-circle' : 'pi pi-times-circle'"
                                    :style="{ color: check.done ? '#2ecc71' : '#ef4444' }" />
                                <span class="text-sm" :class="check.done ? 'text-900' : 'text-500'">
                                    {{ check.label }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Revoke all dialog -->
        <Dialog v-model:visible="confirmRevokeAll" header="Revoke All Sessions"
            :modal="true" :style="{ width: '380px' }">
            <p class="text-600">This will sign you out of all other devices. You will remain logged in here.</p>
            <template #footer>
                <Button label="Cancel" text @click="confirmRevokeAll = false" />
                <Button label="Revoke All" severity="danger" @click="confirmRevokeAll = false" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// ── Password form ─────────────────────────────────────────────
const passwordForm    = ref({ current: '', new: '', confirm: '' });
const passwordError   = ref('');
const passwordSuccess = ref(false);
const savingPassword  = ref(false);

const strengthScore = computed(() => {
    const p = passwordForm.value.new;
    if (!p) return 0;
    let score = 0;
    if (p.length >= 8)  score += 25;
    if (p.length >= 12) score += 15;
    if (/[A-Z]/.test(p)) score += 20;
    if (/[0-9]/.test(p)) score += 20;
    if (/[^A-Za-z0-9]/.test(p)) score += 20;
    return Math.min(score, 100);
});

const strengthLabel = computed(() => {
    const s = strengthScore.value;
    if (s >= 80) return 'Strong';
    if (s >= 50) return 'Moderate';
    if (s >= 25) return 'Weak';
    return 'Too Short';
});

const strengthColor = computed(() => {
    const s = strengthScore.value;
    if (s >= 80) return '#2ecc71';
    if (s >= 50) return '#e6a817';
    return '#ef4444';
});

async function changePassword() {
    passwordError.value   = '';
    passwordSuccess.value = false;

    if (!passwordForm.value.current) { passwordError.value = 'Please enter your current password.'; return; }
    if (passwordForm.value.new.length < 8) { passwordError.value = 'New password must be at least 8 characters.'; return; }
    if (passwordForm.value.new !== passwordForm.value.confirm) { passwordError.value = 'New passwords do not match.'; return; }

    savingPassword.value = true;
    await new Promise((r) => setTimeout(r, 900));
    // TODO: api.post('/api/accounts/change-password/', { old_password: passwordForm.value.current, new_password: passwordForm.value.new })
    savingPassword.value  = false;
    passwordSuccess.value = true;
    passwordForm.value    = { current: '', new: '', confirm: '' };
    setTimeout(() => (passwordSuccess.value = false), 4000);
}

// ── 2FA ───────────────────────────────────────────────────────
const selected2FA = ref('app');
const twoFAMethods = [
    { label: 'Authenticator App', value: 'app',  description: 'Google Authenticator or Authy', icon: 'pi pi-qrcode',  color: '#1976d2', bg: '#e8f0fe' },
    { label: 'SMS / Phone',       value: 'sms',  description: 'Receive a code via SMS',         icon: 'pi pi-mobile',  color: '#2ecc71', bg: '#e8fdf0' },
    { label: 'Email OTP',         value: 'email',description: 'One-time code to your email',    icon: 'pi pi-envelope',color: '#e6a817', bg: '#fef9e7' },
];

// ── Sessions ──────────────────────────────────────────────────
const confirmRevokeAll = ref(false);
const sessions = ref([
    { id: 1, device: 'Kali Linux — Chrome', icon: 'pi pi-desktop',  browser: 'Chrome 121', location: 'Mombasa, KE', lastActive: 'Now',         current: true  },
    { id: 2, device: 'Android — Mobile',    icon: 'pi pi-mobile',   browser: 'Chrome Mobile', location: 'Nairobi, KE', lastActive: '2 hours ago', current: false },
    { id: 3, device: 'Windows — Edge',      icon: 'pi pi-microsoft',browser: 'Edge 120',   location: 'Nairobi, KE', lastActive: 'Yesterday',    current: false },
]);

function revokeSession(id) {
    sessions.value = sessions.value.filter((s) => s.id !== id);
}

// ── Login history ─────────────────────────────────────────────
const loginHistory = ref([
    { time: 'Today, 08:32',       location: 'Mombasa, KE',  status: 'Success' },
    { time: 'Yesterday, 17:15',   location: 'Mombasa, KE',  status: 'Success' },
    { time: 'Yesterday, 09:04',   location: 'Nairobi, KE',  status: 'Success' },
    { time: '16 Feb, 14:22',      location: 'Unknown',       status: 'Failed'  },
    { time: '15 Feb, 08:47',      location: 'Mombasa, KE',  status: 'Success' },
]);

// ── Security checklist ────────────────────────────────────────
const securityChecks = [
    { label: 'Strong password set',          done: true  },
    { label: 'Email address verified',        done: true  },
    { label: 'Two-factor authentication',     done: false },
    { label: 'Recovery email configured',     done: false },
    { label: 'No suspicious login activity',  done: true  },
];
</script>