import matplotlib.pyplot as plt
import numpy as np

# Model names with versions - 수정
models = ["GPT-4o", "Claude Sonnet 3.5", "o3-mini-high", "Gemini 2.0 flash"]
model_labels = [f"(ori)    (trans)\n\n{m}" for m in models]

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

# Setup
x = np.arange(len(models)) * 1.0  # Increased spacing between model groups
width = 0.3  # Bar width

fig, ax = plt.subplots(figsize=(12, 7))

# Colors for categories
colors = {
    'identical': '#1a80bb',
    'equivalent': '#1a80bba5',
    'alternatives': '#1a80bb5e',
    'workaround': '#ea801ca0',
    'incorrect': '#ea801cff'
}

# --- Original version bars ---
bars_ori = []
bars_ori.append(ax.bar(x - width*0.6, identical_ori, width, color=colors['identical'], 
                      label='Identical', edgecolor='black', linewidth=0.5))
bars_ori.append(ax.bar(x - width*0.6, equivalent_ori, width, 
                      bottom=np.array(identical_ori), 
                      color=colors['equivalent'], label='Equivalent', 
                      edgecolor='black', linewidth=0.5))
bars_ori.append(ax.bar(x - width*0.6, alternatives_ori, width, 
                      bottom=np.array(identical_ori)+np.array(equivalent_ori), 
                      color=colors['alternatives'], label='Alternatives', 
                      edgecolor='black', linewidth=0.5))
bars_ori.append(ax.bar(x - width*0.6, workaround_ori, width, 
                      bottom=np.array(identical_ori)+np.array(equivalent_ori)+np.array(alternatives_ori), 
                      color=colors['workaround'], label='Workaround', 
                      edgecolor='black', linewidth=0.5))
bars_ori.append(ax.bar(x - width*0.6, incorrect_ori, width, 
                      bottom=np.array(identical_ori)+np.array(equivalent_ori)+np.array(alternatives_ori)+np.array(workaround_ori), 
                      color=colors['incorrect'], label='Incorrect', 
                      edgecolor='black', linewidth=0.5))

# --- Transformed version bars (without labels to avoid duplicate legends) ---
bars_obf = []
bars_obf.append(ax.bar(x + width*0.6, identical_obf, width, 
                      color=colors['identical'], edgecolor='black', linewidth=0.5))
bars_obf.append(ax.bar(x + width*0.6, equivalent_obf, width, 
                      bottom=np.array(identical_obf), 
                      color=colors['equivalent'], edgecolor='black', linewidth=0.5))
bars_obf.append(ax.bar(x + width*0.6, alternatives_obf, width, 
                      bottom=np.array(identical_obf)+np.array(equivalent_obf), 
                      color=colors['alternatives'], edgecolor='black', linewidth=0.5))
bars_obf.append(ax.bar(x + width*0.6, workaround_obf, width, 
                      bottom=np.array(identical_obf)+np.array(equivalent_obf)+np.array(alternatives_obf), 
                      color=colors['workaround'], edgecolor='black', linewidth=0.5))
bars_obf.append(ax.bar(x + width*0.6, incorrect_obf, width, 
                      bottom=np.array(identical_obf)+np.array(equivalent_obf)+np.array(alternatives_obf)+np.array(workaround_obf), 
                      color=colors['incorrect'], edgecolor='black', linewidth=0.5))

# Value labels function 수정
def add_labels(group_vals, bar_group, is_ori=True):
    totals = np.sum(group_vals, axis=0)
    for cat_idx, bars in enumerate(bar_group):
        for i, bar in enumerate(bars):
            h = bar.get_height()
            x_pos = bar.get_x() + bar.get_width() / 2
            bottom = bar.get_y()
            ratio = group_vals[cat_idx][i] / totals[i] * 100 if totals[i] > 0 else 0
            y_pos = bottom + h/2 if h > 0 else bottom + 0.1
            
            # 2 이하의 값은 바깥에 표시
            if h <= 2:
                # ori 버전은 왼쪽, trans 버전은 오른쪽에 표시
                if is_ori:
                    xytext = (x_pos - width*0.8, bottom + h/2)  # 왼쪽
                    ha = 'right'
                else:
                    xytext = (x_pos + width*0.8, bottom + h/2)  # 오른쪽
                    ha = 'left'
                
                # 값과 비율을 분리하여 표시
                ax.annotate(
                    f"{group_vals[cat_idx][i]}",  # 값만 표시
                    xy=(x_pos, bottom + h/2),
                    xytext=xytext,
                    ha=ha, va='center',
                    fontsize=14,  # 값은 14
                    fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='black', linewidth=1)
                )
                
                # 비율은 별도로 표시
                ax.text(xytext[0], xytext[1] - h/4,
                       f"\n\n({ratio:.1f}%)",
                       ha=ha, va='center',
                       color="black",
                       fontsize=9,  # 비율은 9
                       fontweight='bold')
            else:
                # 기존 방식대로 막대 안에 표시
                ax.text(x_pos, y_pos + h/8,
                       f"{group_vals[cat_idx][i]}",
                       ha="center", va="center", 
                       color="black",
                       fontsize=14,
                       fontweight="bold")
                
                ax.text(x_pos, y_pos - h/8,
                       f"\n({ratio:.1f}%)",
                       ha="center", va="center", 
                       color="black",
                       fontsize=9,
                       fontweight="bold")

# Add labels for both versions (함수 호출 부분도 수정)
add_labels([identical_ori, equivalent_ori, alternatives_ori, workaround_ori, incorrect_ori], bars_ori, is_ori=True)
add_labels([identical_obf, equivalent_obf, alternatives_obf, workaround_obf, incorrect_obf], bars_obf, is_ori=False)

# Customize the plot
ax.set_xlabel("Models", labelpad=15, fontsize=14)  # labelpad로 여백 추가
ax.set_xticks(x)
ax.set_xticklabels(model_labels, fontsize=14)
ax.set_ylabel("Number of bugs", fontsize=14)
ax.set_title("Patch correctness (ori. vs trans.)", fontsize=14, pad=15)

# y축 눈금 폰트 크기 설정
ax.tick_params(axis='both', labelsize=14)

# y축 격자 
ax.yaxis.set_major_locator(plt.MultipleLocator(10))  # 5단위로 눈금 설정
ax.grid(axis='y', linestyle='--', alpha=0.7)  # y축 방향으로만 점선 격자 추가

# Legend
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=14)

plt.tight_layout()
plt.show()
