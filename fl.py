import matplotlib.pyplot as plt
import numpy as np

# 모델 이름
models = ["GPT-4o", "Claude Sonnet 3.5", "o3-mini-high", "Gemini 2.0 flash"]

# ORI 데이터
incorrect_ori = [11, 7, 12, 14]
correct_ori   = [27, 31, 26, 24]

# OBF 데이터
incorrect_obf = [11, 9, 15, 14]
correct_obf   = [27, 29, 23, 24]

x = np.arange(len(models))  # 모델 개수만큼 위치
width = 0.35  # 막대 너비

fig, ax = plt.subplots(figsize=(10, 6))

# --- ORI (왼쪽 막대, correct 먼저) ---
bar1 = ax.bar(x - width/2, correct_ori, width, label="Correct (ori)", color="#2198c3")
bar2 = ax.bar(x - width/2, incorrect_ori, width, bottom=correct_ori, label="Incorrect (ori)", color="#d93802")

# --- OBF (오른쪽 막대, correct 먼저) ---
bar3 = ax.bar(x + width/2, correct_obf, width, label="Correct (obf)", color="#66c2a5")
bar4 = ax.bar(x + width/2, incorrect_obf, width, bottom=correct_obf, label="Incorrect (obf)", color="#fc8d62")

# --- Correct 값 꺾은선 (combo) ---
ax.plot(x - width/2, correct_ori, marker="o", color="blue", linewidth=2, label="Correct Line (ori)")
ax.plot(x + width/2, correct_obf, marker="s", color="purple", linewidth=2, label="Correct Line (obf)")

# --- 라벨 추가 함수 (값 + 비율 모두 표시) ---
def add_labels(correct_vals, incorrect_vals, bars_correct, bars_incorrect):
    for i, (bar_c, bar_i) in enumerate(zip(bars_correct, bars_incorrect)):
        total = correct_vals[i] + incorrect_vals[i]

        # Correct 라벨
        h_c = bar_c.get_height()
        x_pos_c = bar_c.get_x() + bar_c.get_width() / 2
        ratio_c = correct_vals[i] / total * 100
        ax.text(x_pos_c, h_c / 2,
                f"{correct_vals[i]}\n({ratio_c:.1f}%)",
                ha="center", va="center", color="white", fontsize=9, fontweight="bold")

        # Incorrect 라벨
        h_i = bar_i.get_height()
        x_pos_i = bar_i.get_x() + bar_i.get_width() / 2
        bottom_i = bar_i.get_y()
        ratio_i = incorrect_vals[i] / total * 100
        ax.text(x_pos_i, bottom_i + h_i / 2,
                f"{incorrect_vals[i]}\n({ratio_i:.1f}%)",
                ha="center", va="center", color="white", fontsize=9, fontweight="bold")

# ORI + OBF 라벨
add_labels(correct_ori, incorrect_ori, bar1, bar2)
add_labels(correct_obf, incorrect_obf, bar3, bar4)

# 축, 제목, 레이블
ax.set_xlabel("Models")
ax.set_ylabel("Count")
ax.set_title("FL correctness(Original vs Obfuscated)")
ax.set_xticks(x)
ax.set_xticklabels(models)

# 범례 (겹치지 않도록 오른쪽 바깥)
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()
