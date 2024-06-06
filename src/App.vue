<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <!-- <ModelTest /> -->
    <div>
        <NavBar class="overflow-hidden text-white"> </NavBar>

        <router-view></router-view>
    </div>
</template>

<style>
body {
    @apply bg-[#3f3f3f];
}
</style>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
    components: {
        NavBar
    }
}
</script>
