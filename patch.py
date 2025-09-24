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
bars_ori.append(ax.bar(x - width/2, identical_ori, width, color="#43C15E", label="Identical (ori)"))
bars_ori.append(ax.bar(x - width/2, equivalent_ori, width, bottom=np.array(identical_ori), color="#53abc8", label="Equivalent (ori)"))
bars_ori.append(ax.bar(x - width/2, alternatives_ori, width, bottom=np.array(identical_ori)+np.array(equivalent_ori), color="#dbc51f", label="Alternatives (ori)"))
bars_ori.append(ax.bar(x - width/2, workaround_ori, width, bottom=np.array(identical_ori)+np.array(equivalent_ori)+np.array(alternatives_ori), color="#d26409", label="Workaround (ori)"))
bars_ori.append(ax.bar(x - width/2, incorrect_ori, width, bottom=np.array(identical_ori)+np.array(equivalent_ori)+np.array(alternatives_ori)+np.array(workaround_ori), color="#d10303d5", label="Incorrect (ori)"))

# --- OBF (오른쪽 막대) ---
bars_obf = []
bars_obf.append(ax.bar(x + width/2, identical_obf, width, color="#8ac827", label="Identical (obf)"))
bars_obf.append(ax.bar(x + width/2, equivalent_obf, width, bottom=np.array(identical_obf), color="#548794", label="Equivalent (obf)"))
bars_obf.append(ax.bar(x + width/2, alternatives_obf, width, bottom=np.array(identical_obf)+np.array(equivalent_obf), color="#dcba32", label="Alternatives (obf)"))
bars_obf.append(ax.bar(x + width/2, workaround_obf, width, bottom=np.array(identical_obf)+np.array(equivalent_obf)+np.array(alternatives_obf), color="#be6d4d", label="Workaround (obf)"))
bars_obf.append(ax.bar(x + width/2, incorrect_obf, width, bottom=np.array(identical_obf)+np.array(equivalent_obf)+np.array(alternatives_obf)+np.array(workaround_obf), color="#b24932", label="Incorrect (obf)"))

# --- Correct-like Line (identical+equivalent+alternatives) ---
correct_like_ori = np.array(identical_ori) + np.array(equivalent_ori) + np.array(alternatives_ori)
correct_like_obf = np.array(identical_obf) + np.array(equivalent_obf) + np.array(alternatives_obf)

ax.plot(x - width/2, correct_like_ori, marker="o", color="blue", linewidth=2, label="(Id+Eq+Alt) Correct Line (ori)")
ax.plot(x + width/2, correct_like_obf, marker="s", color="purple", linewidth=2, label="(Id+Eq+Alt) Correct Line (obf)")

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
                    ha="center", va="center", color="white", fontsize=8, fontweight="bold")

# ORI 라벨
add_labels([identical_ori, equivalent_ori, alternatives_ori, workaround_ori, incorrect_ori], bars_ori)
# OBF 라벨
add_labels([identical_obf, equivalent_obf, alternatives_obf, workaround_obf, incorrect_obf], bars_obf)

# 축, 제목, 레이블
ax.set_xlabel("Models")
ax.set_ylabel("Count")
ax.set_title("Patch correctness(Ori vs Obf)")
ax.set_xticks(x)
ax.set_xticklabels(models)

# 범례
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()
