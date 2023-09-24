## 最低賃金API

日本の最低賃金(時給)を返却するAPI

## ドキュメント

詳細は [API Reference](https://minimum-wage-api.vercel.app/doc/) を参照してください

## 使い方

```bash
curl -s "https://minimum-wage-api.vercel.app?prefecture=tokyo&date=2023-10-01" | jq 

# [
#   {
#     "prefecture": "東京",
#     "wage": 1113,
#     "date_of_issue": "2023-10-01"
#   }
# ]
```
