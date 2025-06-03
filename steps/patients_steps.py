#from pages.patients_page import PatientPage

from behave import given, when, then

from pages.patients_page import PatientsPage

from playwright.sync_api import expect

import time

@given('I am viewing the patient list')
def step_impl(context):
    context.patients_page.go_to_patient_list_page()

@when("The user clicks on 'Ajouter des filtres'")
def step_impl(context):
    context.patients_page.click_add_filter_button()

@when("The user has opened the filter panel")
def step_impl(context):
    context.patients_page.verify_filter_panel_is_open()

@then("The user clicks the close button")
def step_impl(context):
    context.patients_page.click_close_filter_panel()
    time.sleep(1)

@then("The filter panel is closed")
def step_impl(context):
    context.patients_page.verify_filter_panel_is_closed()

@then("The filter section appears with 'Sexe' and 'Date de naissance'")
def step_impl(context):
    assert context.patients_page.is_filter_section_visible(), "La section des filtres n'est pas affichée !"

@then("The options 'Tous', 'Homme', 'Femme', and 'Non défini' are available")
def step_impl(context):
    context.patients_page.check_gender_options()

@then('The user selects a gender option')
def step_impl(context):
    context.patients_page.select_gender_option()

@then("The selected gender is applied correctly")
def step_impl(context):
    context.patients_page.verify_gender_filter_applied()

@then('I click on the button filter "{value}"')
def step_impl(context, value):
    context.patients_page.click_filter(value)

@then("I verify the selected gender is filtered correctly")
def step_impl(context):
    context.patients_page.verify_filtered_gender()

@then("The user clicks on the 'Date de naissance' field")
def step_impl(context):
    context.patients_page.click_birthdate_field()

@then("The calendar disappears")
def step_impl(context):
    context.patients_page.press_escape()

@then("I fill the date of birth field with '08/03/1947'")
def step_impl(context):
    context.patients_page.fill_date_of_birth()

@then('I check if the table is filtered correctly')
def step_impl(context):
    context.patients_page.check_table_filtered()

@then('I verify that the first displayed patient has "{expected_birth_date}" in the "Date de naissance" column')
def step_impl(context, expected_birth_date):
    context.patients_page.verify_patient_birth_date(expected_birth_date)

@when('I click on the "Réinitialiser" right bar')
def step_impl(context):
    context.patients_page.click_reset_button()

@then("I check if the fields are reset")
def step_impl(context):
    context.patients_page.check_fields_reset()

@when('The user clicks once on the column header "{value}"')
def step_impl(context, value):
    context.patients_page.click_column_header(value)
    time.sleep(0.5)

@then('The table must be sorted in descending order by "{value}"')
def step_impl(context, value):
    names = context.patients_page.get_column_values(value)
    context.patients_page.validate_sorted_descending(names)

@then('The table must be sorted in ascending order by "{value}"')
def step_impl(context, value):
    names = context.patients_page.get_table_column_data(value)
    context.patients_page.validate_sorted_ascending(names)

@when("The user clicks the right arrow")
def step_impl(context):
    context.patients_page.click_next_button()

@then("The next page is displayed")
def step_impl(context):
    context.patients_page.verify_next_page_displayed()

@when("The user clicks the left arrow")
def step_impl(context):
    context.patients_page.click_previous_button()

@then("The previous page is displayed")
def step_impl(context):
    context.patients_page.verify_previous_page_displayed()

@when('The user clicks on page number "{page_number}"')
def step_impl(context, page_number):
    context.patients_page.click_page_number(page_number)
    time.sleep(1)

@then('Page "{page_number}" is displayed')
def step_impl(context, page_number):
    context.patients_page.verify_page_displayed(page_number)

@when('The user selects "{value}" from the "{results_per_page}" dropdown')
def step_impl(context, value, results_per_page):
    context.patients_page.select_results_per_page(value, results_per_page)
    time.sleep(2)

@then('The displayed results should show "1 à {value}" in "{locator}"')
def step_impl(context, value, locator):
    context.patients_page.verify_results_displayed(value, locator)

@then("The patient's details page should be displayed")
def step_impl(context):
    context.patients_page.verify_patient_details_page_displayed()

@when('I click on the settings dropdown')
def step_impl(context):
    context.patients_page.click_settings_dropdown()

@when('I click on "Désactiver"')
def step_impl(context):
    context.patients_page.click_disable_patient()

@when('I confirm the deletion')
def step_impl(context):
    context.patients_page.confirm_deletion()

@then('The header should display "{field_name}"')
def step_impl(context, field_name):
    context.patients_page.verify_info_in_header(field_name)

@then("The patient info header should display pediatric status")
def step_impl(context):
    assert context.patients_page.is_pediatric_status_displayed(), "Pediatric status is missing for underage patient!"

@then("The patient info header should display a pregnancy update link")
def step_impl(context):
    assert context.patients_page.is_pregnancy_update_displayed(), "Pregnancy update link is missing!"

@when('I click on the "{button}" button')
def step_impl(context, button):
    context.patients_page.click_button(button)

@then('A "{locate}" should be visible')
def step_impl(context, locate):
    context.patients_page.verify_element_visibility(locate)

