"""
Quality Metric 결과를 표 형태로 정리
- 행: 모델
- 열: FL-EN, FL-KO, Fix-EN, Fix-KO
"""

import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('quality_metric_results.csv')

# 모델 순서 정의 (차트와 동일)
model_order = ['ax', 'solar', 'exaone', 'kanana', 'midm', 'hyperclovax', 'qwen', 'codellama', '3.5-turbo', '4.1-nano']

# 피벗 테이블 생성 (행: 모델, 열: Setting, 값: QualityMetric)
pivot_table = df.pivot(index='Model', columns='Setting', values='QualityMetric')

# 모델 순서대로 재정렬
pivot_table = pivot_table.reindex(model_order)

# 열 순서 정의
pivot_table = pivot_table[['FL-en', 'FL-ko', 'Fix-en', 'Fix-ko']]

# 열 이름 변경
pivot_table.columns = ['FL-EN', 'FL-KO', 'APR-EN', 'APR-KO']

print("=" * 80)
print("Quality Metric Results by Model and Task")
print("=" * 80)
print(pivot_table.to_string())
print("=" * 80)

# CSV로 저장
pivot_table.to_csv('quality_metric_table.csv')
print("\nTable saved to: quality_metric_table.csv")

# 통계 추가
print("\n" + "=" * 80)
print("Statistics")
print("=" * 80)
print(f"Mean by Task:")
print(pivot_table.mean().to_string())
print(f"\nStandard Deviation by Task:")
print(pivot_table.std().to_string())
print(f"\nMean by Model:")
print(pivot_table.mean(axis=1).to_string())
