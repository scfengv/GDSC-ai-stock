<template>
    <Model></Model>
    <!-- <ModelFlowChart /> -->
    <ProcessFlow :processes="processes"></ProcessFlow>
</template>

<script>
import Model from '@/components/Model.vue'
import ProcessFlow from '@/components/ProcessFlow.vue'
// import ModelFlowChart from '@/components/ModelFlowChart.vue'

export default {
    components: {
        Model,
        ProcessFlow
        // ModelFlowChart
    },
    beforeCreate() {
        this.processes = [
            // {
            //     id: 'STEP1',
            //     title: '',
            //     text: 'PDF to .txt, clean, spilt, output .json\nsplit to paragraphs\nsummary using "facebook/bart-large-cnn"',
            //     files: [
            //         '1_pdf_split.py',
            //         '2_Paragraphs.py',
            //         '3_summary.py',
            //         '4_merge_json.py',
            //         '5_json_to_csv.py'
            //     ]
            // },
            {
                id: 'STEP1',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: [
                    '1_pdf_split.py',
                    'https://github.com/scfengv/GDSC-ai-stock/tree/Earningscall/Data/split'
                ]
            },
            {
                id: 'STEP2',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: [
                    '2_Paragraphs.py',
                    'https://github.com/scfengv/GDSC-ai-stock/tree/Earningscall/Data/Paragraphs'
                ]
            },
            {
                id: 'STEP3',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: [
                    '3_summary.py',
                    'https://github.com/scfengv/GDSC-ai-stock/tree/Earningscall/Data/summary'
                ]
            },
            {
                id: 'STEP4',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: [
                    '4_merge_json.py',
                    'https://github.com/scfengv/GDSC-ai-stock/tree/Earningscall/Data/merge'
                ]
            },
            {
                id: 'STEP5',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: ['5_json_to_csv.py']
            },
            {
                id: 'STEP6',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: [
                    '6_sentiment.ipynb',
                    'https://github.com/scfengv/GDSC-ai-stock/tree/Earningscall/Data/sentiment'
                ]
            },
            {
                id: 'STEP7',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: ['7_merge.ipynb']
            },
            {
                id: 'STEP8',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: [
                    '8_compare.ipynb',
                    'https://github.com/scfengv/GDSC-ai-stock/tree/Earningscall/Data/compare'
                ]
            },
            {
                id: 'STEP9',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: ['9_label.py']
            },
            {
                id: 'STEP10',
                title: '',
                text: '這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述這是描述',
                files: [
                    '10_finetune.ipynb',
                    'https://github.com/scfengv/GDSC-ai-stock/tree/Earningscall/Data/Dataset'
                ]
            }
        ]
    }
}
</script>
