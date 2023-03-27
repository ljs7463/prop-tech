class search:
    def searchDanji(self, sido, sigungu, danji):
        """ 단지를 특정하는 기능"""

        sql = f"""
        SELECT complexNo,
            complexName, 
            sidoCode, 
            sigunguCode,
            bdongCode,
            sigunguName,
            bdongName,
            address, 
            detailAddress
        FROM `aidepartners.aide.complex_danji_information`
        WHERE sigunguName LIKE '%{sido}%' 
              AND sigunguName LIKE '%{sigungu}%' 
              AND complexName LIKE "%{danji}%" 
              AND realEstateTypeName IN ('아파트','아파트분양권')
        
        """
        search = BH.read_table(sql)
        sidoCode, sigunguCode, bdongCode, complexNo = search[
            ["sidoCode", "sigunguCode", "bdongCode", "complexNo"]
        ].iloc[0]
        return sidoCode, sigunguCode, bdongCode, complexNo


class apartProcessing:
    def __init__(self, sidoCode, sigunguCode, bdongCode, complexNo):
        self.sidoCode = sidoCode
        self.sigunguCode = sigunguCode
        self.bdongCode = bdongCode
        self.complexNo = complexNo

    # def extractTargetPrice(self):
    #     """입력받은 단지에 해당하는 실거래 시계열데이터 반환함수"""
    #     sql = f"""
    #     SELECT *
    #     FROM `aidepartners.aide.aide_apartment_price_origin`
    #     WHERE complexNo = "{self.complexNo}"
    #     """
    #     df_target = BH.read_table(sql)
    #     # 날짜 형변환
    #     df_target['yearMonth'] =pd.to_datetime(df_target['yearMonth'])
    #     return df_target

    def regionPrice(self):
        """시도, 시군구, 법정동별 가격 추이"""
        # 입력단지와 같은 시도에 있는 데이터 추출
        sql = f"""
        SELECT *
        FROM `aidepartners.aide.aide_apartment_price_origin`
        WHERE sidoCode = "{self.sidoCode}"
              AND isReal = True
              AND yearMonth >= "2018-03-01"
        """
        df_total = BH.read_table(sql)
        df_target = (
            df_total[df_total["complexNo"] == self.complexNo]
            .sort_values(by="yearMonth", ascending=False)
            .reset_index(drop=True)
        )
        df_sido = df_total.groupby("yearMonth")["averagePyeong"].mean().reset_index()
        df_sigungu = (
            df_total[df_total["sigunguCAode"] == self.sigunguCode]
            .groupby("yearMonth")["averagePyeong"]
            .mean()
            .reset_index()
        )
        df_bdong = (
            df_total[df_total["bdongCode"] == self.bdongCode]
            .groupby("yearMonth")["averagePyeong"]
            .mean()
            .reset_index()
        )

        return df_target, df_sido, df_sigungu, df_bdong

