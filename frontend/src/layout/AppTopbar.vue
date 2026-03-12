<!-- <script setup>
import { useLayout } from '@/layout/composables/layout';
import AppConfigurator from './AppConfigurator.vue';

const { toggleMenu, toggleDarkMode, isDarkTheme } = useLayout();
</script>

<template>
    <div class="layout-topbar">
        <div class="layout-topbar-logo-container">
            <button class="layout-menu-button layout-topbar-action" @click="toggleMenu">
                <i class="pi pi-bars"></i>
            </button>
           
                            <router-link
                    to="/"
                    class="layout-topbar-logo"
                    style="display:flex; align-items:center; gap:10px;"
                >
                    <img
                        src="/src/assets/media/logo.png"
                        alt="ICMFS Logo"
                        style="height:60px; width:auto;"
                    />

                    <span style="white-space:nowrap;margin-left: 50%;font-size: larger;">
                        INTEGRATED CONSTRUCTION MANAGEMENT AND FINANCIAL SYSTEM
                    </span>
                </router-link>
           
        </div>

        <div class="layout-topbar-actions">
            <div class="layout-config-menu">
                <button type="button" class="layout-topbar-action" @click="toggleDarkMode">
                    <i :class="['pi', { 'pi-moon': isDarkTheme, 'pi-sun': !isDarkTheme }]"></i>
                </button>
                <div class="relative">
                    <button
                        v-styleclass="{ selector: '@next', enterFromClass: 'hidden', enterActiveClass: 'p-anchored-overlay-enter-active', leaveToClass: 'hidden', leaveActiveClass: 'p-anchored-overlay-leave-active', hideOnOutsideClick: true }"
                        type="button"
                        class="layout-topbar-action layout-topbar-action-highlight"
                    >
                        <i class="pi pi-palette"></i>
                    </button>
                    <AppConfigurator />
                </div>
            </div>

            <button
                class="layout-topbar-menu-button layout-topbar-action"
                v-styleclass="{ selector: '@next', enterFromClass: 'hidden', enterActiveClass: 'p-anchored-overlay-enter-active', leaveToClass: 'hidden', leaveActiveClass: 'p-anchored-overlay-leave-active', hideOnOutsideClick: true }"
            >
                <i class="pi pi-ellipsis-v"></i>
            </button>

            <div class="layout-topbar-menu hidden lg:block">
                <div class="layout-topbar-menu-content">
                    <button type="button" class="layout-topbar-action">
                        <i class="pi pi-calendar"></i>
                        <span>Calendar</span>
                    </button>
                    <button type="button" class="layout-topbar-action">
                        <i class="pi pi-inbox"></i>
                        <span>Messages</span>
                    </button>
                    <button type="button" class="layout-topbar-action">
                        <i class="pi pi-user"></i>
                        <span>Profile</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
 -->


<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useLayout } from '@/layout/composables/layout';
import { authService } from '@/service/authService';
import AppConfigurator from './AppConfigurator.vue';

const { toggleMenu, toggleDarkMode, isDarkTheme } = useLayout();
const router = useRouter();

// ── Reactive user data ────────────────────────────────────────
const user = computed(() => authService.getUser());

const displayName = computed(() => authService.getDisplayName());

const userInitials = computed(() =>
  displayName.value
    .split(' ')
    .map((n) => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
);

const userRole = computed(() =>
  authService
    .getRole()
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase()) || 'User'
);

const userEmail = computed(() => user.value?.email || '');

// ── Profile dropdown ──────────────────────────────────────────
const profileMenu = ref();

const profileMenuItems = ref([
  {
    label: 'Account',
    items: [
      {
        label: 'My Profile',
        icon: 'pi pi-user-edit',
        command: () => router.push('/app/account/profile'),
      },
      {
        label: 'Security',
        icon: 'pi pi-lock',
        command: () => router.push('/app/account/security'),
      },
      {
        label: 'Preferences',
        icon: 'pi pi-sliders-h',
        command: () => router.push('/app/account/preferences'),
      },
    ],
  },
  { separator: true },
  {
    label: 'Sign Out',
    icon: 'pi pi-sign-out',
    command: () => logout(),
  },
]);

function toggleProfileMenu(event) {
  profileMenu.value.toggle(event);
}

function logout() {
  authService.logout();
  router.push('/login');
}
</script>

