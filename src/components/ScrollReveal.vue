<template>
    <!-- <div ref="revealElement" :class="{ visible: isVisible }" class="reveal-container"> -->
    <div
        ref="revealElement"
        class="opacity-0"
        :class="{ 'animate__animated animate__fadeIn': isVisible }"
    >
        <slot></slot>
    </div>
</template>

<script>
export default {
    data() {
        return {
            isVisible: false
        }
    },
    mounted() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    this.isVisible = true
                    observer.unobserve(this.$refs.revealElement)
                }
            })
        })
        observer.observe(this.$refs.revealElement)
    }
}
</script>
