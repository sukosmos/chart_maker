import matplotlib.pyplot as plt
import numpy as np

# 모델 이름
models = ["GPT-4o", "Claude Sonnet 3.5", "o3-mini-high", "Gemini 2.0 Flash"]

# ORI 데이터
incorrect_ori = [11, 7, 12, 14]
correct_ori   = [27, 31, 26, 24]

# OBF 데이터
incorrect_obf = [11, 9, 15, 14]
correct_obf   = [27, 29, 23, 24]

x = np.arange(len(models)) * 1.2  # 모델 그룹 간 간격 조정
width = 0.35  # Bar width

fig, ax = plt.subplots(figsize=(10, 6))

# --- ORI (왼쪽 막대, correct 먼저) ---
bar1 = ax.bar(x - width*0.6, correct_ori, width, 
              label="Correct", color="#1a80bb", 
              edgecolor='black', linewidth=0.5)
bar2 = ax.bar(x - width*0.6, incorrect_ori, width, 
              bottom=correct_ori, label="Incorrect", 
              color="#ea801c", edgecolor='black', linewidth=0.5)

# --- OBF (오른쪽 막대, correct 먼저) ---
bar3 = ax.bar(x + width*0.6, correct_obf, width, 
              color="#1a80bb", edgecolor='black', linewidth=0.5)
bar4 = ax.bar(x + width*0.6, incorrect_obf, width, 
              bottom=correct_obf, color="#ea801c", 
              edgecolor='black', linewidth=0.5)

# --- 라벨 추가 함수 (값 + 비율 모두 표시) ---
def add_labels(correct_vals, incorrect_vals, bars_correct, bars_incorrect):
    for i, (bar_c, bar_i) in enumerate(zip(bars_correct, bars_incorrect)):
        total = correct_vals[i] + incorrect_vals[i]

        # Correct 라벨
        h_c = bar_c.get_height()
        x_pos_c = bar_c.get_x() + bar_c.get_width() / 2
        ratio_c = correct_vals[i] / total * 100
        
        # 수직 간격을 h_c/12로 줄임 (기존 h_c/8)
        ax.text(x_pos_c, h_c/2 + h_c/12,
                f"{correct_vals[i]}",
                ha="center", va="center", 
                color="black", 
                fontsize=14, 
                fontweight="bold")
        
        ax.text(x_pos_c, h_c/2 - h_c/12,
                f"({ratio_c:.1f}%)",
                ha="center", va="center", 
                color="black", 
                fontsize=11, 
                fontweight="bold")

        # Incorrect 라벨
        h_i = bar_i.get_height()
        x_pos_i = bar_i.get_x() + bar_i.get_width() / 2
        bottom_i = bar_i.get_y()
        ratio_i = incorrect_vals[i] / total * 100
        
        # 수직 간격을 h_i/12로 줄임 (기존 h_i/8)
        ax.text(x_pos_i, bottom_i + h_i/2 + h_i/12,
                f"{incorrect_vals[i]}",
                ha="center", va="center", 
                color="black", 
                fontsize=14, 
                fontweight="bold")
        
        ax.text(x_pos_i, bottom_i + h_i/2 - h_i/12,
                f"\n({ratio_i:.1f}%)",
                ha="center", va="center", 
                color="black", 
                fontsize=11, 
                fontweight="bold")

# ORI + OBF 라벨
add_labels(correct_ori, incorrect_ori, bar1, bar2)
add_labels(correct_obf, incorrect_obf, bar3, bar4)

# 축, 제목, 레이블
ax.set_xlabel("Models", labelpad=15)  # labelpad로 여백 추가
ax.set_ylabel("Number of bugs", fontsize=14)
ax.set_title("FL correctness (ori. vs trans.)", fontsize=14)
ax.set_xticks(x)

# x축 레이블 수정
model_labels = [f"  (ori)     (trans)\n\n{m}" for m in models]
ax.set_xticklabels(model_labels, fontsize=14)

# x축 레이블 여백 조정
ax.set_xlabel("Models", labelpad=15, fontsize=14)

# 범례 위치 수정
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=4)


# y축 격자 
ax.yaxis.set_major_locator(plt.MultipleLocator(10))  # 5단위로 눈금 설정
ax.grid(axis='y', linestyle='--', alpha=0.7)  # y축 방향으로만 점선 격자 추가

plt.tight_layout()
plt.savefig('fl.png', format='png', dpi=300, bbox_inches='tight')
plt.show()
