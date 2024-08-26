import os
import sys
import warnings
from src.functional import rouge_l
from src.promot import data_process, data_save_and_scores
from src.functional import find_common_elements

warnings.filterwarnings('ignore')
sys.path.append(os.path.abspath(__file__))

if __name__ == '__main__':
    count = 1
    data_save_and_scores('taks_3', 'qwen2-72b-instruct', count)
    # data_save_and_scores('taks_3', 'qwen-max', count)
    # data_save_and_scores('taks_3', 'qwen-turbo', count)
    # data_save_and_scores('taks_3', 'qwen-72b-chat', count)
