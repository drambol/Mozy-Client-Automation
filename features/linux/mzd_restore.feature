# Created by gongc1 at 4/17/17
Feature: MZD restore
  As a linux user, I can restore backup files through


  @cleanup @lin-006 @core
  Scenario: As I Linux Client User, I can restore files through mzd files
    When I create user with
      | password   | license type | licenses | user group |
      | test123!@# | Server       | 1        | test       |
    When Linux Client is activated with new user
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | dir1        | test        | 100       |          | test1     |
    When I create linux backupset with
      | name    | paths | excludes |
      | lin-006 | dir1  |          |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to generate mzd
      | entity |
      | dir1   |
    When I restore files through mzd to output "restore_001"
    Then I expect restore dir "restore_001" is the same with backup dir "dir1"
    When I delete the new created user