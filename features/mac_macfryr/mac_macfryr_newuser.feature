Feature: End to End
  As a Mac End User, I can backup my data with Mac Client and restore data through Mac Fryr

  Background:
    When Mac Client is not activated

  @cleanup @e2e @foo @mac_teardown @macfryr_teardown
  Scenario: Activate Mozy Mac Client with new created bifrost credential
    When I create user with
      | password   | license type | licenses |
      | test123!@# | Desktop      | 1        |
    When I launch Mac Client from GUI
    When I activate with bifrost created credential
    When I create 20 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | e2e_003     | e2e         | 2000      | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | e2e_003      |
    Then I expected "Total Selected:" is 20 files
    When I start backup from GUI
    When I wait to backup finished
    When I close Mac Client
    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to generate mzd
      | entity  |
      | e2e_003 |
    When I launch MacFryr Client from GUI
    When I login MacFryr with current user
    When I restore last mzd to directory "e2e_003-output"
    When I close Mac Fryr
    Then I expect restore dir "e2e_003-output" is the same with backup dir "e2e_003"
    When I delete the new created user