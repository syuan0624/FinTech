# 公告

課程:107-2【金融科技-文字探勘與機器學習】  
****
組別:Team 7
成員:
* 沈沛瑄:工海所 碩一 R07525056  
* 林正雄:經濟所 碩二 R05323045  
* 張家郡:網媒所 碩一 R07944036

## HW1

-  ETF爬蟲

    >在所指定的 ETF 資料中，篩選出於 2015 年年底前既已存在的 ETF ，利用爬蟲方法整理出上述篩選後的 ETF 集合中，其每一檔 ETF 的每日收盤價，時間範圍從該 ETF 於 2015 年 年底最後一個交易日起至程式執行的當下，將每日的資料都抓下來，並將整理好的資料彙整在 pandas 的 dataframe。

- 財金指標爬蟲

    >工業生產指數：  
    說明：Fed在2014年編制的一個全新的「勞動市場狀況指數」，這指數綜合了包括非農、勞動市場參與率、空缺數、離職率、失業率及平均薪資等19個就業領域。  
    資料來源 : [Fed](https://www.federalreserve.gov/releases/g17/Current/default.htm ) 

## HW2

- NER標記
    >以NER(Named Entity Recognition) [套件](https://github.com/Determined22/zh-NER-TF)將初步整理過格式的客服資料進行標記，定義人名與事件。

- TDM(Term-document matrix)
    >將Document裡面的各個單詞以視覺化方式呈現彼此間的關係, 用來進行初步檢驗、觀察Document內是否有可進一步分析的現象。

- Co-Occurence Matrix
    >將TDM轉成以term與input sentence間的關係列表,來觀察每個term在各個input sentence中出現的次數。 