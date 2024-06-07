<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="mx-2 mb-16">
        <TimePriceChart></TimePriceChart>
    </div>
    <div class="mx-2 mb-4">
        <ScrollReveal v-for="intro in introes" :key="intro.id">
            <section class="rounded-lg px-4 py-2 mb-6">
                <div class="flex mb-3">
                    <component
                        :is="intro.icon"
                        class="fill-[#fefefe] mr-4 place-self-center h-7 w-7"
                    ></component>
                    <h2 class="text-center text-xl font-bold text-white">{{ intro.title }}</h2>
                </div>
                <p class="text-[#d0d0d0]">{{ intro.content }}</p>
            </section>
        </ScrollReveal>
    </div>
</template>

<script>
import TimePriceChart from '@/components/TimePriceChart.vue'
import IconNews from '@/components/icons/IconNews.vue'
import IconTweets from '@/components/icons/IconTweets.vue'
import IconEarningCall from '@/components/icons/IconEarningCall.vue'
import ScrollReveal from '@/components/ScrollReveal.vue'

export default {
    components: {
        TimePriceChart,
        IconNews,
        IconTweets,
        IconEarningCall,
        ScrollReveal
    },
    created() {
        this.introes = [
            {
                id: 'News',
                icon: 'IconNews',
                title: '新聞報導',
                content:
                    '我們彙整了多家權威新聞媒體的報導，包括最新的企業動態、重大事件、產品發布及市場策略等。這些報導由專業記者撰寫，提供了深入分析和全面視角，讓您能夠了解企業的發展趨勢和行業地位。'
            },
            {
                id: 'Tweets',
                icon: 'IconTweets',
                title: '推特評論',
                content:
                    '我們收集了來自推特上的即時評論，這些評論來自不同背景的用戶，涵蓋了對企業產品、服務以及市場動態的真實反饋。這些評論幫助我們呈現多元且真實的公眾意見。'
            },
            {
                id: 'EarningCall',
                icon: 'IconEarningCall',
                title: '企業財報',
                content:
                    '我們展示了企業的最新經濟財報，包括營收、利潤、支出等關鍵財務數據。我們提供透明且詳盡的財務資訊，讓您能夠深入了解企業的經營狀況和財務健康度，並為您的投資決策提供有力的數據支持。'
            }
        ]
    }
}
</script>
