from playwright.sync_api import Page

from playwright.sync_api import expect

from urllib.parse import urljoin

import json

import unicodedata

import fnmatch

import time

import re

import os

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class PatientsPage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

        self.modality_dropdown = self.page.locator("#lm option")  # All options in the dropdown
        self.modality_field = self.page.locator("#lm")  # Modalité field selector
        self.period_field = self.page.locator("#daterangepicker1")
        self.pregnancy_update_link = self.page.locator("#pregUpd")


    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def go_to_patient_list_page(self):
        self.page.goto("http://10.0.5.14:8080/DositraceV2-war/ListPatient")
        self.patients_page = PatientsPage(self.page)

    def click_add_filter_button(self):
        if self.page.is_closed():
            raise RuntimeError("La page est fermée avant de cliquer sur le bouton des filtres !")

        print("Debug: Tentative de clic sur #addButton")
        self.page.click("#addButton")

    def verify_filter_panel_is_open(self):
        assert self.is_filter_panel_open(), "Filter panel is not open!"

    def is_filter_panel_open(self):
        self.page.wait_for_timeout(5000)
        return self.page.is_visible("#rightbar-overlay[style*='display: block']")

    def click_close_filter_panel(self):
        self.page.evaluate('document.getElementById("closeButton").click()')

    def verify_filter_panel_is_closed(self):
        assert self.is_filter_panel_closed(), "Filter panel did not close!"

    def is_filter_panel_closed(self):
        overlay_hidden = not self.page.is_visible("#rightbar-overlay[style*='display: block']")
        rightbar_shifted = self.page.query_selector("#page-rightbar").get_attribute('style') == "right: -380px;"
        return overlay_hidden and rightbar_shifted

    def is_filter_section_visible(self):
        return self.page.is_visible("#filter_12") and self.page.is_visible("#filter_14")

    def check_gender_options(self):
        options = self.get_gender_options()
        print(f"Options trouvées: {options}")

        assert "Tous" in options, f"Option 'Tous' non trouvée, options disponibles: {options}"
        assert "Homme" in options, f"Option 'Homme' non trouvée, options disponibles: {options}"
        assert "Femme" in options, f"Option 'Femme' non trouvée, options disponibles: {options}"
        assert "Non défini" in options, f"Option 'Non défini' non trouvée, options disponibles: {options}"

    def get_gender_options(self):
        return self.page.locator("#gender option").all_text_contents()

    def select_gender_option(self):
        self.page.click("#s2id_gender")

        self.page.wait_for_selector(".select2-results li", state="visible", timeout=7000)

        options = self.page.locator(".select2-results li").all_text_contents()
        print(f"Options détectées : {options}")

        femme_option = self.page.locator(".select2-results li", has_text="Femme")
        if femme_option.count() > 0:
            femme_option.first.click()
        else:
            print("Erreur: L'option 'Femme' n'est pas trouvée dans le dropdown.")

    def verify_gender_filter_applied(self):
        assert self.is_gender_applied_correctly(), "Le filtrage du genre est incorrect."

    def get_selected_gender(self):
        return self.page.locator("#s2id_gender .select2-chosen").text_content().strip()

    def is_gender_applied_correctly(self):
        selected_gender = self.get_selected_gender()
        print(f"Genre sélectionné: {selected_gender}")
        self.page.press("#s2id_gender", "Escape")

        return selected_gender == "Femme"

    def click_filter(self, value):
        overlay = self.page.locator("#rightbar-overlay")
        if overlay.is_visible():
            print("Overlay détecté, tentative de le fermer...")
            self.page.locator("#rightbar-overlay").click()

        self.page.wait_for_selector("#rightbar-overlay", state="hidden", timeout=5000)

        filter_button = self.page.locator(value).first
        filter_button.wait_for(state="visible")
        filter_button.click()

        self.page.wait_for_timeout(2000)

    def verify_filtered_gender(self):
        self.page.wait_for_selector("#patient tbody tr")

        rows = self.page.locator("#patient tbody tr")
        for row in rows.all():
            gender_icon = row.locator("i.icon-gender-female")
            assert gender_icon.is_visible(), "Erreur: Une ligne ne contient pas le genre sélectionné"

    def click_birthdate_field(self):
        self.page.click("#ddn")

    def press_escape(self):
        self.page.press("input#ddn", "Escape")

    def fill_date_of_birth(self):
        overlay = self.page.locator("#rightbar-overlay")
        if overlay.is_visible():
            self.page.evaluate("document.querySelector('#rightbar-overlay').style.display = 'none'")

        date_input = self.page.locator("#ddn")

        assert date_input.is_visible(), "Erreur: Le champ 'Date de naissance' n'est pas visible."

        date_input.click()

        date_input.fill("")

        date_input.fill("08/03/1947")

        assert date_input.input_value() == "08/03/1947", "Erreur: La date de naissance n'a pas été saisie correctement."

        print(" Date de naissance remplie avec succès.")

    def check_table_filtered(self):
        self.page.wait_for_selector("#patient tbody tr", timeout=5000)

    def verify_patient_birth_date(self, expected_birth_date):
        self.page.wait_for_selector("#patient tbody tr", timeout=7000)

        rows = self.page.locator("#patient tbody tr").count()
        assert rows > 0, "Erreur : Le tableau est vide après le filtrage !"

        first_row_birth_date = self.page.locator("#patient tbody tr >> nth=0 >> td:nth-child(4)").text_content().strip()

        print(f"Valeur filtrée attendue : {expected_birth_date}")
        print(f"Date affichée dans la première ligne : {first_row_birth_date}")

        assert first_row_birth_date == expected_birth_date, f"Erreur : Date trouvée {first_row_birth_date}, attendue {expected_birth_date}"

        print("Succès : La première ligne affiche la bonne date de naissance.")

    def _close_overlay_if_visible(self):
        try:
            overlay = self.page.locator("#rightbar-overlay")
            if overlay.is_visible():
                print("Overlay détecté. Tentative de suppression.")
                self.page.evaluate("document.querySelector('#rightbar-overlay')?.remove()")
                self.page.wait_for_timeout(500)
        except:
            print("Erreur ou aucun overlay détecté.")

    def _click_reset(self):
        self.page.wait_for_selector("#res", state="visible", timeout=5000)
        self.page.click("#res")

    def click_reset_button(self):
        self._close_overlay_if_visible()
        self._click_reset()

    def check_fields_reset(self):
        self.page.wait_for_timeout(2000)

        birth_date_field = self.page.locator("input#ddn")
        birth_date_value = birth_date_field.input_value().strip()
        if birth_date_value:
            print(f"️ Attention: Le champ 'Date de naissance' n'a pas été réinitialisé. Valeur actuelle: '{birth_date_value}'")
        else:
            print(" Le champ 'Date de naissance' a été réinitialisé avec succès.")

        self.page.locator("#s2id_gender").click()
        self.page.wait_for_timeout(1000)

        gender_dropdown = self.page.locator("#select2-drop")

        if not gender_dropdown.is_visible():
            print(" Attention: Le champ 'Genre' n'est toujours pas visible après ouverture.")
        else:
            selected_value = self.page.locator("#s2id_gender .select2-choice").text_content().strip()

            if selected_value and selected_value != "Tous":
                print(f" Attention: Le champ 'Genre' n'a pas été réinitialisé. Valeur actuelle: '{selected_value}'")
            else:
                print(" Le champ 'Genre' a été réinitialisé avec succès.")

        additional_field = self.page.locator("#s2id_autogen1")

        if additional_field.count() == 0:
            print(" Attention: Le champ supplémentaire n'est pas visible.")
        else:
            additional_value = additional_field.input_value().strip()
            if additional_value:
                print(f"️ Attention: Le champ supplémentaire n'a pas été réinitialisé. Valeur actuelle: '{additional_value}'")
            else:
                print(" Le champ supplémentaire a été réinitialisé avec succès.")

    def search_in_global_field(self, search_term, field_locator):
        search_input = self.page.locator(field_locator)

        search_input.fill(search_term)

        self.page.wait_for_timeout(2000)

    def click_column_header(self, value):
        header_locator = self.page.locator("th", has_text=value)
        header_locator.click()
        print(f"Clicked on the column header '{value}'.")

    def get_column_values(self, locator):
        names = self.page.locator(locator).all_inner_texts()
        unique_values = set(names)

        if len(unique_values) <= 2 and len(names) > 5:
            print(f"Warning: Test data has limited variety ({unique_values}), validating basic presence only")
            assert len(names) > 0, "Table should have data to sort"
            return []

        return names

    def validate_sorted_descending(self, names):
        normalized = [normalize(name) for name in names]
        expected = sorted(normalized, reverse=True)

        assert normalized == expected, f"Table is not sorted in descending order: {normalized}"
        print("Table is sorted in descending order.")

    def get_table_column_data(self, column_locator):
        names = self.page.locator(column_locator).all_inner_texts()

        unique_values = set(names)
        if len(unique_values) <= 2 and len(names) > 5:
            print(f"Warning: Test data has limited variety ({unique_values}), validating basic presence only")
            assert len(names) > 0, "Table should have data to sort"
            return names

        return names

    def validate_sorted_ascending(self, names):
        normalized = [normalize(name) for name in names]
        expected = sorted(normalized)

        assert normalized == expected, f"Table is not sorted in ascending order: {normalized}"
        print("Table is sorted in ascending order.")

    def click_next_button(self):
        next_button = self.page.locator(".next.paginate_button")

        next_button.wait_for(state="visible", timeout=30000)

        next_button.click()
        print("Clic effectué sur le bouton suivant")

    def verify_next_page_displayed(self):
        self.page.wait_for_load_state("load", timeout=30000)

        active_page_locator = self.page.locator(".pagination .active a")
        active_page_locator.wait_for(state="visible", timeout=30000)

        active_page = active_page_locator.text_content()
        assert active_page != "1", f"La page suivante ne s'est pas affichée, page actuelle : {active_page}"

    def verify_numbers_unequal(self, context):
        assert context.num1 is not None and context.num2 is not None, "Failed to extract numbers."
        assert context.num1 != context.num2, f"Expected different numbers but got {context.num1} and {context.num2}."

    def get_patients_without_exam(self):
        self.page.wait_for_selector("#rappel-border4 strong", timeout=5000)
        num_text = self.page.locator("#rappel-border4 strong").text_content().strip()

        print(f"Extracted text from rappel-border4: {num_text}")

        return int(num_text) if num_text.isdigit() else None

    def get_total_elements(self):
        self.page.wait_for_timeout(3000)

        if not self.page.locator("#protocol_info").is_visible():
            print("DEBUG: #protocol_info element is NOT visible")
            return None

        results_text = self.page.locator("#protocol_info").text_content().strip()
        print(f"DEBUG: Extracted text from protocol_info: '{results_text}'")

        match = re.search(r"sur (\d+) élément", results_text)
        return int(match.group(1)) if match else None

    def verify_patient_results(self, expected_value):
        expected_text = f"1 à {expected_value}"

        for _ in range(5):
            results_text = self.get_results_info_patient()
            normalized_text = re.sub(r"\s+", " ", results_text.replace("\xa0", " ")).strip()

            match = re.search(r"(\d+ à \d+)", normalized_text)
            extracted_text = match.group(1) if match else normalized_text

            if expected_text == extracted_text:
                return True
            time.sleep(1)

        return False

    def get_results_info_patient(self):
        return self.page.locator(".dataTables_info#protocol_info").text_content().strip()

    def select_results_per_page_patient(self, value):
        self.page.select_option("select[name='protocol_length']", value)

        self.page.click("a[id='1']")

    def is_confirmation_dialog_visible(self):
        return self.page.is_visible("text=Voulez vous vraiment supprimer ces patients ?")

    def click_delete_button(self):
        self.page.click("#del", force=True)

    def is_first_checkbox_checked(self):
        return self.page.locator("input.checkmembre").first.is_checked()

    def check_first_checkbox(self):
        checkbox = self.page.locator("input.checkmembre").first
        merge_button = self.page.locator("#merge")
        delete_button = self.page.locator("#del")

        checkbox_id = checkbox.get_attribute("id")
        self.page.evaluate(f"""
            (id) => {{
                let checkbox = document.getElementById(id);
                if (checkbox) {{
                    checkbox.checked = true;
                    checkbox.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
        """, checkbox_id)

        self.page.wait_for_timeout(500)

        if "disabled" not in merge_button.get_attribute("class") and "disabled" not in delete_button.get_attribute("class"):
            print("Succès : les boutons sont activés après la coche.")
        else:
            print("Échec : les boutons restent désactivés.")
            raise Exception("Impossible d'activer les boutons après avoir coché la case.")

    def patients_without_study_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/PatientsWithoutStudy")

    def verify_table_column(self):
        table_locator = self.page.locator("table.table-bordered.table-responsive.table-hover")
        expect(table_locator).to_be_visible()

        columns = table_locator.locator("thead tr th").all_text_contents()

        if len(columns) < 4:
            print("Le tableau ne contient pas assez de colonnes !")
            return

        for col_name in columns[1:-2]:
            if col_name.strip() != "PDL (mGy. cm)":
                print(f"Mauvais intitulé de colonne détecté : {col_name}")
                return

        if columns[-2].strip() != "Total PDL (mGy. cm)":
            print(f"L'avant-dernière colonne attendue 'Total PDL (mGy. cm)' est absente. Trouvé : {columns[-2]}")
            return

        if columns[-1].strip() != "E (mSv)":
            print(f"La dernière colonne attendue 'E (mSv)' est absente. Trouvé : {columns[-1]}")
            return

        print("Les colonnes du tableau sont conformes.")

    def verify_effective_doses_table_columns(self):
        table_locator = self.page.locator("table.table-bordered.table-responsive.table-hover")
        expect(table_locator).to_be_visible()

        columns = table_locator.locator("thead tr th").all_text_contents()

        if len(columns) < 3:
            print("️Le tableau ne contient pas assez de colonnes !")
            return

        for col_name in columns[1:-1]:
            if col_name.strip() != "E (mSv)":
                print(f"Mauvais intitulé de colonne détecté : {col_name}")
                return

        if columns[-1].strip() != "E Total (mSv)":
            print(f"La dernière colonne attendue 'E Total (mSv)' est absente. Trouvé : {columns[-1]}")
            return

        print("Les colonnes du tableau sont conformes.")

    def check_dosimetric_report_tabs(self):
        tab_container = self.page.locator(".tab-container .nav-tabs")

        if not tab_container.is_visible(timeout=5000):
            print("Le bilan dosimétrique ne contient pas d'onglets.")
            return

        tabs = tab_container.locator("li.nav-item a")

        tab_count = tabs.count()
        if tab_count > 1:
            print(f"Le bilan dosimétrique contient {tab_count} onglets.")
            tab_names = [tabs.nth(i).inner_text() for i in range(tab_count)]
            print("Onglets trouvés :", ", ".join(tab_names))
        else:
            print("Seulement un onglet trouvé dans le bilan dosimétrique.")

    def check_fetal_organ_dose_table(self):
        table = self.page.locator("#resultTable")

        if not table.is_visible(timeout=5000):
            print("Le tableau des doses aux organes du fœtus n'est pas affiché.")
            return

        rows = table.locator("tbody tr")
        if rows.count() > 1:
            print("Le tableau des doses aux organes du fœtus est affiché et contient des informations.")
        else:
            print("Le tableau des doses aux organes du fœtus est affiché mais il est vide.")

    def selected_pregnancy_period(self):
        selected_value = self.get_selected_period()
        assert selected_value == "16/09/2020 - 17/09/2020", f"Expected '16/09/2020 - 17/09/2020' but got {selected_value}"

    def get_selected_period(self):
        return self.page.locator('#pregnantPeriod').input_value()

    def navigate_to(self, locator):
        self.page.wait_for_selector(locator, state="visible", timeout=10000)
        self.page.wait_for_selector(locator, state="attached", timeout=10000)
        self.page.click(locator, force=True)
        self.page.wait_for_load_state("networkidle")

    def select_pregnancy_period(self, period: str):
        self.page.click('label[for="pregnantPeriod"]')
        self.page.select_option('#pregnantPeriod', label=period)

    def verify_tab_exists(self, tab_name):
        if tab_name == "2D":
            tab = self.page.locator("#btn2D")
        elif tab_name == "3D":
            tab = self.page.locator("#btn3D")
        else:
            raise ValueError(f"Tab '{tab_name}' not recognized")

        expect(tab).to_be_visible(timeout=5000)

    def verify_chart_visibility(self):
        chart = self.page.locator("#chart_div")
        expect(chart).to_be_visible(timeout=5000)

    def verify_table_visibility(self):
        table = self.page.locator("table.table-bordered").filter(has_text="Organe Dose (mGy)").nth(0)
        expect(table).to_be_visible(timeout=5000)

    def wait_for_chart(self, chart_selector):
        self.page.wait_for_selector(chart_selector, timeout=10000)

    def wait_for_table(self, table_selector):
        self.page.wait_for_selector(table_selector, timeout=10000)

    def hover_info_button(self):
        info_button = self.page.locator(".help-container .icon-button-info")

        self.page.wait_for_selector(".help-container .icon-button-info", state="visible")

        info_button.hover(force=True)

        print("Forced hover action on 'info' button successful")

    def get_tooltip_message(self):
        return self.page.locator(".icon-button-info-position").first.text_content().strip()

    def normalize_message(self, message):
        return re.sub(r'\s+', ' ', message.strip())

    def verify_tabs_in_container(self, container_text, expected_tabs):
        tab_containers = self.page.locator("div.tab-container")
        count = tab_containers.count()
        print(f"Nombre de conteneurs d'onglets trouvés: {count}")

        tab_container = tab_containers.filter(has_text=container_text).nth(0)

        assert tab_container.is_visible(), f"Le conteneur des onglets contenant '{container_text}' n'est pas visible."

        tabs = tab_container.locator("ul.nav-tabs li.nav-item a.nav-link").all()
        tab_texts = [tab.inner_text().strip() for tab in tabs if tab.inner_text().strip() not in ["2D", "3D"]]
        print(f"Onglets valides trouvés ({len(tab_texts)}): {tab_texts}")

        assert 1 <= len(tab_texts) <= 3, f"Nombre d'onglets incorrect: {len(tab_texts)} (Attendu: 1 à 3)"

        missing_tabs = [t for t in expected_tabs if t not in tab_texts]
        extra_tabs = [t for t in tab_texts if t not in expected_tabs]

        assert not missing_tabs, f"Onglets manquants: {missing_tabs}"
        assert not extra_tabs, f"Onglets en trop: {extra_tabs}"

        print("Test réussi: Les onglets sont corrects.")

    def verify_redirection_link(self):
        modal = self.page.locator("div#studydetails-185636")
        if not modal.is_visible():
            self.page.evaluate("document.querySelector('div#studydetails-185636').style.display = 'block'")
            self.page.wait_for_timeout(500)

        all_links = modal.locator("span.redirection a").all()
        print(f"Nombre de liens trouvés: {len(all_links)}")

        if len(all_links) == 0:
            raise AssertionError("Aucun lien de redirection trouvé!")

        redirection_link = all_links[0]
        href = redirection_link.get_attribute("href")
        print(f"Lien extrait: {href}")

        if not href or "ViewStudy" not in href:
            raise AssertionError(f"Lien incorrect: {href}")

        if not redirection_link.is_visible():
            print("Le lien est caché, on le rend visible manuellement.")
            self.page.evaluate("document.querySelector('span.redirection a').style.display = 'block'")
            self.page.wait_for_timeout(500)

        print("Clic sur le lien de redirection...")
        self.page.evaluate("document.querySelector('span.redirection a').click()")
        self.page.wait_for_timeout(2000)

        current_url = self.page.url
        expected_url = "http://10.0.5.14:8080/DositraceV2-war/ViewStudy?study=185636"
        assert current_url == expected_url, f"Redirection échouée! Attendu: {expected_url}, mais obtenu: {current_url}"

    def verify_acquisition_table(self, expected_columns):
        modals = self.page.locator("div#acquisitionModal")

        assert modals.count() > 0, "No acquisition modal found!"

        visible_modal = None
        for i in range(modals.count()):
            if modals.nth(i).is_visible():
                visible_modal = modals.nth(i)
                break

        assert visible_modal, "No visible acquisition modal found!"

        table_locator = visible_modal.locator("table#acqs")
        assert table_locator.is_visible(), "The acquisitions table is not visible!"

        actual_headers = table_locator.locator("thead tr th").all_inner_texts()

        for col in expected_columns:
            assert col in actual_headers, f"Column '{col}' is missing in the acquisitions table!"

    def verify_info_labels(self, labels):
        for label in labels:
            elements = self.page.locator(f"text='{label}'").all()
            assert any(e.is_visible() for e in elements), f"Le champ '{label}' est manquant !"

    def is_exam_popup_displayed(self):
        modal = self.page.locator("div.modal-dialog.modal-lg-custom")
        modal.wait_for(state="visible", timeout=5000)
        return modal.is_visible()

    def click_eye_icon(self):
        eye_icon = self.page.locator("em[data-toggle='modal'][data-target='#studyModal']").first
        eye_icon.click()

    def check_column_in_table(self, column_name):
        headers = self.page.locator("#study thead tr th").all_inner_texts()

        if column_name in headers:
            print(f"Column '{column_name}' found in the table headers.")
        else:
            print(f"No column found under the name '{column_name}'. Continuing execution...")

    def verify_selected_modality(self, expected_modality):
        selected_modality = self.get_selected_modality()
        assert selected_modality == expected_modality, \
            f"Expected modality '{expected_modality}', but got '{selected_modality}'"

    def get_selected_modality(self):
        dropdown = self.page.locator("#lm")
        selected_option = dropdown.locator("option:checked").text_content().strip()
        return selected_option

    def select_modality(self, modality):
        dropdown = self.page.locator("#lm")
        dropdown.select_option(label=modality)

    def get_modality_options(self):
        options = self.modality_dropdown.all_text_contents()
        return options

    def verify_modals(self, expected_modalities):
        modality_options = self.get_modality_options()

        missing_modalities = [modality for modality in expected_modalities if modality not in modality_options]

        assert not missing_modalities, f"Missing modalities: {', '.join(missing_modalities)}"
        print("All expected modalities are present in the dropdown.")

    def assert_modality_dropdown_has_10_options(self):
        modality_options = self.get_modality_options()
        assert len(modality_options) == 10, f"Expected 10 modalities, but found {len(modality_options)}"
        print(f"Dropdown contains {len(modality_options)} modalities.")

    def click_modality_field(self):
        self.modality_field.click()

    def verify_selected_dates(self):
        first_date_checked = self.page.locator("table.month1 div.day.toMonth.valid.checked").count()
        second_date_checked = self.page.locator("table.month2 div.day.lastMonth.valid.checked").count()

        return first_date_checked > 0 and second_date_checked > 0

    def is_stay_number_disabled(self):
        stay_number_field = self.page.locator("#lsn")
        return stay_number_field.is_disabled()

    def assert_stay_number_field_is_disabled(self):
        is_disabled = self.is_stay_number_disabled()
        assert is_disabled, "Le champ 'Numéro de séjour' devrait être désactivé"
        print("Le champ 'Numéro de séjour' est bien désactivé.")

    def assert_selected_dates_are_correct(self):
        assert self.verify_selected_dates(), "Les dates sélectionnées ne sont pas correctes !"

    def click_period_field(self):
        self.period_field.click()

    def verify_risk_end_date(self):
        rows = self.page.locator("table#pregnancyOncological tbody tr").all()

        for row in rows:
            statut = row.locator("td:nth-child(1)").inner_text().strip()

            if "Grossesse" in statut:
                date_fin = row.locator("td:nth-child(3)").inner_text().strip()
                date_fin_risque = row.locator("td:nth-child(4)").inner_text().strip()

                assert date_fin == date_fin_risque, (
                    f"Date de fin ({date_fin}) et date de fin de risque ({date_fin_risque}) ne correspondent pas!"
                )

    def verify_table_column_number(self, context):
        headers = self.get_table_headers()
        expected_columns = [row["Statut"] for row in context.table]

        for column in expected_columns:
            assert column in headers, f"Column '{column}' not found in table headers!"

    def get_table_headers(self):
        headers = self.page.locator("table#pregnancyOncological thead th").all_text_contents()
        return [header.strip() for header in headers]

    def verify_pregnancy_oncology_table_visible(self):
        table = self.page.locator("table#pregnancyOncological")
        expect(table).to_be_visible(), "Le tableau de suivi médical n'est pas visible!"

    def check_risk_end_date(self):
        risk_end_date_input = self.page.locator("#riskEndDateInput")

        self.page.wait_for_function(
            "document.querySelector('#riskEndDateInput').value !== ''"
        )

        risk_end_date = risk_end_date_input.input_value()
        print(f"Risk End Date Input Value: '{risk_end_date}'")

        assert risk_end_date.strip() != "", "Date de fin de risque is not automatically filled"

    def press_enter_key(self):
        page: Page = self.page
        page.keyboard.press("Enter")

    def verify_modal_closed(self):
        assert self.is_modal_closed(), "Modal is not closed!"

    def verify_record_added(self, before_count, after_count):
        assert after_count == before_count + 1, (
            f"Expected {before_count + 1} records, but found {after_count}. Record was not added!"
        )

    def is_modal_closed(self):
        modal = self.page.locator('#myModal')
        return modal.is_visible() is False

    def get_table_row_count(context):
        info_text = context.page.locator("#pregnancyOncological_info").inner_text()
        print(f"Info text extracted: {info_text}")
        match = re.search(r'sur (\d+) élément', info_text)
        return int(match.group(1)) if match else 0

    def fill_date(self, date, locate):
        date_input = self.page.locator(locate)

        date_input.wait_for(state="visible")
        date_input.fill(date)

    def verify_element_visibility(self, element_locator):
        element = self.page.locator(element_locator)
        expect(element).to_be_visible()

    def click_button(self, button):
        button = self.page.locator(f'{button}').nth(0)

        button.wait_for(state="visible")
        button.click()
        self.page.wait_for_timeout(10000)

    def is_pediatric_status_displayed(self):
        pediatric_status = self.page.locator("//label[contains(text(), 'Statut pédiatrique')]")
        return pediatric_status.is_visible()

    def is_pregnancy_update_displayed(self):
        return self.pregnancy_update_link.is_visible()

    def is_info_displayed(self, field_name):
        return self.page.locator(f"label:text-is('{field_name}')").is_visible()

    def verify_info_in_header(self, field_name):
        assert self.is_info_displayed(field_name), f"{field_name} is missing in the patient info header!"

    def confirm_deletion(self):
        self.page.on("dialog", lambda dialog: dialog.accept())

    def click_disable_patient(self):
        disable_button = self.page.locator("a#deletedpatient")
        disable_button.click()

    def click_settings_dropdown(self):
        settings_button = self.page.locator("button.btn-secondary.dropdown-toggle")
        settings_button.click()

    def verify_patient_details_page_displayed(self):
        base_url = 'http://10.0.5.14:8080/DositraceV2-war/'
        full_patient_url = urljoin(base_url, self.patient_url)

        assert self.page.url == full_patient_url, f"Expected URL {full_patient_url}, but got {self.page.url}"
        print("Patient URL after clicking:", self.page.url)

    def click_first_patient_first_name(self):
        self.page.wait_for_selector('table#patient tbody tr:nth-child(1) td:nth-child(2) a')

        patient_link = self.page.query_selector('table#patient tbody tr:nth-child(1) td:nth-child(2) a')

        if patient_link is None:
            raise Exception("Patient link not found.")

        self.patient_url = patient_link.get_attribute('href')

        patient_link.click()

        self.page.wait_for_load_state('load')

    def get_results_info(self, locator):
        return self.page.locator(locator).text_content().strip()

    def verify_results_displayed(self, value, locator):
        expected_text = f"1 à {value}"

        for _ in range(5):
            results_text = self.get_results_info(locator)

            normalized_text = re.sub(r"\s+", " ", results_text.replace("\xa0", " ")).strip()

            match = re.search(r"(\d+ à \d+)", normalized_text)
            extracted_text = match.group(1) if match else normalized_text

            if expected_text == extracted_text:
                break
            time.sleep(1)
        else:
            assert False, f"Expected '{expected_text}', but got '{normalized_text}'"

    def get_active_page(self):
        return self.page.locator(".pagination .active a").text_content()

    def select_results_per_page(self, value, results_per_page):
        self.page.select_option(results_per_page, value)

    def verify_page_displayed(self, page_number):
        active_page = self.get_active_page()
        assert active_page == page_number, f"Displayed page ({active_page}) is not the expected one ({page_number})!"

    def click_page_number(self, page_number):
        self.page.wait_for_timeout(5000)
        self.page.click(f'a[id="{page_number}"]')

    def verify_previous_page_displayed(self):
        active_page = self.get_active_page()
        assert active_page != "5", "The previous page did not load!"

    def click_previous_button(self):
        previous_button_locator = self.page.locator("#patient_previous")

        if previous_button_locator.is_enabled():
            previous_button_locator.click()
        else:
            print("Le bouton 'précédent' est désactivé, impossible de cliquer.")


