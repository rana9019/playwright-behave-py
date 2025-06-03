Feature: Alerts Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_440
  Scenario: By clicking on the 'Processed' dropdown, you can choose: yes, no, all
    Given I am on the Alertes page
    When I click on the button 'Ajouter des filtres'
    Then The "Traité" dropdown should contain: Tous, Oui, Non

  @A_441
  Scenario: Perform a search in the Filter field for the last 6 months
    Given I am on the Alertes page
    When I click on the "a#b3" button
    And I click on the "button#fil" button
    Then I should see filtered results in the data table

  @A_442
  Scenario: A click on the button "ajouter un filtre" displays the expected filters
    Given I am on the Alertes page
    When I click on the button 'Ajouter des filtres'
    Then I should see the following filters: Traité, Niveau, Type alerte, Equipement, Modalité

  @A_445
  Scenario: Verify if the calendar appears
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears

  @A_446
  Scenario: Filling calendar manually in Alerts page
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    When The user manually enters a date in the field "#daterangepicker1"

  @A_448
  Scenario: The dropdown list of the Level field allows choosing: 1 or 2
    Given I am on the Alertes page
    When I click on the button 'Ajouter des filtres'
    Then The "Niveau" dropdown should contain: 1, 2

  @A_449
  Scenario: The Filter button is functional and displays the notifications based on the selected criteria
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I click on the button 'Ajouter des filtres'
    When I select "1" in the "Niveau" dropdown
    And I click on the 'Filtrer' button
    Then The notifications should be filtered by "Niveau" with value "1"

  @A_450
  Scenario: Verify the global searching
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I take the first value from the table 'table#DataTables_Table_0 tbody'
    And I search for it in the global search field 'input[aria-controls='DataTables_Table_0']'
    Then I should see the correct row displayed in the table 'table#DataTables_Table_0 tbody tr'

  @A_451
  Scenario: Pagination in Alertes page
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When The user selects "10" from the "select[name='DataTables_Table_0_length']" dropdown
    Then The displayed results should show "1 à 10" in "div#DataTables_Table_0_info"
    When The user selects "25" from the "select[name='DataTables_Table_0_length']" dropdown
    Then The displayed results should show "1 à 25" in "div#DataTables_Table_0_info"
    When The user selects "50" from the "select[name='DataTables_Table_0_length']" dropdown
    Then The displayed results should show "1 à 50" in "div#DataTables_Table_0_info"
    When The user selects "100" from the "select[name='DataTables_Table_0_length']" dropdown
    Then The displayed results should show "1 à 100" in "div#DataTables_Table_0_info"

  @A_452
  Scenario: The table can be sorted by "Protocole"
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When The user clicks once on the column header "Protocole"
    Then The table must be sorted in descending order by "#patient tbody tr td.sorting_1 a"
    When The user clicks once on the column header "Protocole"
    Then The table must be sorted in ascending order by "#patient tbody tr td.sorting_1 a"

  @A_454
  Scenario: By checking the box of an examination, it is possible to View the examination or Process it
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Non' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    Then The "input#view-study" button should be visible
    And The "button#treatment-alert" button should be visible

  @A_455
  Scenario: The examination can be viewed
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Non' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "input#view-study" button
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ViewStudy?study=*"

  @A_456
  Scenario: The examination can be processed
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Non' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#treatment-alert" button
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/CreateTreatmentAlert"

  @A_457
  Scenario: User enters the actual reasons and confirms
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Non' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#modify-treatment" button
    When I click on the suggested cause "IMC"
    Then The cause "IMC" should appear in the "Causes réelles" section
    When I click the 'Valider' button

  @A_458
  Scenario: By clicking on Cancel, the user is redirected and sees the information message
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Non' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#treatment-alert" button
    When I click the "Annuler" button
    Then I should see the message "Aucune modification n a été apportée"

  @A_459
  Scenario: By clicking on Validate, the success message appears
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Non' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#treatment-alert" button
    When I write a comment in the textarea
    When I click the 'Valider' button
    Then I should see the success message "Donnée mise à jour avec succès"

  @A_460
  Scenario: Move a suggested cause to the actual causes and vice versa
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Non' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#modify-treatment" button
    When I click on the suggested cause "IMC"
    Then The cause "IMC" should appear in the "Causes réelles" section
    When I click again on the cause "IMC" in the "Causes réelles" section
    Then The cause "IMC" should appear back in the "Causes suggérées" section

  @A_461
  Scenario: It is possible to view "Afficher l'examen", "Afficher le traitement" or "Éditer le traitement"
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Oui' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    Then The "input#view-study" button should be visible
    And The "button#view-treatment" button should be visible
    And The "button#modify-treatment" button should be visible

  @A_463
  Scenario: It is possibke to click on "Modifier", "Accéder à l'examen", and "Accéder aux alertes"
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Oui' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#view-treatment" button
    Then The "a.btn-primary[href^="ModifyTreatmentAlert"]" button should be visible
    And The "a.btn-secondary[href^="ViewStudy"]" button should be visible
    And The "a.btn-secondary[href="ViewAlerts"]" button should be visible

  @A_464
  Scenario: The editing treatment can be accessed
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Oui' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#view-treatment" button
    When I click on the "a.btn-primary[href^="ModifyTreatmentAlert"]" button
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ModifyTreatmentAlert?idtreatment=*"

  @A_465
  Scenario: Exams can be accessed
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Oui' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#view-treatment" button
    When I click on the "a.btn-secondary[href^="ViewStudy"]" button
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ViewStudy?study=*"

  @A_466
  Scenario: Alerts can be accessed
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Oui' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#view-treatment" button
    When I click on the "a.btn-secondary[href="ViewAlerts"]" button
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ViewAlerts"

  @A_467
  Scenario: The alert can be edited
    Given I am on the Alertes page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "01/04/2022 - 30/04/2025" in the field "#daterangepicker1"
    When I click on the left menu toggle button
    When I click on the "button#fil" button
    When I search for 'Oui' in the global search field 'input[aria-controls='DataTables_Table_0']'
    When I click on the first radio button in the table
    When I click on the "button#modify-treatment" button
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ModifyTreatmentAlert"