"""
Quality Metric computation script
- Error types: CO, LE, PR, EO, R
- Tasks: FL / Fix
- Languages: EN / KO
"""

import pandas as pd

# ===============================
# 1. Metric 함수 정의
# ===============================

def compute_quality_metric(counts, total):
    """
    counts: dict with keys ['CO', 'LE', 'PR', 'EO', 'R']
    total: total number of bugs (N)
    """

    # Normalize
    CO = counts.get('CO', 0) / total
    LE = counts.get('LE', 0) / total
    PR = counts.get('PR', 0) / total
    EO = counts.get('EO', 0) / total
    R  = counts.get('R', 0)  / total

    # Raw score with CO weight = 2
    # Range: [-3, 3] (when CO=0 and all negative=1, or CO=1 and all negative=0)
    raw_score = 1 - (LE + PR + EO + R - 2*CO)

    # Completion Quality: scale to [-1, 1]
    quality_metric = raw_score / 3

    return raw_score, quality_metric


# ===============================
# 2. 전체 데이터 입력
# ===============================

N = 169  # total bugs

data = {
    "FL-en": {
        "solar":       {'CO':124, 'LE':1, 'PR':2,   'EO':6,  'R':0},
        "codellama":   {'CO':30,  'LE':2, 'PR':115, 'EO':7,  'R':1},
        "exaone":      {'CO':24,  'LE':0, 'PR':47,  'EO':0,  'R':0},
        "hyperclovax": {'CO':25,  'LE':8, 'PR':81,  'EO':2,  'R':22},
        "kanana":      {'CO':29,  'LE':0, 'PR':45,  'EO':4,  'R':33},
        "midm":        {'CO':51,  'LE':1, 'PR':47,  'EO':0,  'R':9},
        "ax":          {'CO':69,  'LE':0, 'PR':1,   'EO':0,  'R':0},
        "qwen":        {'CO':17,  'LE':0, 'PR':56,  'EO':0,  'R':1},
        "3.5-turbo":   {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
        "4.1-nano":    {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
    },

    "FL-ko": {
        "solar":       {'CO':121, 'LE':5, 'PR':0,   'EO':10, 'R':0},
        "codellama":   {'CO':70,  'LE':0, 'PR':51,  'EO':6,  'R':2},
        "exaone":      {'CO':19,  'LE':2, 'PR':80,  'EO':2,  'R':1},
        "hyperclovax": {'CO':28,  'LE':6, 'PR':86,  'EO':10, 'R':12},
        "kanana":      {'CO':29,  'LE':2, 'PR':74,  'EO':1,  'R':24},
        "midm":        {'CO':66,  'LE':0, 'PR':42,  'EO':0,  'R':12},
        "ax":          {'CO':153, 'LE':3, 'PR':2,   'EO':1,  'R':0},
        "qwen":        {'CO':30,  'LE':3, 'PR':84,  'EO':9,  'R':29},
        "3.5-turbo":   {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
        "4.1-nano":    {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
    },

    "Fix-en": {
        "solar":       {'CO':119, 'LE':0, 'PR':29,  'EO':1,  'R':0},
        "codellama":   {'CO':65,  'LE':0, 'PR':93,  'EO':2,  'R':0},
        "exaone":      {'CO':53,  'LE':0, 'PR':52,  'EO':5,  'R':0},
        "hyperclovax": {'CO':42,  'LE':13,'PR':92,  'EO':21, 'R':5},
        "kanana":      {'CO':39,  'LE':0, 'PR':95,  'EO':13, 'R':5},
        "midm":        {'CO':75,  'LE':0, 'PR':74,  'EO':7,  'R':0},
        "ax":          {'CO':81,  'LE':0, 'PR':6,   'EO':5,  'R':1},
        "qwen":        {'CO':51,  'LE':0, 'PR':97,  'EO':16, 'R':1},
        "3.5-turbo":   {'CO':169, 'LE':0, 'PR':0,   'EO':1,  'R':0},
        "4.1-nano":    {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
    },

    "Fix-ko": {
        "solar":       {'CO':37,  'LE':0, 'PR':1,   'EO':2,  'R':0},
        "codellama":   {'CO':45,  'LE':0, 'PR':35,  'EO':1,  'R':1},
        "exaone":      {'CO':40,  'LE':0, 'PR':55,  'EO':1,  'R':0},
        "hyperclovax": {'CO':38,  'LE':2, 'PR':64,  'EO':6,  'R':0},
        "kanana":      {'CO':38,  'LE':0, 'PR':55,  'EO':5,  'R':5},
        "midm":        {'CO':32,  'LE':0, 'PR':21,  'EO':1,  'R':0},
        "ax":          {'CO':42,  'LE':0, 'PR':2,   'EO':3,  'R':1},
        "qwen":        {'CO':35,  'LE':0, 'PR':91,  'EO':24, 'R':1},
        "3.5-turbo":   {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
        "4.1-nano":    {'CO':169, 'LE':0, 'PR':0,   'EO':0,  'R':0},
    }
}

# ===============================
# 3. 전체 계산
# ===============================

rows = []

for setting, models in data.items():
    for model, counts in models.items():
        raw, qm = compute_quality_metric(counts, N)
        rows.append({
            "Setting": setting,
            "Model": model,
            "RawScore": round(raw, 3),
            "QualityMetric": round(qm, 3),
            **counts
        })

df = pd.DataFrame(rows)

# ===============================
# 4. 결과 출력
# ===============================

print(df)
df.to_csv("quality_metric_results.csv", index=False)
