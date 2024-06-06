<template>
    <section class="w-[94vw] mx-auto">
        <h1 class="text-2xl font-bold mb-2 pl-2">
            {{ model.modelGroup }}
        </h1>
        <div class="bg-[#4a4a4a] rounded-lg px-4 py-2 mb-2">
            <h2 class="text-white">Model Name: {{ model.modelName }}</h2>
            <p class="text-white">Model Founder: {{ model.modelFounder }}</p>
        </div>

        <div class="grid grid-rows-[repeat(2,auto)] gap-y-4 bg-[#4a4a4a] rounded-lg p-4 mb-2">
            <textarea
                ref="textInference"
                class="border border-white/5 bg-[#5b5b5b] px-3 py-2 min-h-24 rounded-lg text-white"
            ></textarea>
            <button @click="modelInference" class="bg-[#1387f8] rounded-lg h-10 text-white">
                Compute
            </button>
        </div>

        <div class="bg-[#4a4a4a] rounded-lg px-4 py-2 mb-2">
            <div
                v-for="(output, index) in model.output"
                :key="output.label"
                class="grid grid-cols-2"
            >
                <div class="w-full grid grid-cols-2 justify-between col-span-2">
                    <div class="text-white">{{ output.label }}</div>
                    <CountTo
                        :start-val="0"
                        :end-val="output.score"
                        :duration="1000"
                        :decimals="3"
                        class="text-right text-white"
                    ></CountTo>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import 'animate.css'
import * as Comlink from 'comlink'
import { CountTo } from 'vue3-count-to'

export default {
    components: {
        CountTo
    },
    data() {
        return {
            model: {
                modelName: '',
                modelFounder: '',
                output: null,

                modelGroup: ''
            }
        }
    },
    created() {},
    mounted() {
        const isNews = this.$route.path.includes('/News')
        const isTweets = this.$route.path.includes('/Tweets')
        const isEarningCall = this.$route.path.includes('/EarningCall')

        console.log('isNews:', isNews)
        console.log('isTweets:', isTweets)
        console.log('isEarningCall:', isEarningCall)

        if (isNews) {
            this.model.modelName = 'tesla_news_title_sentiment_analysis'
            this.model.modelFounder = 'YC9Z'

            this.model.modelGroup = 'News'
        } else if (isTweets) {
            // this.model.modelName = 'tweets-sentiment-analysis-for-tesla'
            // this.model.modelFounder = 'CX330Blake'

            this.model.modelName = 'tweet-sentiment-analysis-for-tesla'
            this.model.modelFounder = 'CX330Blake'

            this.model.modelGroup = 'Tweets'
        } else if (isEarningCall) {
            this.model.modelName = 'tesla_earningscall_sentiment_analysis'
            this.model.modelFounder = 'weip9012'

            this.model.modelGroup = 'Earnings Call'
        }
    },
    computed: {},
    methods: {
        async modelInference() {
            const modelFullName = `${this.model.modelFounder}/${this.model.modelName}`
            const sendMessage = this.$refs['textInference'].value
            console.log(sendMessage)

            const worker = new Worker(new URL('@/workers/model.js', import.meta.url), {
                type: 'module'
            })
            const workerProxy = Comlink.wrap(worker)

            try {
                const data = await workerProxy.fetchData(modelFullName, sendMessage)

                this.model.output = data.flat().map((data) => {
                    data.score = Math.round(data.score * 1000) / 1000
                    data.score = parseFloat(data.score.toFixed(3))
                    return data
                })
            } catch (error) {
                console.error(`Error fetching data: ${error}`)
            }
        }
    }
}
</script>
