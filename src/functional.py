from typing import List
from rouge import Rouge
from transformers import BertTokenizer


def custom_tokenizer(text):
    # 加载预训练的tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    # 使用tokenizer进行分词
    tokens = tokenizer.tokenize(text)

    # 输出分词结果
    return tokens


def rouge_l(reference_summary: str, predicted_summary: str):
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


def find_common_elements(arr1: List, arr2: List) -> float:
    arr1.sort()
    arr2.sort()
    index1, index2 = 0, 0
    common_elements = []

    while index1 < len(arr1) and index2 < len(arr2):
        if arr1[index1] == arr2[index2]:
            common_elements.append(arr1[index1])
            index1 += 1
            index2 += 1
        elif arr1[index1] < arr2[index2]:
            index1 += 1
        else:
            index2 += 1

    return len(common_elements)/(len(arr1)+len(arr2)-len(common_elements))


if __name__ == '__main__':
    # text1 = "今天天气真好！"
    # text2 = "今天天气真不好！"
    # rouge_l(text1, text2)
    # 示例数组
    arr1 = ['A', 'S', 'D', 'W', 'H', 'Q']
    arr2 = ['S', 'A', 'G', 'B', 'Q', 'L', 'D']

    # # 调用函数
    common = find_common_elements(arr1, arr2)

    print(common)
