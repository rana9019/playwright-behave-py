from behave import given, when, then

from playwright.sync_api import expect

@given("I am on the Calcul par protocole page")
def step_impl(context):
    context.nrd_nri_page.calcul_protocole_page_url()

@given("I am on the View IRSN page")
def step_impl(context):
    context.nrd_nri_page.view_irsn_page_url()

@when("The user clicks on 'Modalité'")
def step_click_modalite(context):
    context.page.click("#s2id_idModality .select2-choice")

@then('A dropdown list with the available modalities should be displayed')
def step_verify_modalite_dropdown(context):
    dropdown_option = context.page.locator(".select2-results li", has_text="Radiologie conventionnelle CR CR")
    expect(dropdown_option).to_be_visible()

@when('I select the modality "{value}"')
def step_impl(context, value):
    context.page.click("#s2id_idModality .select2-choice")
    context.page.locator(".select2-results li", has_text=value).click()

    context.page.wait_for_timeout(1000)

@then('The Equipment field is updated with "{value}"')
def step_impl(context, value):
    # Open dropdown
    context.page.click('#s2id_idEquipement .select2-choice')

    # Wait for the results list
    context.page.wait_for_selector('.select2-results li.select2-result-selectable', timeout=10000)

    # Click on the exact item by interpolating the value variable
    context.page.click(f"li.select2-result-selectable:has-text('{value}')")

    # Check that the field updated correctly
    chosen_text = context.page.inner_text('#s2id_idEquipement .select2-chosen')
    print(f"[DEBUG] Text after selection: '{chosen_text}'")
    assert value in chosen_text, f"Expected text not found. Current text: '{chosen_text}'"


@then('The Protocol field is updated with "{name}" with value "{number}"')
def step_impl(context, name, number):
    context.page.wait_for_selector('#s2id_idProtocol', state="visible", timeout=5000)
    context.page.wait_for_load_state("networkidle", timeout=10000)
    context.page.click('#s2id_idProtocol .select2-choice')
    context.page.wait_for_timeout(1000)

    # Interpolate number inside JS code
    js_code = f"""
    () => {{
        const selectElement = document.querySelector('#idProtocol');
        selectElement.value = '{number}';
        const event = new Event('change', {{ bubbles: true }});
        selectElement.dispatchEvent(event);
        $('#idProtocol').select2('val', '{number}');
    }}
    """

    context.page.evaluate(js_code)
    context.page.wait_for_timeout(1000)

    selected_value = context.page.evaluate("""
    () => {
        const selectElement = document.querySelector('#idProtocol');
        return {
            value: selectElement.value,
            displayText: $('#s2id_idProtocol .select2-chosen').text()
        };
    }
    """)

    assert selected_value.get('value') == number, f"Failed to select '{name}' option"
    assert name in selected_value.get('displayText', ''), f"Display text doesn't show '{name}'"


@when('The user clicks on the period "{period}"')
def step_when_user_clicks_on_period(context, period):
    period_button = context.page.locator(f"a.btn.btn-secondary.period:has-text('{period}')")
    period_button.click()

@then('The period "{period}" is selected')
def step_then_period_is_selected(context, period):
    active_button = context.page.locator(f"a.btn.btn-secondary.period.active:has-text('{period}')")
    assert active_button.is_visible(), f"The period '{period}' was not selected correctly"

@then('A section with the filters "UF", "Equipement", "Pédiatrique", and "Nombre d\'examens" is displayed')
def step_then_filter_section_is_displayed(context):
    assert context.page.locator("#filter_1").is_visible(), "UF filter is not visible"
    assert context.page.locator("#filter_2").is_visible(), "Equipement filter is not visible"
    assert context.page.locator("#filter_19").is_visible(), "Pédiatrique filter is not visible"
    assert context.page.locator("#filter_20").is_visible(), "Nombre d'examens filter is not visible"

@when('The user selects "AXIOM Iconos R200 C90-C" from the dropdown list')
def step_when_user_selects_from_dropdown(context):
    context.nrd_nri_page.select_equipement_filter()

