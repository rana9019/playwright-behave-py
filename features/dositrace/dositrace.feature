Feature: Dositrace Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_18
  Scenario: Verify navigation menu items
    Given I am on the Dositrace page
    Then I verify all navigation menu items are present

  @A_19
  Scenario: Toggle the left navigation menu
    Given I am on the Dositrace page
    When I click on the left menu toggle button
    Then I verify the left navigation menu is toggled

  @A_21
  Scenario: Verify that the applications are displayed after clicking the menu arrow
    Given I am on the Dositrace page
    When I click on the dropdown arrow in the header
    Then I check the available applications

  @A_22
  Scenario: Verify the visibility of notification links upon clicking the bell icon
    Given I am on the Dositrace page
    When The notification count is displayed correctly
    Then The link to mark all notifications as read is visible
    And The link to view all notifications is visible

  @A_25
  Scenario: Verify navigation to the Notifications page when clicking on 'Voir toutes les notifications' link
    Given I am on the Dositrace page
    When The notification count is displayed correctly
    Then I click on 'Voir toutes les notifications' link and verify the notifications page is opened

  @A_26
  Scenario: Mark all notifications as read
    Given I am on the Dositrace page
    When The notification count is displayed correctly
    And I click on "Tout marquer comme lu"
    Then I verify that the message "Vous avez 0 notifications" is displayed

  @A_27
  Scenario: Verify Calendar Popup on Clicking Date Input Field
    Given I am on the dashboard notification page
    When I click on the date input field
    Then A calendar appears

  @A_28
  Scenario: Display of dropdown lists to refine searches
    Given I am on the dashboard notification page
    When I click on the "Vu" dropdown
    Then I should see the "Vu" dropdown options

    When I click on the "Type" dropdown
    Then I should see the "Type" dropdown options

    When I click on the "Afficher" dropdown
    Then I should see the "Afficher" dropdown options

  @A_35
  Scenario: Change language by selecting a radio button
    Given I am on the settings page
    When They select "English"
    Then The application language should change to "English"

  @A_37
  Scenario: Click on the Edit button to modify the profile
    Given I am on the settings page
    When They click the "Edit" button
    Then They should be redirected to the profile modification page

  @A_40
  Scenario: The user updates the profile information
    Given I am on the Dositrace page
    When The user clicks on the username
    And He accesses the profile page
    And He clicks on the button to edit the profile
    And He modifies the "Fonction" field with "testing"
    And He clicks on the Modifier button to save
    Then The field "Fonction" must contain "testing"

  @A_42
  Scenario: Click on the "Annuler" button to cancel the modification and return to the profile page
    Given I am on the Dositrace page
    When The user clicks on the username
    And He accesses the profile page
    And He clicks on the button to edit the profile
    When I click on the 'Annuler' button
    Then They should be redirected to the profile page

  @A_47
  Scenario: Click on "Ajouter" to display block options
    Given I am on the Dositrace page
    When They click on the "Ajouter" button
    Then A dropdown menu with 9 block options should appear

  @A_48
  Scenario: Selecting an option and confirming its addition to the dashboard
    Given I am on the Dositrace page
    When They click on the "Ajouter" button
    When They select an option from the dropdown menu
    Then They confirm the addition by clicking on the "Valider" button

  @A_49
  Scenario: Selecting an option and confirming the success message
    Given I am on the Dositrace page
    When They click on the "Ajouter" button
    When They select an option from the dropdown menu
    Then They confirm the addition by clicking on the "Valider" button
    And A success message should appear confirming the update

  @A_53
  Scenario: Verifying the "Valider" button appears
    Given I am on the Dositrace page
    When They click on the "Supprimer" button
    And I click on the trash icon
    Then The "Valider" button should appear

  @A_54
  Scenario: Delete a block from the dashboard
    Given I am on the Dositrace page
    When They click on the "Supprimer" button
    And I click on the trash icon
    Then The "Valider" button should appear
    When They click on the "Valider" button

  @A_55
  Scenario: Confirming the success message after deleting a block from the dashboard
    Given I am on the Dositrace page
    When They click on the "Supprimer" button
    And I click on the trash icon
    Then The "Valider" button should appear
    When They click on the "Valider" button
    Then A success message should appear confirming the update

  @A_57
  Scenario: Verify that the data is updated after changing the filters
    Given I am on the Dositrace page
    When He selects the year "2024"
    And He selects the UF "Radiologie 3"
    Then The dashboard must be updated with the new values

  @A_58
  Scenario: Verify that all period options are visible
    Given I am on the Dositrace page
    Then The period options must be visible

  @A_59
  Scenario: Verify that all the UFs are visible in the dropdown list
    Given I am on the Dositrace page
    When The user opens the UF menu
    Then All available UFs must be displayed

  @A_63
  Scenario: Verify the display of the fields in the Worklist
    Given I am on the Dositrace page
    When The user views the Worklist
    Then Each item in the Worklist must display the required fields 'Heure', 'Patient(s)' and 'Équipement'

  @A_64
  Scenario: Verify that the Worklist window opens
    Given I am on the Dositrace page
    When The user clicks on the link "Liste complète des examens planifiés"
    Then The Worklist window must open

  @A_65
  Scenario: Verify the redirection to the exam search page
    Given I am on the Dositrace page
    When I click on the left menu toggle button
    When The user clicks on the button 'Accéder aux examens'
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/SearchStudy?month=*"

  @A_66
  Scenario: Verify the redirection to the patient search page
    Given I am on the Dositrace page
    When I click on the left menu toggle button
    When The user clicks on the button 'Accéder aux patients'
    Then The patient search page must be displayed

  @A_69
  Scenario: Verify the redirection to the statistics page
    Given I am on the Dositrace page
    When I click on the left menu toggle button
    When The user clicks on the link "Voir l'ensemble des statistiques"
    Then The statistics page must be displayed

  @A_71
  Scenario: The Reminders block on the dashboard is functional
    Given I am on the Dositrace page
    When He retrieves the number of unresolved alerts displayed
    And The user clicks on the link "Alertes non traitées"
    Then He compares the displayed number of alerts with the actual number in the alerts table

  @A_72
  Scenario: Verify the redirection to the unresolved alerts page
    Given I am on the Dositrace page
    When The user clicks on the link "Alertes non traitées"
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ViewAlerts?dashboardPeriod=currMonth"

  @A_75
  Scenario: The user clicks on "PROTOCOLES NON RELIES" and is redirected to "Table de correspondance des protocoles"
    Given I am on the Dositrace page
    When I click on the left menu toggle button
    When The user clicks on the link "PROTOCOLES NON RELIES"
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/CreateProtocolMapping#praw"

  @A_79
  Scenario: The user clicks on "Patients sans examen" and is redirected to "Patients sans examen"
    Given I am on the Dositrace page
    When I click on the left menu toggle button
    When The user clicks on the link "Patients sans examen"
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/PatientsWithoutStudy"

  @A_82
  Scenario: Verify the display of information in the alerts
    Given I am on the Dositrace page
    Then Each alert item must display the exam date, type, breach, and patients

  @A_83
  Scenario: Clicking on the 'Alertes' item on the dashboard redirects to the Alertes menu
    Given I am on the Dositrace page
    When I click on the left menu toggle button
    When I click on the 'Alertes' item on the dashboard
    Then I must be redirected to the Alertes menu

  @A_90
  Scenario: Verify the display of information on the dashboard
    Given I am on the Dositrace page
    Then The Information item must display the internet access and updates

  @A_91
  Scenario: Verify the presence of user guides in the Documents item
    Given I am on the Dositrace page
    Then The Documents item must contain the DOSITRACE and Configuration Center guides

  @A_99
  Scenario: Verify that the button allows printing and downloading the charter
    Given I am on the Dositrace page
    When I press the button at the top right
    Then A menu must be displayed with download and print options
    And I can download the charter in PNG, JPEG, PDF, or SVG

  @A_217
  Scenario: Verify the display and selection of Active and Deleted options
    Given I am on the Dositrace page
    When I click on the Patients button
    Then The options 'Actifs' and 'Supprimés' are available