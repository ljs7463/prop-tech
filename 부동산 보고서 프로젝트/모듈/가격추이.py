class apartTimePrice():
    
    def __init__(self, sido, sigungu, name):
        """검색하고자 하는 시도명, 시군구명, 단지명을 입력받는다."""
        self.sido = sido
        self.sigungu = sigungu
        self.name = name
        
    def extractCode(self):
        """지역 코드 추출"""        
        sql = f"""
        SELECT sidoCode,
               sigunguCode,
        FROM `aidepartners.aide.code_sigungu`
        WHERE sidoName LIKE '%{self.sido}%'
              AND sigunguName LIKE '%{self.sigungu}%'
              AND ((isMulti = True AND guLevel = True AND siLevel = False) OR (isMulti = False AND guLevel = True AND siLevel = True))
        """
        code_data = BH.read_table(sql)
        if len(code_data) >1:
            raise Exception('입력받은 시도,시군구의 코드가 중복이 있습니다. 확인해 주세요') 
            
        else:
            sidoCode = code_data['sidoCode'][0]
            sigunguCode = code_data['sigunguCode'][0]
            
        return sidoCode, sigunguCode
        
        
    def extractDanjiName(self,sidoCode, sigunguCode):
        """단지 특정 및 추출"""

        sql = f"""
        SELECT complexNo, 
               complexName,
               address
        FROM `aidepartners.aide.complex_danji_information`
        WHERE sidoCode = "{sidoCode}"
              AND sigunguCode = "{sigunguCode}"
              AND complexName LIKE '%{self.name}%'        
        """
        danji_data = BH.read_table(sql)
        if len(danji_data) > 1:
            print('중복되는 단지들이 있습니다. 단지를 선택해주세요')
            print('-'*130)
            print('단지목록 : ',list(danji_data['complexName'].unique()))  
            print('-'*130)
            print('주소목록 : ',list(danji_data['address'].unique()))
            print('-'*130)
            answerName = input('앞에서 출력된 단지들중 해당하는 단지를 정확하게 입력해 주세요 : ')
            answerAddress = input('앞에서 출력된 주소중 해당하는 단지의 주소를 정확하게 입력해 주세요 : ')
            cNo = danji_data.loc[(danji_data['complexName']==answerName)&(danji_data['address']==answerAddress),'complexNo'].reset_index(drop = True)[0]
       
        else:
            answerName = danji_data['complexName'].reset_index(drop = True)[0]
            cNo = danji_data.loc[danji_data['complexName']==answerName,'complexNo'][0]
            
            
        return cNo
    
    
    def extractTargetPrice(self):
        """기준단지의 시계열 가격 데이터 추출"""
        
        # 시도, 시군구 코드 추출
        sidoCode, sigunguCode = self.extractCode()
        
        # 단지명 추출
        cNo = self.extractDanjiName(sidoCode, sigunguCode)
        
    
        # 타겟 단지의 실거래 시계열데이터 프레임 추출
        """입력받은 단지에 해당하는 실거래 시계열데이터 반환함수"""
        sql = f"""
        SELECT *
        FROM `aidepartners.aide.aide_apartment_price_origin`
        WHERE complexNo = "{cNo}"
        """
        df_target = BH.read_table(sql)

        if len(df_target) == 0:
            print('단지를 찾지못했습니다.')
        else:
            bdongCode = df_target['bdongCode'].iloc[0]
            
        df_target['yearMonth'] =pd.to_datetime(df_target['yearMonth'])
        return df_target, bdongCode
    
    def recentPrice(self):
        df_target, bdongCode = self.extractTargetPrice()
        startyear = datetime.now()-relativedelta(years = 5)
        sql = f"""
        SELECT *
        FROM `aideprtners.aide.aide_apartment_price_origin`
        WHERE sidoCode LIKE '{bdongCode[:2]}%'
              AND isReal = True
              AND yearMonth >={startYear}
        """
        df_sido = BH.read_table(sql)
        
        pass
#         BH.read_table(sql)
    
    
        
