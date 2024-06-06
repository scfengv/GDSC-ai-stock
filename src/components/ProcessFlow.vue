<template>
    <section class="mx-auto w-[84vw]">
        <h2 class="text-white font-bold text-xl my-3">Production Process</h2>
        <ScrollReveal
            v-for="(process, step) in processes"
            :key="process.id"
            class="bg-[#4a4a4a] rounded-lg min-h-20 flex mb-2 p-4"
        >
            <div class="grid grid-rows-2 place-items-center w-10 h-10 mr-5">
                <div class="text-lg text-white">STEP</div>
                <div class="text-lg text-white">{{ (step + 1).toString().padStart(2, '0') }}</div>
            </div>
            <div class="flex-grow grid grid-cols-2 gap-x-5">
                <div>
                    <div class="text-white">{{ process.title }}</div>
                    <div class="text-[#d0d0d0]">{{ process.text }}</div>
                </div>
                <div class="flex flex-col">
                    <div
                        v-for="file in process.files"
                        :key="file"
                        class="border border-solid border-white text-[#d0d0d0] text-sm rounded-lg px-4 py-2 overflow-hidden whitespace-nowrap text-ellipsis mb-2 last-of-type:mb-0"
                    >
                        {{ file }}
                    </div>
                </div>
            </div>
        </ScrollReveal>
    </section>
</template>

<script>
import ScrollReveal from '@/components/ScrollReveal.vue'

export default {
    props: {
        processes: {
            type: Object,
            required: false
        }
    },
    components: {
        ScrollReveal
    },
    mounted() {
        console.log(this.processes)
    },
    data() {
        return {
            // processes: [
            //     {
            //         id: '1',
            //         title: 'data',
            //         text: 'a',
            //         files: ['1.json', '2.json', '3.json']
            //     },
            //     {
            //         id: '2',
            //         title: 'function',
            //         text: 'border',
            //         files: ['4.json', '5.json']
            //     }
            // ]
        }
    }
}
</script>
