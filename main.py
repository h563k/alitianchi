import os
import sys
import warnings
from src.task_process import data_save_and_scores

warnings.filterwarnings('ignore')
sys.path.append(os.path.abspath(__file__))

if __name__ == '__main__':
    count = 10
    data_save_and_scores('taks_3', 'qwen2-72b-instruct', count)
    # data_save_and_scores('taks_3', 'qwen-max', count)
    # data_save_and_scores('taks_3', 'qwen-turbo', count)
    # data_save_and_scores('taks_3', 'qwen-72b-chat', count)
    # data_save_and_scores('taks_3', 'huatuo-34b-8bit', count, False)
