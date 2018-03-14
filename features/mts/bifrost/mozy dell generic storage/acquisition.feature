Feature: Bifrost Testcases for Dell-Mozy Integration
  Dell-Mozy Integration Test with APS, workflow such as Acquisition,upgrade, downgrade,regrade,suspend,cancel

  @acquisition @aps @INTEGRATION-APS-001 @positive @mozypro
  Scenario: Create a new MozyPro Dell partner(svr disable/sync disable/standard), provision license,send admin activation email, then delete the partner
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name  |
      | test automation admin | dell_mozypro-svr disable-sync diable-standard-generic  |
    Then I should get response 201
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    When I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-002 @positive @mozypro
  Scenario: Create a new MozyPro Dell partner(svr enable/sync disable/standard), provision license,send admin activation email, then delete the partner
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                  | server plan |
      | test automation admin | dell_mozypro-svr enable-sync diable-standard-generic  | true        |
    Then I should get response 201
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-003 @positive @mozypro
  Scenario: Create a new MozyPro Dell partner(svr enable/sync enable/hipaa), provision license,send admin activation email, then delete the partner
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                  | server plan | sync | security_requirement |
      | test automation admin | dell_mozypro-svr enable-sync diable-standard-generic  | true        | true | HIPAA                |
    Then I should get response 201
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-004 @negative @mozypro
  Scenario: Create a new MozyPro Dell partner(svr disable/sync disable/standard), provision license and quota,send email,create a server user under the partner
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name  |
      | test automation admin | dell_mozypro-svr disable-sync diable-standard-desktop  |
    When I create a DellSubPartner new user with
      | password    | type    |
      | QAP@SSw0rd  | Server  |
    Then I should get response 412
      | message |
      | Server Add-on is not enabled for usergroup. Can not set user to be of type Server |
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-005 @positive @mozypro
  Scenario: Create a new MozyPro Dell partner(svr disable/sync true/hipaa), provision license and quota,send email,enable server for the partner and then create a server user under the partner
    When I create 1 DellMozyPro new partner with
      | admin fullname        | name                                                    | sync  | security_requirement |
      | test automation admin | dell_mozypro-svr disable-sync diable-standard-desktop   | true  | HIPAA                |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    When I enable server add-ons for the new created partner
    When I create a DellSubPartner new user with
      | password    | type    |
      | QAP@SSw0rd  | Server  |
    Then I should get response 412
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-006 @positive @mozypro
  Scenario: Create a new MozyPro Standalone Dell user(default/sync disable), provision license and quota, set device limit and storage limit,send user activation email
    1.Create a standalone Ent user with Bifrost, get UID.
    2. Generate quota for the user with Bifrost.
    3. Generate devices for the user with Bifrost.
    4. Set the device limit on the user with Bifrost.
    5. Set the user quota limit on the user with Bifrost.
    6. Deliver the user activation template
    When I create a DellMozyProStandalone new user with
    | password    |
    | QAP@SSw0rd  |
    When I assign storage for the user with
    | type    | value | unit |
    | Generic | 10    | GB   |
    Then I set licenses limit to the new created user
    | license type | licenses |
    | Desktop      |  5       |
    Then I send email to the new created user
    When I delete the new created user

  @acquisition @aps @INTEGRATION-APS-007 @positive @mozyenterprise
  Scenario: Create a new MozyEnterprise Dell partner(svr disable/sync disable/standard), provision license,send admin activation email, then delete the partner
    When I create 1 DellMozyEnterprise new partner with
      | admin fullname        | name  |
      | test automation admin | dell_mozypro-svr disable-sync diable-standard-generic  |
    Then I should get response 201
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-008 @positive @mozyenterprise
  Scenario: Create a new MozyEnterprise Dell partner(svr enable/sync disable/standard), provision license,send admin activation email, then delete the partner
    When I create 1 DellMozyEnterprise new partner with
      | admin fullname        | name                                                  | server plan |
      | test automation admin | dell_mozypro-svr enable-sync diable-standard-generic  | true        |
    Then I should get response 201
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-009 @positive @mozyenterprise
  Scenario: Create a new MozyEnterprise Dell partner(svr enable/sync enable/hipaa), provision license,send admin activation email, then delete the partner
    When I create 1 DellMozyEnterprise new partner with
      | admin fullname        | name                                                  | server plan | sync | security_requirement |
      | test automation admin | dell_mozypro-svr enable-sync diable-standard-generic  | true        | true | HIPAA                |
    Then I should get response 201
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-010 @negative @mozyenterprise
  Scenario: Create a new MozyEnterprise Dell partner(svr disable/sync disable/standard), provision license and quota,send email,create a server user under the partner
    When I create 1 DellMozyEnterprise new partner with
      | admin fullname        | name  |
      | test automation admin | dell_mozypro-svr disable-sync diable-standard-desktop  |
    When I create a DellSubPartner new user with
      | password    | type    |
      | QAP@SSw0rd  | Server  |
    Then I should get response 412
      | message |
      | Server Add-on is not enabled for usergroup. Can not set user to be of type Server |
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-011 @positive @mozyenterprise
  Scenario: Create a new MozyEnterprise Dell partner(svr disable/sync true/hipaa), provision license and quota,send email,enable server for the partner and then create a server user under the partner
    When I create 1 DellMozyEnterprise new partner with
      | admin fullname        | name                                                    | sync  | security_requirement |
      | test automation admin | dell_mozypro-svr disable-sync diable-standard-desktop   | true  | HIPAA                |
    When I assign storage for the partner with
      | type    | value   | unit |
      | Generic | 25      | GB   |
    When I enable server add-ons for the new created partner
    When I create a DellSubPartner new user with
      | password    | type    |
      | QAP@SSw0rd  | Server  |
    Then I should get response 412
    Then I send email to the new created partner
    When I delete the new created partner

  @acquisition @aps @INTEGRATION-APS-012 @positive @mozyenterprise
  Scenario: Create a new MozyEnterprise Standalone Dell user(default/sync disable), provision license and quota, set device limit and storage limit,send user activation email
    1.Create a standalone Ent user with Bifrost, get UID.
    2. Generate quota for the user with Bifrost.
    3. Generate devices for the user with Bifrost.
    4. Set the device limit on the user with Bifrost.
    5. Set the user quota limit on the user with Bifrost.
    6. Deliver the user activation template
    When I create a DellMozyEnterpriseStandalone new user with
    | password    |
    | QAP@SSw0rd  |
    When I assign storage for the user with
    | type    | value | unit |
    | Generic | 10    | GB   |
    Then I set licenses limit to the new created user
    | license type | licenses |
    | Desktop      |  5       |
    Then I send email to the new created user
    When I delete the new created user

