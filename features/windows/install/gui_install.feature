Feature: Install Windows Client via GUI

#  Background:
#    When Windows Client is not installed


  @install @KAL-1
  Scenario: Welcome window appears at launch
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window

  @KAL-2
  Scenario: Cancel dialog launched on Welcome windows
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I click Cancel button

  @KAL-3
  Scenario: Deselecting both options on Welcome window
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I click Install button directly

  @KAL-5
  Scenario: Choose Yes on Cancel dialog
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I click Cancel button
    When I click Yes button on Cancel Dialog

  @KAL-6
  Scenario: Choose No on Cancel dialog
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I click Cancel button
    When I click No button on Cancel Dialog

  @KAL-7
  Scenario: Click finish at cancel dialog
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I click Cancel button
    When I click Yes button on Cancel Dialog
    When I click Finish button

  @KAL-8 @KAL-9
  Scenario: Selecting the "Change Install Location"
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I deselect View the Agreement
    When I select Change Install Location
    When I click Next button
    When I set a location with \Mozy\
    When I click Install button
    When I see an alert information

  @KAL-10
  Scenario: Changing Install Location works well
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I deselect View the Agreement
    When I select Change Install Location
    When I click Next button
    When I set a location with C:\Mozy\
    When I click Install button
    When I open Login window

  @KAL-11
  Scenario: New nested install location works properly
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I deselect View the Agreement
    When I select Change Install Location
    When I click Next button
    When I set an new location with 1 subdirectory
    When I click Install button
    When I open Login window

  @KAL-12
  Scenario: New double-nested install location works properly
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I deselect View the Agreement
    When I select Change Install Location
    When I click Next button
    When I set an new location with 2 subdirectory
    When I click Install button
    When I open Login window

  @KAL-15 @cancel_install
  Scenario:Cancel Install during Installing
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I click Next button
    When I click Accept button
    When I click Cancel button
    When I click Yes button on Cancel Dialog

  @install @smoke @gui @KAL-18
  Scenario: Install Windows Client from GUI
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I click Next button
    When I click Accept button


  @install @smoke @gui
  Scenario: Install Windows Client from GUI
    When I download Windows Client from Jenkins and launch installer
    When I open Welcome window
    When I click Install button directly
