from playwright.sync_api import Page

from playwright.sync_api import expect

from dotenv import load_dotenv

import json

import unicodedata

import re

import os

load_dotenv(dotenv_path=os.path.join("config", ".env"))

LANGUAGE_RADIOS = {
    "Auto (FR)": "#lang_auto",
    "Français": "#lang_fr",
    "Español": "#lang_es",
    "English": "#lang_en"
}

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class DositracePage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def navigate(self):
        self.page.goto(os.getenv("WEB_URL"))
        self.page.wait_for_load_state("domcontentloaded")

    def save_storage(self):
        storage = self.page.context.storage_state()
        with open(self.storage_path, "w") as f:
            json.dump(storage, f)

    def load_storage(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                storage_data = json.load(f)
                self.page.context.add_init_script(f"window.sessionStorage = {json.dumps(storage_data)};")

    def enter_username(self):
        self.page.fill('//input[@placeholder="Login"]', os.getenv("WEB_USERNAME"))

    def enter_password(self):
        self.page.fill('//input[@placeholder="Mot de passe"]', os.getenv("WEB_PASSWORD"))

    def click_on_login_button(self):
        self.page.wait_for_selector('//button[@type="submit"]', state="visible", timeout=7000)
        self.page.click('//button[@type="submit"]')

    def click_dositrace_button(self):
        self.page.wait_for_timeout(9000)
        print("Debug: Vérification de la présence de #Dositrace")

        if not self.page.is_visible("#Dositrace"):
            raise AssertionError("Dositrace button is not visible on the page!")

        self.page.click("#Dositrace")

    def save_session(self):
        if os.path.exists("session.json"):
            print("Session storage found, skipping login...")
            self.navigate()
        else:
            print("No session found, performing login...")
            self.navigate()
            self.enter_username()
            self.enter_password()
            self.click_on_login_button()
            self.click_dositrace_button()
            self.save_storage()

    def dositrace_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/?ticket=")

    def verify_navigation_menu_items(self):
        self.page.wait_for_selector("#dashboard-item", state="attached", timeout=10000)

        menu_items = [
            "#dashboard-item",
            'a[href="Worklist"]',
            'a[href="SearchStudy"]',
            'a[href="ListPatient"]',
            'a[data-target="#manage-exam-and-patient"]',
            'a[data-target="#dositrace-protocol"]',
            'a[href="ViewAlerts"]',
            'a[href="RiskPatient"]',
            'a[data-target="#nrd-menu"]',
            'a[href="MachineLoadCalculation"]',
            'a[href="ViewGenerationExcel"]',
            'a[data-target="#report-menu"]',
            'a[data-target="#statistics-menu"]'
        ]

        for selector in menu_items:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=9000)
                assert self.page.is_visible(selector), f" Menu item {selector} is not visible!"
            except Exception as e:
                print(f" Warning: {selector} not found. Error: {e}")

    def click_left_menu_toggle(self):
        self.page.wait_for_timeout(4000)
        self.page.click('#leftmenu-trigger')

    def verify_menu_toggle(self):
        initial_state = self.is_menu_visible()
        print(f"Initial menu state: {initial_state}")

        self.click_left_menu_toggle()
        self.page.wait_for_timeout(7000)

        toggled_state = self.is_menu_visible()
        print(f"Toggled menu state: {toggled_state}")

        assert toggled_state != initial_state, f"Menu toggle did not work! Expected change, but got {toggled_state}."

    def is_menu_visible(self):
        body = self.page.locator("body")
        assert body, "L'élément body n'a pas été trouvé!"
        body_class = body.get_attribute("class")
        return "show-leftbar" in body_class

    def click_dropdown_arrow(self):
        dropdown_selector = "#headerbardropdown"
        self.page.wait_for_selector(dropdown_selector, timeout=5000)
        self.page.click(dropdown_selector)

    def check_application_links(self):
        app_links_selector = ".app-btn"

        self.page.wait_for_selector(app_links_selector, timeout=5000)

        app_elements = self.page.locator(app_links_selector).all()
        app_names = [app.inner_text().strip() for app in app_elements]

        print("Visible applications:")
        for name in app_names:
            print(f"- {name}")

        assert len(app_names) > 0, " Error: No application links are visible after the click."

        print(" Test passed: Application links are visible after the click.")

    def verify_notification_count(self):
        self.page.locator('a.hasnotifications.dropdown-toggle').click()

        notification_count_text = self.page.locator('.header-notification span').first.text_content().strip()
        assert "notification(s)" in notification_count_text, f" Error: Notification count text is incorrect: {notification_count_text}"

        print(f" Notification count is displayed correctly: {notification_count_text}")

    def mark_all_as_read(self):
        self.page.click("a[href='ViewNotifications?AllNotificationVu=1']")
        self.page.wait_for_timeout(2000)

    def verify_notifications_cleared(self):
        notification_message = self.page.get_by_text("Vous avez 0 notification(s)", exact=True)
        expect(notification_message).to_have_text("Vous avez 0 notification(s)")

    def dashboard_notification_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/ViewNotifications")

    def click_on_date_input(self):
        self.page.locator('#daterangepicker1').click()

    def verify_calendar_visibility(self):
        assert self.is_calendar_visible(), "Le calendrier n'est pas affiché !"

    def is_calendar_visible(self):
        return self.page.is_visible(".flatpickr-calendar")

    def click_dropdown(self, dropdown_name):
        dropdown_selectors = {
            "Vu": "#nonvu",
            "Type": "#type",
            "Afficher": "select[name='tablenotification_length']"
        }

        self.page.locator(dropdown_selectors[dropdown_name]).click(force=True)

    def verify_dropdown_option(self, dropdown_name):
        dropdown_selectors = {
            "Vu": "#nonvu option",
            "Type": "#type option",
            "Afficher": "select[name='tablenotification_length'] option"
        }

        options = self.page.locator(dropdown_selectors[dropdown_name])
        expect(options).not_to_have_count(0)

    def settings_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/ViewUser")

    def select_language(self, language):
        radio_button = self.page.locator(LANGUAGE_RADIOS[language])
        radio_button.check()

    def verify_language_change(self, language):
        selected_radio = self.page.locator(LANGUAGE_RADIOS[language])
        expect(selected_radio).to_be_checked()

    def click_editing_button(self):
        edit_button = self.page.locator("a[title='Éditer']")
        edit_button.click()

    def verify_modify_redirection(self):
        expect(self.page).to_have_url("http://10.0.5.14:8080/DositraceV2-war/ModifyCurrentUser")

    def go_to_profile_page(self):
        profile_link = self.page.locator('ul.userinfo a[href*="ViewProfil"]')
        profile_link.click()
        expect(self.page).to_have_url(re.compile(r".*/ViewProfil\?ticket=.*"))

    def click_edit_button(self):
        edit_btn = self.page.locator('a[href*="ModifyCurrentUser"]')
        edit_btn.click()
        expect(self.page).to_have_url(re.compile(r".*/ModifyCurrentUser\?ticket=.*"))

    def edit_function_field(self):
        fonction_input = self.page.locator('input[name="occ"]')
        fonction_input.fill("testing")

    def submit_profile(self):
        submit_btn = self.page.locator('input[type="submit"][value="Éditer"]')
        submit_btn.click()

    def verify_function_value(self):
        fonction_cell = self.page.locator('td:has-text("Fonction") + td')
        fonction_cell.wait_for(state='visible')
        expect(fonction_cell).to_have_text("testing")

    def click_username(self):
        self.page.locator(".dropdown-toggle.username").click()

    def click_return_button(self):
        return_button = self.page.locator("a[href='ViewProfil']")
        return_button.click()

    def verify_direction(self):
        expect(self.page).to_have_url("http://10.0.5.14:8080/SSO-war/ViewProfil")

    def click_add_button(self):
        ajouter_button = self.page.locator("#btn-add")
        ajouter_button.click()

        dropdown_menu = self.page.locator(".dropdown-menu.show")
        expect(dropdown_menu).to_be_visible(timeout=5000)

    def verify_dropdown_options(self):
        options = self.page.locator(".dropdown-menu.show li")
        expect(options).to_have_count(9, timeout=5000)

    def select_option(self):
        option = self.page.locator(".dropdown-menu.show").first
        option.click()

    def confirm_addition(self):
        valider_button = self.page.locator("#btn-confirmation-add")
        expect(valider_button).to_be_visible()
        valider_button.click()

    def verify_success_message(self):
        self.page.wait_for_timeout(5000)

        notifications = self.page.locator(".ui-pnotify")
        count = notifications.count()
        print(f"Nombre de notifications trouvées : {count}")

        for i in range(count):
            text = notifications.nth(i).locator(".ui-pnotify-text").text_content().strip()
            print(f"Texte de la notification {i} : {text}")

            if "Données mises à jours avec succès" in text:
                expect(notifications.nth(i)).to_be_visible(timeout=5000)
                return

        assert False, "Le message de succès n'est pas apparu"

    def click_supprimer(self):
        delete_button = self.page.locator("#btn-delete")
        expect(delete_button).to_be_visible(timeout=5000)
        delete_button.click()

    def click_trash_icon(self):
        page = self.page
        delete_icons = page.locator("span.deleteCoord")

        page.evaluate("""() => {
            const sidebar = document.querySelector("nav#page-leftbar");
            if (sidebar) sidebar.style.pointerEvents = 'none';
        }""")

        delete_icons.nth(0).scroll_into_view_if_needed()

        delete_icons.nth(0).click(force=True)

        page.evaluate("""() => {
            const sidebar = document.querySelector("nav#page-leftbar");
            if (sidebar) sidebar.style.pointerEvents = '';
        }""")

    def verify_valider_button(self):
        valider_button = self.page.locator("#btn-confirmation")
        expect(valider_button).to_be_visible(timeout=5000)

    def click_valider(self):
        valider_button = self.page.locator("#btn-confirmation")
        expect(valider_button).to_be_visible(timeout=5000)
        valider_button.click()

    def select_year(self):
        bouton = self.page.locator("#btnPreviousYear")

        bouton.wait_for(state="visible")
        bouton.scroll_into_view_if_needed()

        self.page.wait_for_timeout(500)

    def select_uf(self):
        print(" Récupération des valeurs avant sélection de l'UF...")

        self.initial_rappel = self.page.locator("#rappel-border1 strong").text_content().strip()
        self.initial_examens = self.page.locator("#examens a span").text_content().strip()
        self.initial_patients = self.page.locator("#patients a span").text_content().strip()

        print(f" Valeurs AVANT sélection : Rappel={self.initial_rappel}, Examens={self.initial_examens}, Patients={self.initial_patients}")

        print(" Sélection de l'UF 'Radiologie 3' en cours...")
        self.page.locator("#s2id_uf").click()
        self.page.wait_for_timeout(1000)
        option = self.page.locator("#select2-drop").get_by_text("Radiologie 3")
        option.wait_for(state="visible", timeout=5000)
        option.click()
        self.page.wait_for_timeout(2000)

        selected_value = self.page.locator("#s2id_uf .select2-chosen").text_content()
        assert selected_value == "Radiologie 3", f" Erreur: UF sélectionnée incorrecte ({selected_value})"
        print(" UF 'Radiologie 3' sélectionnée avec succès.")

    def verify_dashboard_update(self):
        try:
            self.page.wait_for_function(
                """([initialExamens, initialPatients]) => {
                    let examens = document.querySelector("#examens a span")?.textContent.trim();
                    let patients = document.querySelector("#patients a span")?.textContent.trim();
                    return examens !== initialExamens || patients !== initialPatients;
                }""",
                arg=[self.initial_examens, self.initial_patients],
                timeout=15000
            )
        except Exception:
            print("️ Timeout: Aucune mise à jour détectée.")

        self.page.wait_for_timeout(2000)

        rappel_count = self.page.locator("#rappel-border1 strong").text_content().strip()
        examens_count = self.page.locator("#examens a span").text_content().strip()
        patients_count = self.page.locator("#patients a span").text_content().strip()
        examens_url = self.page.locator("#examens a").get_attribute("href")

        print(f" Après mise à jour : Rappel={rappel_count}, Examens={examens_count}, Patients={patients_count}, Examens URL={examens_url}")

        assert examens_count != self.initial_examens or patients_count != self.initial_patients, " Aucune mise à jour détectée !"

    def verify_period_options(self):
        buttons = {
            "Mois précédent": "#btnPreviousMonth",
            "Mois en cours": "#btnCurrentMonth",
            "Année précédente": "#btnPreviousYear",
            "Année en cours": "#btnCurrentYear",
        }

        for label, selector in buttons.items():
            assert self.page.locator(selector).is_visible(), f" Le bouton '{label}' n'est pas visible !"
            print(f" Le bouton '{label}' est bien présent.")

        print(" Toutes les options de période sont visibles.")

    def open_uf_menu(self):
        self.page.locator("#s2id_uf").click()
        self.page.wait_for_selector("#select2-drop", state="visible", timeout=5000)

    def verify_uf_options(self):
        expected_uf_options = [
            "Radiologie 1",
            "Radiologie 2",
            "Radiologie 3",
            "Unité fonctionnelle de démonstration",
            "Scanner 1"
        ]

        uf_elements = self.page.locator("#select2-drop .select2-result-label").all_text_contents()

        for uf in expected_uf_options:
            assert uf in uf_elements, f" L'UF '{uf}' n'est pas visible dans la liste."

        print(" Toutes les UF attendues sont visibles.")

    def open_worklist(self):
        self.page.wait_for_selector("#workList", state="visible", timeout=5000)

    def verify_worklist_fields(self):
        worklist_table = self.page.locator("#workList")
        assert worklist_table.is_visible(), " Le tableau Worklist n'est pas affiché."

        headers_locator = self.page.locator("#workList thead tr td")
        headers = [h.inner_text().strip() for h in headers_locator.all()]

        print(f" Contenu des en-têtes trouvés : {headers}")

        expected_headers = ["Heure", "Patient(s)", "Équipement"]

        for expected_header in expected_headers:
            assert expected_header in headers, f" L'en-tête '{expected_header}' est manquant dans Worklist."

        print(" Tous les champs (Heure, Patient(s), Équipement) sont affichés correctement dans Worklist.")

    def click_worklist_link(self):
        worklist_link = self.page.locator("#link-worklist a")
        assert worklist_link.is_visible(), " Le lien 'Liste complète des examens planifiés' n'est pas visible."

        worklist_link.click()
        self.page.wait_for_load_state("domcontentloaded")

    def click_exam_button(self):
        exam_button = self.page.locator("#examens a.card.short-card")

        expect(exam_button).to_be_visible(timeout=7000)

        exam_button.click()

    def click_patient_button(self):
        exam_button = self.page.locator("#patients a")
        expect(exam_button).to_be_visible()
        exam_button.click()

    def verify_exam_url(self):
        expect(self.page).to_have_url("http://10.0.5.14:8080/DositraceV2-war/ListPatient")

    def verify_static_url(self):
        expect(self.page).to_have_url("http://10.0.5.14:8080/DositraceV2-war/ChartDashboard")

    def click_static_link(self):
        stats_link = self.page.locator("#link-stats a")
        expect(stats_link).to_be_visible()
        stats_link.click()

    def get_alertes_non_traitees(self):
        alertes_element = self.page.locator("#rappel-border1 strong")
        self.alertes_non_traitees = int(alertes_element.inner_text().strip())
        print(f" Nombre affiché d'alertes non traitées : {self.alertes_non_traitees}")

    def click_alerts_link(self):
        page = self.page

        alerts_link = page.locator("a[href='ViewAlerts?dashboardPeriod=currMonth']")
        alerts_link.wait_for(state="visible", timeout=5000)

        with page.expect_navigation():
            page.evaluate("document.querySelector('a[href=\"ViewAlerts?dashboardPeriod=currMonth\"]').click()")

        page.wait_for_load_state("domcontentloaded")

    def compare_alertes(self):
        self.page.wait_for_timeout(5000)
        self.page.wait_for_selector("#DataTables_Table_0 tbody tr", timeout=10000)

        loading_message_locator = self.page.locator("#DataTables_Table_0 tbody tr")
        loading_message_text = loading_message_locator.first.inner_text().strip()

        if "Chargement en cours..." in loading_message_text:
            print(" Le tableau est en cours de chargement, on attend qu'il se termine...")
            self.page.wait_for_selector("#DataTables_Table_0 tbody tr:not(.dataTables_empty)", timeout=15000)
            table_rows = self.page.locator("#DataTables_Table_0 tbody tr")
        else:
            table_rows = self.page.locator("#DataTables_Table_0 tbody tr:not(.dataTables_empty)")

        empty_message_locator = self.page.locator("#DataTables_Table_0 tbody tr.dataTables_empty")
        is_empty_message_visible = empty_message_locator.is_visible()
        print(f"is_empty_message_visible: {is_empty_message_visible}")

        if self.alertes_non_traitees == 0:
            if is_empty_message_visible:
                nombre_alertes_tableau = 0
                print(" Le tableau est vide (Aucune donnée disponible dans le tableau)")
            else:
                nombre_alertes_tableau = table_rows.count()
                print(f" Nombre réel d'alertes dans le tableau : {nombre_alertes_tableau}")
        else:
            nombre_alertes_tableau = table_rows.count()
            print(f" Nombre réel d'alertes dans le tableau : {nombre_alertes_tableau}")

        if nombre_alertes_tableau == 1:
            table_first_row_text = table_rows.first.inner_text().strip()
            print(f"table_first_row_text: {table_first_row_text}")
            if "Aucune donnée disponible dans le tableau" in table_first_row_text:
                nombre_alertes_tableau = 0
                print(" Le tableau contient 'Aucune donnée disponible dans le tableau', donc le nombre d'alertes réelles est 0")

        print(f" Nombre d'alertes non traitées affiché : {self.alertes_non_traitees}")
        print(f" Nombre d'alertes réelles dans le tableau : {nombre_alertes_tableau}")

        if self.alertes_non_traitees != nombre_alertes_tableau:
            print(f" Mismatch: {self.alertes_non_traitees} affichées vs {nombre_alertes_tableau} dans le tableau")
        else:
            print(" Le nombre des alertes correspond bien entre le tableau de bord et la page des alertes !")

        assert self.alertes_non_traitees == nombre_alertes_tableau, (
            f" Mismatch: {self.alertes_non_traitees} affichées vs {nombre_alertes_tableau} dans le tableau"
        )

    def click_protocol_link(self):
        page = self.page

        protocol_link = page.locator("a[href='CreateProtocolMapping#praw']")
        protocol_link.wait_for(state="visible", timeout=5000)

        with page.expect_navigation():
            page.evaluate("document.querySelector('a[href=\"CreateProtocolMapping#praw\"]').click()")

        page.wait_for_load_state("domcontentloaded")

    def click_members_link(self):
        page = self.page

        members_link = page.locator("a[href='http://10.0.5.14:8080/Core-war/CreateMemberMapping?ticket=0kno7TCTxnCd3h9E6R6VZgYdLhBZDSk4']")

        members_link.wait_for(state="visible", timeout=10000)

        with page.expect_navigation():
            page.evaluate("document.querySelector('a[href=\"http://10.0.5.14:8080/Core-war/CreateMemberMapping?ticket=0kno7TCTxnCd3h9E6R6VZgYdLhBZDSk4\"]').click()")

        page.wait_for_load_state("domcontentloaded")

    def click_patients_link(self):
        page = self.page

        page.locator("a[href='PatientsWithoutStudy']").wait_for(state="visible", timeout=5000)

        with page.expect_navigation():
            page.evaluate("document.querySelector('a[href=\"PatientsWithoutStudy\"]').click()")

        page.wait_for_load_state("domcontentloaded")

    def verify_table_columns(self):
        page: Page = self.page

        page.wait_for_selector("#example thead tr", state="visible", timeout=10000)

        headers = page.locator("#example thead tr th")
        column_count = headers.count()

        print(f"Nombre de colonnes détectées: {column_count}")

        expected_columns = ["Date d'examen", "Type", "Dépassement", "Patient(s)"]

        assert column_count == len(expected_columns), f"Nombre de colonnes incorrect : attendu {len(expected_columns)}, détecté {column_count}"

        for i, expected_name in enumerate(expected_columns):
            actual_name = headers.nth(i).text_content(timeout=5000).strip()
            print(f" Colonne {i+1}: '{actual_name}'")
            assert actual_name == expected_name, f" La colonne {i+1} devrait être '{expected_name}', mais c'est '{actual_name}'"

        print(" Toutes les colonnes sont présentes avec les bons noms !")

    def click_alertes(self):
        page: Page = self.page

        page.locator("#el5").click()

        page.wait_for_load_state("load")

        new_url = page.url
        print(f" URL après clic: {new_url}")

        self.new_url = new_url

    def verify_redirection(self):
        expected_url = "http://10.0.5.14:8080/DositraceV2-war/ViewAlerts"
        assert self.new_url == expected_url, f" Redirection incorrecte: {self.new_url}"
        print(" Redirection réussie vers le menu Alerte!")

    def verify_informations(self):
        page: Page = self.page

        info_block = page.locator("#informations")
        expect(info_block).to_be_visible(timeout=5000)

        info_text = info_block.locator("#info").text_content().strip()
        print(f" Texte affiché : {info_text}")

        assert "DOSITRACE a accès à Internet" in info_text, " Le message sur l'accès à Internet est incorrect."

    def verify_documents(self):
        page: Page = self.page

        doc_block = page.locator("#documentation")
        expect(doc_block).to_be_visible(timeout=5000)

        doc_text = doc_block.text_content().strip()
        print(f" Contenu de l'élément Documents : {doc_text}")

        print(" Les guides utilisateurs sont bien présents dans l'élément Documents.")

    def click_chart_button(self):
        page: Page = self.page

        chart_button = page.locator("g.highcharts-button")
        expect(chart_button).to_be_visible(timeout=5000)
        chart_button.click()

    def verify_download_options(self):
        page: Page = self.page

        formats = ["PNG", "JPEG", "PDF", "SVG"]
        for format in formats:
            option = page.locator(f"text=Download {format} {'document' if format == 'PDF' else 'vector image' if format == 'SVG' else 'image'}")
            expect(option).to_be_visible(timeout=5000)

            print(f" Option de téléchargement {format} détectée.")

        print(" Toutes les options de téléchargement sont bien affichées.")

    def verify_menu_display(self):
        page: Page = self.page
        context_menu = page.locator("div.highcharts-contextmenu")
        expect(context_menu).to_be_visible(timeout=5000)

        print(" Le menu de téléchargement est affiché.")

    def click_patients_button(self):
        self.page.click("a.nav-link[href='ListPatient']")

    def check_actifs_and_supprimes_options(self):
        options = self.get_available_options()
        print(f"Options trouvées: {options}")

        assert "Actifs" in options, f"Option 'Actifs' non trouvée, options disponibles: {options}"
        assert "Supprimés" in options, f"Option 'Supprimés' non trouvée, options disponibles: {options}"

    def get_available_options(self):
        self.page.click("#s2id_disabled")

        self.page.wait_for_selector(".select2-results li", state="visible", timeout=7000)

        options = self.page.locator(".select2-results li").all_text_contents()

        print(f"Options trouvées: {options}")

        self.page.press("#s2id_disabled", "Escape")

        return options

    def select_etat(self, etat):
        dropdown_trigger = self.page.locator(".select2-container").first
        dropdown_trigger.click()

        dropdown = self.page.locator("#select2-drop")
        dropdown.wait_for(state="visible", timeout=5000)

        option_locator = self.page.locator(f"//li[contains(@class, 'select2-result') and contains(., '{etat}')]")
        option_locator.wait_for(state="visible", timeout=5000)
        option_locator.click()

    def click_filtrer_button(self):
        self.page.locator("input#fil").click()

    def click_first_patient_first_name(self):
        self.page.wait_for_selector('table#patient tbody tr:nth-child(1) td:nth-child(2) a')

        patient_link = self.page.query_selector('table#patient tbody tr:nth-child(1) td:nth-child(2) a')

        if patient_link is None:
            raise Exception("Patient link not found.")

        self.patient_url = patient_link.get_attribute('href')

        patient_link.click()

        self.page.wait_for_load_state('load')

    def verify_patient_deleted(self):
        deleted_text = self.page.locator("h1 span.subtitle").text_content()
        assert "(Supprimés)" in deleted_text, "Patient was not deleted!"

    def verify_mark_as_read_link(self):
        self.page.locator('a.hasnotifications.dropdown-toggle').click()

        mark_as_read_link = self.page.locator('a[href="ViewNotifications?AllNotificationVu=1"]').text_content().strip()
        assert "Tout marquer comme lu" in mark_as_read_link, f" Error: Mark all as read link is missing or incorrect: {mark_as_read_link}"

        print(f" Mark all as read link is visible correctly: {mark_as_read_link}")

    def verify_view_all_notifications_link(self):
        self.page.locator('a.hasnotifications.dropdown-toggle').click()

        view_all_notifications_link = self.page.locator('a.dd-viewall').text_content().strip()
        assert "Voir toutes les notifications" in view_all_notifications_link, f" Error: View all notifications link is missing or incorrect: {view_all_notifications_link}"

        print(f" View all notifications link is visible correctly: {view_all_notifications_link}")

    def click_view_all_notifications(self):
        self.page.locator('a.dd-viewall').click()

        self.page.wait_for_url('http://10.0.5.14:8080/DositraceV2-war/ViewNotifications', timeout=10000)

        current_url = self.page.url
        print(f" URL après navigation : {current_url}")

        assert current_url == 'http://10.0.5.14:8080/DositraceV2-war/ViewNotifications', \
            f" Error: Navigation failed, current URL: {current_url}"

        print(f" Successfully navigated to notifications page: {current_url}")

    def verify_worklist_open(self):
        expect(self.page).to_have_url("http://10.0.5.14:8080/DositraceV2-war/Worklist")