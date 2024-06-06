<template>
    <Model></Model>
    <ProcessFlow :processes="processes"></ProcessFlow>
</template>

<script>
import Model from '@/components/Model.vue'
import ProcessFlow from '@/components/ProcessFlow.vue'

export default {
    components: {
        Model,
        ProcessFlow
    },
    beforeCreate() {
        this.processes = [
            {
                id: 'STEP1',
                title: 'Make X-Crawler',
                text: '製作爬取推文的爬蟲',
                files: ['']
            },
            {
                id: 'STEP2',
                title: 'Data Set',
                text: '從 Kaggle 蒐集和 Twitter 爬取到的推文作為資料集',
                files: ['']
            },
            {
                id: 'STEP3',
                title: 'Labeling',
                text: '利用 Huggingface 訓練好的兩個模型，幫資料集做 Label',
                files: [
                    'austinmw/distilbert-base-uncased-finetuned-tweets-a',
                    'cardiffnlp/twitter-roberta-base-sentiment-latest'
                ]
            },
            {
                id: 'STEP4',
                title: 'Fine-Tuning',
                text: '利用 Label 好的資料，Fine-Tunging BERT 作為最後的模型',
                files: ['CX330Blake/tweet-sentiment-analysis-for-tesla']
            },
            {
                id: 'STEP5',
                title: 'Final Data',
                text: '用最終模型將所有資料集分類並計算加權分數',
                files: ['']
            }
        ]
    }
}
</script>