@when('I enter "{date}" in the "{field}" field')
def step_impl(context, date, field):
    context.patients_page = getattr(context, "patients_page", PatientsPage(context.page))
    context.patients_page.fill_date(date, field)

@when('I get the number of lines in the table before inserting a new record')
def step_impl(context):
    context.before_count = context.patients_page.get_table_row_count()
    print(f"Table row count before insertion: {context.before_count}")

@then('I get the number of lines in the table after inserting a new record')
def step_impl(context):
    context.after_count = context.patients_page.get_table_row_count()
    print(f"Table row count after insertion: {context.after_count}")

@then('The pregnancy record should be saved in the table')
def step_impl(context):
    context.patients_page.verify_record_added(context.before_count, context.after_count)

@then('The pregnancy update modal should be closed')
def step_impl(context):
    context.patients_page.verify_modal_closed()

@then('I click enter')
def step_impl(context):
    context.patients_page.press_enter_key()

@then('The "Date de fin de risque" field should be filled automatically')
def step_impl(context):
    context.patients_page.check_risk_end_date()

@then("The pregnancy and oncology follow-up table should be visible")
def step_impl(context):
    context.patients_page.verify_pregnancy_oncology_table_visible()

@then("The table should contain the following columns")
def step_impl(context):
    context.patients_page.verify_table_column_number(context)

@then("The risk end date should match the end date for pregnancies")
def step_impl(context):
    context.patients_page.verify_risk_end_date()

@when("I click on the period field")
def step_impl(context):
    context.patients_page.click_period_field()

@when('I enter "{date_range}" in the period field')
def step_impl(context, date_range):
    period_field = context.page.locator("#daterangepicker1")

    expect(period_field).to_be_visible()
    period_field.click()

    period_field.fill(date_range)

@then('The selected dates should be displayed correctly')
def step_impl(context):
    context.patients_page.assert_selected_dates_are_correct()

@then('The "Numéro de séjour" field should be disabled')
def step_impl(context):
    context.patients_page.assert_stay_number_field_is_disabled()

@when('I click on the "Modalité" field')
def step_impl(context):
    context.patients_page.click_modality_field()

@then('A dropdown with 10 modalities should be displayed')
def step_impl(context):
    context.patients_page.assert_modality_dropdown_has_10_options()

@then('The modalities should include "Radiologie conventionnelle CR", "Scanner", "Mammographie", "Médecine nucléaire", "Médecine nucléaire (TEP SCAN)", "Panoramique dentaire", "Ostéodensitométrie", "Radio Fluoroscopie", "Angiographie", "..."')
def step_impl(context):
    expected_modalities = [
        "...",
        "Radiologie conventionnelle CR", "Scanner", "Mammographie", "Médecine nucléaire",
        "Médecine nucléaire (TEP SCAN)", "Panoramique dentaire", "Ostéodensitométrie",
        "Radio Fluoroscopie", "Angiographie"
    ]
    context.patients_page.verify_modals(expected_modalities)
    print("All expected modalities are present in the dropdown.")

@when('I select "{modality}" from the dropdown')
def step_impl(context, modality):
    context.patients_page.select_modality(modality)

@then('The selected modality should be "{modality}"')
def step_impl(context, modality):
    context.patients_page.verify_selected_modality(modality)

@then('I check that the table contains a column labeled "{column_name}"')
def step_impl(context, column_name):
    context.patients_page.check_column_in_table(column_name)

@when('I click on the eye icon next to the exam')
def step_impl(context):
    context.patients_page.click_eye_icon()

@then('The exam details popup should be displayed')
def step_impl(context):
    assert context.patients_page.is_exam_popup_displayed(), "Exam details popup did not appear."

@then("On the left side of the pop-up, the following information is displayed")
def step_impl(context):
    labels = [
        "Date et heure",
        "Taille",
        "Poids",
        "IMC",
        "Numéro d'examen",
        "Type d'examen",
        "Examen demandé",
        "Protocole DOSITRACE correspondant",
        "Régions anatomiques liées au protocole DOSITRACE",
        "Activité",
        "Radiopharmaceutique",
        "PDL"
    ]
    context.patients_page.verify_info_labels(labels)

@then("The right side of the pop-up contains acquisition details displayed in a table with the following columns")
def step_impl(context):
    expected_columns = ["N°", "Nom", "Dose"]

    context.patients_page.verify_acquisition_table(expected_columns)

@then("Clicking on the redirection logo redirects to the 'Visualisation Examen' page")
def step_impl(context):
    context.patients_page.verify_redirection_link()

@then('Wait')
def step_impl(context):
    context.page.wait_for_timeout(20000)

@then("The block can contain up to 3 tabs")
def step_impl(context):
    context.patients_page.verify_tabs_in_container("Cumul de doses", [
        "Cumul de doses à l'organe",
        "Cumul de doses au fœtus",
        "Cumul Doses à la peau"
    ])

@then('The tooltip should display the message "{expected_message}"')
def step_impl(context, expected_message):
    actual_message = context.patients_page.get_tooltip_message()
    expected_message = context.patients_page.normalize_message(expected_message)

    assert actual_message == expected_message, f"Expected: '{expected_message}', but got: '{actual_message}'"

