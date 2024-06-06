<template>
    <div class="md:grid md:grid-cols-[3fr,1fr] md:gap-x-4">
        <div v-if="data.length" class="grid grid-cols-2 md:grid-rows-2 gap-x-4 md:gap-y-4 mb-4">
            <div class="bg-[#4a4a4a] rounded-lg grid place-items-center">
                <div class="py-2">
                    <!-- <div class="text-4xl">{{ getPredictPrice }}</div> -->
                    <CountTo
                        :start-val="0"
                        :end-val="getPredictPrice"
                        :duration="1000"
                        :decimals="2"
                        class="text-4xl text-white"
                    ></CountTo>
                    <div class="text-white">
                        <span>明日預測價格&nbsp;</span>
                    </div>
                </div>
            </div>
            <div class="bg-[#4a4a4a] rounded-lg grid place-items-center">
                <div class="py-2">
                    <!-- <div class="text-4xl">{{ getLastestPrice }}</div> -->
                    <CountTo
                        :start-val="0"
                        :end-val="getLastestPrice"
                        :duration="1000"
                        :decimals="2"
                        class="text-4xl text-white"
                    ></CountTo>
                    <div class="text-white">
                        <span>收市&nbsp;</span>
                        <span>{{ data[data.length - 1].date }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="bg-[#4a4a4a] rounded-lg">
            <div ref="chart" class="w-full h-[400px]"></div>
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3'
import { CountTo } from 'vue3-count-to'

export default {
    name: 'TimePriceChart',
    components: {
        CountTo
    },
    data() {
        return {
            data: []
        }
    },
    mounted() {
        const data = [
            { date: '2024-04-09', price: 176.8800048828125 },
            { date: '2024-04-10', price: 171.75999450683594 },
            { date: '2024-04-11', price: 174.60000610351562 },
            { date: '2024-04-12', price: 171.0500030517578 },
            { date: '2024-04-15', price: 161.47999572753906 },
            { date: '2024-04-16', price: 157.11000061035156 },
            { date: '2024-04-17', price: 155.4499969482422 },
            { date: '2024-04-18', price: 149.92999267578125 },
            { date: '2024-04-19', price: 147.0500030517578 },
            { date: '2024-04-22', price: 142.0500030517578 },
            { date: '2024-04-23', price: 144.67999267578125 },
            { date: '2024-04-24', price: 162.1300048828125 },
            { date: '2024-04-25', price: 170.17999267578125 },
            { date: '2024-04-26', price: 168.2899932861328 },
            { date: '2024-04-29', price: 194.0500030517578 },
            { date: '2024-04-30', price: 183.27999877929688 },
            { date: '2024-05-01', price: 179.99000549316406 },
            { date: '2024-05-02', price: 180.00999450683594 },
            { date: '2024-05-03', price: 181.19000244140625 },
            { date: '2024-05-06', price: 184.75999450683597 },
            { date: '2024-05-07', price: 177.80999755859375 },
            { date: '2024-05-08', price: 174.72000122070312 },
            { date: '2024-05-09', price: 171.97000122070312 },
            { date: '2024-05-10', price: 168.47000122070312 },
            { date: '2024-05-13', price: 171.88999938964844 },
            { date: '2024-05-14', price: 177.5500030517578 },
            { date: '2024-05-15', price: 173.99000549316406 },
            { date: '2024-05-16', price: 174.83999633789062 },
            { date: '2024-05-17', price: 177.4600067138672 },
            { date: '2024-05-20', price: 175.29190063476562 }
        ]

        const numberToShow = 30
        this.data = data.slice(-numberToShow).map((d) => {
            d.date = d.date.replace('2024-', '')
            return d
        })

        this.createChart()
        window.addEventListener('resize', this.createChart)
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.createChart)
    },
    computed: {
        getLastestPrice() {
            return parseFloat(this.data[this.data.length - 1].price.toFixed(2))
        },
        getPredictPrice() {
            return parseFloat(this.data[this.data.length - 1].price.toFixed(2))
        }
    },
    methods: {
        createChart() {
            const container = this.$refs.chart
            container.innerHTML = ''

            const margin = { top: 10, right: 20, bottom: 40, left: 35 }
            const width = container.clientWidth - margin.left - margin.right
            const height = container.clientHeight - margin.top - margin.bottom

            const svg = d3
                .select(container)
                .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform', `translate(${margin.left}, ${margin.top})`)

            const x = d3
                .scaleBand()
                .domain(this.data.map((d) => d.date))
                .range([0, width])
                .paddingInner(1)
                .paddingOuter(0)

            const minPrice = d3.min(this.data, (d) => d.price)
            const maxPrice = d3.max(this.data, (d) => d.price)
            const padding = (maxPrice - minPrice) * 0.2

            const y = d3
                .scaleLinear()
                .domain([minPrice - padding, maxPrice + padding])
                .range([height, 0])

            const line = d3
                .line()
                .x((d) => x(d.date))
                .y((d) => y(d.price))

            const xAxis = d3
                .axisBottom(x)
                // .ticks(this.data.length)
                // .ticks(7)
                .tickFormat((d, i) => {
                    // 只顯示 7 個刻度
                    const numTicks = 10
                    const everyNth = Math.ceil(this.data.length / numTicks)
                    return i % everyNth === 1 ? d : ''
                })
                .tickSize(0)
                .tickPadding(20)

            const yAxis = d3.axisLeft(y).tickSize(0).tickPadding(8)

            svg.append('g')
                .attr('transform', `translate(0, ${height})`)
                .call(xAxis)
                .selectAll('text')
                .style('fill', 'white')

            svg.append('g').call(yAxis).selectAll('text').style('fill', 'white')

            // svg.selectAll('.domain').remove()

            const gradient = svg
                .append('defs')
                .append('linearGradient')
                .attr('id', 'gradient')
                .attr('x1', '0%')
                .attr('y1', '0%')
                .attr('x2', '0%')
                .attr('y2', '100%')

            gradient
                .append('stop')
                .attr('offset', '0%')
                .attr('stop-color', 'limegreen')
                .attr('stop-opacity', 0.2)

            gradient
                .append('stop')
                .attr('offset', '100%')
                .attr('stop-color', 'limegreen')
                .attr('stop-opacity', 0)

            // 繪製線條和填充漸層
            svg.append('path')
                .datum(this.data)
                .attr('fill', 'none')
                .attr('stroke', 'limegreen')
                .attr('stroke-width', 2)
                .attr('d', line)

            svg.append('path')
                .datum(this.data)
                .attr('fill', 'url(#gradient)')
                .attr('stroke', 'none')
                .attr(
                    'd',
                    d3
                        .area()
                        .x((d) => x(d.date))
                        .y0(height)
                        .y1((d) => y(d.price))
                )
        }
    }
}
</script>
