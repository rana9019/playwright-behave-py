from behave import given, when, then


@given("I am on the Risk Patient page")
def step_impl(context):
    context.risk_patient_page.risk_patient_page_url()

@when("I fill in some filters")
def step_impl(context):
    context.risk_patient_page.fill_filters()

@then("All filter fields should be reset")
def step_impl(context):
    context.risk_patient_page.verify_filters_reset()

@when('I click on "Oui" in "Suivi nécessaire"')
def step_impl(context):
    context.risk_patient_page.click_oui_in_suivi_necesaire()

@then("The table should display only the rows with 'Oui' selected")
def step_verify_filtered_results(context):
    context.risk_patient_page.verify_table_filtered_by_oui()

@when("The user selects 'Oui' in the filter")
def step_select_oui_filter(context):
    context.risk_patient_page.select_oui_filter()

@when("I get the column headers of the first table")
def step_impl(context):
    context.first_table_columns = context.risk_patient_page.get_table_header(context.page, 1)

@when("I get the column headers of the second table")
def step_impl(context):
    context.second_table_columns = context.risk_patient_page.get_table_header(context.page, 2)

@then("All column headers in the second table should exist in the first table")
def step_impl(context):
    for col in context.second_table_columns:
        assert col in context.first_table_columns, f"Missing column: {col}"

@then("The last 'statut de suivi' should be 'Suivi non réalisé' or 'Suivi réalisé' or 'Suivi non demandé'")
def step_verify_suivi_statut(context):
    context.risk_patient_page.verify_last_suivi_statut()

@then('"Suivi non réalisé" becomes red')
def step_impl(context):
    context.risk_patient_page.suivi_non_realise_red()

@then('The button in "Réalisation du suivi" gets activated')
def step_impl(context):
    context.risk_patient_page.button_activated()

@when("I click on the button 'réalisation du suivi'")
def step_impl(context):
    context.risk_patient_page.click_follow_up_button()

@then("A popup appears with a checkbox, a comment area, and two buttons 'Annuler' and 'Enregistrer'")
def step_impl(context):
    context.risk_patient_page.popup_appears()

@when("I check the checkbox 'Suivi réalisé'")
def step_impl(context):
    context.risk_patient_page.check_follow_up_checkbox()

@when("I fill the comment area with 'Commentaire de suivi'")
def step_impl(context):
    context.risk_patient_page.fill_comment()

@when("I click on the button 'Enregistrer'")
def step_impl(context):
    context.risk_patient_page.click_save_button()

@then("If 'Suivi réalisé' is checked then the status becomes 'Suivi réalisé' in green")
def step_impl(context):
    context.risk_patient_page.check_suivi_status()

@then("The page reloads with the active filters retained")
def step_impl(context):
    context.risk_patient_page.page_reload_with_filters()

@when('I click on "Non" in "Suivi nécessaire"')
def step_impl(context):
    context.risk_patient_page.click_non_in_suivi_necesaire()

@when('I click on "Oui" in Suivi necessary')
def step_impl(context):
    context.risk_patient_page.click_non_in_suivi_necessary()

@then("The status becomes 'Suivi non nécessaire' and appears in black")
def step_impl(context):
    context.risk_patient_page.status_is_no_follow_up()

@then("The 'réalisation du suivi' button remains inactive")
def step_impl(context):
    context.risk_patient_page.follow_up_button_is_inactive()

@then('The tooltip text should match the follow-up status from the table')
def step_impl(context):
    context.risk_patient_page.verify_tooltip_matches_status(context.page)

