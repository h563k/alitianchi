#!/usr/bin/env bash

home="/opt/project/alitianchi"
CONDA_PATH="/root/miniconda3"
ENV_NAME="huatuo"


# 激活conda环境
. "${CONDA_PATH}/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"
ps aux | grep llamafactory | awk '{print $2}' | xargs kill
cd "$home"
rm -rf logs/$current_time.log

# 参数src/llamafactory/hparams/model_args.py
# 使用date命令并格式化输出，精确到日期
full_path=$(python src/config.py --full_path True)
current_time=$(date +"%Y-%m-%d")
CUDA_VISIBLE_DEVICES=0,1
API_PORT=9997
nohup llamafactory-cli api \
    --model_name_or_path $full_path \
    --template baichuan \
    --infer_dtype float16 \
    --flash_attn disabled >"log/$current_time.log" 2>&1 &