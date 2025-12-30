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
COLOR_CORRECT = "#00b0be"     # 파란색
COLOR_INCORRECT = "#ffb255"   # 주황색
COLOR_NULL = "#A3A3A3" 

# ======================================================
# 3. Fix 데이터 (data 파일 기준)
# ======================================================
# Fix-en: solar, codellama, exaone, hyperclovax, kanana, midm, ax, qwen, 3.5-turbo, 4.1-nano
correct_en   = [21, 13, 12, 3, 15, 3, 17, 19, 40, 29]
incorrect_en = [143, 156, 152, 166, 154, 155, 152, 150, 129, 140]
null_en      = [5, 0, 5, 0, 0, 11, 0, 0, 0, 0]

# Fix-ko: solar, codellama, exaone, hyperclovax, kanana, midm, ax, qwen, 3.5-turbo, 4.1-nano
correct_ko   = [24, 7, 16, 1, 16, 9, 21, 21, 42, 31]
incorrect_ko = [136, 161, 148, 168, 153, 123, 147, 148, 127, 138]
null_ko      = [9, 1, 5, 0, 0, 37, 1, 0, 0, 0]

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
# 4. Plot 설정 (EN–KO 간격)
# ======================================================
x = np.arange(len(models)) * 1.2   # 모델 간 간격
width = 0.32   # 막대 너비를 줄여서 EN-KO 간격 생성

fig, ax = plt.subplots(figsize=(14, 6))

