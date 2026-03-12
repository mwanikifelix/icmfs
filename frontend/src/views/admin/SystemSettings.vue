<template>
    <div class="grid">
        <div class="col-12">

            <!-- Header -->
            <div class="border-round-xl mb-4 p-4 flex align-items-center justify-content-between flex-wrap gap-3"
                style="background:linear-gradient(135deg,#0d2347 0%,#1976d2 100%);">
                <div class="flex align-items-center gap-3">
                    <div class="flex align-items-center justify-content-center border-round-lg"
                        style="width:3rem;height:3rem;background:#e6a817;">
                        <i class="pi pi-cog text-xl" style="color:#0d2347;" />
                    </div>
                    <div>
                        <h4 class="mt-0 mb-1" style="color:#fff;">System Settings</h4>
                        <span class="text-sm" style="color:#b3c8e8;">Platform configuration, integrations and maintenance</span>
                    </div>
                </div>
                <div class="flex align-items-center gap-2">
                    <div class="flex align-items-center gap-2 px-3 py-1 border-round"
                        style="background:rgba(46,204,113,0.2);">
                        <span class="text-xs font-medium" style="color:#2ecc71;">● All systems operational</span>
                    </div>
                </div>
            </div>

            <div class="grid">
                <!-- Left nav -->
                <div class="col-12 lg:col-3">
                    <div class="card p-0">
                        <div v-for="section in sections" :key="section.key"
                            class="flex align-items-center gap-3 px-4 py-3 cursor-pointer transition-all transition-duration-200"
                            :style="activeSection === section.key
                                ? 'background:#e8f0fe;border-left:3px solid #1976d2;'
                                : 'border-left:3px solid transparent;'"
                            @click="activeSection = section.key">
                            <div class="flex align-items-center justify-content-center border-round"
                                style="width:2rem;height:2rem;" :style="{ background: section.bg }">
                                <i :class="section.icon" style="font-size:0.8rem;" :style="{ color: section.color }" />
                            </div>
                            <span class="text-sm font-medium"
                                :style="activeSection === section.key ? 'color:#1976d2;' : 'color:var(--text-color);'">
                                {{ section.label }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Right panel -->
                <div class="col-12 lg:col-9">

                    <!-- ── General ── -->
                    <div v-show="activeSection === 'general'" class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-building mr-2" style="color:#1976d2;" />General Settings
                        </h5>
                        <div class="grid">
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">System Name</label>
                                <InputText v-model="general.systemName" class="w-full" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Organisation</label>
                                <InputText v-model="general.org" class="w-full" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Country</label>
                                <Dropdown v-model="general.country" :options="['Kenya','Uganda','Tanzania']" class="w-full" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Currency</label>
                                <Dropdown v-model="general.currency" :options="['KES','USD','EUR']" class="w-full" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Financial Year Start</label>
                                <Dropdown v-model="general.fyStart" :options="['January','April','July','October']" class="w-full" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">System Timezone</label>
                                <Dropdown v-model="general.timezone" :options="['Africa/Nairobi','UTC']" class="w-full" />
                            </div>
                            <div class="col-12 field">
                                <label class="block font-medium mb-2 text-600">System Description</label>
                                <Textarea v-model="general.description" rows="2" class="w-full" autoResize />
                            </div>
                        </div>
                        <Button label="Save General Settings" icon="pi pi-check" :loading="saving"
                            style="background:#1976d2;border-color:#1976d2;" @click="save" />
                    </div>

                    <!-- ── Security ── -->
                    <div v-show="activeSection === 'security'" class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-lock mr-2" style="color:#1976d2;" />Security Settings
                        </h5>
                        <div class="flex flex-column gap-4">
                            <div v-for="s in securitySettings" :key="s.key"
                                class="flex align-items-center justify-content-between p-3 border-round-lg"
                                style="background:var(--surface-50);">
                                <div>
                                    <div class="font-medium text-900">{{ s.label }}</div>
                                    <div class="text-500 text-sm">{{ s.description }}</div>
                                </div>
                                <ToggleSwitch v-model="security[s.key]" />
                            </div>

                            <Divider />

                            <div class="grid">
                                <div class="col-12 md:col-6 field">
                                    <label class="block font-medium mb-2 text-600">Session Timeout (minutes)</label>
                                    <InputNumber v-model="security.sessionTimeout" class="w-full" :min="5" :max="480" />
                                </div>
                                <div class="col-12 md:col-6 field">
                                    <label class="block font-medium mb-2 text-600">Max Login Attempts</label>
                                    <InputNumber v-model="security.maxLoginAttempts" class="w-full" :min="3" :max="10" />
                                </div>
                                <div class="col-12 md:col-6 field">
                                    <label class="block font-medium mb-2 text-600">Password Min Length</label>
                                    <InputNumber v-model="security.passwordMinLength" class="w-full" :min="6" :max="32" />
                                </div>
                                <div class="col-12 md:col-6 field">
                                    <label class="block font-medium mb-2 text-600">Password Expiry (days)</label>
                                    <InputNumber v-model="security.passwordExpiry" class="w-full" :min="30" :max="365" />
                                </div>
                            </div>
                        </div>
                        <Button label="Save Security Settings" icon="pi pi-check" :loading="saving"
                            style="background:#1976d2;border-color:#1976d2;" @click="save" />
                    </div>

                    <!-- ── Email ── -->
                    <div v-show="activeSection === 'email'" class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-envelope mr-2" style="color:#e6a817;" />Email / SMTP Settings
                        </h5>
                        <div class="grid">
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">SMTP Host</label>
                                <InputText v-model="email.host" class="w-full" placeholder="smtp.gmail.com" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Port</label>
                                <InputNumber v-model="email.port" class="w-full" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Username</label>
                                <InputText v-model="email.username" class="w-full" placeholder="no-reply@icmfs.co.ke" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Password</label>
                                <Password v-model="email.password" class="w-full" fluid toggleMask :feedback="false" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">From Name</label>
                                <InputText v-model="email.fromName" class="w-full" placeholder="ICMFS System" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Encryption</label>
                                <Dropdown v-model="email.encryption" :options="['TLS','SSL','None']" class="w-full" />
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <Button label="Save SMTP" icon="pi pi-check" :loading="saving"
                                style="background:#1976d2;border-color:#1976d2;" @click="save" />
                            <Button label="Send Test Email" icon="pi pi-send" outlined severity="secondary" />
                        </div>
                    </div>

                    <!-- ── Backup ── -->
                    <div v-show="activeSection === 'backup'" class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-database mr-2" style="color:#2ecc71;" />Backup & Recovery
                        </h5>

                        <!-- Last backup status -->
                        <div class="flex align-items-center gap-3 p-3 border-round-lg mb-4"
                            style="background:#e8fdf0;border:1px solid #2ecc71;">
                            <i class="pi pi-check-circle text-2xl" style="color:#2ecc71;" />
                            <div>
                                <div class="font-semibold text-900">Last backup successful</div>
                                <div class="text-500 text-sm">Today at 02:00 AM · 2.34 GB · PostgreSQL snapshot</div>
                            </div>
                        </div>

                        <div class="grid mb-4">
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Backup Frequency</label>
                                <Dropdown v-model="backup.frequency" :options="['Daily','Weekly','Monthly']" class="w-full" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Backup Time</label>
                                <InputText v-model="backup.time" class="w-full" placeholder="02:00" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Retention (days)</label>
                                <InputNumber v-model="backup.retention" class="w-full" :min="7" :max="365" />
                            </div>
                            <div class="col-12 md:col-6 field">
                                <label class="block font-medium mb-2 text-600">Storage Location</label>
                                <Dropdown v-model="backup.storage" :options="['Local','AWS S3','Google Cloud','Azure']" class="w-full" />
                            </div>
                        </div>

                        <div class="flex gap-2">
                            <Button label="Save Backup Settings" icon="pi pi-check" :loading="saving"
                                style="background:#1976d2;border-color:#1976d2;" @click="save" />
                            <Button label="Backup Now" icon="pi pi-cloud-upload" outlined
                                style="border-color:#2ecc71;color:#2ecc71;" />
                        </div>
                    </div>

                    <!-- ── Integrations ── -->
                    <div v-show="activeSection === 'integrations'" class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-link mr-2" style="color:#a855f7;" />Integrations
                        </h5>
                        <div class="flex flex-column gap-3">
                            <div v-for="intg in integrations" :key="intg.id"
                                class="flex align-items-center justify-content-between p-3 border-round-lg border-1"
                                style="border-color:var(--surface-border);">
                                <div class="flex align-items-center gap-3">
                                    <div class="flex align-items-center justify-content-center border-round"
                                        style="width:2.5rem;height:2.5rem;" :style="{ background: intg.bg }">
                                        <i :class="intg.icon" :style="{ color: intg.color }" />
                                    </div>
                                    <div>
                                        <div class="font-semibold text-900">{{ intg.name }}</div>
                                        <div class="text-500 text-sm">{{ intg.description }}</div>
                                    </div>
                                </div>
                                <div class="flex align-items-center gap-3">
                                    <Tag :value="intg.status"
                                        :severity="intg.status==='Connected'?'success':intg.status==='Partial'?'warn':'secondary'" />
                                    <Button :label="intg.status==='Connected'?'Configure':'Connect'"
                                        :icon="intg.status==='Connected'?'pi pi-cog':'pi pi-plug'"
                                        :outlined="intg.status==='Connected'"
                                        size="small"
                                        :style="intg.status!=='Connected'?'background:#1976d2;border-color:#1976d2;':''" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- ── Maintenance ── -->
                    <div v-show="activeSection === 'maintenance'" class="card">
                        <h5 class="mt-0 mb-4" style="color:#0d2347;">
                            <i class="pi pi-wrench mr-2" style="color:#e6a817;" />Maintenance
                        </h5>

                        <Message severity="warn" class="mb-4" :closable="false">
                            These actions affect all users. Only execute during off-hours.
                        </Message>

                        <div class="flex flex-column gap-3">
                            <div v-for="action in maintenanceActions" :key="action.label"
                                class="flex align-items-center justify-content-between p-3 border-round-lg"
                                style="background:var(--surface-50);">
                                <div>
                                    <div class="font-medium text-900">{{ action.label }}</div>
                                    <div class="text-500 text-sm">{{ action.description }}</div>
                                </div>
                                <Button :label="action.btn" :icon="action.icon"
                                    :severity="action.danger ? 'danger' : 'secondary'"
                                    :outlined="!action.danger"
                                    size="small" />
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

const activeSection = ref('general');
const saving        = ref(false);

const sections = [
    { key:'general',      label:'General',      icon:'pi pi-building',   color:'#1976d2', bg:'#e8f0fe' },
    { key:'security',     label:'Security',     icon:'pi pi-lock',       color:'#ef4444', bg:'#fde8e8' },
    { key:'email',        label:'Email / SMTP', icon:'pi pi-envelope',   color:'#e6a817', bg:'#fef9e7' },
    { key:'backup',       label:'Backup',       icon:'pi pi-database',   color:'#2ecc71', bg:'#e8fdf0' },
    { key:'integrations', label:'Integrations', icon:'pi pi-link',       color:'#a855f7', bg:'#f3e8ff' },
    { key:'maintenance',  label:'Maintenance',  icon:'pi pi-wrench',     color:'#6b7280', bg:'#f3f4f6' },
];

const general = ref({
    systemName:  'ICMFS',
    org:         'Technical University of Mombasa',
    country:     'Kenya',
    currency:    'KES',
    fyStart:     'January',
    timezone:    'Africa/Nairobi',
    description: 'Integrated Construction Management and Financial System',
});

const security = ref({
    enforce2FA:          false,
    passwordComplexity:  true,
    auditLogging:        true,
    ipWhitelist:         false,
    singleSession:       false,
    sessionTimeout:      60,
    maxLoginAttempts:    5,
    passwordMinLength:   8,
    passwordExpiry:      90,
});

const securitySettings = [
    { key:'enforce2FA',         label:'Enforce 2FA',              description:'Require all users to set up two-factor auth'   },
    { key:'passwordComplexity', label:'Password Complexity',      description:'Require uppercase, numbers and symbols'        },
    { key:'auditLogging',       label:'Full Audit Logging',       description:'Log all system actions to the audit trail'     },
    { key:'ipWhitelist',        label:'IP Whitelist',             description:'Restrict access to approved IP ranges only'    },
    { key:'singleSession',      label:'Single Active Session',    description:'Prevent simultaneous logins per user'          },
];

const email = ref({
    host: 'smtp.gmail.com', port: 587, username: '', password: '',
    fromName: 'ICMFS System', encryption: 'TLS',
});

const backup = ref({ frequency:'Daily', time:'02:00', retention:30, storage:'Local' });

const integrations = [
    { id:1, name:'M-Pesa Daraja API',  description:'Safaricom payment gateway', icon:'pi pi-mobile',  color:'#2ecc71', bg:'#e8fdf0', status:'Connected' },
    { id:2, name:'SMS Gateway',         description:'Bulk SMS via AfricasTalking',icon:'pi pi-comment', color:'#1976d2', bg:'#e8f0fe', status:'Connected' },
    { id:3, name:'Google Maps',         description:'Site location and mapping',  icon:'pi pi-map',     color:'#ef4444', bg:'#fde8e8', status:'Partial'   },
    { id:4, name:'KRA iTax',            description:'Tax compliance integration', icon:'pi pi-file',    color:'#e6a817', bg:'#fef9e7', status:'Disconnected'},
    { id:5, name:'AWS S3',              description:'Document and media storage', icon:'pi pi-cloud',   color:'#a855f7', bg:'#f3e8ff', status:'Disconnected'},
];

const maintenanceActions = [
    { label:'Clear System Cache',    description:'Force-clear Redis and session cache',    btn:'Clear Cache',    icon:'pi pi-sync',    danger:false },
    { label:'Rebuild Search Index',  description:'Re-index all projects and documents',    btn:'Rebuild Index',  icon:'pi pi-search',  danger:false },
    { label:'Run Database Vacuum',   description:'Reclaim PostgreSQL storage space',       btn:'Run Vacuum',     icon:'pi pi-database',danger:false },
    { label:'Enable Maintenance Mode', description:'Show maintenance page to all users', btn:'Enable',         icon:'pi pi-wrench',  danger:true  },
    { label:'Purge Old Audit Logs',  description:'Delete audit logs older than 2 years',  btn:'Purge Logs',     icon:'pi pi-trash',   danger:true  },
];

async function save() {
    saving.value = true;
    await new Promise(r => setTimeout(r, 800));
    saving.value = false;
}
</script>