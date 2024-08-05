import pandas as pd

news_dict = pd.read_json('news_dict.json', orient='records')

search_id = "v-tatarstane-27-iyulya-dnyom-v-zapadnykh-rayonakh-ozhidayutsya-dozhd"

if search_id in news_dict:
    print("Новость уже есть в словаре, пропускаем итерацию")
else:
    print("Свежая новость, добавляем в словарь")