# ======================================================
# 5. Stacked bar + 숫자
# ======================================================
for i, model in enumerate(models):
    # ---------- EN (left half) ----------
    # Correct (bottom)
    ax.bar(x[i] - width*0.6, correct_en[i], width,
           color=COLOR_CORRECT,
           edgecolor="black", linewidth=0.4)
    # Incorrect (middle)
    ax.bar(x[i] - width*0.6, incorrect_en[i], width,
           bottom=correct_en[i],
           color=COLOR_INCORRECT,
           edgecolor="black", linewidth=0.4)
    # Null (top)
    ax.bar(x[i] - width*0.6, null_en[i], width,
           bottom=correct_en[i] + incorrect_en[i],
           color=COLOR_NULL,
           edgecolor="black", linewidth=0.4)

    # 텍스트 추가
    if correct_en[i] > 0:
        if correct_en[i] <= 5:
            # 작은 값은 화살표로 표시 (왼쪽)
            y_pos = correct_en[i] / 2
            ax.annotate(f"{correct_en[i]}",
                       xy=(x[i] - width*0.6, y_pos),
                       xytext=(x[i] - width*1.5, y_pos),
                       ha='right', va='center',
                       fontsize=10, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(x[i] - width*0.6, correct_en[i] / 2,
                    f"{correct_en[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")
    
    if incorrect_en[i] > 0:
        if incorrect_en[i] <= 5:
            # 작은 값은 화살표로 표시 (왼쪽)
            y_pos = correct_en[i] + incorrect_en[i] / 2
            ax.annotate(f"{incorrect_en[i]}",
                       xy=(x[i] - width*0.6, y_pos),
                       xytext=(x[i] - width*1.5, y_pos),
                       ha='right', va='center',
                       fontsize=10, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(x[i] - width*0.6,
                    correct_en[i] + incorrect_en[i] / 2,
                    f"{incorrect_en[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")
    
    if null_en[i] > 0:
        if null_en[i] <= 5:
            # 작은 값은 화살표로 표시 (왼쪽)
            y_pos = correct_en[i] + incorrect_en[i] + null_en[i] / 2
            ax.annotate(f"{null_en[i]}",
                       xy=(x[i] - width*0.6, y_pos),
                       xytext=(x[i] - width*1.5, y_pos),
                       ha='right', va='center',
                       fontsize=10, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(x[i] - width*0.6,
                    correct_en[i] + incorrect_en[i] + null_en[i] / 2,
                    f"{null_en[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")

    # ---------- KO (right half) ----------
    # Correct (bottom)
    ax.bar(x[i] + width*0.6, correct_ko[i], width,
           color=COLOR_CORRECT,
           edgecolor="black", linewidth=0.4)
    # Incorrect (middle)
    ax.bar(x[i] + width*0.6, incorrect_ko[i], width,
           bottom=correct_ko[i],
           color=COLOR_INCORRECT,
           edgecolor="black", linewidth=0.4)
    # Null (top)
    ax.bar(x[i] + width*0.6, null_ko[i], width,
           bottom=correct_ko[i] + incorrect_ko[i],
           color=COLOR_NULL,
           edgecolor="black", linewidth=0.4)

    # 텍스트 추가
    if correct_ko[i] > 0:
        if correct_ko[i] <= 5:
            # 작은 값은 화살표로 표시 (오른쪽)
            y_pos = correct_ko[i] / 2
            ax.annotate(f"{correct_ko[i]}",
                       xy=(x[i] + width*0.6, y_pos),
                       xytext=(x[i] + width*1.5, y_pos),
                       ha='left', va='center',
                       fontsize=10, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(x[i] + width*0.6, correct_ko[i] / 2,
                    f"{correct_ko[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")
    
    if incorrect_ko[i] > 0:
        if incorrect_ko[i] <= 5:
            # 작은 값은 화살표로 표시 (오른쪽)
            y_pos = correct_ko[i] + incorrect_ko[i] / 2
            ax.annotate(f"{incorrect_ko[i]}",
                       xy=(x[i] + width*0.6, y_pos),
                       xytext=(x[i] + width*1.5, y_pos),
                       ha='left', va='center',
                       fontsize=10, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(x[i] + width*0.6,
                    correct_ko[i] + incorrect_ko[i] / 2,
                    f"{incorrect_ko[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")
    
    if null_ko[i] > 0:
        if null_ko[i] <= 5:
            # 작은 값은 화살표로 표시 (오른쪽)
            y_pos = correct_ko[i] + incorrect_ko[i] + null_ko[i] / 2
            ax.annotate(f"{null_ko[i]}",
                       xy=(x[i] + width*0.6, y_pos),
                       xytext=(x[i] + width*1.5, y_pos),
                       ha='left', va='center',
                       fontsize=10, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black', linewidth=1))
        else:
            ax.text(x[i] + width*0.6,
                    correct_ko[i] + incorrect_ko[i] + null_ko[i] / 2,
                    f"{null_ko[i]}", ha="center", va="center", fontweight="bold", fontsize=11, color="black")

# ======================================================
# 6. 그룹 구분 점선 추가
# ======================================================
# kllm(0-5) | os(6-7) | gpt(8-9)
divider_positions = [
    x[5] + (x[6] - x[5]) / 2,  # kllm-os 경계
    x[7] + (x[8] - x[7]) / 2   # os-gpt 경계
]

for pos in divider_positions:
    ax.axvline(x=pos, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)

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
    loc="upper center",
    bbox_to_anchor=(0.5, -0.25),
    ncol=3,
    frameon=True,
    edgecolor="black",
    fancybox=False
)

# ======================================================
# 8. Axis / Grid
# ======================================================
ax.set_ylabel("Number of bugs", fontsize=12)

ax.set_xticks(x)
ax.set_xticklabels([f"(EN) (KR)\n{m}" for m in models], fontsize=10)

ax.yaxis.set_major_locator(plt.MultipleLocator(20))
ax.grid(axis="y", linestyle="--", alpha=0.6)

# Y축 범위 확장하여 상단 여백 확보
ax.set_ylim(0, 185)
ax.set_xlim(-0.5, x[-1] + 0.5)

# 그룹 라벨 추가
ax.text((x[0] + x[5]) / 2, 178, 'Ko-LLMs', ha='center', fontsize=11, fontweight='bold', color='gray')
ax.text((x[6] + x[7]) / 2, 178, 'Global open-source LLMs', ha='center', fontsize=11, fontweight='bold', color='gray')
ax.text((x[8] + x[9]) / 2, 178, 'Commercial LLMs', ha='center', fontsize=11, fontweight='bold', color='gray')

# 제목을 하단에 추가
ax.set_xlabel("APR correctness (EN vs KR)", fontsize=14, fontweight="bold", labelpad=15)

# ======================================================
# 9. Save
# ======================================================
plt.tight_layout()
plt.savefig("APR_en_ko.png", dpi=300, bbox_inches="tight")
plt.show()
