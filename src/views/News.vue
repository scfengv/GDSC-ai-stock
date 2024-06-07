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
                title: 'Raw Data',
                text: '原始 Tesla 資料集，來自華爾街日報等四個新聞網站。',
                sources: [
                    {
                        name: 'CNBC',
                        url: 'https://github.com/scfengv/GDSC-ai-stock/blob/news/tweets_raw/TSLA_20100629_20210602_CNBC_t_Tesla_en.csv'
                    },
                    {
                        name: 'Reuters',
                        url: 'https://github.com/scfengv/GDSC-ai-stock/blob/news/tweets_raw/TSLA_20100629_20210602_Reuters_t_Tesla_en.csv'
                    },
                    {
                        name: 'Wall Street Journal',
                        url: 'https://github.com/scfengv/GDSC-ai-stock/blob/news/tweets_raw/TSLA_20100629_20210602_WSJ_t_Tesla_en.csv'
                    },
                    {
                        name: 'Bloomberg',
                        url: 'https://github.com/scfengv/GDSC-ai-stock/blob/news/tweets_raw/TSLA_20100629_20210602_business_t_Tesla_en.csv'
                    }
                ]
            },
            {
                id: 'STEP2',
                title: 'Preprocessing',
                text: '利用 Distilroberta 和 Deberta 這兩個 Hugging Face 上的 Pretrained model 做資料預處理，對 Raw data 進行標記。',
                sources: [
                    {
                        name: 'Pretrained model 1',
                        url: 'https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis'
                    },
                    {
                        name: 'Pretrained model 2',
                        url: 'https://huggingface.co/mrm8488/deberta-v3-ft-financial-news-sentiment-analysis'
                    }
                ]
            },
            {
                id: 'STEP3',
                title: 'Labelled Data',
                text: '對 Raw data 進行正向、負向、中立情感標記的結果。',
                sources: [
                    // {
                    //     name: 'Tsla_dataset.csv',
                    //     url: 'https://github.com/scfengv/GDSC-ai-stock/blob/news/tsla_dataset.csv'
                    // }
                ]
            },
            {
                id: 'STEP4',
                title: 'Finetune BERT',
                text: '利用 03 標記資料 Finetune BERT 得到我們預使用的模型。',
                sources: [
                    {
                        name: 'YC9Z/tesla_news_title_sentiment_analysis',
                        url: 'https://huggingface.co/YC9Z/tesla_news_title_sentiment_analysis'
                    }
                ]
            },
            {
                id: 'STEP5',
                title: 'Predicted Data',
                text: '最後利用我們 Finetuned 後的模型對 Raw data 做最終預測。',
                sources: [
                    // {
                    //     name: 'Tsla_news_sentiment_score.csv',
                    //     url: ''
                    // }
                ]
            }
        ]
    }
}
</script>
