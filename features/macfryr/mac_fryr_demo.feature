Feature: Fryr demo feature
  Demo Feature for Client Automation

  @smoke @MacFryr-001 @macfryr_teardown
  Scenario: Mac Fryr restore by username and password
    When I log in BUS console to select my restore machine
      | user_email     |
      | ken.xu@emc.com |
    Then I navigate to Freyja page to request a mzd restore
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | 中文文件夹                                  |
      |                 |                                  | Test Report for Android 1.7.2 Release.docx |
    Then I use Mac Restore Manager to restore the selected files with Useremail 'ken.xu@emc.com' and Password '666666'
    Then I check the Mac restore job finished successfully

  @smoke @MacFryr-002 @macfryr_teardown
  Scenario: Mac Fryr mzd restore by mzd file
    When I log in BUS console to select my restore machine
      | user_email     |
      | ken.xu@emc.com |
    Then I navigate to Freyja page to request a mzd restore
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | Symbol_Folder                              |
      |                 |                                  | Test Report for Android 1.7.2 Release.docx |
    Then I use Mac Restore Manager to restore the selected files by double clicking .mzd file
    Then I check the Mac restore job finished successfully

  @smoke @MacFryr-003 @macfryr_teardown
    Scenario: Mac Fryr archive restore
    When I log in BUS console to select my restore machine
      | user_email     |
      | ken.xu@emc.com |
    Then I navigate to Freyja page to request an archive restore
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | 中文文件夹                                  |
      |                 |                                  | Symbol_Folder                              |
      |                 |                                  | Test Report for Android 1.7.2 Release.docx |
    Then I use Mac Restore Manager to decrypt the package by archive restore
    Then I check the Mac restore job finished successfully

  @smoke @MacFryr-004 @macfryr_teardown
    Scenario: Mac Fryr decrypt a single file
    When I visit cas host to be authenticated to do direct download from freyja site
    When I log in BUS console to select my restore machine
      | user_email          |
      | ken1020pkey@emc.com |
    Then I delete all files in 'MACFRYR' installer folder
    Then I navigate to Freyja page to download an encrypted file/folder directly
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | Test Report for Android 1.7.2 Release.docx |
    Then I use Mac Restore Manager to decrypt the file with personal key '1234'
    Then I check the Mac restore job finished successfully

  @smoke @MacFryr-005 @macfryr_teardown
  Scenario: Mac Fryr mzd restore with personal key
    When I log in BUS console to select my restore machine
      | user_email          |
      | ken1020pkey@emc.com |
    Then I navigate to Freyja page to request a mzd restore
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7M1      | /Users/xuk7/Documents/TestData   | 中文文件夹                                  |
      |                 |                                  | Test Report for Android 1.7.2 Release.docx |
    Then I use Mac Restore Manager to restore the selected files with useremail and password
      | user_email          | password | encrypt_type | encrypt_key |
      | ken1020pkey@emc.com | 666666   | pkey         | 1234        |
    Then I check the Mac restore job finished successfully

  @smoke @MacFryr-006 @macfryr_teardown
  Scenario: Mac Fryr mzd restore with ckey
    When I log in BUS console to select my restore machine
      | user_email          |
      | ken1020ckey@emc.com |
    Then I navigate to Freyja page to request a mzd restore
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7M1      | /Users/xuk7/Documents/TestData   | 中文文件夹                                  |
      |                 |                                  | Test Report for Android 1.7.2 Release.docx |
    Then I use Mac Restore Manager to restore the selected files with useremail and password
      | user_email          | password | encrypt_type | encrypt_key |
      | ken1020ckey@emc.com | 666666   | ckey         | Rich.ckey   |
    Then I check the Mac restore job finished successfully
