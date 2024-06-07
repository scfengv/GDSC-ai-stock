<template>
    <section class="mx-auto w-[94vw]">
        <h2 class="text-white font-bold text-xl my-3">Production Process</h2>
        <ScrollReveal
            v-for="(process, step) in processes"
            :key="process.id"
            class="bg-[#4a4a4a] rounded-lg flex mb-2 p-4"
        >
            <div class="grid grid-rows-2 place-items-center w-10 h-10 mr-5">
                <div class="text-lg text-white">STEP</div>
                <div class="text-lg text-white">{{ (step + 1).toString().padStart(2, '0') }}</div>
            </div>
            <div class="flex-grow md:grid md:grid-cols-2 md:gap-x-5">
                <div>
                    <div class="text-white font-bold text-lg pb-3">
                        {{ process.title }}
                    </div>
                    <div class="text-[#d0d0d0]">{{ process.text }}</div>
                </div>
                <div class="grid grid-rows-[repeat(auto-fill,1fr)] mt-3 gap-y-2">
                    <a
                        v-for="source in process.sources"
                        :key="source.id"
                        :href="source.url"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="border border-solid border-white text-[#d0d0d0] text-sm rounded-lg px-4 h-9 grid items-center"
                    >
                        <span class="overflow-hidden whitespace-nowrap text-ellipsis">
                            {{ source.name }}
                        </span>
                    </a>
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
    }
}
</script>