@then('The results in the table should display only entries with "AXIOM Iconos R200 C90-C"')
def step_then_results_should_display_filtered_entries(context):
    table_rows = context.page.locator("tbody tr")

    filtered_rows = context.page.locator("tbody tr td:nth-child(3)", has_text="AXIOM Iconos R200 C90-C")
    assert filtered_rows.count() > 0, "No rows were filtered with 'AXIOM Iconos R200 C90-C'"

    for row in table_rows.element_handles():
        equipment_cell = row.query_selector("td:nth-child(3)")
        equipment_text = equipment_cell.inner_text() if equipment_cell else ""
        assert "AXIOM Iconos R200 C90-C" in equipment_text, f"Unexpected equipment: {equipment_text}"

@when("I fill up some filters")
def step_impl(context):
    context.nrd_nri_page.fill_up_filters()

@then("all the filters fields should be reset")
def step_impl(context):
    context.nrd_nri_page.verify_filters_are_reset()

@given('I am viewing the list nrd protocol raw')
def step_impl(context):
    context.nrd_nri_page.go_to_list_nrd_protocol_raw()

@given("I am on the List protocol national page")
def step_impl(context):
    context.nrd_nri_page.list_protocol_national_page_url()

@then('The tabs "Adulte" and "Pédiatrie" must be visible')
def step_check_tabs_visible(context):
    adulte_tab = context.page.locator('a.nav-link[href="#adulte"]')
    pediatrie_tab = context.page.locator('a.nav-link[href="#pedia"]')

    expect(adulte_tab).to_be_visible()
    expect(pediatrie_tab).to_be_visible()

@when("Clicking on the Start Date field displays a calendar allowing date selection")
def step_impl(context):
    context.page.click('#datepicker')

    context.page.wait_for_selector('.flatpickr-calendar', state='visible', timeout=5000)

    is_visible = context.page.is_visible('.flatpickr-calendar')
    print(f"[DEBUG] Calendar visible: {is_visible}")
    assert is_visible, "The calendar did not appear after clicking on the date field."

@when('the user fills the Number of exams field with {value:d}')
def step_fill_nbexamen(context, value):
    nbexamen_selector = '#nbexamen'
    context.page.fill(nbexamen_selector, str(value))

@then('the Number of exams field value should be {expected_value:d}')
def step_check_nbexamen_value(context, expected_value):
    nbexamen_selector = '#nbexamen'
    current_value = context.page.eval_on_selector(nbexamen_selector, 'el => el.value')
    print(f"[DEBUG] Current Number of exams field value: {current_value}")
    assert int(current_value) == expected_value, f"Expected {expected_value}, but got {current_value}"

@when('the user increments the Number of exams field by 1 using the arrow')
def step_increment_nbexamen(context):
    context.page.eval_on_selector('#nbexamen', 'el => el.stepUp()')

@when('the user decrements the Number of exams field by 1 using the arrow')
def step_decrement_nbexamen(context):
    context.page.eval_on_selector('#nbexamen', 'el => el.stepDown()')

@when('the user checks the "IMC renseigné et compris entre 17 et 35" checkbox')
def step_check_checkbox_weight(context):
    checkbox_selector = '#inlinecheckbox1'
    checkbox = context.page.locator(checkbox_selector)
    checkbox.check(force=True)

@then('the checkbox "IMC renseigné et compris entre 17 et 35" should be checked')
def step_verify_checkbox_checked(context):
    checkbox_selector = '#inlinecheckbox1'
    is_checked = context.page.is_checked(checkbox_selector)
    print(f"[DEBUG] Checkbox checked: {is_checked}")
    assert is_checked, "The checkbox should be checked, but it is not."

@when('the user clicks the "Valider" button')
def step_impl(context):
    validate_button = context.page.locator('#btn-validate')
    validate_button.wait_for(state="visible", timeout=5000)
    validate_button.click()

@then('a success message "Donnée mise à jour avec succès" should appear')
def step_impl(context):
    success_message = context.page.locator("text=Donnée mise à jour avec succès")
    success_message.wait_for(state="visible", timeout=5000)
    assert success_message.is_visible(), "Success message not visible"

@then('I should see the text "{value}"')
def step_impl(context, value):
    heading = context.page.locator("h1", has_text=value)
    expect(heading).to_be_visible()

@when('I click the "Retour" button')
def step_impl(context):
    context.page.click('a.btn.btn-secondary:has-text("Retour")')

