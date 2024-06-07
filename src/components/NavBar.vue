<template>
    <nav
        class="fixed md:static top-0 left-0 mb-2 z-20 md:w-[100vw] md:border-b md:border-black/5 md:border-solid"
    >
        <button
            class="bg-[rgba(63,63,63,0.9)] rounded-lg h-12 w-12 grid place-items-center ml-3 mt-2 md:hidden"
            @click="toggleMenu"
        >
            <IconMenu></IconMenu>
        </button>

        <div
            class="md:static md:flex md:justify-center fixed z-20 top-0 left-0 h-screen md:h-auto md:translate-x-0 -translate-x-full transition-transform bg-[#2f2f2f] pl-3 pr-5"
            :class="{ 'translate-x-0': isMenuVisible }"
        >
            <button class="md:hidden h-12 w-12 grid place-items-center mt-2" @click="toggleMenu">
                <IconMenu></IconMenu>
            </button>
            <router-link
                v-for="link in links"
                :key="link.id"
                :to="{ path: link.path }"
                class="block px-5 py-3 font-semibold rounded-xl min-w-48 text-white md:text-center"
                :class="['hover:bg-[#5f5f5f]']"
            >
                {{ link.text }}
            </router-link>
        </div>
    </nav>
    <div
        v-show="isMenuVisible"
        @click="toggleMenu"
        class="absolute top-0 left-0 z-10 h-screen w-screen bg-[rgba(0,0,0,0.5)]"
    ></div>
</template>

<script>
import IconMenu from '@/components/icons/IconMenu.vue'

export default {
    components: {
        IconMenu
    },
    data() {
        return {
            isMenuVisible: false
        }
    },
    beforeCreate() {
        this.links = [
            {
                id: 'Home',
                path: '/',
                text: 'Home'
            },
            {
                id: 'EarningCall',
                path: '/EarningCall',
                text: 'EarningCall'
            },
            {
                id: 'News',
                path: '/News',
                text: 'News'
            },
            {
                id: 'Tweets',
                path: '/Tweets',
                text: 'Tweets'
            }
        ]
    },
    methods: {
        toggleMenu() {
            this.isMenuVisible = !this.isMenuVisible
        }
    }
}
</script>

<style scoped>
/* we will explain what these classes do next! */
.v-enter-active,
.v-leave-active {
    transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}
</style>
