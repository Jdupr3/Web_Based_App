select "LPN", "Item", "Reference_LPN_Nbr", "Bar_Cd", "Initial_Qty", "LPN_Size_Qty", "LPN_Chute_Cd", "Key", "Key2", INBOUND_OUTBOUND_INDICATOR, LPN_STATUS, LPN_FACILITY_STATUS,
LISTAGG("GRP_TYPE" , ', ')
within group (order by "LPN", "Item", "Reference_LPN_Nbr", "Bar_Cd", "Initial_Qty", "LPN_Size_Qty", "LPN_Chute_Cd", "Key", "Key2", INBOUND_OUTBOUND_INDICATOR, LPN_STATUS, LPN_FACILITY_STATUS) VAS_CODE
from (
SELECT
  "LPN_for_Orders"."TC_LPN_ID" AS "LPN",
  "Items_for_LPN_Dtl_Orders"."ITEM_NAME"                                                     AS "Item",
   CASE
    WHEN ("LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='O')
    THEN "LPN_for_Orders"."TC_REFERENCE_LPN_ID"
    WHEN "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='I'
    THEN "LPN_for_Orders"."TC_LPN_ID"
    ELSE "LPN_for_Orders"."TC_LPN_ID"
  END AS "Reference_LPN_Nbr",
  "Items_for_LPN_Dtl_Orders"."ITEM_BAR_CODE"                                                 AS "Bar_Cd",
   "LPN_DETAIL_for_Orders"."INITIAL_QTY"                                                      AS "Initial_Qty",
 "LPN_DETAIL_for_Orders"."SIZE_VALUE"                                                  AS "LPN_Size_Qty",
  "LPN_for_Orders"."CHUTE_ID"                                                                AS "LPN_Chute_Cd",
   CONCAT(CASE
    WHEN ("LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='O')
    THEN "LPN_for_Orders"."TC_REFERENCE_LPN_ID"
    WHEN "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='I'
    THEN "LPN_for_Orders"."TC_LPN_ID"
    ELSE "LPN_for_Orders"."TC_LPN_ID"
  END, "Items_for_LPN_Dtl_Orders"."ITEM_BAR_CODE") AS "Key",
CONCAT(CASE
    WHEN ("LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='O')
    THEN "LPN_for_Orders"."TC_LPN_ID"
    WHEN "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='I'
    THEN "LPN_for_Orders"."TC_LPN_ID"
    ELSE "LPN_for_Orders"."TC_REFERENCE_LPN_ID"
  END, "Items_for_LPN_Dtl_Orders"."ITEM_BAR_CODE") AS "Key2",
  "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR",
  "LPN_for_Orders"."LPN_STATUS",
  "LPN_for_Orders"."LPN_FACILITY_STATUS",
  "VAS_CARTON"."GRP_TYPE"

FROM "NIKEWM1014PRD"."LPN" "LPN_for_Orders"
INNER JOIN "NIKEWM1014PRD"."LPN_DETAIL" "LPN_DETAIL_for_Orders"
ON "LPN_for_Orders"."LPN_ID" = "LPN_DETAIL_for_Orders"."LPN_ID"

INNER JOIN "NIKEWM1014PRD"."LPN_DETAIL" "LPN_DETAIL_for_Orders"
ON "LPN_for_Orders"."LPN_ID" = "LPN_DETAIL_for_Orders"."LPN_ID"


INNER JOIN
  (SELECT "ITEM_CBO"."ITEM_BAR_CODE" AS "ITEM_BAR_CODE",
    "ITEM_CBO"."ITEM_ID"             AS "ITEM_ID",
    "ITEM_CBO"."ITEM_NAME"           AS "ITEM_NAME"
  FROM "NIKEWM1014PRD"."ITEM_CBO" "ITEM_CBO"
  INNER JOIN "NIKEWM1014PRD"."ITEM_FACILITY_MAPPING_WMS" "ITEM_FACILITY_MAPPING_WMS"
  ON "ITEM_CBO"."ITEM_ID" = "ITEM_FACILITY_MAPPING_WMS"."ITEM_ID"
  INNER JOIN "NIKEWM1014PRD"."ITEM_WMS" "ITEM_WMS"
  ON "ITEM_CBO"."ITEM_ID"                                           = "ITEM_WMS"."ITEM_ID"
  ) "Items_for_LPN_Dtl_Orders" ON "LPN_DETAIL_for_Orders"."ITEM_ID" = "Items_for_LPN_Dtl_Orders"."ITEM_ID"

left outer join "NIKEWM1014PRD"."VAS_CARTON" "VAS_CARTON" on "LPN_for_Orders"."TC_LPN_ID" = "VAS_CARTON"."CARTON_NBR"
and
"LPN_DETAIL_for_Orders"."LPN_DETAIL_ID" = "VAS_CARTON"."CARTON_DTL_ID"

WHERE "LPN_for_Orders"."LPN_TYPE"                                  <> 2
AND
  --"LPN_for_Orders"."LPN_FACILITY_STATUS" = 20 And
  (("LPN_for_Orders"."TC_REFERENCE_LPN_ID"       = '' AND "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='O' AND SUBSTR("LPN_for_Orders"."TC_REFERENCE_LPN_ID",1,3)<>'003')
OR ("LPN_for_Orders"."TC_LPN_ID"                 = '00089949010006563923' AND "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='I')
OR ("LPN_for_Orders"."TC_LPN_ID"                 = '' AND "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR"='O'))
AND ("LPN_DETAIL_for_Orders"."SIZE_VALUE" > 0)


GROUP BY "LPN_for_Orders"."TC_LPN_ID" ,
  "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR",
"LPN_for_Orders"."TC_REFERENCE_LPN_ID" ,
  "Items_for_LPN_Dtl_Orders"."ITEM_BAR_CODE" ,
  "Items_for_LPN_Dtl_Orders"."ITEM_NAME" ,
  "LPN_for_Orders"."CHUTE_ID",
  "LPN_for_Orders"."INBOUND_OUTBOUND_INDICATOR",
  "LPN_for_Orders"."LPN_STATUS",
  "LPN_for_Orders"."LPN_FACILITY_STATUS"
  ,"LPN_DETAIL_for_Orders"."SIZE_VALUE",
  "LPN_DETAIL_for_Orders"."INITIAL_QTY",
  "VAS_CARTON"."GRP_TYPE"
  ) FULLQRY
  group by  "LPN", "Item", "Reference_LPN_Nbr", "Bar_Cd", "Initial_Qty", "LPN_Size_Qty", "LPN_Chute_Cd", "Key", "Key2", INBOUND_OUTBOUND_INDICATOR, LPN_STATUS, LPN_FACILITY_STATUS