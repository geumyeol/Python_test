# equity is a 66 x 7 table (inclusive of the headers, risk measure/risk class/risk factor type/bucket/issuer name/stock name/
# net sensitivity). tables is a 14 x 4 table (inclusive of the headers, Bucket number/Risk weight for equity spot price/Risk weight
# for equity repo rate/Correlation)

import pandas as pd
import numpy as np

# equity.xlsx, tables.xlsx 파일 로드 / tables file 헤더 No=>1
equity = pd.read_excel('equity.xlsx', engine='openpyxl')
table = pd.read_excel('tables.xlsx', engine='openpyxl', header=1)

# table 파일의 각 헤더하위 데이터 가져오기
RW_for_spot = list(table['Risk weight for equity spot price'])
RW_for_repo = list(table['Risk weight for equity repo rate'])

# list [(spot[0], repo[0]), (spot[1], repo[1]), (spot[2], repo[2]),...]
RW_tuple = list(zip(RW_for_spot, RW_for_repo))

# equity 파일 내 bucket,risk ractor type 헤더하위 데이터 가져오기
bucket = list(equity['bucket'])
risk_factor_type = list(equity['risk factor type'])

# 함수 구현
def corr_matrix(factor_type, bucket, issuer):
    l = len(factor_type)
    mat = np.identity(l)
    factor_type = list(factor_type)
    issuer = list(issuer)

    for i in range(l):
        for j in range(l):

            if i != j:
                if factor_type[i] != factor_type[j] and issuer[i] == issuer[j]:
                    mat[i, j] = 0.999

                if factor_type[i] == factor_type[j]:
                    mat[i, j] = table['Correlation'][bucket - 1]

                if factor_type[i] != factor_type[j] and issuer[i] != issuer[j]:
                    mat[i, j] = table['Correlation'][bucket - 1] * 0.999

    return mat


def cor_env(input_array, state):
    l = input_array.shape[0]
    if state == 'medium':
        result = input_array
    elif state == 'high':
        result = np.minimum(np.ones((l, l)), input_array * 1.25)
    else:
        result = np.maximum(2 * input_array - 1, 0.75 * input_array)

    return result

temp1 = []
for i in bucket:
    temp1.append(RW_tuple[i-1])


temp2 = []
for i in range(len(bucket)):
    if i < 39:
        temp2.append(temp1[i][0])
    else:
        temp2.append(temp1[i][1])

equity['RW'] = temp2
equity['Risk weighted sensitivity'] = equity['net sensitivity'] * equity['RW']

bucket_dict = {}
for i in range(1, 14):
    bucket_dict[i] = equity[equity['bucket'] == i]


result_mat = np.zeros((13, 3))
for i in range(1, 14):

    if i != 11:
        df = bucket_dict[i]
        W = np.array(df['Risk weighted sensitivity']).reshape(1, -1)

        temp = np.matmul(W.T, W)

        cm = corr_matrix(df['risk factor type'], i, df['issuer name'])
        cm_med = cor_env(cm, 'medium')
        cm_high = cor_env(cm, 'high')
        cm_low = cor_env(cm, 'low')

        risk_med = np.sqrt(max(0, np.sum(temp * cm_med)))
        risk_high = np.sqrt(max(0, np.sum(temp * cm_high)))
        risk_low = np.sqrt(max(0, np.sum(temp * cm_low)))

        result_mat[i - 1, 0] = risk_med
        result_mat[i - 1, 1] = risk_high
        result_mat[i - 1, 2] = risk_low
    else:
        result_mat[i - 1, 0] = sum(np.abs(bucket_dict[i]['Risk weighted sensitivity']))
        result_mat[i - 1, 1] = sum(np.abs(bucket_dict[i]['Risk weighted sensitivity']))
        result_mat[i - 1, 2] = sum(np.abs(bucket_dict[i]['Risk weighted sensitivity']))

index = table['Bucket number']
column = ['Medium correlations', 'High correlations', 'Low correlations']
delta_risk_table = pd.DataFrame(result_mat, index=index, columns=column).round(4)
print(delta_risk_table)

# the output delta risk table is a 13 x 3 matrix(table) exclusive of the headers