Feature: Bifrost Testcases for Dell-Mozy Integration, workflow: SUSPEND/RESUME/CANCEL
    Dell-Mozy Integration Test with APS, workflow such as Upgrade, downgrade,regrade,suspend,cancel
  @suspend @aps @suspend_aps_integration_001
  Scenario: Suspend a new created standalone Dell-Pro user, and un-suspend the account
    Precondition: Create a standalone user under Dell-Pro root partner, generate 10G quota,set limit 5 devices.
    1. Verify the user account via Bifrost.
    2. Suspend the user via Bifrost.
    3. Then un-suspend the user via Bifrost.
    When I create a DellMozyProStandalone new user with
      | password    |
      | QAP@SSw0rd  |
    When I assign storage for the user with
      | type    | value | unit |
      | Generic | 10    | GB   |
    Then I set licenses limit to the new created user
      | license type | licenses |
      | Desktop      |  5       |
    When I search the new created user via bifrost
    Then I should get response 200
    When I suspend the new created user
    When I resume the new created user
    Then I send email to the new created user
    When I delete the new created user

  @suspend @aps @suspend_aps_integration_002
  Scenario: Suspend a new created standalone Dell-Enterprise user, and un-suspend the account
    Precondition: Create a standalone user under Dell-Enterprise root partner, generate 10G quota,set limit 5 devices.
    1. Verify the user account via Bifrost.
    2. Suspend the user via Bifrost.
    3. Then un-suspend the user via Bifrost.
    When I create a DellMozyEnterpriseStandalone new user with
      | password    |
      | QAP@SSw0rd  |
    When I assign storage for the user with
      | type    | value | unit |
      | Generic | 10    | GB   |
    Then I set licenses limit to the new created user
      | license type | licenses |
      | Desktop      |  5       |
    When I search the new created user via bifrost
    Then I should get response 200
    When I suspend the new created user
    When I resume the new created user
    Then I send email to the new created user
    When I delete the new created user

  @suspend @aps @suspend_aps_integration_003
  Scenario: Suspend a new created Dell-Pro partner,and un-suspend the account
      Precondition: Create a Dell-Pro partner, generate 25G quota,unlimited devices.
      1.Verify the customer account CID via Bifrost.
      2.Suspend the partner
      3. Then un-suspend the partner.
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                    | sync  | security_requirement | external id                 |
      | test automation admin | dell_mozypro-svr disable-sync diable-standard-desktop   | true  | HIPAA                | suspend_aps_integration_003 |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I search partner by
      | external id                 |
      | suspend_aps_integration_003 |
    When I suspend the new created partner
    When I resume the new created partner
    When I delete the new created partner

  @suspend @aps @suspend_aps_integration_004
  Scenario: Suspend a new created Dell-Ent partner,and un-suspend the account
      Precondition: Create a Dell-Ent partner, generate 50G quota,10 devices.
      1.Verify the customer account CID via Bifrost.
      2.Suspend the partner
      3. Then un-suspend the partner.
    When I create 1 DellMozyEnterprise new partner with
      | admin fullname        | name                                                    | sync  | security_requirement | external id                 |
      | test automation admin | dell_mozypro-svr disable-sync diable-standard-desktop   | true  | HIPAA                | suspend_aps_integration_004 |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I search partner by
      | external id                 |
      | suspend_aps_integration_004 |
    When I suspend the new created partner
    When I resume the new created partner
    When I delete the new created partner