import matplotlib.pyplot as plt

# 축 이름
x_labels = ["identical", "equivalent", "alternatives", "workaround", "incorrect"]
y_labels = ["identical", "equivalent", "alternatives", "workaround", "incorrect"]

# 데이터셋 (각 행은 y, 각 열은 x)
datasets = {
    "GPT-4o": [
        [0, 3, 5, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 0, 2],
        [0, 1, 2, 1, 0],
    ],
    "Claude Sonnet 3.5": [
        [0, 2, 0, 0, 3],
        [2, 0, 3, 1, 0],
        [2, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ],
    "o3-mini-high": [
        [0, 1, 0, 0, 3],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0]
    ],
    "Gemini 2.0 Flash": [
        [0, 2, 1, 1, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}

def get_bubble_color(i, j):
    """
    i: ori category index (y-axis)
    j: trans category index (x-axis)
    returns: color for the bubble
    """
    # Category indices
    identical_equiv = [0, 1]      # identical, equivalent
    alternatives_idx = 2          # alternatives
    workaround_idx = 3           # workaround
    incorrect_idx = 4            # incorrect
    
    # Correct categories (identical, equivalent, alternatives)
    correct_indices = [0, 1, 2]
    # Incorrect categories (workaround, incorrect)
    incorrect_indices = [3, 4]
    
    if i in identical_equiv and j in [1, 2]:  # identical/equivalent -> equivalent/alternatives
        return '#f39c12'  # 주황색
    elif (i in correct_indices and j in incorrect_indices) or (i == workaround_idx and j == incorrect_idx):
        return '#e74c3c'  # 붉은색 (correct -> incorrect/workaround 또는 workaround -> incorrect)
    elif i in incorrect_indices and j in incorrect_indices and i != workaround_idx:
        return '#9b59b6'  # 보라색 (incorrect -> incorrect, except workaround -> incorrect)
    else:
        return '#1a80bb'  # 기존 파란색

# 2x2 subplot 생성
fig, axes = plt.subplots(2, 2, figsize=(20, 14))  # 세로 길이 12 -> 14로 증가
fig.suptitle("Patch Correctness Changes", fontsize=20, y=0.95)

# 각 subplot에 데이터셋 그리기
for ax, (title, data) in zip(axes.flat, datasets.items()):
    x, y, sizes = [], [], []
    values = []
    colors = []  # 버블별 색상을 저장할 리스트
    
    # 모든 좌표에 대해 처리 (0 포함)
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            x.append(j)
            y.append(i)
            size = data[i][j] * 1000 if data[i][j] > 0 else 0
            sizes.append(size)
            values.append(data[i][j])
            colors.append(get_bubble_color(i, j))  # 색상 결정

    # Add diagonal line (x=y) - modified to cover entire plot area
    ax.plot([-0.8, len(x_labels)-0.5], [-0.8, len(y_labels)-0.5], 
            linestyle='--', color='red', alpha=0.5, linewidth=2)
    
    # Scatter plot
    scatter = ax.scatter(x, y, s=sizes, alpha=0.7,
                        c=colors,
                        edgecolor='black', 
                        linewidth=1)
    
    # 값이 0보다 큰 경우에만 값 표시
    for i, (x_pos, y_pos, value) in enumerate(zip(x, y, values)):
        if value > 0:
            ax.text(x_pos, y_pos, str(value), 
                    ha='center', va='center',
                    color='black',
                    fontweight='bold',
                    fontsize=20)
    
    # 축 레이블 추가 및 스타일 개선
    ax.set_title(title, pad=20, fontsize=20)
    ax.set_xlabel('After', loc='center', fontsize=20)  # x축 레이블 추가
    ax.set_ylabel('Before', loc='center', fontsize=20)    # y축 레이블 추가
    
    # x축 설정
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=16)
    
    # y축 설정
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels, fontsize=16)
    
    # 그리드 스타일 개선
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 축 범위 설정 유지
    ax.set_xlim(-0.8, len(x_labels)-0.5)
    ax.set_ylim(-0.8, len(y_labels)-0.5)
    
    # margins 설정 유지
    ax.margins(0.15)

# 전체 레이아웃 조정 - subplot 간격 증가
plt.tight_layout(rect=[0.03, 0.03, 1, 0.95], 
                w_pad=4.0,  # 가로 간격 3.0 -> 4.0으로 증가
                h_pad=3.0)  # 세로 간격 추가

# 차트 저장
plt.savefig('bubble_chart.svg', format='svg', dpi=300, bbox_inches='tight')

plt.show()