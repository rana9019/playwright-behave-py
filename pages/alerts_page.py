from playwright.sync_api import Page

from playwright.sync_api import expect

from dotenv import load_dotenv

import json

import unicodedata

import re

import os

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class AlertsPage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def alertes_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/ViewAlerts")

    def verify_dropdown(self, label, expected_options):
        select_locator = self.page.locator(f'label:has-text("{label}") + div select')
        actual_options = select_locator.locator('option').all_text_contents()
        actual_options_cleaned = [opt.strip() for opt in actual_options]

        assert set(expected_options) == set(actual_options_cleaned), \
            f"Options affichées pour '{label}' : {actual_options_cleaned}, attendues : {expected_options}"

    def verify_filtered_results(self):
        info_locator = self.page.locator('div#DataTables_Table_0_info')
        info_locator.wait_for(state="visible", timeout=5000)
        result_text = info_locator.inner_text()

        assert "élément" in result_text.lower(), f"Le texte retourné était : '{result_text}'"

    def verify_filters(self, filters):
        expected_filters = [f.strip() for f in filters.split(',')]

        filter_labels = self.page.locator('div[id^="filter_"] label').all_text_contents()

        filter_labels_cleaned = [label.strip() for label in filter_labels]

        assert set(expected_filters) == set(filter_labels_cleaned), \
            f"Filtres affichés : {filter_labels_cleaned}, attendus : {expected_filters}"

    def enter_date(self, date, value):
        date_input = self.page.locator(value)
        assert date_input.is_visible(), "Le champ de saisie de date n'est pas visible"

        date_input.fill(date)
        print(" Dates saisies manuellement")

    def click_filtrer_button(self):
        self.page.locator("input#fil").click()

    def verify_notifications_filtered(self, filter, value):
        filtered_values = self.page.locator(f'tbody tr td:nth-child(7)').all_text_contents()
        filtered_values_cleaned = [val.strip() for val in filtered_values]

        assert value in filtered_values_cleaned, \
            f"Valeurs filtrées dans la colonne '{filter}': {filtered_values_cleaned}, attendues : {value}"

    def verify_button_visibility(self, button_locator):
        button = self.page.locator(button_locator)
        expect(button).to_be_visible()

    def click_suggested_cause(self, cause_text):
        cause_span = self.page.locator('div#cause-possible span.label-cause', has_text=cause_text)

        button = cause_span.locator('xpath=preceding-sibling::button')

        button.wait_for(state="visible", timeout=5000)
        button.click()

    def is_cause_in_real_section(self, cause_text):
        return self.page.locator(f'div#cause-real span.label-cause', has_text=cause_text).is_visible()

    def click_valid_button(self):
        valider_button = self.page.locator('input[type="submit"][value="Valider"]')
        valider_button.click()

    def when_click_annuler(self):
        annuler_button = self.page.locator('a.btn.btn-secondary', has_text="Annuler")
        annuler_button.click()
        self.page.wait_for_load_state("networkidle")  # Ensure page is fully loaded

    def then_check_message(self):
        message_locator = self.page.locator("text=Aucune modification n a été apportée")
        expect(message_locator).to_be_visible()

    def write_comment(self, comment_text):
        textarea = self.page.locator('textarea[name="comment"]')
        textarea.fill(comment_text)

    def verify_update_message(self, message):
        success_message = self.page.locator(f"text={message}")
        expect(success_message).to_be_visible(timeout=5000)

    def click_real_cause(self, cause_text):
        cause_span = self.page.locator('div#cause-real span.label-cause', has_text=cause_text)

        button = cause_span.locator('xpath=preceding-sibling::button')

        button.scroll_into_view_if_needed(timeout=5000)
        button.click()

    def is_cause_in_suggested_section(self, cause_text):
        return self.page.locator(f'div#cause-possible span.label-cause', has_text=cause_text).is_visible()

    def select_option_in_dropdown(self, value, dropdown):
        dropdown_locator = self.page.locator(f'label:has-text("{dropdown}") + div select')
        dropdown_locator.select_option(value)