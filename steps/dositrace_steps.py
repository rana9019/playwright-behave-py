from behave import given, when, then


@given("I am on the Dositrace page")
def step_impl(context):
    context.dositrace_page.dositrace_page_url()

@then("I verify all navigation menu items are present")
def step_impl(context):
    context.dositrace_page.verify_navigation_menu_items()

@when("I click on the left menu toggle button")
def step_impl(context):
    context.dositrace_page.click_left_menu_toggle()

@then("I verify the left navigation menu is toggled")
def step_impl(context):
    context.dositrace_page.verify_menu_toggle()

@when('I click on the dropdown arrow in the header')
def step_impl(context):
    context.dositrace_page.click_dropdown_arrow()

@then('I check the available applications')
def step_impl(context):
    context.dositrace_page.check_application_links()

@when('The notification count is displayed correctly')
def step_impl(context):
    context.dositrace_page.verify_notification_count()

@when('I click on "Tout marquer comme lu"')
def step_impl(context):
    context.dositrace_page.mark_all_as_read()

@then('I verify that the message "Vous avez 0 notifications" is displayed')
def step_impl(context):
    context.dositrace_page.verify_notifications_cleared()

@given("I am on the dashboard notification page")
def step_impl(context):
    context.dositrace_page.dashboard_notification_url()

@when('I click on the date input field')
def step_impl(context):
    context.dositrace_page.click_on_date_input()

@then("A calendar appears")
def step_impl(context):
    context.dositrace_page.verify_calendar_visibility()

@when('I click on the "{dropdown_name}" dropdown')
def step_impl(context, dropdown_name):
    context.dositrace_page.click_dropdown(dropdown_name)

@then('I should see the "{dropdown_name}" dropdown options')
def step_impl(context, dropdown_name):
    context.dositrace_page.verify_dropdown_option(dropdown_name)

@given("I am on the settings page")
def step_impl(context):
    context.dositrace_page.settings_url()

@when('they select "{language}"')
def step_impl(context, language):
    context.dositrace_page.select_language(language)

@then('the application language should change to "{language}"')
def step_impl(context, language):
    context.dositrace_page.verify_language_change(language)

@when('They click the "Edit" button')
def step_impl(context):
    context.dositrace_page.click_editing_button()

@then("they should be redirected to the profile modification page")
def step_impl(context):
    context.dositrace_page.verify_modify_redirection()

@when("He accesses the profile page")
def step_impl(context):
    context.dositrace_page.go_to_profile_page()

@when("He clicks on the button to edit the profile")
def step_impl(context):
    context.dositrace_page.click_edit_button()

@when('He modifies the "Fonction" field with "testing"')
def step_impl(context):
    context.dositrace_page.edit_function_field()

@when("He clicks on the Modifier button to save")
def step_impl(context):
    context.dositrace_page.submit_profile()

@then('The field "Fonction" must contain "testing"')
def step_impl(context):
    context.dositrace_page.verify_function_value()

@when("The user clicks on the username")
def step_impl(context):
    context.dositrace_page.click_username()

@when("I click on the 'Annuler' button")
def step_impl(context):
    context.dositrace_page.click_return_button()

@then("they should be redirected to the profile page")
def step_impl(context):
    context.dositrace_page.verify_direction()

@when('they click on the "Ajouter" button')
def step_impl(context):
    context.dositrace_page.click_add_button()

@then("a dropdown menu with 9 block options should appear")
def step_impl(context):
    context.dositrace_page.verify_dropdown_options()

@when('they select an option from the dropdown menu')
def step_impl(context):
    context.dositrace_page.select_option()

@then('they confirm the addition by clicking on the "Valider" button')
def step_impl(context):
    context.dositrace_page.confirm_addition()

@then('a success message should appear confirming the update')
def step_impl(context):
    context.dositrace_page.verify_success_message()

@when('they click on the "Supprimer" button')
def step_impl(context):
    context.dositrace_page.click_supprimer()

@when('I click on the trash icon')
def step_impl(context):
    context.dositrace_page.click_trash_icon()

@then('the "Valider" button should appear')
def step_impl(context):
    context.dositrace_page.verify_valider_button()

@when('they click on the "Valider" button')
def step_impl(context):
    context.dositrace_page.click_valider()

@when('He selects the year "2024"')
def step_impl(context):
    context.dositrace_page.select_year()

@when('He selects the UF "Radiologie 3"')
def step_impl(context):
    context.dositrace_page.select_uf()

