Feature: Exams Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_126
  Scenario: Filling calendar manually in Exams page
    Given I am on the Examens page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    When The user manually enters a date in the field "#daterangepicker1"

  @A_127
  Scenario: A date can be entered manually
    Given I am on the Examens page
    When The user clicks on "#daterangepicker1"
    And The user manually enters a date in the field "#daterangepicker1"

  @A_131
  Scenario Outline: Quickly select a date range
    Given I am on the Examens page
    When I click on the left menu toggle button
    When The user clicks on the button "<periode>"
    Then The selected dates match the period "<periode>"

    Examples:
      | periode           |
      | 3 derniers mois      |
      |  6 derniers mois  |
      |  12 derniers mois  |
      | dernier mois  |