<template>
    <Model></Model>
    <ProcessFlow :processes="processes"></ProcessFlow>
    <TradeProcess1></TradeProcess1>
</template>

<script>
import Model from '@/components/Model.vue'
import ProcessFlow from '@/components/ProcessFlow.vue'
import TradeProcess1 from '@/components/TradeProcess1.vue'

export default {
    components: {
        Model,
        ProcessFlow,
        TradeProcess1
    },
    beforeCreate() {
        this.processes = [
            {
                id: 'STEP1',
                title: 'Raw Data',
                text: '原始tesla資料集，來自華爾街日報等四個新聞網站',
                files: [
                    'TSLA_20100629_20210602_CNBC_t_Tesla_en.csv',
                    'TSLA_20100629_20210602_Reuters_t_Tesla_en.csv',
                    'TSLA_20100629_20210602_WSJ_t_Tesla_en.csv',
                    'TSLA_20100629_20210602_business_t_Tesla_en.csv'
                ]
            },
            {
                id: 'STEP2',
                title: 'Preprocessing',
                text: '利用Distilroberta和Deberta這兩個hugging face上的pretrained model做資料預處理，對raw data進行標記',
                files: [
                    'mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis',
                    'mrm8488/deberta-v3-ft-financial-news-sentiment-analysis'
                ]
            },
            {
                id: 'STEP3',
                title: 'Labelled Data',
                text: '對raw data進行正向、負向、中立情感標記的結果',
                files: ['Tsla_dataset.csv']
            },
            {
                id: 'STEP4',
                title: 'Finetune BERT',
                text: '利用03標記資料finetune BERT得到我們預使用的模型',
                files: ['YC9Z/tesla_news_title_sentiment_analysis']
            },
            {
                id: 'STEP5',
                title: 'Predicted Data',
                text: '最後利用我們finetuned後的模型對raw data做最終預測',
                files: ['Tsla_news_sentiment_score.csv']
            }
        ]
    }
}
</script>
