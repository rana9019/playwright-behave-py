from playwright.sync_api import Page

from playwright.sync_api import expect

from dotenv import load_dotenv

from urllib.parse import urljoin

import json

import unicodedata

import fnmatch

import time

import re

import os

load_dotenv(dotenv_path=os.path.join("config", ".env"))

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def go_to_login_page(self):
        self.page.goto("http://10.0.5.14:8080/SSO-war/")

    def verify_current_url(self, expected_url):
        self.page.wait_for_timeout(2000)
        current_url = self.page.url

        if "*" in expected_url:
            if not fnmatch.fnmatch(current_url, expected_url):
                raise AssertionError(
                    f" URL mismatch: expected pattern '{expected_url}', got '{current_url}'"
                )
        else:
            if current_url != expected_url:
                raise AssertionError(
                    f" URL mismatch: expected '{expected_url}', got '{current_url}'"
                )

        print(f" Current URL matches expected pattern: {expected_url}")

    def enter_username(self):
        self.page.fill('//input[@placeholder="Login"]', os.getenv("WEB_USERNAME"))

    def enter_password(self):
        self.page.fill('//input[@placeholder="Mot de passe"]', os.getenv("WEB_PASSWORD"))

    def click_on_login_button(self):
        self.page.wait_for_selector('//button[@type="submit"]', state="visible", timeout=7000)
        self.page.click('//button[@type="submit"]')

    def enter_wrong_login(self, login):
        self.page.fill('//input[@placeholder="Login"]', login)

    def enter_wrong_password(self, password):
        self.page.fill('//input[@placeholder="Mot de passe"]', password)

    def click_dositrace_button(self):
        self.page.wait_for_timeout(9000)
        print("Debug: Vérification de la présence de #Dositrace")

        if not self.page.is_visible("#Dositrace"):
            raise AssertionError("Dositrace button is not visible on the page!")

        self.page.click("#Dositrace")

    def verify_error_message(self, expected_message):
        error_locator = self.page.locator("div.ui-pnotify-text")
        error_locator.wait_for(state="visible", timeout=10000)
        actual_message = error_locator.text_content()
        assert expected_message in actual_message, f" Expected '{expected_message}', got '{actual_message}'"
        print(f" Error message verified: '{actual_message}'")

    def navigate_to_password_reset_page(self):
        self.page.goto("http://10.0.5.14:8080/SSO-war/ViewMdpLost")

    def enter_login(self, login):
        self.page.fill('input[name="username"]', login)

    def enter_email(self, email):
        self.page.fill('input[name="email"]', email)

    def click_submit_button(self):
        self.page.click('button[type="submit"]')

    def verify_login_email_and_submit_button(self):
        assert self.page.locator('input[name="username"]').is_visible()
        assert self.page.locator('input[name="email"]').is_visible()
        assert self.page.locator('button[type="submit"]').is_visible()
        print("Les champs login, email et le bouton valider sont visibles.")

    def is_login_field_visible(self):
        login_input = self.page.locator('input[name="username"]')
        expect(login_input).to_be_visible()

    def is_password_field_visible(self):
        password_input = self.page.locator('input[name="password"]')
        expect(password_input).to_be_visible()

    def is_login_button_visible(self):
        login_button = self.page.locator('button[type="submit"]')
        expect(login_button).to_be_visible()

    def is_forgot_password_link_visible(self):
        forgot_link = self.page.locator('a[href="ViewMdpLost"]')
        expect(forgot_link).to_be_visible()

    def click_header_username(self):
        username_selector = ".dropdown-toggle.username"
        self.page.wait_for_selector(username_selector, timeout=5000)
        self.page.click(username_selector)

    def verify_profile_and_logout_links(self):
        self.page.wait_for_timeout(1000)

        profile_text = self.page.locator('ul.dropdown-menu.userinfo .username small').text_content().strip()
        assert "Connecté en tant que :" in profile_text, f" Error: Profile text is incorrect: {profile_text}"

        logout_text = self.page.locator('#logoutButton').text_content().strip()
        assert "Déconnexion" in logout_text, f" Error: Logout link text is incorrect: {logout_text}"

        print(" Profile and Logout links are visible correctly")

    def check_logout_success_message(self):
        success_popup = self.page.locator("div.ui-pnotify-text")
        expect(success_popup).to_be_visible()
        expect(success_popup).to_have_text("Déconnexion réussie")
        print("Déconnexion réussie confirmée par le message de succès.")

    def click_logout(self):
        self.page.locator("a.dropdown-toggle.username").click()
        self.page.wait_for_timeout(500)

        logout_link = self.page.locator("a[href*='DoDeconnexion']")
        expect(logout_link).to_be_visible()
        logout_link.click()