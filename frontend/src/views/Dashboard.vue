

<script setup>
import BestSellingWidget from '@/components/dashboard/BestSellingWidget.vue';
import NotificationsWidget from '@/components/dashboard/NotificationsWidget.vue';
import RecentSalesWidget from '@/views/projects/ProjectList.vue';
import RevenueStreamWidget from '@/components/dashboard/RevenueStreamWidget.vue';
import StatsWidget from '@/components/dashboard/StatsWidget.vue';
import ProjectList from '@/views/projects/ProjectList.vue';
</script>

<template>
    <div class="grid grid-cols-1 gap-1">
        <StatsWidget />

        <div class="col-span-12 xl:col-span-6">
            <ProjectList />
            <BestSellingWidget />z
        </div>
        <div class="col-span-12 xl:col-span-6">
            <RevenueStreamWidget />
            <NotificationsWidget />
        </div>
    </div>
</template>
