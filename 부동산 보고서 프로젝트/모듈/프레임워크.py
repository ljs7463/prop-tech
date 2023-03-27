from dataclasses import dataclass


class FeasibilityTest:
    def __init__(self, sidoName, sigunguName, bdongName, danjiName):
        self.sidoName = sidoName
        self.sigunguName = sigunguName
        self.bdongName = bdongName
        self.danjiName = danjiName

    def duplicateTest(self):
        """단지명 중복여부 및 오입력 확인 및 코드추출 -> 추후에 데코레이터로 생성"""
        sql = f"""
        SELECT sidoCode, sigunguCode, bdongCode, complexNo
        FROM `aidepartners.aide.complex_danji_information`
        WHERE sigunguName LIKE "%{self.sidoName}%"
              AND sigunguName LIKE "%{self.sigunguName}%"
              AND bdongName LIKE "%{self.bdongName}%"
              AND complexName = "{self.danjiName}"
        """
        dupl = BH.read_table(sql)

        # 중복검증
        if len(dupl) != 1:
            raise Exception("동일한 단지명으로 중복이 있습니다.")
        else:
            sidoCode, sigunguCode, bdongCode, complexNo = dupl.iloc[0]
            return sidoCode, sigunguCode, bdongCode, complexNo

    def regionData(self, sidoCode, sigunguCode, bdongCode, complexNo):
        """입력 단지에 해당하는 지역별 데이터 프레임 생성"""
        sql = f"""
        SELECT *
        FROM `aidepartners.aide.aide_apartment_price_origin`
        WHERE yearMonth >= '2018-01-01'
              AND sidoCode = '{sidoCode}'
              AND ((isReal = True) or (predict = True))
        """
        # 시도
        df = BH.read_table(sql)
        # 입력단지
        df_danji = df[df["complexNo"] == complexNo].reset_index(drop=True)
        return df, df_danji

    def danjiPrice(self, df_danji):
        """입력단지의 면적 그룹별 가격추이"""

        # 면적그룹 리스트
        areaList = list(df_danji["areaSixGroupNo"].unique())

        # viz
        fig = plt.figure(figsize=(14, 5))
        sns.lineplot(
            df_danji["yearMonth"],
            df_danji["averagePyeong"],
            hue=df_danji["areaSixGroupNo"],
        )

        # y축 설정
        current_values = plt.gca().get_yticks()
        plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])

        # grid 설정
        plt.grid(axis="y", c="lightgray")
        plt.grid(axis="x", c="lightgray")

        # 결과 이미지 객체로 저장
        graph = fig

        # 이미지 not show
        plt.close(fig)
        return fig

    def regionPrice(self, df):
        """시도, 시군구, 법정동 평당가 평균의 추이"""
        df[df["isReal"] == True].groupby("yearMonth")["averagePyeong"].mean()

