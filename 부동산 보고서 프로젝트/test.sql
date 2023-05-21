SELECT
    origin.complexNo,
    origin.complexName,
    origin.sigunguCode,
    origin.bdongCode,
    origin.address,
    origin.totalHouseholdCount,
    origin.useApproveYear,
    CASE
        WHEN origin.useApproveYear >= '2018' THEN "new"
        WHEN origin.useApproveYear < "2018"
        AND origin.useApproveYear >= "2003" THEN "normal"
        WHEN origin.useApproveYear < "2003" THEN "old"
    END AS status,
    origin.supplyArea,
    origin.supplyPyeong,
    origin.jeonyongArea,
    origin.jeonyongPyeong,
    origin.areaSixGroupNo,
    origin.tradeType,
    origin.dealPrice,
    origin.pricePerSupplyPyeong,
    origin.averagePyeong,
    origin.averagePrice,
    origin.isFloor,
    origin.isProcessing1,
    origin.isProcessing2,
    origin.isProcessing3,
    origin.interpolate,
    origin.isReal,
    origin.yearMonth,
    origin.predict,
    realPrice.recentPrice,
    realPrice.subTable
FROM
    `aidepartners.aide.aide_apartment_price_origin` AS origin -- 실거래 업데이트 된 내역을 불러오기 위한 JOIN 과정
    LEFT JOIN (
        -- complex_area_information_prod + complex_real_price_prod
        SELECT
            priceTable.complexNo,
            priceTable.areaSixGroupNo,
            priceTable.dealPrice AS recentPrice,
            priceTable.subTable
        FROM
            (
                SELECT
                    area.complexNo,
                    area.areaSixGroupNo,
                    price.contractDate,
                    price.dealPrice,
                    True AS subTable,
                    ROW_NUMBER() OVER(
                        PARTITION BY dealPrice
                        ORDER BY
                            contractDate DESC
                    ) AS rn
                FROM
                    `aidepartners.aide.complex_area_information_prod` AS area
                    LEFT JOIN (
                        SELECT
                            complexNo,
                            areaNo,
                            contractDate,
                            dealPrice
                        FROM
                            `aidepartners.aide.complex_real_price_prod`
                        WHERE
                            deleteYn is null
                            AND tradeType = 'A1'
                    ) AS price ON area.complexNo = price.complexNo
                    AND area.pyeongNo = price.areaNo
            ) AS priceTable
        WHERE
            priceTable.rn = 1
    ) AS realPrice ON origin.complexNo = realPrice.complexNo
    AND origin.areaSixGroupNo = realPrice.areaSixGroupNo
WHERE
    origin.yearMonth >= '2013-01-01'
    AND origin.totalHouseholdCount >= 100
    AND origin.complexNo IN (
        SELECT
            complexNo
        FROM
            `aidepartners.aide.complex_danji_information`
        WHERE
            (
                sigunguCode = "{sigunguCode}"
                OR ST_DISTANCE(
                    st_geogpoint({ lon }, { lat }),
                    st_geogpoint(longitude, latitude)
                ) <= 2000
            )
            AND realEstateTypeName = '아파트'
    )
    AND origin.areaSixGroupNo = 'A1'