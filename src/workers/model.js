import { expose } from 'comlink'
// importScripts('https://unpkg.com/comlink/dist/umd/comlink.js');

const fetchData = async (model, text) => {
    // https://api-inference.huggingface.co/models/YC9Ztesla_news_title_sentiment_analysis
    // https://api-inference.huggingface.co/models/weip9012/tesla_earningscall_sentiment_analysis
    const response = await fetch(
        `https://api-inference.huggingface.co/models/${model}`,
        {
            headers: { Authorization: 'Bearer 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' },
            method: 'POST',
            body: JSON.stringify(text)
        }
    )
    const result = await response.json()
    return result
}

expose({ fetchData })