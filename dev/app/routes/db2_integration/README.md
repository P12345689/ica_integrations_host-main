# db2_integration Integration

This integration provides functionality for Connect and Fetch data from an IBM DB2 Warehouse.

## Usage

To use this integration, follow these steps:

1. Set up the necessary environment variables (e.g., `DB2_DATABASE`, `DB2_HOSTNAME`, `DB2_PORT`, `DB2_UID`, `DB2_PWD`, `DB2_SSL_CONN`, `DB2_SSL_TRUST_STORE`, `DB2_SSL_PSS`, `DB2_JDBC_DRIVER`, `DB2_DRIVER_JAR`).

## API Endpoints

### POST /system/db2_integration/fetch_data_with_truststore/invoke

Fetch data from an IBM DB2 Warehouse that has an SSL Truststore. Example here is querying from the IBM Cognitive Marketing Data Platform (CMDP)

```bash
curl --location --request POST 'http://localhost:8080/system/db2_integration/fetch_data_with_truststore/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{"query": "select * from V2REFR2.V_REF_UT_BRAND", "num_rows": 2}' | jq
```

```json
{
  "status": "success",
  "invocationId": "98a069cd-c645-447f-aeac-4f4aadea2d6a",
  "response": [
    {
      "data": "[{\"UT_CD\":\"30GQH\",\"UT_DSCR\":\"6941-14V Support as a Service for Lenovo\",\"UT_LVL\":\"30\",\"PARENT_UT_CD\":\"20G73\",\"UT_LVL_10_CD\":\"10C00\",\"UT_LVL_10_DSCR\":\"IBM Infrastructure\",\"UT_LVL_15_CD\":\"15TSS\",\"UT_LVL_15_DSCR\":\"Technology Lifecycle Services\",\"UT_LVL_17_CD\":\"17MVS\",\"UT_LVL_17_DSCR\":\"Multivendor Services\",\"UT_LVL_20_CD\":\"20G73\",\"UT_LVL_20_DSCR\":\"Support as a Service and non-Data Center Support\",\"UT_LVL_30_CD\":\"30GQH\",\"UT_LVL_30_DSCR\":\"6941-14V Support as a Service for Lenovo\",\"MAP_TO_UT_CD\":null,\"EFF_FROM_DT\":\"2023-12-11\",\"EFF_TO_DT\":\"9999-12-31\",\"PUB_DT\":\"2023-12-11\",\"REC_TYPE\":\"add\",\"INACT_FLG\":\"N\",\"CREATE_TS\":\"2023-12-11 17:02:56.910498\",\"UPDT_TS\":\"2024-04-08 17:02:01.776687\",\"PLG_FLG\":null,\"TECH_FLG\":null},{\"UT_CD\":\"30G48\",\"UT_DSCR\":\"6941-11D Expert Labs zSys&LinuxONE Svcs TLS Sales Withdrawn\",\"UT_LVL\":\"30\",\"PARENT_UT_CD\":\"20GOP\",\"UT_LVL_10_CD\":\"10C00\",\"UT_LVL_10_DSCR\":\"IBM Infrastructure\",\"UT_LVL_15_CD\":\"15TSS\",\"UT_LVL_15_DSCR\":\"Technology Lifecycle Services\",\"UT_LVL_17_CD\":\"17O5H\",\"UT_LVL_17_DSCR\":\"Technology Services Withdrawn\",\"UT_LVL_20_CD\":\"20GOP\",\"UT_LVL_20_DSCR\":\"TLS - Technology Services Withdrawn\",\"UT_LVL_30_CD\":\"30G48\",\"UT_LVL_30_DSCR\":\"6941-11D Expert Labs zSys&LinuxONE Svcs TLS Sales Withdrawn\",\"MAP_TO_UT_CD\":\"30CF5\",\"EFF_FROM_DT\":\"2024-01-08\",\"EFF_TO_DT\":\"9999-12-31\",\"PUB_DT\":\"2023-07-10\",\"REC_TYPE\":\"update\",\"INACT_FLG\":\"N\",\"CREATE_TS\":\"2023-01-09 17:02:35.567138\",\"UPDT_TS\":\"2024-04-08 17:02:01.776687\",\"PLG_FLG\":null,\"TECH_FLG\":null}]"
    }
  ]
}
```

