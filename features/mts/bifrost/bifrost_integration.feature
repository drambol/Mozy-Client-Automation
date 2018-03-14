# Created by zhangj79 at 3/20/17
Feature: Bifrost Demo
  Demo Bifrost Create New User

  @smoke @BIF-002 @demo
  Scenario: Create a new MozyPro user under sub-partner, provision licenses for the user
    When I create user with
    | password    | license type | licenses | user group  |
    | test123!@#  | Desktop      | 1        | test        |
    When I delete the new created user

  @smoke @BIF-001 @demo
  Scenario: Create a new mozypro user under sub-partner and provision license keys for the user
    When I act as the partner
      | admin username                         | partner id |
      | mozyautotest+scott+jordan+1441@emc.com | 428896     |
    When I create 1 user under the partner
      | password   | partner id | API_KEY |
      | test123!@# | 428896     | G4STuxfDn8sOi4q4dmvNVQGysoYX3qpCTFRbP2wNRuxDzPkikgk0TtlRIy238JWp |
    Then I generate 2 licenses to default user group
      | license type |
      | Desktop      |
    When I transfer 2 licenses to the user
    Then there should be 2 licenses for the user
    # Enter steps here

  @smoke @client_configuration @demo
  Scenario: Log in BUS and Search Partner
    When I log in BUS console to select my partner info
      | partner name                    |
      | test elk framework test partner |
    When I create a new client config and uncheck backup set
      | name                    | type    | user group | backup sets          |
      | TC_client_configuration | Desktop | aaaaaa     | windows_backup_sets  |
