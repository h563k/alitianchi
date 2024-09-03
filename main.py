import os
import sys
import warnings
from src.task_process import data_save_and_scores_multiple, multiple_agent_process

warnings.filterwarnings('ignore')
sys.path.append(os.path.abspath(__file__))

if __name__ == '__main__':
    """支持模型
    付费api
    qwen2-72b-instruct,qwen-max,qwen-turbo,qwen-72b-chat
    本地api
    huatuo-34b-8bit,huatuo-7bit
    反向代理api
    qwen,kimi,glm,spark
    """
    # count = 200
    model_names = ['glm', 'qwen']
    # data_save_and_scores_multiple('task2', model_names, count, False)
    print(multiple_agent_process('task2', model_names))
