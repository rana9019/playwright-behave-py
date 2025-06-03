from behave import given, when, then


@given("I am on the Alertes page")
def step_impl(context):
    context.alerts_page.alertes_page_url()

@then('the "{label}" dropdown should contain: {options}')
def step_impl(context, label, options):
    expected_options = [opt.strip() for opt in options.split(',')]
    context.alerts_page.verify_dropdown(label, expected_options)
    print(f"Dropdown for '{label}' contains all expected options.")

@then('I should see filtered results in the data table')
def step_impl(context):
    context.alerts_page.verify_filtered_results()

@then('I should see the following filters: {filters}')
def step_impl(context, filters):
    context.alerts_page.verify_filters(filters)

@then('The user selects a date "{date}" in the field "{value}"')
def step_impl(context, date, value):
    context.alerts_page.enter_date(date, value)

@when("I click on the 'Filtrer' button")
def step_impl(context):
    context.alerts_page.click_filtrer_button()

@then('the notifications should be filtered by "{filter}" with value "{value}"')
def step_impl(context, filter, value):
    context.alerts_page.verify_notifications_filtered(filter, value)

@then('the "{value}" button should be visible')
def step_impl(context, value):
    context.alerts_page.verify_button_visibility(value)

@when('I click on the suggested cause "{cause_text}"')
def step_click_suggested_cause(context, cause_text):
    context.alerts_page.click_suggested_cause(cause_text)

@then('the cause "{cause_text}" should appear in the "Causes réelles" section')
def step_verify_cause_in_real_section(context, cause_text):
    assert context.alerts_page.is_cause_in_real_section(cause_text), f"'{cause_text}' not found in Causes réelles"

@when("I click the 'Valider' button")
def step_impl(context):
    context.alerts_page.click_valid_button()

@when('I click the "Annuler" button')
def step_impl(context):
    context.alerts_page.when_click_annuler()

@then('I should see the message "Aucune modification n a été apportée"')
def step_impl(context):
    context.alerts_page.then_check_message()

@when('I write a comment in the textarea')
def step_impl(context):
    context.alerts_page.write_comment("Ceci est un commentaire de test pour validation.")

@then('I should see the success message "Donnée mise à jour avec succès"')
def step_impl(context):
    context.alerts_page.verify_update_message("Donnée mise à jour avec succès")

@when("I click on the first radio button in the table")
def step_impl(context):
    context.page.wait_for_selector("table tbody input[type='radio']", timeout=10000)

    first_radio = context.page.locator("table tbody input[type='radio']").first
    first_radio.click()

    context.clicked_radio_value = first_radio.get_attribute("value")
    print(f"Clicked radio with value: {context.clicked_radio_value}")


@when('I click again on the cause "{cause_text}" in the "Causes réelles" section')
def step_click_real_cause(context, cause_text):
    context.alerts_page.click_real_cause(cause_text)

@then('the cause "{cause_text}" should appear back in the "Causes suggérées" section')
def step_verify_cause_back_in_suggested(context, cause_text):
    assert context.alerts_page.is_cause_in_suggested_section(cause_text), f"'{cause_text}' not found in Causes suggérées"

@when('I select "{value}" in the "{dropdown}" dropdown')
def step_impl(context, value, dropdown):
    context.alerts_page.select_option_in_dropdown(value, dropdown)