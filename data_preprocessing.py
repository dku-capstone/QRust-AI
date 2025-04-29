import pandas as pd
import re
from urllib.parse import urlparse
from tld import get_tld

# 1. 데이터 로드
df = pd.read_csv("urldata.csv")

# 2. 라벨 이진화
df['label'] = df['label'].apply(lambda x: 0 if x == 'benign' else 1)

# 3. 각 feature 계산
df['hostname_length'] = df['url'].apply(lambda x: len(urlparse(x).netloc))
df['count_dir'] = df['url'].apply(lambda x: urlparse(x).path.count('/'))
df['count-www'] = df['url'].apply(lambda x: x.count('www'))
df['url_length'] = df['url'].apply(lambda x: len(str(x)))

def fd_length(url):
    try:
        return len(urlparse(url).path.split('/')[1])
    except:
        return 0
df['fd_length'] = df['url'].apply(fd_length)

df['count-'] = df['url'].apply(lambda x: x.count('-'))
df['count.'] = df['url'].apply(lambda x: x.count('.'))

def get_tld_length(url):
    try:
        return len(get_tld(url, fail_silently=True))
    except:
        return -1
df['tld_length'] = df['url'].apply(get_tld_length)

df['count-digits'] = df['url'].apply(lambda x: sum(c.isdigit() for c in x))
df['count='] = df['url'].apply(lambda x: x.count('='))

# 4. 필요한 컬럼만 저장
final_columns = ['url', 'label'] + [
    'hostname_length', 'count_dir', 'count-www',
    'url_length', 'fd_length', 'count-', 'count.',
    'tld_length', 'count-digits', 'count='
]
df[final_columns].to_csv("urldata_features10.csv", index=False)
print("10개 feature 기반 데이터 저장 완료: urldata_features10.csv")