#!/bin/bash

# 参数检查
if [ $# -lt 2 ]; then
    echo "Usage: $0 <ip_file> <max_delay> [output_file]"
    echo "示例: $0 ip_list.txt 50 result.txt"
    exit 1
fi

ip_file=$1
max_delay=$2
output_file=${3:-"filtered_ips.txt"}  # 默认输出文件

# 临时文件处理
tmp_file=$(mktemp)
trap 'rm -f $tmp_file' EXIT

# 确定ping参数
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ping_cmd="ping -c 1 -W 1"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    ping_cmd="ping -c 1 -t 1"
else
    echo "不支持的操作系统"
    exit 1
fi

# 主处理循环
while read -r ip; do
    [ -z "$ip" ] && continue
    
    # 执行ping并提取延迟
    if output=$($ping_cmd $ip 2>&1); then
        delay=$(echo "$output" | awk -F'[= ]' '/time=|时间/{print $(NF-1)}' | grep -oE '[0-9.]+')
        
        # 数值有效性检查
        if [[ "$delay" =~ ^[0-9.]+$ ]]; then
            # 阈值比较（支持小数）
            if (( $(echo "$delay < $max_delay" | bc -l) )); then
                printf "%-15s %sms\n" "$ip" "$delay" >> $tmp_file
            fi
        fi
    fi
done < "$ip_file"

# 排序输出（排除无结果情况）
if [ -s $tmp_file ]; then
    # 按延迟排序并格式化
    sort -nk2 $tmp_file | column -t > $output_file
    echo "结果已保存至: $output_file"
else
    echo "未找到符合阈值($max_delay ms)的IP"
    rm -f $output_file
fi
