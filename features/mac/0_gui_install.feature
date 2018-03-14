Feature: Install Mac Client via GUI
# Run GUI installation. Clean installation is better but not mandatory


  Background:
    When Mac Client is not installed

  @smoke @mac-00005 @mac_teardown
  Scenario: Install Mac Client via GUI
    When I launch installer
    Then I shall see the installer window is launched
    When I proceed with the installation
    Then I shall see the installation is finished successfully
    Then I shall see the installer correctly installed necessary files
    Then I shall see the related processes are started
    Then I shall see the setup assistant is launched

  @medium @mac-00010 @mac_teardown
  Scenario: Mozy EULA panel of installation requires acceptance
    When I launch installer
     And I proceed to the EULA panel
    Then I shall see "Software License Agreement" in installer window
    When I click the button "Go Back" in installer window 1 times
    Then I shall see "Important Information" in installer window
    When I click the button "Continue" in installer window 2 times
    Then I shall see the Apple Licence Acceptance page is shown
    When I click the button "Read License" in Apple Licence Acceptance page
    Then I shall see the Apple Licence Acceptance page is collapsed
    When I click the button "Continue" in installer window 1 times
     And I click the button "Disagree" in Apple Licence Acceptance page
    Then I shall see the installer window is closed
    When I install the client silently
