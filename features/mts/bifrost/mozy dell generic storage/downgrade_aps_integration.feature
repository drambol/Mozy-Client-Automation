Feature: Bifrost Testcases for Dell-Mozy Integration, workflow: DOWNGRADE
    Dell-Mozy Integration Test with APS, workflow such as Upgrade, downgrade,regrade,suspend,cancel
  @downgrade @aps @downgrade_aps_integration_001
  Scenario: Downgrade a new created Dell-Pro partner
      Precondition: Create a Dell-Pro partner with a valid CID,aka external id, generate 25G quota,unlimited devices.
      Partner type: MozyPro & Server Enable & Sync Enable
      1.Verify the customer account CID via bifrost.
      2.Downgrade the offer to 20G for the partner
      3.Then delete the partner.
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                    | server plan | sync  | security_requirement | external id                   |
      | test automation admin | dell_mozypro-svr enable-sync enable-standard-generic    | true        | true  | HIPAA                | downgrade_aps_integration_001 |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I search partner by
      | external id                   |
      | downgrade_aps_integration_001 |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 20      | GB   |
    Then the partner storage should be
      | type    | value | unit |
      | Generic | 20    | GB   |
    When I delete the new created partner

  @downgrade @aps @downgrade_aps_integration_002
  Scenario: Downgrade a new created Dell-Pro partner
      Precondition: Create a Dell-Pro partner with a valid CID,aka external id, generate 25G quota,unlimited devices.
      Partner type: MozyPro & Server Enable & Sync Diable
      1.Verify the customer account CID via bifrost.
      2.Downgrade the offer to 0G for the partner
      3.Then delete the partner.
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                   | server plan  | security_requirement | external id                   |
      | test automation admin | dell_mozypro-svr enable-sync diable-standard-generic   | true         | HIPAA                | downgrade_aps_integration_002 |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I search partner by
      | external id                   |
      | downgrade_aps_integration_002 |
    When I assign storage for the partner with
      | type    | value  | unit |
      | Generic | 0      | GB   |
    Then the partner storage should be
      | type    | value | unit |
      | Generic | 0     | GB   |
    When I delete the new created partner

  @downgrade @aps @downgrade_aps_integration_003
  Scenario: Downgrade a new created Dell-Pro partner
      Precondition: Create a Dell-Pro partner with a valid CID,aka external id, generate 25G quota,unlimited devices.
      Partner type: MozyPro & Server Diable & Sync Enable
      1.Verify the customer account CID via bifrost.
      2.Downgrade the offer to 0G for the partner
      3.Then delete the partner.
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                    | sync | external id                   |
      | test automation admin | dell_mozypro-svr disable-sync enable-standard-generic   | true | downgrade_aps_integration_003 |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I search partner by
      | external id                   |
      | downgrade_aps_integration_003 |
    When I assign storage for the partner with
      | type    | value  | unit |
      | Generic | 0      | GB   |
    Then the partner storage should be
      | type    | value | unit |
      | Generic | 0     | GB   |
    When I delete the new created partner

  @downgrade @aps @downgrade_aps_integration_004
  Scenario: Downgrade a new created Dell-Pro partner
      Precondition: Create a Dell-Pro partner with a valid CID,aka external id, generate 0G quota,unlimited devices.
      Partner type: MozyPro & Server Diable & Sync Disable
      1.Verify the customer account CID via bifrost.
      2.Downgrade the offer to 0G for the partner
      3.Then delete the partner.
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                   | external id                   |
      | test automation admin | dell_mozypro-svr disable-sync disable-standard-desktop | downgrade_aps_integration_004 |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 0       | GB   |
    Then I send email to the new created partner
    When I search partner by
      | external id                   |
      | downgrade_aps_integration_003 |
    When I assign storage for the partner with
      | type    | value  | unit |
      | Generic | 0      | GB   |
    Then the partner storage should be
      | type    | value | unit |
      | Generic | 0     | GB   |
    When I delete the new created partner

#  @downgrade @aps @downgrade_aps_integration_002
#  Scenario: Downgrade a new created Dell-Pro partner to a storage which is lower than used storage
#      Precondition: Create a Dell-Pro partner with a valid CID,aka external id, generate 25G quota,unlimited devices.
#      1.Verify the customer account CID via bifrost.
#      2.Downgrade the offer to 20G for the partner
#      3.Then delete the partner.
#    When I create 1 DellMozyPro new partner with
#      | admin fullname        | name                                                    | sync  | security_requirement | external id                   |
#      | test automation admin | dell_mozypro-svr disable-sync diable-standard-desktop   | true  | HIPAA                | downgrade_aps_integration_002 |
#    When I assign storage for the partner with
#      | type    | value   | unit |
#      | Generic | 25      | GB   |
#    When I create a DellSubPartner new user with
#      | password    | type     |
#      | QAP@SSw0rd  | Desktop  |
#    Then I set licenses limit to the new created user
#      | license type | licenses |
#      | Desktop      |  5       |
#    Then I activate 2 machine with the new created user
#    Then I send email to the new created partner
#    When I search partner by
#      | external id                   |
#      | downgrade_aps_integration_002 |
#    Then I set licenses limit to the new created user
#      | license type | licenses |
#      | Desktop      |  1       |
##    When I assign storage for the partner with
##      | type    | value   | unit |
##      | Generic | 20      | GB   |
##    Then the partner storage should be
##      | type    | value | unit |
##      | Generic | 20    | GB   |
##    When I delete the new created partner
#
#  Scenario: Downgrade a new created Dell-Pro partner to a storage which is equal to used storage
#      Precondition: Create a Dell-Pro partner with a valid CID,aka external id, generate 25G quota,unlimited devices.
#      1.Verify the customer account CID via bifrost.
#      2.Downgrade the offer to 20G for the partner
#      3.Then delete the partner.
#    When I create 1 DellMozyPro new partner with
#      | admin fullname        | name                                                    | sync  | security_requirement | external id                   |
#      | test automation admin | dell_mozypro-svr disable-sync diable-standard-desktop   | true  | HIPAA                | downgrade_aps_integration_001 |
#    When I assign storage for the partner with
#      | type    | value   | unit |
#      | Generic | 25      | GB   |
##    Then I send email to the new created partner
##    When I search partner by
##      | external id                   |
##      | downgrade_aps_integration_001 |
##    When I assign storage for the partner with
##      | type    | value   | unit |
##      | Generic | 20      | GB   |
##    Then the partner storage should be
##      | type    | value | unit |
##      | Generic | 20    | GB   |
##    When I delete the new created partner