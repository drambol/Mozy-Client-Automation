# Created by zhangj79 at 3/20/17
Feature: Bifrost Testcases for Dell-Mozy Integration
  Dell-Mozy Integration Scenario Test

  @integration-bus @mozy_dell_integration-001 @BIFROST-3043
  Scenario: Create a new MozyPro partner, and check billing report, suspend partner
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name |
      | test automation admin | test automation dell mozypro partner - DELL-INTEGRATION-001  |
    When I log in BUS console to select my partner info
      | partner name |
      | test automation dell mozypro partner |
    Then I create a report
      | report type     | report name             |
      | Billing Summary | test automation report  |
    When I suspend the new created partner
    When I delete the new created partner

  @verify-license-total @mozy_dell_integration-002 @BIFROST-3069
  Scenario: Create a new MozyPro partner, provision 1k licenses and check get /accounts/licenses response,check total count value
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name |
      | test automation admin | clientQAAuomtaion_Bifrost_1000_licenses  |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1000     |
    When I get licenses for the partner
      | exclude sub-partner | license type |
      | true                |  Desktop     |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1001  |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1000   | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 0     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1000   | 0     |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 0     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 90     | 909   |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 909   |
        When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 90     | 910   |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 910   |
        When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 90     | 911   |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 910   |
    When I delete the new created partner

  @verify-license-total @mozy_dell_integration-003 @BIFROST-3069
  Scenario: Create a new MozyPro partner, provision 2k licenses and check get /accounts/licenses response,check total count value
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name |
      | test automation admin | clientQAAuomtaion_Bifrost_2000_licenses |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1000     |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1000     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1      | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1      | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1      | 1001  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 0     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 0     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 1001  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1000   | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1     |
     When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1000   | 10    |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 10  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1000   |  999  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1000   | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1000   | 1001  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1001   | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1001   | 10    |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 10    |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1001   | 998   |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 998   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1001   | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1001   | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1001   | 1001  |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1999   | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1999   | 2     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 2000   | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 0     |
    When I delete the new created partner

  @verify-license-total @mozy_dell_integration-004 @BIFROST-3069
  Scenario: Create a new MozyPro partner, provision 1001 licenses and check get /accounts/licenses response,check total count value
    1.offset=0 and limit=1
    2.offset=0 and limit=999
    3.offset=0 and limit=1000
    4.offset=0 and limit=1001
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                    |
      | test automation admin | clientQAAuomtaion_Bifrost_1001_licenses |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1000     |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1        |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 1001   | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 1001   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 1001   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1001  |
    Then get licenses response detail should be
      | total  | count |
      | 1001   | 1000  |
    When I delete the new created partner

  @verify-license-total @mozy_dell_integration-005 @BIFROST-3069
  Scenario: Create a new MozyPro partner, provision 999 licenses and check get /accounts/licenses response,check total count value
    1.offset=0 and limit=1
    2.offset=0 and limit=998
    3.offset=0 and limit=999
    4.offset=0 and limit=1000
    5.offset=0 and limit=1001
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                    |
      | test automation admin | clientQAAuomtaion_Bifrost_999_licenses  |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 999      |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 999    | 1     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 998   |
    Then get licenses response detail should be
      | total  | count |
      | 999    | 998   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 999    | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 999    | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1001  |
    Then get licenses response detail should be
      | total  | count |
      | 999    | 999   |
    When I delete the new created partner

  @verify-license-total @mozy_dell_integration-006 @BIFROST-3069
  Scenario: Create a new MozyPro partner, provision 0 licenses and check get /accounts/licenses response,check total count value
    1.offset=0 and limit=0
    2.offset=0 and limit=1
    3.offset=0 and limit=1000
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                  |
      | test automation admin | clientQAAuomtaion_Bifrost_0_licenses  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 0     |
    Then get licenses response detail should be
      | total  | count |
      | 0      | 0     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1     |
    Then get licenses response detail should be
      | total  | count |
      | 0      | 0     |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 0      | 0     |
    When I delete the new created partner

  @verify-license-total @sub-partners @mozy_dell_integration-007 @BIFROST-3069
  Scenario: Create a new MozyPro partner, provision 2k licenses,create sub-partner provision 200 licenses and check get /accounts/licenses response,check total count value
    When I create 1 DellMozyPro new partner with
      | admin fullname        | admin password | name |
      | test automation admin | QAP@SSw0rd     | clientQAAutomation_Bifrost_2000_licenses_parent_partner |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1000     |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1000     |
    When I log in BUS console as bifrost new created partner
    When I add a new pro plan for the partner
      | name    | periods | server licenses price | server min licenses | server quota price | desktop licenses price | desktop min licenses | desktop quota price |
      | default | monthly | 1                     |  1                  | 1                  | 1                      | 1                    | 1                   |
    When I add a new role for the partner
      | name    | include all |
      | default | false        |
    When I create 1 DellSubPartner new partner with
      | name                                                  |
      | clientQAAutomation_Bifrost_200_licenses_sub_partner  |
    When I provision license for the subpartner
      | license type | licenses |
      | Desktop      | 200      |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | false               |  Desktop     | 1      | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 2200   | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | false               |  Desktop     | 1199   | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 2200   | 1000  |
   When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | false               |  Desktop     | 1199   | 1001  |
    Then get licenses response detail should be
      | total  | count |
      | 2200   | 1000  |
   When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 999    | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 2000   | 999   |
    When I delete the new created partner

  @verify-license-total @sub-partners @mozy_dell_integration-008 @BIFROST-3069
  Scenario: Create a new MozyPro partner, provision 999 licenses,create sub-partner provision 1 licenses and check get /accounts/licenses response,check total count value
    When I create 1 DellMozyPro new partner with
      | admin fullname        | admin password | name |
      | test automation admin | QAP@SSw0rd     | clientQAAutomation_Bifrost_999_licenses_parent_partner |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 999      |
    When I log in BUS console as bifrost new created partner
    When I add a new pro plan for the partner
      | name    | periods | server licenses price | server min licenses | server quota price | desktop licenses price | desktop min licenses | desktop quota price |
      | default | monthly | 1                     |  1                  | 1                  | 1                      | 1                    | 1                   |
    When I add a new role for the partner
      | name    | include all |
      | default | false        |
    When I create 1 DellSubPartner new partner with
      | name                                                  |
      | clientQAAutomation_Bifrost_1_licenses_sub_partner  |
    When I provision license for the subpartner
      | license type | licenses |
      | Desktop      | 1        |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | false               |  Desktop     | 0      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true               |  Desktop      | 0      | 999   |
    Then get licenses response detail should be
      | total  | count |
      | 999    | 999   |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 0   | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 999   | 999  |
     When I provision license for the subpartner
      | license type | licenses |
      | Desktop      | 1        |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | false                |  Desktop     | 0    | 1   |
    Then get licenses response detail should be
      | total  | count |
      | 1001   | 1   |
     When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | false               |  Desktop     | 0    | 1000   |
    Then get licenses response detail should be
      | total  | count |
      | 1001   | 1000   |
    When I delete the new created partner

  @verify-license-total @sub-partners @mozy_dell_integration-009 @BIFROST-3069
  Scenario: Create a new MozyPro partner, provision 1k licenses,create sub-partner provision 1 licenses and check get /accounts/licenses response,check total count value
    When I create 1 DellMozyPro new partner with
      | admin fullname        | admin password | name |
      | test automation admin | QAP@SSw0rd     | clientQAAutomation_Bifrost_1000_licenses_parent_partner |
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1000     |
    When I log in BUS console as bifrost new created partner
    When I add a new pro plan for the partner
      | name    | periods | server licenses price | server min licenses | server quota price | desktop licenses price | desktop min licenses | desktop quota price |
      | default | monthly | 1                     |  1                  | 1                  | 1                      | 1                    | 1                   |
    When I add a new role for the partner
      | name    | include all |
      | default | false        |
    When I create 1 DellSubPartner new partner with
      | name                                                  |
      | clientQAAutomation_Bifrost_1_licenses_sub_partner  |
    When I provision license for the subpartner
      | license type | licenses |
      | Desktop      | 1        |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | false               |  Desktop     | 0      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 1001   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | false               |  Desktop     | 1      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 1001   | 1000  |
    When I get licenses for the partner
      | exclude sub-partner | license type | offset | limit |
      | true                |  Desktop     | 1      | 1000  |
    Then get licenses response detail should be
      | total  | count |
      | 1000   | 999   |
