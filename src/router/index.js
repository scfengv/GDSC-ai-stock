import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: () => import('../views/Home.vue')
        },
        {
            path: '/EarningCall',
            name: 'EarningCall',
            component: () => import('../views/EarningCall.vue')
        },
        {
            path: '/News',
            name: 'News',
            component: () => import('../views/News.vue')
        },
        {
            path: '/Tweets',
            name: 'Tweets',
            component: () => import('../views/Tweets.vue')
        },
    ]
})

export default router
