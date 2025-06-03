Feature: Rapport Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_541
  Scenario: Filling calendar manually in Static Rapport page
    Given I am on the Rapport Statistiques page
    When The user clicks on "input#period"
    Then The calendar "input#period" appears
    When The user manually enters a date in the field "input#period"