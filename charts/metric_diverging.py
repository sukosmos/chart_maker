"""
Quality Metric Diverging Bar Chart
- X축: 모델
- Y축: Metric 값 (CO는 positive, LE/PR/EO/R은 negative)
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

# 모델 순서 정의
model_order = ['ax', 'solar', 'exaone', 'kanana', 'midm', 'hyperclovax', 'qwen', 'codellama', '3.5-turbo', '4.1-nano']

# 4개의 subplot 생성 (FL-EN, FL-KO, APR-EN, APR-KO)
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Quality Metric Components: Positive (CO) vs Negative (LE, PR, EO, R)', 
             fontweight='bold', fontsize=16, y=0.995)

settings = [
    ('FL-en', 'FL-EN'),
    ('FL-ko', 'FL-KO'),
    ('Fix-en', 'APR-EN'),
    ('Fix-ko', 'APR-KO')
]

colors = {
    'positive': '#2ca02c',   # 초록색 (positive)
    'LE': '#d62728',         # 빨간색
    'PR': '#ff7f0e',         # 주황색
    'EO': '#9467bd',         # 보라색
    'R': '#8c564b',          # 갈색
}

for idx, (setting, title) in enumerate(settings):
    ax = axes[idx // 2, idx % 2]
    
    # 데이터 추출
    co_values = []
    le_values = []
    pr_values = []
    eo_values = []
    r_values = []
    
    for model in model_order:
        row = df[(df['Model'] == model) & (df['Setting'] == setting)]
        co_values.append(row['CO'].values[0])
        le_values.append(-row['LE'].values[0])
        pr_values.append(-row['PR'].values[0])
        eo_values.append(-row['EO'].values[0])
        r_values.append(-row['R'].values[0])
    
    x = np.arange(len(model_order))
    width = 0.35
    
    # 막대 그리기 - Positive
    bars_positive = ax.bar(x, co_values, width, label='CO (Correct)', 
                          color=colors['positive'], edgecolor='black', linewidth=0.5)
    
    # 막대 그리기 - Negative (stacked)
    bars_le = ax.bar(x, le_values, width, label='LE (Less Effective)', 
                     color=colors['LE'], edgecolor='black', linewidth=0.5)
    bars_pr = ax.bar(x, pr_values, width, bottom=le_values, label='PR (Partial Regression)', 
                     color=colors['PR'], edgecolor='black', linewidth=0.5)
    
    # EO는 LE + PR 위에 쌓기
    eo_bottom = [le + pr for le, pr in zip(le_values, pr_values)]
    bars_eo = ax.bar(x, eo_values, width, bottom=eo_bottom, label='EO (Exact Output)', 
                     color=colors['EO'], edgecolor='black', linewidth=0.5)
    
    # R은 LE + PR + EO 위에 쌓기
    r_bottom = [le + pr + eo for le, pr, eo in zip(le_values, pr_values, eo_values)]
    bars_r = ax.bar(x, r_values, width, bottom=r_bottom, label='R (Regression)', 
                    color=colors['R'], edgecolor='black', linewidth=0.5)
    
    # 값 표시 - Positive
    for bar in bars_positive:
        height = bar.get_height()
        if height > 5:  # 값이 충분히 클 때만 표시
            ax.text(bar.get_x() + bar.get_width()/2., height/2,
                   f'{int(height)}',
                   ha='center', va='center',
                   fontsize=9, fontweight='bold', color='white')
    
    # 값 표시 - Negative stacked
    for i, (le, pr, eo, r) in enumerate(zip(le_values, pr_values, eo_values, r_values)):
        x_pos = x[i]
        # LE
        if le < -3:
            ax.text(x_pos, le/2, f'{abs(int(le))}',
                   ha='center', va='center', fontsize=8, fontweight='bold', color='white')
        # PR
        if pr < -3:
            ax.text(x_pos, le + pr/2, f'{abs(int(pr))}',
                   ha='center', va='center', fontsize=8, fontweight='bold', color='white')
        # EO
        if eo < -3:
            ax.text(x_pos, le + pr + eo/2, f'{abs(int(eo))}',
                   ha='center', va='center', fontsize=8, fontweight='bold', color='white')
        # R
        if r < -3:
            ax.text(x_pos, le + pr + eo + r/2, f'{abs(int(r))}',
                   ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # 축 설정
    ax.set_title(title, fontweight='bold', fontsize=13)
    ax.set_xlabel('Model', fontweight='bold', fontsize=11)
    ax.set_ylabel('Count', fontweight='bold', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(model_order, rotation=45, ha='right')
    ax.axhline(y=0, color='black', linewidth=1)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_xlim(-0.5, x[-1] + 0.5)
    
    # 범례 (첫 번째 subplot에만)
    if idx == 0:
        ax.legend(loc='upper left', frameon=True, edgecolor='black', fontsize=8, ncol=2)
    
    # 그룹 구분선 추가
    ax.axvline(x=5.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axvline(x=7.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)

# 레이아웃 조정
plt.tight_layout()
plt.savefig('quality_metric_diverging_bar.png', dpi=300, bbox_inches='tight')
print("Quality Metric diverging bar chart saved: quality_metric_diverging_bar.png")
