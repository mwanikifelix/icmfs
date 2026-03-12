
 <template>
  <section class="py-8">
    <div class="max-w-screen-xl mx-auto px-4">
      <div class="grid">
        <div class="col-12 md:col-6 flex flex-column justify-content-center">
          <h1 class="text-6xl font-bold text-900 mb-4">
            Integrated Construction Management & Financing System
          </h1>
          <p class="text-xl text-600 mb-5 line-height-3">
            Empowering Kenya's Affordable Housing Program with cutting-edge project management, 
            multi-region tracking, and seamless M-Pesa payment integration.
          </p>
          <div class="flex gap-3">
            <router-link to="/register">
              <Button label="Get Started" icon="pi pi-arrow-right" iconPos="right" size="large" />
            </router-link>
            <router-link to="/about">
              <Button label="Learn More" severity="secondary" outlined size="large" />
            </router-link>
          </div>
        </div>
        <div class="col-12 md:col-6">
          <div class="surface-card p-4 border-round shadow-2">
            <img 
              src="https://via.placeholder.com/600x400/1976D2/FFFFFF?text=ICMFS+Dashboard" 
              alt="ICMFS Dashboard" 
              class="w-full border-round" 
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import Button from 'primevue/button'
</script>