@when("I hover over the 'info' button in the top-left corner")
def step_impl(context):
    context.patients_page.hover_info_button()

@when('I wait for the table "{table_selector}"')
def step_impl(context, table_selector):
    context.patients_page.wait_for_table(table_selector)

@then('I wait for the chart "{chart_selector}"')
def step_impl(context, chart_selector):
    context.patients_page.wait_for_chart(chart_selector)

@then('I verify that the table is visible')
def step_impl(context):
    context.patients_page.verify_table_visibility()

@then('I verify that the chart is visible')
def step_impl(context):
    context.patients_page.verify_chart_visibility()

@then('The tab "{locator}" should be active')
def step_impl(context, locator):
    active_tab = context.page.locator(f'a[href="{locator}"].active')
    assert active_tab.count() > 0, f"Error: The tab {locator} is not active!"

@then('I verify that the "{tab_name}" tab exists')
def step_impl(context, tab_name):
    context.patients_page.verify_tab_exists(tab_name)

@when('I select a pregnancy period "{period}"')
def step_impl(context, period):
    context.patients_page.select_pregnancy_period(period)

@when('I click on the tab "{locator}"')
def step_impl(context, locator):
    context.patients_page.navigate_to(f'a[href="{locator}"]')

@then('I should see the selected pregnancy period')
def step_impl(context):
    context.patients_page.selected_pregnancy_period()

@then('I should see the fetal organ dose table')
def step_impl(context):
    context.patients_page.check_fetal_organ_dose_table()

@then('I should see multiple tabs in the dosimetric report')
def step_impl(context):
    context.patients_page.check_dosimetric_report_tabs()

@then("I should see a table displaying effective doses for each examination modality and the total dose")
def step_impl(context):
    context.patients_page.verify_effective_doses_table_columns()

@then("I should see a table displaying PDL values, total PDL, and effective dose")
def step_impl(context):
    context.patients_page.verify_table_column()

@given("I am on the 'Patients Without Study' page")
def step_impl(context):
    context.patients_page.patients_without_study_page_url()

@when('I check the first checkbox in the table')
def step_impl(context):
    context.patients_page.check_first_checkbox()

@then('the checkbox should be checked')
def step_impl(context):
    assert context.patients_page.is_first_checkbox_checked(), "La case n'est pas cochée"

@when("I click on the delete button")
def step_impl(context):
    context.patients_page.click_delete_button()

@then("a confirmation dialog should appear")
def step_impl(context):
    assert context.patients_page.is_confirmation_dialog_visible(), "Confirmation dialog not displayed"

@when('I search for "{search_term}" in the global search protocol field')
def step_impl(context, search_term):
    context.patients_page.search_term(search_term)

@when('The user selects "{value}" results per page in patient results without exams page')
def step_impl(context, value):
    context.patients_page.select_results_per_page_patient(value)
    time.sleep(2)

@then('The displayed results should show "1 à {value}" in patient results without exams page')
def step_impl(context, value):
    is_result_correct = context.patients_page.verify_patient_results(value)

    assert is_result_correct, f"Expected '1 à {value}', but the result was not as expected."

@when("I extract the total number of elements displayed")
def step_impl(context):
    context.num1 = context.patients_page.get_total_elements()

@when("I extract the number of patients without an exam")
def step_impl(context):
    context.num2 = context.patients_page.get_patients_without_exam()
    print(f"Patients without an exam: {context.num2}")

@then("the two numbers should not be equal")
def step_impl(context):
    context.patients_page.verify_numbers_unequal(context)

@when("I take the first value from the table '{value}'")
def step_impl(context, value):
    print(" Waiting for at least one table row to be visible...")

    context.page.wait_for_selector(f"{value} tr", timeout=10000)

    first_row = context.page.locator(f"{value} tr").first
    print(f" First row text: {first_row.inner_text()}")

    cells = first_row.locator("td")
    count = cells.count()
    print(f" Found {count} cells in the first row.")

    for i in range(count):
        cell_value = cells.nth(i).inner_text().strip()
        if cell_value:
            context.first_value = cell_value
            print(f" First non-empty value found in cell {i}: {context.first_value}")
            return

    raise Exception(" No non-empty cell found in the first row.")

@when("I search for it in the global search field '{value}'")
def step_impl(context, value):
    search_input = context.page.locator(value)
    search_input.fill(context.first_value)

@then("I should see the correct row displayed in the table '{value}'")
def step_impl(context, value):
    context.page.wait_for_timeout(1000)
    row = context.page.locator(value).first
    text = row.inner_text().strip()
    print(f" Row text after filtering: {text}")
    assert context.first_value in text, f"Expected '{context.first_value}' in table row: '{text}'"

@when("I search for '{text}' in the global search field '{value}'")
def step_impl(context, text, value):
    search_input = context.page.locator(value)

    print(f" Searching for: {text}")
    search_input.wait_for(state="visible", timeout=5000)
    search_input.fill("")
    search_input.type(text, delay=100)

    context.page.wait_for_timeout(1000)


