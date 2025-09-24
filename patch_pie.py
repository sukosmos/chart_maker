import matplotlib.pyplot as plt

# 모델 이름
models = ["Gpt-4o", "Claude", "o3-mini-high", "Gemini-flash"]

# ORI 데이터
identical_ori   = [11, 11, 11,  9]
equivalent_ori  = [ 5, 12,  6,  9]
alternatives_ori= [ 5,  7,  5,  4]
workaround_ori  = [ 4,  1,  3,  1]
incorrect_ori   = [13,  7, 13, 15]

# OBF 데이터
identical_obf   = [ 5, 11,  9,  4]
equivalent_obf  = [ 6,  8,  8, 10]
alternatives_obf= [10,  6,  1,  4]
workaround_obf  = [ 6,  3,  4,  2]
incorrect_obf   = [11, 10, 16, 18]

# 색상 (논문용 대비 강조 팔레트)
colors = ["#98c127", "#00b0be", "#ffdd19", "#ffb255", "#f45f74"]

# 데이터 묶기
ori_data = list(zip(identical_ori, equivalent_ori, alternatives_ori, workaround_ori, incorrect_ori))
obf_data = list(zip(identical_obf, equivalent_obf, alternatives_obf, workaround_obf, incorrect_obf))

fig, axes = plt.subplots(2, len(models), figsize=(16, 8))

# custom autopct 함수: 값 + 비율
def autopct_format(values):
    def inner_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f"{val}\n({pct:.1f}%)"
    return inner_autopct

fig, axes = plt.subplots(2, len(models), figsize=(16, 8))

for i, model in enumerate(models):
    # ORI pie
    axes[0, i].pie(ori_data[i], labels=["Identical", "Equivalent", "Alternatives", "Workaround", "Incorrect"],
                   autopct=autopct_format(ori_data[i]), startangle=90, colors=colors, textprops={'fontsize': 8})
    axes[0, i].set_title(f"{model} (ori)", fontsize=12)

    # OBF pie
    axes[1, i].pie(obf_data[i], labels=["Identical", "Equivalent", "Alternatives", "Workaround", "Incorrect"],
                   autopct=autopct_format(obf_data[i]), startangle=90, colors=colors, textprops={'fontsize': 8})
    axes[1, i].set_title(f"{model} (obf)", fontsize=12)

plt.suptitle("Patch correctness (Original vs Obfuscated)", fontsize=16)
plt.tight_layout()
plt.show()