### POST /system/db2_integration/fetch_data_without_truststore/invoke

Fetch data from an IBM DB2 Warehouse that does not have an SSL Truststore. Example here is querying from the Marketing Analyst Data Repository (ADR) and pulling geography codes and information.

```bash
curl --location --request POST 'http://localhost:8080/system/db2_integration/fetch_data_without_truststore/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{"query": "SELECT * FROM adr.SRC_EPM_DIM_GEOGRAPHY_ACTIVE", "num_rows": 2}' | jq
```

```json
{
  "status": "success",
  "invocationId": "58ce56e2-c1c9-4332-9954-24106e397462",
  "response": [
    {
      "data": "[{\"ETL_KEY\":942616,\"DATA_KEY\":\"25629e2b07253f61e50226aef291ef67\",\"RUN_SEQ\":177750,\"SRC_DELETED\":\"U\",\"EXTR_TS\":\"2024-09-05 06:44:21.894432\",\"SK_COUNTRY\":1482,\"SK_COUNTRY_MEASUREMENT\":-1,\"SK_REGION\":-1,\"SK_GEO_MARKET\":-1,\"SK_GEOGRAPHY\":-1,\"SK_TOTAL_GEOGRAPHY\":-1,\"COUNTRY_CODE\":\"LEA\",\"COUNTRY_NAME\":null,\"COUNTRY_NAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEDIUM_NAME\":null,\"COUNTRY_MEDIUM_NAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_SHORTNAME\":null,\"COUNTRY_SHORTNAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEASUREMENT_CODE\":\"Unassigned\",\"COUNTRY_MEASUREMENT_CODE_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEASUREMENT_NAME\":\"Unassigned\",\"COUNTRY_MEASUREMENT_NAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEASUREMENT_MEDIUM_NAME\":\"Unassigned\",\"COUNTRY_MEASUREMENT_MEDIUM_NAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEASUREMENT_SHORTNAME\":\"Unassigned\",\"COUNTRY_MEASUREMENT_SHORTNAME_USTOP_VIEW\":\"Unassigned\",\"REGION_CODE\":\"Unassigned\",\"REGION_CODE_USTOP_VIEW\":\"Unassigned\",\"REGION_NAME\":\"Unassigned\",\"REGION_NAME_USTOP_VIEW\":\"Unassigned\",\"REGION_MEDIUM_NAME\":\"Unassigned\",\"REGION_MEDIUM_NAME_USTOP_VIEW\":\"Unassigned\",\"REGION_SHORTNAME\":\"Unassigned\",\"REGION_SHORTNAME_USTOP_VIEW\":\"Unassigned\",\"MARKET_CODE\":\"Unassigned\",\"MARKET_CODE_USTOP_VIEW\":\"Unassigned\",\"MARKET_NAME\":\"Unassigned\",\"MARKET_NAME_USTOP_VIEW\":\"Unassigned\",\"MARKET_MEDIUM_NAME\":\"Unassigned\",\"MARKET_MEDIUM_NAME_USTOP_VIEW\":\"Unassigned\",\"MARKET_SHORTNAME\":\"Unassigned\",\"MARKET_SHORTNAME_USTOP_VIEW\":\"Unassigned\",\"GEOGRAPHY_CODE\":\"Unassigned\",\"GEOGRAPHY_NAME\":\"Unassigned\",\"GEOGRAPHY_MEDIUM_NAME\":\"Unassigned\",\"GEOGRAPHY_SHORTNAME\":\"Unassigned\",\"GEOGRAPHY_COMPLIANCE_CODE\":\"Unassigned\",\"TOTAL_GEOGRAPHY_CODE\":\"Unassigned\",\"TOTAL_GEOGRAPHY_NAME\":\"Unassigned\",\"TOTAL_GEOGRAPHY_MEDIUM_NAME\":\"Unassigned\",\"TOTAL_GEOGRAPHY_SHORTNAME\":\"Unassigned\",\"TOTAL_GEOGRAPHY_COMPLIANCE_CODE\":\"Unassigned\",\"IBM_GLOBAL_CODE\":null,\"IBM_GLOBAL_NAME\":null,\"IBM_GLOBAL_MEDIUM_NAME\":null,\"IBM_GLOBAL_SHORTNAME\":null,\"AUDIT_TIMESTAMP\":\"2024-09-04 14:27:49.633993\"},{\"ETL_KEY\":941829,\"DATA_KEY\":\"25629e2b07253f61e50226aef291ef67\",\"RUN_SEQ\":177750,\"SRC_DELETED\":\"U\",\"EXTR_TS\":\"2024-09-05 06:44:21.894432\",\"SK_COUNTRY\":1001,\"SK_COUNTRY_MEASUREMENT\":-1,\"SK_REGION\":-1,\"SK_GEO_MARKET\":-1,\"SK_GEOGRAPHY\":-1,\"SK_TOTAL_GEOGRAPHY\":-1,\"COUNTRY_CODE\":\"080\",\"COUNTRY_NAME\":null,\"COUNTRY_NAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEDIUM_NAME\":null,\"COUNTRY_MEDIUM_NAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_SHORTNAME\":null,\"COUNTRY_SHORTNAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEASUREMENT_CODE\":\"Unassigned\",\"COUNTRY_MEASUREMENT_CODE_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEASUREMENT_NAME\":\"Unassigned\",\"COUNTRY_MEASUREMENT_NAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEASUREMENT_MEDIUM_NAME\":\"Unassigned\",\"COUNTRY_MEASUREMENT_MEDIUM_NAME_USTOP_VIEW\":\"Unassigned\",\"COUNTRY_MEASUREMENT_SHORTNAME\":\"Unassigned\",\"COUNTRY_MEASUREMENT_SHORTNAME_USTOP_VIEW\":\"Unassigned\",\"REGION_CODE\":\"Unassigned\",\"REGION_CODE_USTOP_VIEW\":\"Unassigned\",\"REGION_NAME\":\"Unassigned\",\"REGION_NAME_USTOP_VIEW\":\"Unassigned\",\"REGION_MEDIUM_NAME\":\"Unassigned\",\"REGION_MEDIUM_NAME_USTOP_VIEW\":\"Unassigned\",\"REGION_SHORTNAME\":\"Unassigned\",\"REGION_SHORTNAME_USTOP_VIEW\":\"Unassigned\",\"MARKET_CODE\":\"Unassigned\",\"MARKET_CODE_USTOP_VIEW\":\"Unassigned\",\"MARKET_NAME\":\"Unassigned\",\"MARKET_NAME_USTOP_VIEW\":\"Unassigned\",\"MARKET_MEDIUM_NAME\":\"Unassigned\",\"MARKET_MEDIUM_NAME_USTOP_VIEW\":\"Unassigned\",\"MARKET_SHORTNAME\":\"Unassigned\",\"MARKET_SHORTNAME_USTOP_VIEW\":\"Unassigned\",\"GEOGRAPHY_CODE\":\"Unassigned\",\"GEOGRAPHY_NAME\":\"Unassigned\",\"GEOGRAPHY_MEDIUM_NAME\":\"Unassigned\",\"GEOGRAPHY_SHORTNAME\":\"Unassigned\",\"GEOGRAPHY_COMPLIANCE_CODE\":\"Unassigned\",\"TOTAL_GEOGRAPHY_CODE\":\"Unassigned\",\"TOTAL_GEOGRAPHY_NAME\":\"Unassigned\",\"TOTAL_GEOGRAPHY_MEDIUM_NAME\":\"Unassigned\",\"TOTAL_GEOGRAPHY_SHORTNAME\":\"Unassigned\",\"TOTAL_GEOGRAPHY_COMPLIANCE_CODE\":\"Unassigned\",\"IBM_GLOBAL_CODE\":null,\"IBM_GLOBAL_NAME\":null,\"IBM_GLOBAL_MEDIUM_NAME\":null,\"IBM_GLOBAL_SHORTNAME\":null,\"AUDIT_TIMESTAMP\":\"2024-09-04 14:27:49.633993\"}]"
    }
  ]
}
```