from behave import given, when, then


@given("I am on the Examens page")
def step_impl(context):
    context.exams_page.examens_page_url()

@when('The user clicks on "{value}"')
def step_impl(context, value):
    context.exams_page.click_date_field(value)

@then('The calendar "{value}" appears')
def step_impl(context, value):
    context.exams_page.calendar_is_displayed(value)

@when('The user manually enters a date in the field "{value}"')
def step_impl(context, value):
    context.exams_page.enter_date_manually(value)

@when("The user clicks on the calendar's Close button")
def step_impl(context):
    context.exams_page.close_calendar()

@then("The user clicks on the Close button of the calendar")
def step_impl(context):
    context.exams_page.verify_calendar_closed()

@then("All six shortcuts should be functional")
def step_impl(context):
    shortcuts = [
        context.login_page.shortcut_3_days,
        context.login_page.shortcut_5_days,
        context.login_page.shortcut_7_days,
        context.login_page.shortcut_week,
        context.login_page.shortcut_month,
        context.login_page.shortcut_year,
    ]

    for shortcut in shortcuts:
        assert context.exams_page.verify_shortcut_functionality(shortcut), f"Shortcut {shortcut} is not functional!"

@when('The user clicks on the button "{period}"')
def step_impl(context, period):
    context.exams_page.select_quick_date(period)

@then('The selected dates match the period "{period}"')
def step_impl(context, period):
    context.exams_page.verify_selected_date(period)