Feature: NRD NRI Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_481
  Scenario: User selects a period from the available options
    Given I am on the Calcul par protocole page
    When I click on the left menu toggle button
    When The user clicks on the period "2021"
    Then The period "2021" is selected
    When The user clicks on the period "2022"
    Then The period "2022" is selected
    When The user clicks on the period "2023"
    Then The period "2023" is selected
    When The user clicks on the period "12 derniers mois"
    Then The period "12 derniers mois" is selected

  @A_482
  Scenario: User clicks on "Ajouter un filtre" and sees the filter section with options
    Given I am on the Calcul par protocole page
    When I click on the button 'Ajouter des filtres'
    Then A section with the filters "UF", "Equipement", "Pédiatrique", and "Nombre d'examens" is displayed

  @A_487
  Scenario: User performs a search in the "Equipement" filter field and filters the results correctly
    Given I am on the Calcul par protocole page
    When I click on the button 'Ajouter des filtres'
    When The user selects "AXIOM Iconos R200 C90-C" from the dropdown list
    Then I click on the button filter "input#fil"
    Then Wait
    Then The results in the table should display only entries with "AXIOM Iconos R200 C90-C"

  @A_488
  Scenario: Click on "Réinitialiser" to clear all filters on the "Calcul par protocol" page
    Given I am on the Calcul par protocole page
    When I click on the button 'Ajouter des filtres'
    When I fill up some filters
    And I click on the "Réinitialiser" right bar
    Then All the filters fields should be reset

  @A_489
  Scenario: Verify that the user can change the number of results of the list nrd protocol raw per page
    Given I am viewing the list nrd protocol raw
    When The user selects "10" from the "select[name='tablenotification_length']" dropdown
    Then The displayed results should show "1 à 10" in "div#tablenotification_info"
    When The user selects "25" from the "select[name='tablenotification_length']" dropdown
    Then The displayed results should show "1 à 25" in "div#tablenotification_info"
    When The user selects "50" from the "select[name='tablenotification_length']" dropdown
    Then The displayed results should show "1 à 50" in "div#tablenotification_info"
    When The user selects "100" from the "select[name='tablenotification_length']" dropdown
    Then The displayed results should show "1 à 100" in "div#tablenotification_info"

  @A_491
  Scenario: The table can be sorted by Protocole
    Given I am on the Calcul par protocole page
    When I click on the left menu toggle button
    When The user clicks once on the column header "Protocole machine"
    Then The table must be sorted in descending order by "#patient tbody tr td.sorting_1 a"
    When The user clicks once on the column header "Protocole machine"
    Then The table must be sorted in ascending order by "#patient tbody tr td.sorting_1 a"

  @A_490
  Scenario: Verify the global searching in Calcul par protocol page
    Given I am on the Calcul par protocole page
    Then Wait
    When I take the first value from the table 'table#tablenotification tbody'
    And I search for it in the global search field 'input[aria-controls='tablenotification']'
    Then I should see the correct row displayed in the table 'table#tablenotification tbody tr'

  @A_495
  Scenario: Display of the Modalities dropdown list
    Given I am on the View IRSN page
    When The user clicks on 'Modalité'
    Then A dropdown list with the available modalities should be displayed

  @A_496
  Scenario: The Equipment and Protocol dropdown lists appear after selecting a modality
    Given I am on the View IRSN page
    When I select the modality "Radiologie conventionnelle CR CR"
    Then The Equipment field is updated with "AXIOM LUMINOS VO"
    Then The Protocol field is updated with "Bassin" with value "905"

  @A_497
  Scenario: Verify Calendar Popup in IRSN page
    Given I am on the View IRSN page
    When Clicking on the Start Date field displays a calendar allowing date selection

  @A_498
  Scenario: Verify selecting date from the calendar in IRSN page
    Given I am on the View IRSN page
    When The user manually enters a date in the field "#datepicker"

  @A_500
  Scenario: User can fill or modify the Number of exams field using input or arrows
    Given I am on the View IRSN page
    When The user fills the Number of exams field with 5
    Then The Number of exams field value should be 5
    When The user increments the Number of exams field by 1 using the arrow
    Then The Number of exams field value should be 6
    When The user decrements the Number of exams field by 1 using the arrow
    Then The Number of exams field value should be 5

  @A_501
  Scenario: User can check the checkbox for patients with weight and height information
    Given I am on the View IRSN page
    When The user checks the "IMC renseigné et compris entre 17 et 35" checkbox
    Then The checkbox "IMC renseigné et compris entre 17 et 35" should be checked

  @A_502
  Scenario: User submits the form and sees success message
    Given I am on the View IRSN page
    When I select the modality "Radiologie conventionnelle CR CR"
    Then The Equipment field is updated with "AXIOM LUMINOS VO"
    Then The Protocol field is updated with "Bassin" with value "905"
    Then The user selects a date "29/08/2023" in the field "#datepicker"
    When The user clicks the "Valider" button
    Then A success message "Donnée mise à jour avec succès" should appear

  @A_504
  Scenario: User submits the form and go to "Radiologie" page
    Given I am on the View IRSN page
    When I select the modality "Radiologie conventionnelle CR CR"
    Then The Equipment field is updated with "AXIOM LUMINOS VO"
    Then The Protocol field is updated with "Bassin" with value "905"
    Then The user selects a date "29/08/2023" in the field "#datepicker"
    When The user clicks the "Valider" button
    Then I should see the text "IRSN Radiologie"

  @A_514
  Scenario: User submits the form and go to "Recueil NRD IRSN" page
    Given I am on the View IRSN page
    When I select the modality "Radiologie conventionnelle CR CR"
    Then The Equipment field is updated with "AXIOM LUMINOS VO"
    Then The Protocol field is updated with "Bassin" with value "905"
    Then The user selects a date "29/08/2023" in the field "#datepicker"
    When The user clicks the "Valider" button
    When I click the "Retour" button
    Then I should see the text "Recueil NRD IRSN"

  @A_515
  Scenario: The page displays two tabs: Adult and Pediatrics
    Given I am on the List protocol national page
    Then The tabs "Adulte" and "Pédiatrie" must be visible
