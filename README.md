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

-  資料收集與文字探勘共現性進行資料視覺化
    >文字探勘淘金：從客服聯繫紀錄找出淺在銷售機會  
    1.針對自訂議題收集相關文本  
    2.將收集到的文本用NER挑選出【自定義類別】  
    3.將文件與有分類過的單詞進行TDM(term to matrix)  
    4.將TDM轉成Co-Occurrence Matrix  
    5.繪製出各類別之間的共現圖

    - NER標記
        >以NER(Named Entity Recognition) [套件](https://github.com/Determined22/zh-NER-TF)將初步整理過格式的客服資料進行標記，定義人名與事件。

    - TDM(Term-document matrix)
        >將Document裡面的各個單詞以視覺化方式呈現彼此間的關係, 用來進行初步檢驗、觀察Document內是否有可進一步分析的現象。

    - Co-Occurence Matrix
        >將TDM轉成以term與input sentence間的關係列表,來觀察每個term在各個input sentence中出現的次數。 
## HW3
- 介紹評比績效指標
    - 請每組繳交至少兩頁的 word 檔案，說明使用的指標，並上傳到作業區中，有關介紹指標的部分，請盡量包含下面 4 點:  
    >1. 介紹指標的由來，例如發明人或是提出的機構
    >2. 介紹這個指標的內涵，包含如何計算
    >3. 介紹指標的依據，根據甚麼樣的財務理論或是邏輯來建立
    >4. 指標的應用面，例如有那些著名的機構有採用你這個指標

## HW4

- ETF評比績效理論實作  
    - 使用以下3篇論文作為評估ETF之指標的實作，評比指標如A,B,C三項  
    >A.2009_JBF_Portfolio performance evaluation with generalized Sharpe ratios_ASKSR : 使用第38式  
    >B.2011_JBF_Omega performance measure and portfolio insurance : 使用第8式，L=無風險利率  
    >C.2013_EL_A global index of riskiness : 使用P.494頁中的Q(g)  

## Final Project

- 我們的專案選擇呈現在LineBot上面，野村證券原先也擁有LineBot，主要針對原先內容提出兩個擴充功能：  
    >1. 使用LineBot進行開戶教學，方便客戶查看開戶表單的填寫方式，希望能提高開戶率。  
    >2. 直接在LineBot上與真人客服聯繫，同時記錄對話文字內容，並可以將這些文字內容導回HW2所提的EDA流程。  
    >Demo影片：[107-2_Fintech_第7組_Demo影片](https://youtu.be/F34ItE4Rwvw)  

