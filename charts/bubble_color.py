import matplotlib.pyplot as plt

# 축 이름
x_labels = ["identical", "equivalent", "alternatives", "workaround", "incorrect"]
y_labels = ["identical", "equivalent", "alternatives", "workaround", "incorrect"]

# 데이터셋 (각 행은 y, 각 열은 x)
datasets = {
    "GPT-4o": [
        [0, 2, 1, 0, 2],
        [2, 0, 3, 1, 0],
        [3, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ],
    "Claude": [
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
    "Gemini 2.0 flash": [
        [0, 2, 1, 1, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}

# 모델별 색상 정의
model_colors = {
    "GPT-4o": '#1a80bb',         # 파란색
    "Claude": '#ea801c',         # 주황색
    "o3-mini-high": '#298c8c',   # 청록색
    "Gemini 2.0 flash": '#f2c45f'  # 노란색
}

# 2x2 subplot 생성
fig, axes = plt.subplots(2, 2, figsize=(20, 14))
fig.suptitle("Patch Changes", fontsize=20, y=0.95)

# 모델별 기본 색상 정의
model_base_colors = {
    "GPT-4o": ('#1a80bb', '#e74c3c'),         # (기본색, 붉은색)
    "Claude": ('#ea801c', '#ff6b6b'),         # (기본색, 붉은색)
    "o3-mini-high": ('#298c8c', '#ff7675'),   # (기본색, 붉은색)
    "Gemini 2.0 flash": ('#f2c45f', '#fab1a0') # (기본색, 붉은색)
}

def get_bubble_color(title, i, j):
    """색상 결정 함수"""
    # Correct/Incorrect 카테고리 구분
    correct_indices = [0, 1, 2]  # identical, equivalent, alternatives
    incorrect_indices = [3, 4]   # workaround, incorrect
    
    if i in correct_indices and j in incorrect_indices:
        return model_base_colors[title][1]  # 붉은색 계열
    return model_base_colors[title][0]      # 기본 색상

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
            colors.append(get_bubble_color(title, i, j))  # 색상 결정

    # 산점도 그리기 - colors 매개변수 수정
    scatter = ax.scatter(x, y, s=sizes, alpha=0.7,
                        c=colors,  # 색상 리스트 사용
                        edgecolor='black', 
                        linewidth=1)

    # 값이 0보다 큰 경우에만 값 표시
    for i, (x_pos, y_pos, value) in enumerate(zip(x, y, values)):
        if value > 0:
            ax.text(x_pos, y_pos, str(value), 
                    ha='center', va='center',
                    color='black',  # 텍스트는 검정색 유지
                    fontweight='bold',
                    fontsize=16)
    
    # 축 레이블 추가 및 스타일 개선
    ax.set_title(title, pad=20, fontsize=20)
    ax.set_xlabel('trans', loc='left', fontsize=16)  # x축 레이블 추가
    ax.set_ylabel('ori', loc='bottom', fontsize=16)    # y축 레이블 추가
    
    # x축 설정
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=14)
    
    # y축 설정
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels, fontsize=14)
    
    # 그리드 스타일 개선
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 축 범위 명시적 설정
    ax.set_xlim(-0.5, len(x_labels)-0.5)
    ax.set_ylim(-0.5, len(y_labels)-0.5)
    
    # 여백 조정
    ax.margins(0.2)

# 전체 레이아웃 조정 - subplot 간격 증가
plt.tight_layout(rect=[0.03, 0.03, 1, 0.95], 
                w_pad=4.0,  # 가로 간격 3.0 -> 4.0으로 증가
                h_pad=3.0)  # 세로 간격 추가

# 차트 저장
plt.savefig('bubble_chart_color.png', format='png', dpi=300, bbox_inches='tight')

plt.show()
