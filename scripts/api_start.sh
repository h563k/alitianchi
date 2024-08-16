#!/usr/bin/env bash
# conda create -n llama_fact python=3.11
# export PYTHONPATH=$PYTHONPATH:'pwd'
# 使用date命令并格式化输出，精确到日期
current_time=$(date +"%Y-%m-%d")
CONDA_PATH=/root/miniconda3
ENV_NAME=huatuo

. "${CONDA_PATH}/etc/profile.d/conda.sh"
conda activate $ENV_NAME

cd /opt/project/alitianchi
nohup xinference-local --host 0.0.0.0 --port 9997 >"logs/$current_time.log" 2>&1 &
