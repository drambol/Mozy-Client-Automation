Feature:As a Mozy Linux user,
  I want to restore and decrypt a single file that is encrypted with a personal
  or cKey so that I can actually use the file that I have restored to my machine

  Background:
    When Linux Client is activated with "{env}_{oemclient}_ckey"
    When Linux Client is ready for backup at "on-demand" mode

  @cleanup @core @regression @lin-122
  Scenario: Decrypt a single file
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | dir1        | test        | 100       |          | test1     |
    When I create linux backupset with
      | name    | paths | excludes |
      | decrypt | dir1  |          |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    When I visit cas host to be authenticated to do direct download from freyja site
    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to direct download
      | entity                |
      | dir1/test_test1_0.txt |
    When I decrypt files "test_test1_0.txt" to "decrypt"
    Then I expect restore dir "decrypt/test_test1_0.txt" is the same with backup dir "dir1/test_test1_0.txt"

  @cleanup @core @regression @lin-361
  # Remove this test case since I notice tarball is unable to generate on Freyja, looks like a freya bug
    Scenario: Decrypt a tarball
    When I create 10 test files with
        | file_folder | file_prefix | file_size | file_ext | file_name |
        | dir1        | test        | 100       |          | test1     |
      When I create linux backupset with
        | name    | paths | excludes |
        | decrypt | dir1  |          |
      When I wait state be one of "IDLE,AUTHENTICATED"
      When I start backup
      When I wait state to be "IDLE"
      When I visit cas host to be authenticated to do direct download from freyja site
      When I logon Freyja through BUS console
      When I click backup files for current machine
      When I select below files to generate tarball
        | entity |
        | dir1  |
      When I decrypt tarball files to "decrypt"
      Then I expect restore dir "decrypt" is the same with backup dir "dir1"

