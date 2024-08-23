import os
import sys
import warnings
from src.rag_sample import answer_process

warnings.filterwarnings('ignore')
sys.path.append(os.path.abspath(__file__))

if __name__ == '__main__':
    task_list = ['task_1', 'task_2', 'task_3', 'task_4', 'task_5']
    answer_process(task_list)
