Feature: End to End
  As a Mac End User, I can backup my data with Mac Client and restore data through Mac Fryr


  Background:
    When Mac Client is activated with credential '{env}_{oemclient}_pk'

  @cleanup @e2e @foo @mac_teardown @macfryr_teardown
  Scenario: I can use mac fryr client to restore files that backup from mac fryr
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | e2e_002     | smoke       | 1000      | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | e2e_002      |
    Then I expected "Total Selected:" is 10 files
    When I start backup from GUI
    When I wait to backup finished
    Then I expected "Awaiting Backup:" is 0 files
    When I close Mac Client
    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to generate mzd
      | entity  |
      | e2e_002 |
    When I launch MacFryr Client from GUI
    When I login MacFryr with current user
    When I restore last mzd to directory "e2e_002-output"
    When I close Mac Fryr
    Then I expect restore dir "e2e_002-output" is the same with backup dir "e2e_002"