@then("The dashboard must be updated with the new values")
def step_impl(context):
    context.dositrace_page.verify_dashboard_update()

@then("the period options must be visible")
def step_impl(context):
    context.dositrace_page.verify_period_options()

@when("The user opens the UF menu")
def step_impl(context):
    context.dositrace_page.open_uf_menu()

@then("All available UFs must be displayed")
def step_impl(context):
    context.dositrace_page.verify_uf_options()

@when("The user views the Worklist")
def step_impl(context):
    context.dositrace_page.open_worklist()

@then("Each item in the Worklist must display the required fields 'Heure', 'Patient(s)' and 'Équipement'")
def step_impl(context):
    context.dositrace_page.verify_worklist_fields()

@when('The user clicks on the link "Liste complète des examens planifiés"')
def step_impl(context):
    context.dositrace_page.click_worklist_link()

@when("The user clicks on the button 'Accéder aux examens'")
def step_impl(context):
    context.dositrace_page.click_exam_button()

@when("The user clicks on the button 'Accéder aux patients'")
def step_impl(context):
    context.dositrace_page.click_patient_button()

@then('The patient search page must be displayed')
def step_impl(context):
    context.dositrace_page.verify_exam_url()

@when('The user clicks on the link "Voir l\'ensemble des statistiques"')
def step_impl(context):
    context.dositrace_page.click_static_link()

@then('The statistics page must be displayed')
def step_impl(context):
    context.dositrace_page.verify_static_url()

@when("He retrieves the number of unresolved alerts displayed")
def step_impl(context):
    context.dositrace_page.get_alertes_non_traitees()

@when('The user clicks on the link "Alertes non traitées"')
def step_impl(context):
    context.dositrace_page.click_alerts_link()

@then("He compares the displayed number of alerts with the actual number in the alerts table")
def step_impl(context):
    context.dositrace_page.compare_alertes()

@when('The user clicks on the link "PROTOCOLES NON RELIES"')
def step_impl(context):
    context.dositrace_page.click_protocol_link()

@when('The user clicks on the link "MEMBRES NON RELIES"')
def step_impl(context):
    context.dositrace_page.click_members_link()

@when('The user clicks on the link "Patients sans examen"')
def step_impl(context):
    context.dositrace_page.click_patients_link()

@then("Each alert item must display the exam date, type, breach, and patients")
def step_impl(context):
    context.dositrace_page.verify_table_columns()

@when("I click on the 'Alertes' item on the dashboard")
def step_impl(context):
    context.dositrace_page.click_alertes()

@then("I must be redirected to the Alertes menu")
def step_impl(context):
    context.dositrace_page.verify_redirection()


@then("The Information item must display the internet access and updates")
def step_impl(context):
    context.dositrace_page.verify_informations()

@then("The Documents item must contain the DOSITRACE and Configuration Center guides")
def step_impl(context):
    context.dositrace_page.verify_documents()

@when("I press the button at the top right")
def step_impl(context):
    context.dositrace_page.click_chart_button()

@then("A menu must be displayed with download and print options")
def step_impl(context):
    context.dositrace_page.verify_menu_display()

@then("I can download the charter in PNG, JPEG, PDF, or SVG")
def step_impl(context):
    context.dositrace_page.verify_download_options()

@when("I click on the Patients button")
def step_impl(context):
    context.dositrace_page.click_patients_button()

@then("The options 'Actifs' and 'Supprimés' are available")
def step_impl(context):
    context.dositrace_page.check_actifs_and_supprimes_options()

@when('I select "{etat}" from the dropdown list "État"')
def step_impl(context, etat):
    context.dositrace_page.select_etat(etat)

@when("I click on the button 'Filtrer'")
def step_click_filtrer(context):
    context.dositrace_page.click_filtrer_button()

@when("I click on the first patient's first name")
def step_impl(context):
    context.dositrace_page.click_first_patient_first_name()

@then('The patient should be deleted')
def step_impl(context):
    context.dositrace_page.verify_patient_deleted()

@then('The link to mark all notifications as read is visible')
def step_impl(context):
    context.dositrace_page.verify_mark_as_read_link()

@then('The link to view all notifications is visible')
def step_impl(context):
    context.dositrace_page.verify_view_all_notifications_link()

@then("I click on 'Voir toutes les notifications' link and verify the notifications page is opened")
def step_impl(context):
    context.dositrace_page.click_view_all_notifications()

@then("The Worklist window must open")
def step_impl(context):
    context.dositrace_page.verify_worklist_open()

