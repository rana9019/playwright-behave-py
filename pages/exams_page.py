from playwright.sync_api import Page

from playwright.sync_api import expect

import unicodedata

import time

import re

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class ExamsPage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

        self.period_field = self.page.locator("#daterangepicker1")
        self.shortcut_3_days = self.page.locator("a[shortcut='day,-3']")
        self.shortcut_5_days = self.page.locator("a[shortcut='day,-5']")
        self.shortcut_7_days = self.page.locator("a[shortcut='day,-7']")
        self.shortcut_week = self.page.locator("a[shortcut='prev,week']")
        self.shortcut_month = self.page.locator("a[shortcut='prev,month']")
        self.shortcut_year = self.page.locator("a[shortcut='prev,year']")


    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def examens_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/SearchStudy")

    def click_date_field(self, value):
        date_input = self.page.locator(value)
        date_input.click()

    def calendar_is_displayed(self, value):
        date_field = self.page.locator(value)

        assert date_field.count() > 0, "Le champ Date n'est pas trouvé"

        assert date_field.is_visible(), "Le champ Date n'est pas visible"
        assert date_field.is_enabled(), "Le champ Date n'est pas cliquable"

        date_field.click()
        self.page.wait_for_timeout(1000)

        print(" Clic sur le champ Date effectué")

    def enter_date_manually(self, value):
        date_input = self.page.locator(value)
        assert date_input.is_visible(), "Le champ de saisie de date n'est pas visible"

        date_input.fill("05/04/2023 - 10/04/2023")
        print(" Dates saisies manuellement")

    def close_calendar(self):
        close_button = self.page.locator(".apply-btn")
        expect(close_button).to_be_visible()

        close_button.click()
        print(" Clic sur le bouton 'Fermer' effectué")

    def verify_calendar_closed(self):
        calendar = self.page.locator(".date-picker-wrapper")
        self.page.wait_for_timeout(1000)
        expect(calendar).not_to_be_visible()
        print(" Le calendrier s'est bien fermé")

    def verify_shortcut_functionality(self, shortcut_element):
        old_date = self.get_selected_date()
        self.click_shortcut(shortcut_element)
        new_date = self.get_selected_date()
        return old_date != new_date

    def click_shortcut(self, shortcut_element):
        expect(shortcut_element).to_be_visible(timeout=5000)
        shortcut_element.click()
        self.page.wait_for_timeout(1000)

    def get_selected_date(self):
        return self.period_field.input_value()

    def select_quick_date(self, period):
        button_selector = self.get_date_button_selector(period)
        if button_selector is None:
            raise ValueError(f" Le bouton pour la période '{period}' n'est pas défini.")

        button = self.page.locator(button_selector)

        expect(button).to_be_visible(timeout=3000)

        self.page.evaluate("(buttonSelector) => document.querySelector(buttonSelector).setAttribute('onclick', 'return false;')", button_selector)

        button.click()

        print(f" Clic sur le bouton '{period}' effectué")

        time.sleep(1)

    def get_date_button_selector(self, period):
        date_buttons = {
            "dernier mois": "#b1",
            "3 derniers mois": "#b2",
            "6 derniers mois": "#b3",
            "12 derniers mois": "#b4",
        }
        return date_buttons.get(period)

    def verify_selected_date(self):
        date_field = self.page.locator("#daterangepicker1")

        expect(date_field).to_be_visible(timeout=5000)
        expect(date_field).to_have_value(re.compile(r"\d{1,2}/\d{1,2}/\d{4} - \d{1,2}/\d{1,2}/\d{4}"), timeout=5000)

        time.sleep(1)

        selected_date_range = date_field.input_value()
        print(f" Date sélectionnée : {selected_date_range}")

        assert "2025" in selected_date_range, " Les dates ne sont pas mises à jour correctement"
        print(" Les dates sont bien mises à jour")



