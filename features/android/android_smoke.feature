Feature: Android demo feature
  Demo Feature for Client Automation

  @smoke @Android-001
  Scenario: Install Mozy APP to emulator and log in with default account
    When I start Android simulator and appium server
    Then I install Mozy Client to the Android Simulator
    Then I log in Mozy Android App with default account

  @smoke @Android-002
  Scenario: Check version of Mozy APP
    Then I verify Mozy Android APP version

  @smoke @Android-003
  Scenario: Check UI of My Mozy tab
    Then I view My Mozy tab and check all elements

  @smoke @Android-004
  Scenario: Check UI of All Files tab
    Then I view All Files tab and check all elements

  @smoke @Android-005
  Scenario: Check UI of Sync folder, and verify search function
    Then I view the files in Sync folder
    Then I search file in Sync folder with keyword '.txt'

  @smoke @Android-006
  Scenario: Check UI of each backup machine, and verify search function
    Then I view All Files tab and check all elements
    Then I click into each backup machine and search with keyword '.txt'

  @smoke @Android-011
  Scenario: Verify sign out function of Mozy APP
    Then I sign out Mozy Android App

  @smoke @Android-012
  Scenario: Tear down job, close emulator and Appium server
    Then I close Android simulator and appium server