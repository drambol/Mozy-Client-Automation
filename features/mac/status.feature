# Created by zhouf10 at 7/20/17
Feature: The functionality of Mozy status menu
  As MacMozy user, I want to use the status menu to operate Mozy


  Background:
    When Mac Client is activated with credential '{env}_{oemclient}'

  @high @mac-04000 @cleanup @mac_setup @mac_teardown
  Scenario: Click status icon to check the menu bar
    When I click the status icon
    Then  The following menu items are present
      | name      |
      | Backed Up |
      | No Files Selected For Backup |
      | Last Backup |
      | Backup Up Now |
      | Suspend Scheduled Backups For |
      | Restore Files |
      | Open Mozy     |

  @high @mac-04005 @cleanup @mac_setup @mac_teardown
  Scenario: Right-click status icon to check the menu bar
    When I right-click the status icon
    Then  The following menu items are present
      | name      |
      | Backed Up |
      | No Files Selected For Backup |
      | Last Backup |
      | Backup Up Now |
      | Suspend Scheduled Backups For |
      | Restore Files |
      | Open Mozy     |
      | View Log File |
      | Collect Log Files |
      | Open Decrypt |
      | Uninstall Mozy |

  @high @mac-04010 @cleanup @mac_setup @mac_teardown
  Scenario: Launch backup by clicking status menu item
    When I create 2 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-04010   | mac-04010   | 1000      | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | mac-04010    |
    When I click the menu item "Back Up Now"
    Then I shall see the action field displays as "Pause Backup"

  @high @mac-04015 @cleanup @mac_setup @mac_teardown
  Scenario: Pending status field gets updated when files added
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-04015   | mac-04015   | 1048576   | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | mac-04015    |
    When I click the status icon
    Then I shall see the pending status field displays as "Files Pending: 10 (10.49 MB)"
