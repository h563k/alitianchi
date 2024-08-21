#!/usr/bin/env bash

home="/opt/project/alitianchi"
CONDA_PATH="/root/miniconda3"
ENV_NAME="fast_chat"


# 激活conda环境
. "${CONDA_PATH}/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"
cd "$home"
rm -rf logs/$current_time.log

# 参数src/llamafactory/hparams/model_args.py
# 使用date命令并格式化输出，精确到日期
full_path=$(python src/config.py --full_path True)
current_time=$(date +"%Y-%m-%d")
rm -rf logs/$current_time.log
CUDA_VISIBLE_DEVICES=0,1
export OPENAI_API_BASE=http://localhost:8000/v1
export OPENAI_API_KEY=EMPTY

nohup python -m scripts.fast_chat >"log/$current_time.log" 2>&1 &