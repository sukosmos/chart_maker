import matplotlib.pyplot as plt
import numpy as np

# 모델 이름
models = ["GPT-4o", "Claude Sonnet 3.5", "o3-mini-high", "Gemini 2.0 flash"]

# ORI 데이터
identical_ori   = [11, 11, 11,  9]
equivalent_ori  = [5,  12,  6,  9]
alternatives_ori= [5,  7,  5,  4]
workaround_ori  = [4,  1,  3,  1]
incorrect_ori   = [13,  7, 13, 15]

# OBF 데이터
identical_obf   = [5, 11, 9,  4]
equivalent_obf  = [6,  8,  8, 10]
alternatives_obf= [10,  6,  1,  4]
workaround_obf  = [6,  3,  4,  2]
incorrect_obf   = [11, 10, 16, 18]

x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 7))

# --- ORI (왼쪽 막대) ---
bars_ori = []
bars_ori.append(ax.bar(x - width/2, identical_ori, width, color="#1a80bb", label="Identical (ori)", edgecolor='black', linewidth=0.5))
bars_ori.append(ax.bar(x - width/2, equivalent_ori, width, bottom=np.array(identical_ori), color="#1a80bbc0", label="Equivalent (ori)", edgecolor='black', linewidth=0.5))
bars_ori.append(ax.bar(x - width/2, alternatives_ori, width, bottom=np.array(identical_ori)+np.array(equivalent_ori), color="#1a80bb98", label="Alternatives (ori)", edgecolor='black', linewidth=0.5))
bars_ori.append(ax.bar(x - width/2, workaround_ori, width, bottom=np.array(identical_ori)+np.array(equivalent_ori)+np.array(alternatives_ori), color="#ea801cff", label="Workaround (ori)", edgecolor='black', linewidth=0.5))
bars_ori.append(ax.bar(x - width/2, incorrect_ori, width, bottom=np.array(identical_ori)+np.array(equivalent_ori)+np.array(alternatives_ori)+np.array(workaround_ori), color="#ea801cc3", label="Incorrect (ori)", edgecolor='black', linewidth=0.5))

# --- OBF (오른쪽 막대) ---
bars_obf = []
bars_obf.append(ax.bar(x + width/2, identical_obf, width, color="#298c8c", label="Identical (trans)", edgecolor='black', linewidth=0.5))
bars_obf.append(ax.bar(x + width/2, equivalent_obf, width, bottom=np.array(identical_obf), color="#298c8cbd", label="Equivalent (trans)", edgecolor='black', linewidth=0.5))
bars_obf.append(ax.bar(x + width/2, alternatives_obf, width, bottom=np.array(identical_obf)+np.array(equivalent_obf), color="#298c8c95", label="Alternatives (trans)", edgecolor='black', linewidth=0.5))
bars_obf.append(ax.bar(x + width/2, workaround_obf, width, bottom=np.array(identical_obf)+np.array(equivalent_obf)+np.array(alternatives_obf), color="#f2c45f", label="Workaround (trans)", edgecolor='black', linewidth=0.5))
bars_obf.append(ax.bar(x + width/2, incorrect_obf, width, bottom=np.array(identical_obf)+np.array(equivalent_obf)+np.array(alternatives_obf)+np.array(workaround_obf), color="#f2c35fc3", label="Incorrect (trans)", edgecolor='black', linewidth=0.5))

# --- Correct-like Line (identical+equivalent+alternatives) ---
correct_like_ori = np.array(identical_ori) + np.array(equivalent_ori) + np.array(alternatives_ori)
correct_like_obf = np.array(identical_obf) + np.array(equivalent_obf) + np.array(alternatives_obf)

'''
ax.plot(x - width/2, correct_like_ori, marker="o", color="#fc8edd", linewidth=2, label="(Id+Eq+Alt) Correct Line (ori)")
ax.plot(x + width/2, correct_like_obf, marker="s", color="#fbff0d", linewidth=2, linestyle="--", label="(Id+Eq+Alt) Correct Line (trans)")
'''

# --- 라벨 추가 함수 (0도 표시) ---
def add_labels(group_vals, bar_group):
    totals = np.sum(group_vals, axis=0)  # 모델별 total
    for cat_idx, bars in enumerate(bar_group):
        for i, bar in enumerate(bars):
            h = bar.get_height()
            x_pos = bar.get_x() + bar.get_width() / 2
            bottom = bar.get_y()
            ratio = group_vals[cat_idx][i] / totals[i] * 100 if totals[i] > 0 else 0
            # 높이가 0인 경우에도 표시 → 막대 중심 대신 bottom에 표시
            y_pos = bottom + h/2 if h > 0 else bottom + 0.1
            ax.text(x_pos, y_pos,
                    f"{group_vals[cat_idx][i]}\n({ratio:.1f}%)",
                    ha="center", va="center", color="black", fontsize=8, fontweight="bold")

# ORI 라벨
add_labels([identical_ori, equivalent_ori, alternatives_ori, workaround_ori, incorrect_ori], bars_ori)
# OBF 라벨
add_labels([identical_obf, equivalent_obf, alternatives_obf, workaround_obf, incorrect_obf], bars_obf)

# 축, 제목, 레이블
ax.set_xlabel("Models")
ax.set_ylabel("Count")
ax.set_title("Patch correctness (orig. vs trans.)")
ax.set_xticks(x)
ax.set_xticklabels(models)

# y축 격자 
ax.yaxis.set_major_locator(plt.MultipleLocator(5))  # 5단위로 눈금 설정
ax.grid(axis='y', linestyle='--', alpha=0.7)  # y축 방향으로만 점선 격자 추가

# 범례
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()
