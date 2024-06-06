<template>
    <main class="mx-2" ref="main">
        <div class="relative">
            <ul class="grid grid-cols-1 gap-y-2 py-2 pl-9">
                <li v-for="(data, index) in dataFile1" :key="data.name" class="z-10">
                    <router-link
                        :to="{
                            path: `${index}`
                        }"
                        class="px-2 block h-9 overflow-hidden text-ellipsis whitespace-nowrap place-content-center border-2 border-blue-300 rounded-lg"
                    >
                        {{ data.name }}
                    </router-link>
                </li>
            </ul>

            <svg class="w-full h-full absolute top-0 left-0">
                <path :d="path" class="stroke-blue-400 fill-none"></path>
            </svg>
        </div>

        <svg class="h-5 w-full">
            <path d="M4 0 V20" class="stroke-blue-400 fill-none"></path>
        </svg>

        <div class="relative">
            <ul class="grid grid-cols-1 gap-y-2 py-2 px-9">
                <li v-for="(process, index) in processes1" :key="process.name" class="z-10">
                    <router-link
                        :to="{
                            path: `${index}`
                        }"
                        class="px-2 block h-9 overflow-hidden text-ellipsis whitespace-nowrap place-content-center border-2 border-blue-300 rounded-lg"
                    >
                        {{ process.name }}
                    </router-link>
                </li>
            </ul>

            <svg class="w-full h-full absolute top-0 left-0">
                <path :d="[path2, path22]" class="stroke-blue-400 fill-none"></path>
            </svg>
        </div>

        <svg class="h-5 w-full">
            <path d="M300 0 V999" class="stroke-blue-400 fill-none"></path>
        </svg>

        <div class="relative">
            <ul class="grid grid-cols-1 gap-y-2 py-2 px-9">
                <li v-for="(data, index) in dataFile2" :key="data.name" class="z-10">
                    <router-link
                        :to="{
                            path: `${index}`
                        }"
                        class="px-2 block h-9 overflow-hidden text-ellipsis whitespace-nowrap place-content-center border-2 border-blue-300 rounded-lg"
                    >
                        {{ data.name }}
                    </router-link>
                </li>
            </ul>

            <svg class="w-full h-full absolute top-0 left-0">
                <path :d="[filePath2, filePath22]" class="stroke-blue-400 fill-none"></path>
            </svg>
        </div>

        <svg class="h-5 w-full">
            <path d="M4 0 V999" class="stroke-blue-400 fill-none"></path>
        </svg>

        <div class="relative">
            <ul class="grid grid-cols-1 gap-y-2 py-2 px-9">
                <li v-for="(process, index) in processes2" :key="process.name" class="z-10">
                    <router-link
                        :to="{
                            path: `${index}`
                        }"
                        class="px-2 block h-9 overflow-hidden text-ellipsis whitespace-nowrap place-content-center border-2 border-blue-300 rounded-lg"
                    >
                        {{ process.name }}
                    </router-link>
                </li>
            </ul>

            <svg class="w-full h-full absolute top-0 left-0">
                <path :d="[processPath2, processPath22]" class="stroke-blue-400 fill-none"></path>
            </svg>
        </div>

        <svg class="h-5 w-full">
            <path d="M284 0 V999 M300 0 V999" class="stroke-blue-400 fill-none"></path>
        </svg>

        <div class="relative">
            <ul class="grid grid-cols-1 gap-y-2 py-2 px-9">
                <li v-for="(data, index) in dataFile3" :key="data.name" class="z-10">
                    <router-link
                        :to="{
                            path: `${index}`
                        }"
                        class="px-2 block h-9 overflow-hidden text-ellipsis whitespace-nowrap place-content-center border-2 border-blue-300 rounded-lg"
                    >
                        {{ data.name }}
                    </router-link>
                </li>
            </ul>

            <svg class="w-full h-full absolute top-0 left-0">
                <path :d="filePath3" class="stroke-blue-400 fill-none"></path>
            </svg>
        </div>
    </main>
</template>

