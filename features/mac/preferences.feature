# Created by zhouf10 at 7/25/17
Feature: The functionality of Mozy Preferences window
  As MacMozy user, I want to use the Preferences window to operate Mozy


  Background:
    When Mac Client is activated with credential '{env}_{oemclient}'

  @high @mac-05000 @cleanup @mac_setup @mac_teardown
  Scenario: Launch backup by clicking "Back Up Now" button
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-05000   | mac-05000   | 1000      | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | mac-05000    |
    When I click the "Back Up Now" button
    Then I shall see the text on the "Back Up Now" button changes to "Pause Backup"
    When I click the status icon
    Then I shall see the action field displays as "Pause Backup"

  @high @mac-05005 @cleanup @mac_setup @mac_teardown
  Scenario: Verify the functionality of "History" button
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-05005   | mac-05005   | 1000      | txt      | testdata  |
     And I add backup dirs as
      | include_dirs |
      | mac-05005    |
    When I start backup from GUI
     And I wait to backup finished
    When I click the "History..." button
    Then I shall see a sheet containing the backup history is pulled down

  @high @mac-05050 @cleanup @mac_setup @mac_teardown
  Scenario: Verify functionality of selecting recommended backup sets
    When I create 1 test files under "Documents" with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-05050   | mac-05050   | 1000      | txt      | testdata  |
     And I select the recommended backup sets "Documents Folder"
    # Then I expected "Documents Folder" appears in the top pane of selection tab
    Then I expected the selected files are shown by "Awaiting Backup:"
    When I delete test data under "Documents" with
      | file_folder |
      | mac-05050   |
