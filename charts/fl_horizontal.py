import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# ======================================================
# 0. Global font 설정
# ======================================================
plt.rcParams.update({
    "font.size": 11,
    "font.family": "sans-serif"
})

# ======================================================
# 1. 모델 및 그룹 정의
# ======================================================
kllm_models = ["ax", "solar", "exaone", "kanana", "midm", "hyperclovax"]
os_models   = ["qwen", "codellama"]
gpt_models  = ["gpt-3.5", "gpt-4.1"]

models = kllm_models + os_models + gpt_models

def get_group(model):
    if model in kllm_models:
        return "kllm"
    elif model in os_models:
        return "os"
    else:
        return "gpt"

# ======================================================
# 2. 색상 정의 (언어별)
# ======================================================
COLOR_CORRECT = "#1a80bb"     # 파란색
COLOR_INCORRECT = "#ea801c"   # 주황색
COLOR_NULL = "#A3A3A3"        # 진한 회색

# ======================================================
# 3. FL 데이터 (data 파일 기준)
# ======================================================
# FL-en: solar, codellama, exaone, hyperclovax, kanana, midm, ax, qwen, 3.5-turbo, 4.1-nano
correct_en   = [53, 47, 54, 14, 49, 26, 56, 47, 61, 53]
incorrect_en = [108, 122, 110, 155, 120, 113, 113, 122, 108, 116]
null_en      = [8, 0, 5, 0, 0, 30, 0, 0, 0, 0]

# FL-ko: solar, codellama, exaone, hyperclovax, kanana, midm, ax, qwen, 3.5-turbo, 4.1-nano
correct_ko   = [44, 31, 34, 14, 45, 21, 48, 42, 68, 64]
incorrect_ko = [109, 136, 130, 155, 124, 132, 121, 127, 101, 105]
null_ko      = [16, 2, 5, 0, 0, 16, 0, 0, 0, 0]

# 순서 재정렬: kllm(ax, solar, exaone, kanana, midm, hyperclovax) + os(qwen, codellama) + gpt(3.5, 4.1)
# 원본 순서: solar(0), codellama(1), exaone(2), hyperclovax(3), kanana(4), midm(5), ax(6), qwen(7), 3.5(8), 4.1(9)
order = [6, 0, 2, 4, 5, 3, 7, 1, 8, 9]
correct_en = [correct_en[i] for i in order]
incorrect_en = [incorrect_en[i] for i in order]
null_en = [null_en[i] for i in order]
correct_ko = [correct_ko[i] for i in order]
incorrect_ko = [incorrect_ko[i] for i in order]
null_ko = [null_ko[i] for i in order]

# ======================================================
# 4. Plot 설정 (가로 버전)
# ======================================================
y = np.arange(len(models)) * 1.2   # 모델 간 간격
height = 0.32   # 막대 높이

fig, ax = plt.subplots(figsize=(12, 10))

