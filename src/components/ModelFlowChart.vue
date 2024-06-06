<template>
    <div ref="chart" class="chart"></div>
</template>

<script>
import * as d3 from 'd3'
import IconCode from './icons/IconCode.vue'
import { h, createApp } from 'vue'

export default {
    name: 'ModelFlowChart',
    components: {
        IconCode
    },
    mounted() {
        this.drawChart()
    },
    methods: {
        drawChart() {
            const data = [
                { id: 'start', label: 'Start', x: 100, y: 200, href: '#start' },
                { id: 'a', label: 'A', x: 300, y: 100, href: '#a' },
                { id: 'b', label: 'B', x: 300, y: 300, href: '#b' },
                { id: 'c', label: 'C', x: 500, y: 200, href: '#c' },
                { id: 'end', label: 'End', x: 700, y: 200, href: '#end' }
            ]

            const links = [
                { source: 'start', target: 'a' },
                { source: 'start', target: 'b' },
                { source: 'a', target: 'c' },
                { source: 'b', target: 'c' },
                { source: 'c', target: 'end' }
            ]

            const svg = d3
                .select(this.$refs.chart)
                .append('svg')
                .attr('width', 800)
                .attr('height', 400)

            const link = svg
                .append('g')
                .selectAll('path')
                .data(links)
                .enter()
                .append('path')
                .attr('stroke-width', 2)
                .attr('stroke', '#999')
                .attr('fill', 'none')
                .attr('d', (d) => {
                    const source = data.find((node) => node.id === d.source)
                    const target = data.find((node) => node.id === d.target)
                    return `M${source.x},${source.y} H${source.x + 100} V${target.y} H${target.x}`
                })

            const node = svg
                .append('g')
                .selectAll('a')
                .data(data)
                .enter()
                .append('a')
                .attr('xlink:href', (d) => d.href)

            node.append('g')
                .attr('x', (d) => d.x)
                .attr('y', (d) => d.y)
                .each(function (d, i) {
                    const n = d3.select(this).node()

                    const iconCodeApp = createApp({
                        render() {
                            return h(IconCode)
                        }
                    })

                    iconCodeApp.mount(n)
                })

            node.append('rect')
                .attr('width', 100)
                .attr('height', 50)
                .attr('rx', 8)
                .attr('ry', 8)
                .attr('fill', '#fff')
                .attr('stroke', '#000')
                .attr('x', (d) => d.x - 50)
                .attr('y', (d) => d.y - 25)

            node.append('text')
                .attr('dy', '.35em')
                .attr('text-anchor', 'middle')
                .attr('x', (d) => d.x)
                .attr('y', (d) => d.y)
                .text((d) => d.label)
        }
    }
}
</script>

<style scoped>
.chart {
    width: 100%;
    height: 100%;
}
</style>
