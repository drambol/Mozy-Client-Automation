Feature: Fryr smoke feature
  Smoke cases for windows restore manager

  @smoke @Winfryr-001 @winfryr_teardown
  Scenario: Win Fryr mzd restore by username and password
    When I log in BUS console to select my restore machine
      | user_email     |
      | ken.xu@emc.com |
    Then I navigate to Freyja page to request a mzd restore
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | 中文文件夹                                  |
      |                 |                                  | Test Report for Android 1.7.2 Release.docx |
    Then I use Windows Restore Manager to restore the selected files with Useremail 'ken.xu@emc.com' and Password '666666'
    Then I check the restore job finished successfully

  @smoke @Winfryr-002 @winfryr_teardown
  Scenario: Win Fryr mzd restore by mzd file
    When I log in BUS console to select my restore machine
      | user_email     |
      | ken.xu@emc.com |
    Then I navigate to Freyja page to request a mzd restore
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | Symbol_Folder                              |
      |                 |                                  | Test Report for Android 1.7.2 Release.docx |
    Then I use Windows Restore Manager to restore the selected files by double clicking .mzd file
    Then I check the restore job finished successfully

  @smoke @Winfryr-003 @winfryr_teardown
    Scenario: Win Fryr archive restore
    When I log in BUS console to select my restore machine
      | user_email     |
      | ken.xu@emc.com |
    Then I navigate to Freyja page to request an archive restore
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | 中文文件夹                                  |
      |                 |                                  | Symbol_Folder                              |
      |                 |                                  | Test Report for Android 1.7.2 Release.docx |
    Then I use Windows Restore Manager to decrypt the package by archive restore
    Then I check the restore job finished successfully

  @smoke @Winfryr-004 @winfryr_teardown
    Scenario: Win Fryr decrypt a single file
    When I visit cas host to be authenticated to do direct download from freyja site
    When I log in BUS console to select my restore machine
      | user_email          |
      | ken1020pkey@emc.com |
    Then I navigate to Freyja page to download an encrypted file/folder directly
      | restore_machine | folder_hierarchy                 | restore_item                               |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | Test Report for Android 1.7.2 Release.docx |
    Then I use Windows Restore Manager to decrypt the file
    Then I check the decrypt job finished successfully

  @smoke @Winfryr-005 @winfryr_teardown
    Scenario: Win Fryr decrypt a folder contents
    When I visit cas host to be authenticated to do direct download from freyja site
    When I log in BUS console to select my restore machine
      | user_email          |
      | ken1020pkey@emc.com |
    Then I navigate to Freyja page to download an encrypted file/folder directly
      | restore_machine | folder_hierarchy                 | restore_item  |
      | CNENXUK7L2C     | C:/Users/xuk7/Documents/TestData | Symbol_Folder |
    Then I use Windows Restore Manager to decrypt the folder 'Symbol_Folder'
    Then I check the restore job finished successfully

  @Winfryr-006 @winfryr_lsh_teardown
    Scenario: Legal Search and Hold feature, export files and check export job status
    When I log in BUS console
    When I act as partner
      | partner name                   |
      | LSH Integration MozyEnt Noedit |
    Then I navigate to Freyja page to request to search and export files
      | keyword |
      | version |
    When I clear database folder of Mozy Restore Manager
    Then I use Windows Restore Manager to export files from the .mzdx seed
    Then I verify the export job status is 'Completed'
    Then I close LSH Windows Restore Manager from GUI

  @Winfryr-007 @winfryr_lsh_teardown
    Scenario: Legal Search and Hold feature, export files and generate edrm xmls
    When I log in BUS console
    When I act as partner
      | partner name                   |
      | LSH Integration MozyEnt Noedit |
    Then I navigate to Freyja page to request to search and export files
      | keyword |
      | version |
    When I clear database folder of Mozy Restore Manager
    Then I use Windows Restore Manager to export files from the .mzdx seed
    Then I export EDRM file with version 'v1.2'
    Then I export EDRM file with version 'v2.0'
    Then I close LSH Windows Restore Manager from GUI

  @Winfryr-008 @winfryr_lsh_teardown
    Scenario: Legal Search and Hold feature, export files and archive the export job
    When I log in BUS console
    When I act as partner
      | partner name                   |
      | LSH Integration MozyEnt Noedit |
    Then I navigate to Freyja page to request to search and export files
      | keyword |
      | version |
    When I clear database folder of Mozy Restore Manager
    Then I use Windows Restore Manager to export files from the .mzdx seed
    Then I archive the export job and check it in archived job list

  @Winfryr-009 @winfryr_lsh_teardown
    Scenario: Legal Search and Hold feature, export files and archive the export job
    When I log in BUS console
    When I act as partner
      | partner name                   |
      | LSH Integration MozyEnt Noedit |
    Then I navigate to Freyja page to request to search and export files
      | keyword |
      | iso     |
    When I clear database folder of Mozy Restore Manager
    Then I kick off an export job without waiting for it completed
    When I log in BUS console
    When I act as partner
      | partner name                   |
      | LSH Integration MozyEnt Noedit |
    Then I navigate to Freyja page to request to search and export files
      | keyword  |
      | Benefits |
    Then I use Windows Restore Manager to add an export job in queue

  @Winfryr-010 @winfryr_lsh_teardown
    Scenario: Legal Search and Hold feature, export files and archive the export job
    When I log in BUS console
    When I act as partner
      | partner name                   |
      | LSH Integration MozyEnt Noedit |
    Then I navigate to Freyja page to request to search and export files
      | keyword |
      | iso     |
    When I clear database folder of Mozy Restore Manager
    Then I kick off an export job without waiting for it completed
    Then I verify the export job status is 'Downloading'
    Then I expand action panel and click 'Pause' button to job 'default job'
    Then I verify the export job status is 'Paused'
    Then I expand action panel and click 'Resume' button to job 'default job'
    Then I verify the export job status is 'Downloading'
    Then I close LSH Windows Restore Manager from GUI

  @Winfryr-111 @winfryr_lsh_teardown
    Scenario: Legal Search and Hold feature, export files and archive the export job
    When I log in BUS console
    When I act as partner
      | partner name                   |
      | LSH Integration MozyEnt Noedit |
    Then I navigate to Freyja page to request to search and export files
      | keyword |
      | iso     |
    When I clear database folder of Mozy Restore Manager
    Then I kick off an export job without waiting for it completed
    Then I verify the export job status is 'Downloading'
    Then I expand action panel and click 'Cancel' button to job 'default job'
    Then I verify the confirm dialog will display about the cancel action and click action button
      | message                                   | action |
      | Are you sure you want to cancel this job? | Yes    |
    Then I verify the export job status is 'Cancelled'
    Then I close LSH Windows Restore Manager from GUI