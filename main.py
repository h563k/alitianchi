import os
import sys
import warnings
from src.task_process import data_save_and_scores_multiple, multiple_agent_score
from src.human import human_score

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
    ranges = [30, 210]
    model_names = ['glm', 'qwen', 'kimi', 'spark']
    model_names = ['glm', 'qwen']
    # data_save_and_scores_multiple('task2', model_names, ranges, False)
    # datas = multiple_agent_score('task2', model_names)
    human_score()
