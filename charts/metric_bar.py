"""
Quality Metric Grouped Bar Chart
- X축: 모델
- Y축: Quality Metric
- 그룹: FL-EN, FL-KO, APR-EN, APR-KO
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 한글 폰트 설정
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 읽기
df = pd.read_csv('quality_metric_results.csv')

# 모델 순서 정의 (차트와 동일)
model_order = ['ax', 'solar', 'exaone', 'kanana', 'midm', 'hyperclovax', 'qwen', 'codellama', '3.5-turbo', '4.1-nano']

# 각 태스크별 데이터 추출
fl_en = []
fl_ko = []
apr_en = []
apr_ko = []

for model in model_order:
    fl_en.append(df[(df['Model'] == model) & (df['Setting'] == 'FL-en')]['QualityMetric'].values[0])
    fl_ko.append(df[(df['Model'] == model) & (df['Setting'] == 'FL-ko')]['QualityMetric'].values[0])
    apr_en.append(df[(df['Model'] == model) & (df['Setting'] == 'Fix-en')]['QualityMetric'].values[0])
    apr_ko.append(df[(df['Model'] == model) & (df['Setting'] == 'Fix-ko')]['QualityMetric'].values[0])

# 그래프 설정
fig, ax = plt.subplots(figsize=(14, 6))

x = np.arange(len(model_order))
width = 0.2  # 막대 너비

# 색상 정의
colors = {
    'FL-EN': '#1f77b4',   # 파란색
    'FL-KO': '#ff7f0e',   # 주황색
    'APR-EN': '#2ca02c',  # 초록색
    'APR-KO': '#d62728',  # 빨간색
}

# 막대 그리기
bars1 = ax.bar(x - width*1.5, fl_en, width, label='FL-EN', color=colors['FL-EN'], edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x - width*0.5, fl_ko, width, label='FL-KO', color=colors['FL-KO'], edgecolor='black', linewidth=0.5)
bars3 = ax.bar(x + width*0.5, apr_en, width, label='APR-EN', color=colors['APR-EN'], edgecolor='black', linewidth=0.5)
bars4 = ax.bar(x + width*1.5, apr_ko, width, label='APR-KO', color=colors['APR-KO'], edgecolor='black', linewidth=0.5)

# 각 막대에 값 표시 (막대 안쪽)
for i, (bar1, bar2, bar3, bar4) in enumerate(zip(bars1, bars2, bars3, bars4)):
    # FL-EN
    height1 = bar1.get_height()
    ax.text(bar1.get_x() + bar1.get_width()/2., height1 - 0.05,
            f'{height1:.3f}', ha='center', va='top', fontsize=8, rotation=90, color='white', fontweight='bold')
    # FL-KO
    height2 = bar2.get_height()
    ax.text(bar2.get_x() + bar2.get_width()/2., height2 - 0.05,
            f'{height2:.3f}', ha='center', va='top', fontsize=8, rotation=90, color='white', fontweight='bold')
    # APR-EN
    height3 = bar3.get_height()
    ax.text(bar3.get_x() + bar3.get_width()/2., height3 - 0.05,
            f'{height3:.3f}', ha='center', va='top', fontsize=8, rotation=90, color='white', fontweight='bold')
    # APR-KO
    height4 = bar4.get_height()
    ax.text(bar4.get_x() + bar4.get_width()/2., height4 - 0.05,
            f'{height4:.3f}', ha='center', va='top', fontsize=8, rotation=90, color='white', fontweight='bold')

# 축 설정
ax.set_xlabel('Model', fontweight='bold', fontsize=12)
ax.set_ylabel('Quality Metric', fontweight='bold', fontsize=12)
ax.set_title('Quality Metric Comparison Across Models and Tasks', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(model_order, rotation=45, ha='right')
ax.set_ylim(0, 1.1)

# 그리드
ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# 범례 (그래프 아래)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), frameon=True, edgecolor='black', fontsize=10, ncol=4)

# 그룹 구분선 추가 (K-LLM | OS | GPT)
ax.axvline(x=5.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax.axvline(x=7.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)

# 그룹 라벨 추가
ax.text(2.5, 1.05, 'K-LLM', ha='center', fontsize=11, fontweight='bold', color='gray')
ax.text(6.5, 1.05, 'Open-source', ha='center', fontsize=11, fontweight='bold', color='gray')
ax.text(8.5, 1.05, 'GPT', ha='center', fontsize=11, fontweight='bold', color='gray')

# 저장
plt.tight_layout()
plt.savefig('quality_metric_grouped_bar.png', dpi=300, bbox_inches='tight')
print("Quality Metric grouped bar chart saved: quality_metric_grouped_bar.png")
