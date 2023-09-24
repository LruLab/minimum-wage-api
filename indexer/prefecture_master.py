from tinydb import TinyDB, Query

db = TinyDB("./data/prefecture_master.json")
q = Query()

# Ordered by PrefCode (https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html)
PREFECTURE_LIST = [
    {"prefecture": "北海道", "pref_code": 1, "aliases": ["Hokkaido", "hokkaido", "ほっかいどう"]},
    {"prefecture": "青森", "pref_code": 2, "aliases": ["Aomori", "aomori", "あおもり", "青森県"]},
    {"prefecture": "岩手", "pref_code": 3, "aliases": ["Iwate", "iwate", "いわて", "岩手県"]},
    {"prefecture": "宮城", "pref_code": 4, "aliases": ["Miyagi", "miyagi", "みやぎ", "宮城県"]},
    {"prefecture": "秋田", "pref_code": 5, "aliases": ["Akita", "akita", "あきた", "秋田県"]},
    {"prefecture": "山形", "pref_code": 6, "aliases": ["Yamagata", "yamagata", "やまがた", "山形県"]},
    {"prefecture": "福島", "pref_code": 7, "aliases": ["Fukushima", "fukushima", "ふくしま", "福島県"]},
    {"prefecture": "茨城", "pref_code": 8, "aliases": ["Ibaraki", "ibaraki", "いばらき", "茨城県"]},
    {"prefecture": "栃木", "pref_code": 9, "aliases": ["Tochigi", "tochigi", "とちぎ", "栃木県"]},
    {"prefecture": "群馬", "pref_code": 10, "aliases": ["Gunma", "gunma", "ぐんま", "群馬県"]},
    {"prefecture": "埼玉", "pref_code": 11, "aliases": ["Saitama", "saitama", "さいたま", "埼玉県"]},
    {"prefecture": "千葉", "pref_code": 12, "aliases": ["Chiba", "chiba", "ちば", "千葉県"]},
    {"prefecture": "東京", "pref_code": 13, "aliases": ["Tokyo", "tokyo", "とうきょう", "東京都"]},
    {"prefecture": "神奈川", "pref_code": 14, "aliases": ["Kanagawa", "kanagawa", "かながわ", "神奈川県"]},
    {"prefecture": "新潟", "pref_code": 15, "aliases": ["Niigata", "niigata", "にいがた", "新潟県"]},
    {"prefecture": "富山", "pref_code": 16, "aliases": ["Toyama", "toyama", "とやま", "富山県"]},
    {"prefecture": "石川", "pref_code": 17, "aliases": ["Ishikawa", "ishikawa", "いしかわ", "石川県"]},
    {"prefecture": "福井", "pref_code": 18, "aliases": ["Fukui", "fukui", "ふくい", "福井県"]},
    {"prefecture": "山梨", "pref_code": 19, "aliases": ["Yamanashi", "yamanashi", "やまなし", "山梨県"]},
    {"prefecture": "長野", "pref_code": 20, "aliases": ["Nagano", "nagano", "ながの", "長野県"]},
    {"prefecture": "岐阜", "pref_code": 21, "aliases": ["Gifu", "gifu", "ぎふ", "岐阜県"]},
    {"prefecture": "静岡", "pref_code": 22, "aliases": ["Shizuoka", "shizuoka", "しずおか", "静岡県"]},
    {"prefecture": "愛知", "pref_code": 23, "aliases": ["Aichi", "aichi", "あいち", "愛知県"]},
    {"prefecture": "三重", "pref_code": 24, "aliases": ["Mie", "mie", "みえ", "三重県"]},
    {"prefecture": "滋賀", "pref_code": 25, "aliases": ["Shiga", "shiga", "しが", "滋賀県"]},
    {"prefecture": "京都", "pref_code": 26, "aliases": ["Kyoto", "kyoto", "きょうと", "京都府"]},
    {"prefecture": "大阪", "pref_code": 27, "aliases": ["Osaka", "osaka", "おおさか", "大阪府"]},
    {"prefecture": "兵庫", "pref_code": 28, "aliases": ["Hyogo", "hyogo", "ひょうご", "兵庫県"]},
    {"prefecture": "奈良", "pref_code": 29, "aliases": ["Nara", "nara", "なら", "奈良県"]},
    {"prefecture": "和歌山", "pref_code": 30, "aliases": ["Wakayama", "wakayama", "わかやま", "和歌山県"]},
    {"prefecture": "鳥取", "pref_code": 31, "aliases": ["Tottori", "tottori", "とっとり", "鳥取県"]},
    {"prefecture": "島根", "pref_code": 32, "aliases": ["Shimane", "shimane", "しまね", "島根県"]},
    {"prefecture": "岡山", "pref_code": 33, "aliases": ["Okayama", "okayama", "おかやま", "岡山県"]},
    {"prefecture": "広島", "pref_code": 34, "aliases": ["Hiroshima", "hiroshima", "ひろしま", "広島県"]},
    {"prefecture": "山口", "pref_code": 35, "aliases": ["Yamaguchi", "yamaguchi", "やまぐち", "山口県"]},
    {"prefecture": "徳島", "pref_code": 36, "aliases": ["Tokushima", "tokushima", "とくしま", "徳島県"]},
    {"prefecture": "香川", "pref_code": 37, "aliases": ["Kagawa", "kagawa", "かがわ", "香川県"]},
    {"prefecture": "愛媛", "pref_code": 38, "aliases": ["Ehime", "ehime", "えひめ", "愛媛県"]},
    {"prefecture": "高知", "pref_code": 39, "aliases": ["Kochi", "kochi", "こうち", "高知県"]},
    {"prefecture": "福岡", "pref_code": 40, "aliases": ["Fukuoka", "fukuoka", "ふくおか", "福岡県"]},
    {"prefecture": "佐賀", "pref_code": 41, "aliases": ["Saga", "saga", "さが", "佐賀県"]},
    {"prefecture": "長崎", "pref_code": 42, "aliases": ["Nagasaki", "nagasaki", "ながさき", "長崎県"]},
    {"prefecture": "熊本", "pref_code": 43, "aliases": ["Kumamoto", "kumamoto", "くまもと", "熊本県"]},
    {"prefecture": "大分", "pref_code": 44, "aliases": ["Oita", "oita", "おおいた", "大分県"]},
    {"prefecture": "宮崎", "pref_code": 45, "aliases": ["Miyazaki", "miyazaki", "みやざき", "宮崎県"]},
    {"prefecture": "鹿児島", "pref_code": 46, "aliases": ["Kagoshima", "kagoshima", "かごしま", "鹿児島県"]},
    {"prefecture": "沖縄", "pref_code": 47, "aliases": ["Okinawa", "okinawa", "おきなわ", "沖縄県"]},
]

if __name__ == "__main__":
    for index, prefecture in enumerate(PREFECTURE_LIST, 1):
        if len(db.search(q.prefecture == prefecture["prefecture"])) == 0:
            db.insert(prefecture)
        else:
            db.update(prefecture, q.prefecture == prefecture["prefecture"])
