Feature: Bifrost Testcases for Dell-Mozy Integration, workflow: UPGRADE
  Dell-Mozy Integration Test with APS, workflow such as Upgrade, downgrade,regrade,suspend,cancel

  @upgrade @aps @upgrade_aps_integration_001
  Scenario: Create a new MozyPro Dell partner(svr enable,sync disable,standard), provision license and quota, send admin activation email; upgrade the quota offer 0GB->10GB(note: since devices are unlimit, no need to upgrade)
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                        | external id                 | server plan |
      | test automation admin | dell_mozypro-svr enable-sync disable-standard-server        | upgrade_aps_integration_001 | true        |
    When I assign storage for the partner with
      | type    | value     | unit  |
      | Generic |  0        | GB    |
    Then the partner storage should be
      | type    | value     | unit  |
      | Generic |  0        | GB    |
    Then I send email to the new created partner
    When I search partner by
      | external id                 |
      | upgrade_aps_integration_001 |
    Then I should get response 200
    When I assign storage for the partner with
      | type    | value | unit  |
      | Generic | 10    | GB    |
    Then the partner storage should be
      | type    | value | unit  |
      | Generic | 10    | GB    |
    When I delete the new created partner

  @upgrade @aps @upgrade_aps_integration_002
  Scenario: Create a new MozyEnterprise Dell partner(svr enable,sync disable,standard), provision license and quota, send admin activation email; upgrade the quota offer 0GB->10GB(note: since devices are unlimit, no need to upgrade)
    When I create 1 DellMozyEnterprise new partner with
      | admin fullname        | name                                                        | external id                 | server plan |
      | test automation admin | dell_mozyenterprise-svr enable-sync disable-standard-server | upgrade_aps_integration_002 | true        |
    When I assign storage for the partner with
      | type    | value     | unit  |
      | Generic |  0        | GB    |
    Then the partner storage should be
      | type    | value     | unit  |
      | Generic |  0        | GB    |
    Then I send email to the new created partner
    When I search partner by
      | external id                 |
      | upgrade_aps_integration_002 |
    Then I should get response 200
    When I assign storage for the partner with
      | type    | value | unit  |
      | Generic | 10    | GB    |
    Then the partner storage should be
      | type    | value | unit  |
      | Generic | 10    | GB    |
    When I delete the new created partner

  @upgrade @aps @upgrade_aps_integration_003
  Scenario: Check the maximum licenses number that can provision
    When I create 1 DellMozyEnterprise new partner with
      | admin fullname        | name                                                        | external id                 |
      | test automation admin | dell_mozypro-svr enable-sync disable-standard-server        | upgrade_aps_integration_003 |
#    Then I send email to the new created partner
#    When I search partner by
#      | external id                 |
#      | upgrade_aps_integration_001 |
#    Then I should get response 200
    When I provision license for the partner
      | license type | licenses |
      | Desktop      | 1000     |
#    When I provision license for the partner
#      | license type | licenses |
#      | Desktop      | 1000     |
#    When I provision license for the partner
#      | license type | licenses |
#      | Desktop      | 1000     |
#    When I provision license for the partner
#      | license type | licenses |
#      | Desktop      | 1000     |
#    When I provision license for the partner
#      | license type | licenses |
#      | Desktop      | 1000     |
#    When I provision license for the partner
#      | license type | licenses |
#      | Desktop      | 1000     |
#    When I delete the new created partner

#  @upgrade @aps @INTEGRATION-APS-006
#    Scenario: Create a new MozyPro partner,provision license and quota, then search the partner via external id, upgrade the quota and licenses
#    1. Given an existing CID(the CID belongs to a SMB partner),verify the customer account CID with Bifrost.
#    2. Generate quota for the partner.
#    3. Generate devices for the partner.
#    4. Upgrade quota and devices for the partner.
#    When I create 1 DellMozyPro new partner with
#      | admin fullname        | name                                                        | external id                   |
#      | test automation admin | dell_mozypro-svr enable-sync diable-standard-external id    | mozy dell INTEGRATION-APS-006 |
#    When I assign storage for the partner with
#      | type    | value   | unit |
#      | Desktop | 5       | GB   |
#    When I generate licenses to the new created partner
#      | license type | licenses |
#      | Desktop      | 5        |
#    When I create a DellSubPartner new user with
#    When I search partner by
#      | external id                   |
#      | mozy dell INTEGRATION-APS-006 |
#    When I assign storage for the partner with
#      | type    | value   | unit |
#      | Desktop | 15      | GB   |
#
#
#  @upgrade @aps @INTEGRATION-APS-007
#    Scenario: Create a new MozyPro partner,provision license and quota, then search the partner via external id, upgrade the quota and licenses
#    1. Given an existing CID(the CID belongs to a SMB partner),verify the customer account CID with Bifrost.
#    2. Generate quota for the partner.
#    3. Generate devices for the partner.
#    4. Upgrade quota and devices for the partner.
#    When I create 1 DellMozyPro new partner with
#      | admin fullname        | name                                                        | external id                   | sync |
#      | test automation admin | dell_mozypro-svr enable-sync enable-standard-external id    | mozy dell INTEGRATION-APS-007 | true |
#    When I assign storage for the partner with
#      | type    | value   | unit |
#      | Desktop | 5       | GB   |
#    When I generate licenses to the new created partner
#      | license type | licenses |
#      | Desktop      | 5        |
#    When I create a DellSubPartner new user with
#    When I search partner by
#      | external id                   |
#      | mozy dell INTEGRATION-APS-007 |
#    Then I should get id as the new created partner
#    When I assign storage for the partner with
#      | type    | value | unit |
#      | Desktop | 10    | GB   |
#    Then I should get response 200
#
#    @upgrade @aps @INTEGRATION-APS-008
#      Scenario: Create a new MozyEnterprise partner,provision license and quota, then search the partner via external id, upgrade the quota and licenses
#      When I create 1 DellMozyEnterprise new partner with
#      | admin fullname        | name                                                            | external id                   | server plan |
#      | test automation admin | dell_mozypro-svr enable-sync diable-standard-external id       | mozy dell INTEGRATION-APS-005  | true        |
#    When I assign storage for the partner with
#      | type    | value   | unit |
#      | Desktop | 5       | GB   |
#    When I generate licenses to the new created partner
#      | license type | licenses |
#      | Desktop      | 50       |
#    When I search partner by
#      | external id                   |
#      | mozy dell INTEGRATION-APS-005 |
