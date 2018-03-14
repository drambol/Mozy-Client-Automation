Feature: Activate
  As a Mozy Linux User, I can activate my mozy account

  Background:
    When I unlink machine
    When I wait state to be "UNINITIALIZED"


  @smoke @lin-155 @cleanup @regression @core
  Scenario: Activate User Account
    When Linux Client is activated with "{env}_{oemclient}"
    Then I expect state be one of "AUTHENTICATED;RUNNING"

  @lin-112 @smoke @regression @core
  Scenario: Change User account
    When Linux Client is activated with "{env}_{oemclient}"
    Then I expect state be one of "AUTHENTICATED;RUNNING"
    When I unlink machine
    When I wait state to be "UNINITIALIZED"
    When Linux Client is activated with "{env}_{oemclient}_pk"
    Then I expect state be one of "AUTHENTICATED;RUNNING"

  @lin-168 @regression @core
  Scenario: Activate as a user who has a CKey configured on a URL
    When Linux Client is activated with "{env}_{oemclient}_ckey"
    Then I expect state be one of "AUTHENTICATED;RUNNING"
    Then I expect account details with
      | MACHINE ENCRYPTION |
      | Administrator Key  |


  @lin-156 @regression @core
  Scenario: Activate with a valid user and invalid password
    When I activate Linux Client with credential as below
      | email             | password |
      | {env}_{oemclient} | invalid  |
    Then I expect state be one of "UNINITIALIZED"

  @lin-157 @regression @core
  Scenario: Activate with a invalid user and invalid password
    When I activate Linux Client with credential as below
      | email           | password |
      | invalid@emc.com | invalid  |
    Then I expect state be one of "UNINITIALIZED"

  @lin-159 @regression @core
  Scenario: Activate with a user with no key provisioned
    When I create user with
      | password   | license type | licenses | user group |
      | test123!@# | Server       | 0        | test       |
    When Linux Client is activated with new user
    Then I expect state be one of "UNINITIALIZED"

  @lin-87 @regression @core
  Scenario: Activate with invalid password file
    When I activate Linux Client with credential as below
      | email             | password_file |
      | {env}_{oemclient} | invalid       |
    Then I expect state be one of "UNINITIALIZED"


  @lin-373 @regression @core
  Scenario: Activate with valid password file
    When I activate Linux Client with credential as below
      | email             | password_file |
      | {env}_{oemclient} | valid         |
    Then I expect state be one of "AUTHENTICATED;RUNNING"

  @lin-98 @regression @core
  Scenario: Activate custom key from file and password from file
    When I activate Linux Client with credential as below
      | email             | password_file | customkeytext |
      | {env}_{oemclient} | valid         | abc           |
    Then I expect state be one of "AUTHENTICATED;RUNNING"

  @lin-386 @regression @core
  Scenario: Change Encryptions
    When I activate Linux Client with credential as below
      | email             | password_file | customkeytext |
      | {env}_{oemclient} | valid         | abc           |
    Then I expect state be one of "AUTHENTICATED;RUNNING"
    When I unlink machine
    When I activate Linux Client with credential as below
      | email             | password_file | customkeytext |
      | {env}_{oemclient} | valid         | 123test       |
    Then I expect state be one of "AUTHENTICATED;RUNNING"

#  @lin-foo
#  Scenario: Active with new created user
#    When I create user with
#      | password   | license type | licenses | user group                  |
#      | test123!@# | Server       | 1        | CKEY_NOBACKUPSET_SERVER_AUTO |





