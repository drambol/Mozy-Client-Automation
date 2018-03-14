Feature: iOS demo feature
  Demo Feature for Client Automation

  @smoke @iOS-001
  Scenario: Start Appium Server, launch iOS simulator, install Mozy APP and log in
    When I start iOS simulator and install Mozy iOS APP
    Then I log in Mozy iOS App with default account
#
  @smoke @iOS-002
  Scenario: Check UI of My Mozy tab
    Then I view My Mozy tab and check all elements in Mozy iOS

  @smoke @iOS-003
  Scenario: Check UI of All Files tab
    Then I view All Files tab and check all elements in Mozy iOS

  @smoke @iOS-004
  Scenario: Check UI of Sync folder, and verify search function
    Then I view the files in Sync folder in Mozy iOS
    Then I search file in Sync folder with keyword txt in Mozy iOS

  @smoke @iOS-005
  Scenario: Check UI of each backup machine, and verify search function
    Then I view All Files tab and check all elements in Mozy iOS
    Then I click into each backup machine and search with keyword MozyPro in Mozy iOS

  @smoke @iOS-011
  Scenario: iOS demo scenario 2
    Then I verify Mozy iOS APP version is 1.72.201718702

  @smoke @iOS-012
  Scenario: iOS demo scenario 3
    Then I logout Mozy iOS APP
    Then I close iOS simulator and appium server