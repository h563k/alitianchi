from rouge import Rouge
from transformers import BertTokenizer


def custom_tokenizer(text):
    # 加载预训练的tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    # 使用tokenizer进行分词
    tokens = tokenizer.tokenize(text)

    # 输出分词结果
    return tokens


def rouge_l(reference_summary, predicted_summary):
    # 初始化ROUGE对象
    rouge = Rouge()
    reference_summary = custom_tokenizer(reference_summary)
    predicted_summary = custom_tokenizer(predicted_summary)
    # 将分词结果转换为字符串形式，每个词之间用空格隔开
    reference_summary = ' '.join(reference_summary)
    predicted_summary = ' '.join(predicted_summary)
    # 计算ROUGE分数
    scores = rouge.get_scores(predicted_summary, reference_summary, avg=True)

    # 输出ROUGE-L分数
    return scores


if __name__ == '__main__':
    text1 = "今天天气真好！"
    text2 = "今天天气真不好！"
    print(rouge_l(text1, text2))