<script>
export default {
    data() {
        return {
            inputValue: '',
            modelOutput: ''
        }
    },
    created() {
        this.dataFile1 = [
            {
                name: 'TSLA_20100629_20210602_business_t_Tesla_en.csv'
            },
            {
                name: 'TSLA_20100629_20210602_CNBC_t_Tesla_en.csv'
            },
            {
                name: 'TSLA_20100629_20210602_Reuters_t_Tesla_en.csv'
            },
            {
                name: 'TSLA_20100629_20210602_WSJ_t_Tesla_en.csv'
            }
        ]
        this.processes1 = [
            {
                name: 'pro_data.ipynb'
            }
        ]
        this.dataFile2 = [
            {
                name: 'tsla_merged.csv'
            }
        ]
        this.processes2 = [
            {
                name: 'data_preprocess_1.ipynb'
            },
            {
                name: 'data_preprocess_2.ipynb'
            }
        ]
        this.dataFile3 = [
            {
                name: 'tsla_merged_res.csv'
            },
            {
                name: 'tsla_merged_res_2.csv'
            }
        ]
    },
    mounted() {
        console.log(this.$refs['main'])
    },
    computed: {
        path() {
            const mx = 36
            return [
                `M${mx} 26 H${mx - 8}`,
                `M${mx} 70 H${mx - 8}`,
                `M${mx} 114 H${mx - 8}`,
                `M${mx} 158 H${mx - 8}`,
                `M${mx - 8} 26 Q${mx - 16} 26, ${mx - 16} 34`,
                `M${mx - 8} 70 Q${mx - 16} 70, ${mx - 16} 78`,
                `M${mx - 8} 114 Q${mx - 16} 114, ${mx - 16} 106`,
                `M${mx - 8} 158 Q${mx - 16} 158, ${mx - 16} 150`,
                `M${mx - 16} 34 V150`,
                `M${mx - 16} 92 H${mx - 24}`,
                `M${mx - 24} 92 Q${mx - 32} 92, ${mx - 32} 100`,
                `M${mx - 32} 100 V1580`
            ]
        },
        path2() {
            const mx = 36
            return [
                `M${mx} 26 H${mx - 24}`,
                `M${mx - 24} 26 Q${mx - 32} 26, ${mx - 32} 18`,
                `M${mx - 32} 18 V0`
            ]
        },
        path22() {
            const mx = 268
            return [
                `M${mx} 26 H${mx + 24}`,
                `M${mx + 24} 26 Q${mx + 32} 26, ${mx + 32} 34`,
                `M${mx + 32} 34 V999`
            ]
        },
        path3() {
            const mx = 268
            return [
                `M${mx} 26 H${mx + 24}`,
                `M${mx + 24} 26 Q${mx + 32} 26, ${mx + 32} 34`,
                `M${mx + 32} 34 V999`
            ]
        },
        filePath2() {
            const mx = 36
            return [
                `M${mx} 26 H${mx - 24}`,
                `M${mx - 24} 26 Q${mx - 32} 26, ${mx - 32} 34`,
                `M${mx - 32} 34 V999`
            ]
        },
        filePath22() {
            const mx = 268
            return [
                `M${mx} 26 H${mx + 24}`,
                `M${mx + 24} 26 Q${mx + 32} 26, ${mx + 32} 18`,
                `M${mx + 32} 18 V0`
            ]
        },
        processPath2() {
            const mx = 36
            return [
                `M${mx} 26 H${mx - 8}`,
                `M${mx} 70 H${mx - 8}`,
                `M${mx - 8} 26 Q${mx - 16} 26, ${mx - 16} 34`,
                `M${mx - 8} 70 Q${mx - 16} 70, ${mx - 16} 62`,
                `M${mx - 16} 34 V62`,
                `M${mx - 16} 48 H${mx - 24}`,
                `M${mx - 24} 48 Q${mx - 32} 48, ${mx - 32} 40`,
                `M${mx - 32} 40 V0`

                // `M${mx - 8} 26 Q${mx - 16} 26, ${mx - 16} 18`,
                // `M${mx - 24} 70 Q${mx - 32} 70, ${mx - 32} 62`,
                // `M${mx - 24} 70 H${mx - 8}`,
                // `M${mx - 16} 18 V0`,
                // `M${mx - 32} 62 V0`
            ]
        },
        processPath22() {
            const mx = 268
            return [
                `M${mx} 26 H${mx + 24}`,
                `M${mx} 70 H${mx + 8}`,
                `M${mx + 24} 26 Q${mx + 32} 26, ${mx + 32} 34`,
                `M${mx + 8} 70 Q${mx + 16} 70, ${mx + 16} 78`,
                `M${mx + 32} 34 V999`,
                `M${mx + 16} 78 V999`
            ]
        },
        filePath3() {
            const mx = 268
            return [
                `M${mx} 26 H${mx + 8}`,
                `M${mx} 70 H${mx + 24}`,
                `M${mx + 8} 26 Q${mx + 16} 26, ${mx + 16} 18`,
                `M${mx + 24} 70 Q${mx + 32} 70, ${mx + 32} 62`,
                `M${mx + 16} 18 V0`,
                `M${mx + 32} 62 V0`
            ]
        }
    },
    methods: {
        async query() {
            console.log(`請求已發出，傳送的訊息為：${this.inputValue}`)
            const API_TOKEN = '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'
            const response = await fetch(
                'https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-zh-en',
                {
                    headers: { Authorization: `Bearer ${API_TOKEN}` },
                    method: 'POST',
                    body: JSON.stringify({ inputs: this.inputValue })
                }
            )

            this.modelOutput = (await response.json())[0].translation_text
            console.log(this.modelOutput)
        }
    }
}
</script>
