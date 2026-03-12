<template>
  <div class="min-h-screen flex align-items-center justify-content-center surface-ground">
    <div class="text-center">
      <h1 class="text-6xl font-bold mb-4 text-primary">ICMFS</h1>
      <p class="text-xl text-600 mb-4">Integrated Construction Management & Financing System</p> 
      <router-link >
         <Button label="Get Started" icon="pi pi-arrow-right" iconPos="right" size="large" /> 
      </router-link>
    </div>


   <div class="min-h-screen surface-ground">
   <PublicNavbar /> 
    <Login/> 
    <!--  <HeroWidget />  -->
   <!--  <StatsWidget /> -->
   <!--  <FeaturesWidget />
     <RegionsWidget /> 
     <CTAWidget />
     <FooterWidget /> 
     <TopbarWidget/> 
     <PricingWidget/>  -->

 <!-- <HighlightsWidget />  -->
  </div>
  </div>
</template>

<script setup>
import PublicNavbar from '@/components/landing/PublicNavbar.vue'; 
import Login from '@/views/public/Login.vue'; 
/* import HeroWidget from '@/components/landing/HeroWidget.vue' 
import StatsWidget from '@/components/landing/StatsWidget.vue' 
import FeaturesWidget from '@/components/landing/FeaturesWidget.vue' 
 import RegionsWidget from '@/components/landing/RegionsWidget.vue' 
import CTAWidget from '@/components/landing/CTAWidget.vue' 
 import FooterWidget from '@/components/landing/FooterWidget.vue' 
 import TopbarWidget from '@/components/landing/TopbarWidget.vue' 
 import PricingWidget from '@/components/landing/PricingWidget.vue' 
 import HighlightsWidget from '@/components/landing/HighlightsWidget.vue' 
 import Button from 'primev ue/button'; */
</script>