# ======================================================
# 5. Stacked bar + 숫자 (가로 버전)
# ======================================================
for i, model in enumerate(models):
    # ---------- EN (위쪽) ----------
    # Correct (left)
    ax.barh(y[i] + height*0.6, correct_en[i], height,
            color=COLOR_CORRECT,
            edgecolor="black", linewidth=0.4)
    # Incorrect (middle)
    ax.barh(y[i] + height*0.6, incorrect_en[i], height,
            left=correct_en[i],
            color=COLOR_INCORRECT,
            edgecolor="black", linewidth=0.4)
    # Null (right)
    ax.barh(y[i] + height*0.6, null_en[i], height,
            left=correct_en[i] + incorrect_en[i],
            color=COLOR_NULL,
            edgecolor="black", linewidth=0.4)

    # 텍스트 추가
    if correct_en[i] > 0:
        if correct_en[i] <= 5:
            # 작은 값은 화살표로 표시 (위쪽)
            x_pos = correct_en[i] / 2
            ax.annotate(f"{correct_en[i]}",
                       xy=(x_pos, y[i] + height*0.6),
                       xytext=(x_pos, y[i] + height*1.8),
                       ha='center', va='bottom',
                       fontsize=11, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(correct_en[i] / 2, y[i] + height*0.6,
                    f"{correct_en[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")
    
    if incorrect_en[i] > 0:
        if incorrect_en[i] <= 5:
            # 작은 값은 화살표로 표시 (위쪽)
            x_pos = correct_en[i] + incorrect_en[i] / 2
            ax.annotate(f"{incorrect_en[i]}",
                       xy=(x_pos, y[i] + height*0.6),
                       xytext=(x_pos, y[i] + height*1.8),
                       ha='center', va='bottom',
                       fontsize=11, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(correct_en[i] + incorrect_en[i] / 2, y[i] + height*0.6,
                    f"{incorrect_en[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")
    
    if null_en[i] > 0:
        if null_en[i] <= 5:
            # 작은 값은 화살표로 표시 (위쪽)
            x_pos = correct_en[i] + incorrect_en[i] + null_en[i] / 2
            ax.annotate(f"{null_en[i]}",
                       xy=(x_pos, y[i] + height*0.6),
                       xytext=(x_pos, y[i] + height*1.8),
                       ha='center', va='bottom',
                       fontsize=11, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(correct_en[i] + incorrect_en[i] + null_en[i] / 2, y[i] + height*0.6,
                    f"{null_en[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")

    # ---------- KO (아래쪽) ----------
    # Correct (left)
    ax.barh(y[i] - height*0.6, correct_ko[i], height,
            color=COLOR_CORRECT,
            edgecolor="black", linewidth=0.4)
    # Incorrect (middle)
    ax.barh(y[i] - height*0.6, incorrect_ko[i], height,
            left=correct_ko[i],
            color=COLOR_INCORRECT,
            edgecolor="black", linewidth=0.4)
    # Null (right)
    ax.barh(y[i] - height*0.6, null_ko[i], height,
            left=correct_ko[i] + incorrect_ko[i],
            color=COLOR_NULL,
            edgecolor="black", linewidth=0.4)

    # 텍스트 추가
    if correct_ko[i] > 0:
        if correct_ko[i] <= 5:
            # 작은 값은 화살표로 표시 (아래쪽)
            x_pos = correct_ko[i] / 2
            ax.annotate(f"{correct_ko[i]}",
                       xy=(x_pos, y[i] - height*0.6),
                       xytext=(x_pos, y[i] - height*1.8),
                       ha='center', va='top',
                       fontsize=11, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(correct_ko[i] / 2, y[i] - height*0.6,
                    f"{correct_ko[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")
    
    if incorrect_ko[i] > 0:
        if incorrect_ko[i] <= 5:
            # 작은 값은 화살표로 표시 (아래쪽)
            x_pos = correct_ko[i] + incorrect_ko[i] / 2
            ax.annotate(f"{incorrect_ko[i]}",
                       xy=(x_pos, y[i] - height*0.6),
                       xytext=(x_pos, y[i] - height*1.8),
                       ha='center', va='top',
                       fontsize=11, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(correct_ko[i] + incorrect_ko[i] / 2, y[i] - height*0.6,
                    f"{incorrect_ko[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")
    
    if null_ko[i] > 0:
        if null_ko[i] <= 5:
            # 작은 값은 화살표로 표시 (아래쪽)
            x_pos = correct_ko[i] + incorrect_ko[i] + null_ko[i] / 2
            ax.annotate(f"{null_ko[i]}",
                       xy=(x_pos, y[i] - height*0.6),
                       xytext=(x_pos, y[i] - height*1.8),
                       ha='center', va='top',
                       fontsize=11, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(correct_ko[i] + incorrect_ko[i] + null_ko[i] / 2, y[i] - height*0.6,
                    f"{null_ko[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")

# ======================================================
# 6. 그룹 구분 점선 추가
# ======================================================
# kllm(0-5) | os(6-7) | gpt(8-9)
divider_positions = [
    y[5] + (y[6] - y[5]) / 2,  # kllm-os 경계
    y[7] + (y[8] - y[7]) / 2   # os-gpt 경계
]

for pos in divider_positions:
    ax.axhline(y=pos, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)

# ======================================================
# 7. Legend
# ======================================================
legend_elements = [
    Patch(facecolor=COLOR_CORRECT, label="Correct"),
    Patch(facecolor=COLOR_INCORRECT, label="Incorrect"),
    Patch(facecolor=COLOR_NULL, label="NULL")
]

ax.legend(
    handles=legend_elements,
    loc="lower right",
    ncol=1,
    frameon=True,
    edgecolor="black",
    fancybox=False
)

# ======================================================
# 8. Axis / Grid
# ======================================================
ax.set_xlabel("Number of bugs", fontsize=12)

ax.set_yticks(y)
ax.set_yticklabels([f"{m}\n(EN)\n(KO)" for m in models], fontsize=10)

ax.xaxis.set_major_locator(plt.MultipleLocator(20))
ax.grid(axis="x", linestyle="--", alpha=0.6)

# 제목 추가
ax.set_title("FL correctness (EN vs KO)", fontsize=14, fontweight="bold", pad=15)

# Y축 반전 (위에서 아래로)
ax.invert_yaxis()

# ======================================================
# 9. Save
# ======================================================
plt.tight_layout()
plt.savefig("FL_en_ko_horizontal.png", dpi=300, bbox_inches="tight")
plt.show()
