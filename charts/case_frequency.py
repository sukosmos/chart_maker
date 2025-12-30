"""
Case Frequency Line Chart
- 4개 그래프: FL-en, FL-ko, Fix-en, Fix-ko
- 각 그래프에 5가지 케이스: CO, LE, PR, EO, R
- Y축 분할: 하단(0-40), 상단(80-180)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# 한글 폰트 설정
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

# 모델 순서 (차트와 동일)
models_original = ['solar', 'codellama', 'exaone', 'hyperclovax', 'kanana', 'midm', 'ax', 'qwen', '3.5-turbo', '4.1-nano']
# 재정렬 순서: ax, solar, exaone, kanana, midm, hyperclovax, qwen, codellama, 3.5-turbo, 4.1-nano
order = [6, 0, 2, 4, 5, 3, 7, 1, 8, 9]
models = [models_original[i] for i in order]

# ============================================================
# FL-EN 데이터
# ============================================================
fl_en_data = {
    'solar':       {'CO':124, 'LE':1,  'PR':2,   'EO':6,  'R':0},
    'codellama':   {'CO':30,  'LE':2,  'PR':115, 'EO':7,  'R':1},
    'exaone':      {'CO':24,  'LE':0,  'PR':47,  'EO':0,  'R':0},
    'hyperclovax': {'CO':25,  'LE':8,  'PR':81,  'EO':2,  'R':22},
    'kanana':      {'CO':29,  'LE':0,  'PR':45,  'EO':4,  'R':33},
    'midm':        {'CO':51,  'LE':1,  'PR':47,  'EO':0,  'R':9},
    'ax':          {'CO':69,  'LE':0,  'PR':1,   'EO':0,  'R':0},
    'qwen':        {'CO':17,  'LE':0,  'PR':56,  'EO':0,  'R':1},
    '3.5-turbo':   {'CO':169, 'LE':0,  'PR':0,   'EO':0,  'R':0},
    '4.1-nano':    {'CO':169, 'LE':0,  'PR':0,   'EO':0,  'R':0},
}

# ============================================================
# FL-KO 데이터
# ============================================================
fl_ko_data = {
    'solar':       {'CO':121, 'LE':5, 'PR':0,   'EO':10, 'R':0},
    'codellama':   {'CO':70,  'LE':0, 'PR':51,  'EO':6,  'R':2},
    'exaone':      {'CO':19,  'LE':2, 'PR':80,  'EO':2,  'R':1},
    'hyperclovax': {'CO':28,  'LE':6, 'PR':86,  'EO':10, 'R':12},
    'kanana':      {'CO':29,  'LE':2, 'PR':74,  'EO':1,  'R':24},
    'midm':        {'CO':66,  'LE':0, 'PR':42,  'EO':0,  'R':12},
    'ax':          {'CO':153, 'LE':3, 'PR':2,   'EO':1,  'R':0},
    'qwen':        {'CO':30,  'LE':3, 'PR':84,  'EO':9,  'R':29},
    '3.5-turbo':   {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
    '4.1-nano':    {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
}

# ============================================================
# Fix-EN 데이터
# ============================================================
fix_en_data = {
    'solar':       {'CO':119, 'LE':0,  'PR':29, 'EO':1,  'R':0},
    'codellama':   {'CO':65,  'LE':0,  'PR':93, 'EO':2,  'R':0},
    'exaone':      {'CO':53,  'LE':0,  'PR':52, 'EO':5,  'R':0},
    'hyperclovax': {'CO':42,  'LE':13, 'PR':92, 'EO':21, 'R':5},
    'kanana':      {'CO':39,  'LE':0,  'PR':95, 'EO':13, 'R':5},
    'midm':        {'CO':75,  'LE':0,  'PR':74, 'EO':7,  'R':0},
    'ax':          {'CO':81,  'LE':0,  'PR':6,  'EO':5,  'R':1},
    'qwen':        {'CO':51,  'LE':0,  'PR':97, 'EO':16, 'R':1},
    '3.5-turbo':   {'CO':169, 'LE':0,  'PR':0,  'EO':1,  'R':0},
    '4.1-nano':    {'CO':169, 'LE':0,  'PR':0,  'EO':0,  'R':0},
}

# ============================================================
# Fix-KO 데이터
# ============================================================
fix_ko_data = {
    'solar':       {'CO':37,  'LE':0, 'PR':1,  'EO':2,  'R':0},
    'codellama':   {'CO':45,  'LE':0, 'PR':35, 'EO':1,  'R':1},
    'exaone':      {'CO':40,  'LE':0, 'PR':55, 'EO':1,  'R':0},
    'hyperclovax': {'CO':38,  'LE':2, 'PR':64, 'EO':6,  'R':0},
    'kanana':      {'CO':38,  'LE':0, 'PR':55, 'EO':5,  'R':5},
    'midm':        {'CO':32,  'LE':0, 'PR':21, 'EO':1,  'R':0},
    'ax':          {'CO':42,  'LE':0, 'PR':2,  'EO':3,  'R':1},
    'qwen':        {'CO':35,  'LE':0, 'PR':91, 'EO':24, 'R':1},
    '3.5-turbo':   {'CO':169, 'LE':0, 'PR':0,  'EO':0,  'R':0},
    '4.1-nano':    {'CO':169, 'LE':0, 'PR':0,  'EO':0,  'R':0},
}

# ============================================================
# 데이터 추출 함수
# ============================================================
def extract_case_data(data_dict, models):
    co = [data_dict[m]['CO'] for m in models]
    le = [data_dict[m]['LE'] for m in models]
    pr = [data_dict[m]['PR'] for m in models]
    eo = [data_dict[m]['EO'] for m in models]
    r = [data_dict[m]['R'] for m in models]
    return co, le, pr, eo, r

# ============================================================
# 그래프 그리기
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Case Frequency by Model', fontsize=16, fontweight='bold', y=0.995)

# 색상 정의
colors = {
    'CO': '#2E86AB',  # 파란색
    'LE': '#A23B72',  # 자주색
    'PR': '#F18F01',  # 주황색
    'EO': '#C73E1D',  # 빨간색
    'R': '#6A994E',   # 초록색
}

# 마커 정의
markers = {
    'CO': 'o',
    'LE': 's',
    'PR': '^',
    'EO': 'D',
    'R': 'v',
}

x = np.arange(len(models))

# ============================================================
# FL-EN
# ============================================================
ax = axes[0, 0]
co, le, pr, eo, r = extract_case_data(fl_en_data, models)
ax.plot(x, co, marker=markers['CO'], color=colors['CO'], linewidth=2, markersize=8, label='Code Only (CO)')
ax.plot(x, le, marker=markers['LE'], color=colors['LE'], linewidth=2, markersize=8, label='Language Error (LE)')
ax.plot(x, pr, marker=markers['PR'], color=colors['PR'], linewidth=2, markersize=8, label='Prompt Repeat (PR)')
ax.plot(x, eo, marker=markers['EO'], color=colors['EO'], linewidth=2, markersize=8, label='Empty Output (EO)')
ax.plot(x, r, marker=markers['R'], color=colors['R'], linewidth=2, markersize=8, label='Self Repeat (R)')

ax.set_xticks(x)
ax.set_xticklabels(models, rotation=45, ha='right')
ax.set_ylabel('Frequency', fontweight='bold', fontsize=11)
ax.set_title('FL-EN', fontweight='bold', fontsize=13)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', frameon=True, edgecolor='black')
ax.set_ylim(-5, 180)
ax.set_yscale('symlog', linthresh=50)  # 로그 스케일 적용 (50 이하는 선형)

# ============================================================
# FL-KO
# ============================================================
ax = axes[0, 1]
co, le, pr, eo, r = extract_case_data(fl_ko_data, models)
ax.plot(x, co, marker=markers['CO'], color=colors['CO'], linewidth=2, markersize=8, label='Code Only (CO)')
ax.plot(x, le, marker=markers['LE'], color=colors['LE'], linewidth=2, markersize=8, label='Language Error (LE)')
ax.plot(x, pr, marker=markers['PR'], color=colors['PR'], linewidth=2, markersize=8, label='Prompt Repeat (PR)')
ax.plot(x, eo, marker=markers['EO'], color=colors['EO'], linewidth=2, markersize=8, label='Empty Output (EO)')
ax.plot(x, r, marker=markers['R'], color=colors['R'], linewidth=2, markersize=8, label='Self Repeat (R)')

ax.set_xticks(x)
ax.set_xticklabels(models, rotation=45, ha='right')
ax.set_ylabel('Frequency', fontweight='bold', fontsize=11)
ax.set_title('FL-KO', fontweight='bold', fontsize=13)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', frameon=True, edgecolor='black')
ax.set_ylim(-5, 180)

# ============================================================
# APR-EN
# ============================================================
ax = axes[1, 0]
co, le, pr, eo, r = extract_case_data(fix_en_data, models)
ax.plot(x, co, marker=markers['CO'], color=colors['CO'], linewidth=2, markersize=8, label='Code Only (CO)')
ax.plot(x, le, marker=markers['LE'], color=colors['LE'], linewidth=2, markersize=8, label='Language Error (LE)')
ax.plot(x, pr, marker=markers['PR'], color=colors['PR'], linewidth=2, markersize=8, label='Prompt Repeat (PR)')
ax.plot(x, eo, marker=markers['EO'], color=colors['EO'], linewidth=2, markersize=8, label='Empty Output (EO)')
ax.plot(x, r, marker=markers['R'], color=colors['R'], linewidth=2, markersize=8, label='Self Repeat (R)')

ax.set_xticks(x)
ax.set_xticklabels(models, rotation=45, ha='right')
ax.set_ylabel('Frequency', fontweight='bold', fontsize=11)
ax.set_title('APR-EN', fontweight='bold', fontsize=13)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', frameon=True, edgecolor='black')
ax.set_ylim(-5, 180)

# ============================================================
# APR-KO
# ============================================================
ax = axes[1, 1]
co, le, pr, eo, r = extract_case_data(fix_ko_data, models)
ax.plot(x, co, marker=markers['CO'], color=colors['CO'], linewidth=2, markersize=8, label='Code Only (CO)')
ax.plot(x, le, marker=markers['LE'], color=colors['LE'], linewidth=2, markersize=8, label='Language Error (LE)')
ax.plot(x, pr, marker=markers['PR'], color=colors['PR'], linewidth=2, markersize=8, label='Prompt Repeat (PR)')
ax.plot(x, eo, marker=markers['EO'], color=colors['EO'], linewidth=2, markersize=8, label='Empty Output (EO)')
ax.plot(x, r, marker=markers['R'], color=colors['R'], linewidth=2, markersize=8, label='Self Repeat (R)')

ax.set_xticks(x)
ax.set_xticklabels(models, rotation=45, ha='right')
ax.set_ylabel('Frequency', fontweight='bold', fontsize=11)
ax.set_title('APR-KO', fontweight='bold', fontsize=13)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', frameon=True, edgecolor='black')
ax.set_ylim(-5, 180)

# ============================================================
# 저장
# ============================================================
plt.tight_layout()
plt.savefig('case_frequency_2.png', dpi=300, bbox_inches='tight')
print("Case frequency chart saved: case_frequency_2.png")