<template>
  <div class="layout-topbar">

    <!-- ── Logo area ── -->
    <div class="layout-topbar-logo-container">
      <button class="layout-menu-button layout-topbar-action" @click="toggleMenu">
        <i class="pi pi-bars"></i>
      </button>
      <router-link
        to="/app/dashboard"
        class="layout-topbar-logo"
        style="display: flex; align-items: center; gap: 10px"
      >
        <img src="/src/assets/media/logo.png" alt="ICMFS Logo" style="height: 60px; width: auto" />
        <span style="white-space: nowrap; margin-left: 50%; font-size: larger">
          INTEGRATED CONSTRUCTION MANAGEMENT AND FINANCIAL SYSTEM
        </span>
      </router-link>
    </div>

    <!-- ── Right actions ── -->
    <div class="layout-topbar-actions">
      <div class="layout-config-menu">

        <!-- Dark mode -->
        <button type="button" class="layout-topbar-action" @click="toggleDarkMode">
          <i :class="['pi', { 'pi-moon': isDarkTheme, 'pi-sun': !isDarkTheme }]"></i>
        </button>

        <!-- Theme picker -->
        <div class="relative">
          <button
            v-styleclass="{
              selector: '@next',
              enterFromClass: 'hidden',
              enterActiveClass: 'p-anchored-overlay-enter-active',
              leaveToClass: 'hidden',
              leaveActiveClass: 'p-anchored-overlay-leave-active',
              hideOnOutsideClick: true
            }"
            type="button"
            class="layout-topbar-action layout-topbar-action-highlight"
          >
            <i class="pi pi-palette"></i>
          </button>
          <AppConfigurator />
        </div>
      </div>

      <!-- Mobile overflow -->
      <button
        class="layout-topbar-menu-button layout-topbar-action"
        v-styleclass="{
          selector: '@next',
          enterFromClass: 'hidden',
          enterActiveClass: 'p-anchored-overlay-enter-active',
          leaveToClass: 'hidden',
          leaveActiveClass: 'p-anchored-overlay-leave-active',
          hideOnOutsideClick: true
        }"
      >
        <i class="pi pi-ellipsis-v"></i>
      </button>

      <div class="layout-topbar-menu hidden lg:block">
        <div class="layout-topbar-menu-content">

          <!-- Calendar -->
          <button type="button" class="layout-topbar-action">
            <i class="pi pi-calendar"></i>
            <span>Calendar</span>
          </button>

          <!-- Messages -->
          <button type="button" class="layout-topbar-action">
            <i class="pi pi-inbox"></i>
            <span>Messages</span>
          </button>

          <!-- ── Profile button ── -->
          <button
            type="button"
            class="layout-topbar-action"
            style="gap: 0.5rem; padding: 0.4rem 0.75rem;"
            @click="toggleProfileMenu"
            aria-haspopup="true"
            aria-controls="profile-menu"
          >
            <!-- Avatar circle with initials -->
            <span
              class="flex align-items-center justify-content-center border-circle font-bold text-sm flex-shrink-0"
              style="width: 2rem; height: 2rem; background: #1976d2; color: #ffffff;"
            >
              {{ userInitials }}
            </span>

            <!-- Name + role (hidden on mobile) -->
            <span class="hidden md:flex flex-column align-items-start" style="line-height: 1.3;">
              <span
                class="font-semibold text-sm"
                style="max-width: 130px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
              >
                {{ displayName }}
              </span>
              <span class="text-xs text-500">{{ userRole }}</span>
            </span>

            <i class="pi pi-angle-down text-xs text-500"></i>
          </button>

        </div>
      </div>
    </div>
  </div>

  <!-- ── Profile dropdown panel ── -->
  <Menu id="profile-menu" ref="profileMenu" :model="profileMenuItems" popup>

    <!-- User info header -->
    <template #start>
      <div
        class="px-3 pt-3 pb-2 flex align-items-center gap-3"
        style="border-bottom: 1px solid var(--surface-border); min-width: 230px;"
      >
        <!-- Big initials avatar -->
        <span
          class="flex align-items-center justify-content-center border-circle font-bold flex-shrink-0"
          style="width: 3rem; height: 3rem; background: #1976d2; color: #fff; font-size: 1.1rem;"
        >
          {{ userInitials }}
        </span>

        <div style="overflow: hidden; flex: 1;">
          <div
            class="font-bold text-900 text-sm"
            style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
          >
            {{ displayName }}
          </div>
          <div
            class="text-400 text-xs mt-1"
            style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
          >
            {{ userEmail }}
          </div>
          <div class="mt-2">
            <Tag
              :value="userRole"
              style="background: #0d2347; color: #e6a817; font-size: 0.6rem; padding: 0.15rem 0.5rem;"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- Custom item template — Sign Out gets red color -->
    <template #item="{ item, props }">
      <a
        v-bind="props.action"
        class="flex align-items-center gap-2"
        :style="item.label === 'Sign Out' ? 'color: #ef4444;' : ''"
      >
        <i
          :class="item.icon"
          :style="item.label === 'Sign Out' ? 'color: #ef4444;' : ''"
        />
        <span>{{ item.label }}</span>
      </a>
    </template>

  </Menu>
</template>