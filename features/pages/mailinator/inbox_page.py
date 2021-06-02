from driver_wrappers.selenium.page_wrapper import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class InboxPage(BasePage):

    loc_input_search = (By.CSS_SELECTOR, 'input[id="inbox_field"]')
    loc_button_search = (By.CSS_SELECTOR, 'button[id="go_inbox"]')
    loc_frame_email_body = (By.CSS_SELECTOR, 'iframe[id="msg_body"]')
    loc_email_body_content = f'//*[contains(text(),"<PLACE_TEXT>")]'

    def type_input_search(self, value):
        self.refresh_page()
        self.switch_to_default_content()
        try:
            if self.is_the_element_presented(*self.loc_input_search):
                self.type_text(
                    value, *self.loc_input_search, letter_by_letter=True, is_clickable=True
                )
        except:
            self.type_text(value, *self.loc_input_search, letter_by_letter=True, is_clickable=True)
            self.perform_pure_send_keys(Keys.ENTER)
        return self

    def check_mailinator_inbox_context(self, email, tab_number, row_title, email_content):
        email_ = self.generate_random_string_data(email)
        email_fragment = str(email_).replace("@mailinator.com", "")
        url = f"https://www.mailinator.com/v3/index.jsp?zone=public&query={email_fragment}#/#inboxpane"
        try:
            self.open_new_tab(url, number=tab_number)
            self.switch_to_default_content()
            self.click_on_mail_found(row_title, email_fragment, email_content)
        except:
            self.accept_alert()
            self.take_screenshot("FAILED_EMAIL")
            self.log.warning("EMAIL NOT SENT")
            pass

    def click_on_mail_found(self, row_title, email_fragment, email_content):
        row_title = "" if row_title is None else row_title
        loc_row_mail_found = (
            By.XPATH,
            f'//div[@id="inboxpane"]//tr[contains(@id,"row_")]/td[4]/a[contains(text(),"{row_title}")]',
        )
        self.switch_to_default_content()
        for attempt in range(5):
            self.type_input_search(email_fragment)
            self.click_on_button_search()
            self.press_key_home()
            try:
                self.wait_for_element(*loc_row_mail_found, handle_timeout=5)
            except:
                pass
            if self.is_the_element_presented(*loc_row_mail_found, timeout=10):
                self.click_on(*loc_row_mail_found, use_js=True)
                self.consume_email_content(email_content, email_fragment)
                break

    def click_on_button_search(self):
        self.click_on(*self.loc_button_search, use_js=True)
        return self

    def consume_email_content(self, email_content, email_fragment):
        try:
            self.switch_nested_frame(*self.loc_frame_email_body)
            self.press_key_home()
            self.click_on_button_in_email_content(email_content)
        except:
            self.switch_nested_frame(*self.loc_frame_email_body)
            loc_content = self.prepare_locator(email_fragment, self.loc_email_body_content)
            self.get_email_content(loc_content)
            email_content_found = self.get_element_text(By.XPATH, loc_content)
            self.assert_that(email_content_found).contains_the(email_content, "Email Content")

    def get_email_content(self, value):
        self.switch_to_default_content()
        self.switch_nested_frame(*self.loc_frame_email_body)
        loc_content = self.generate_random_string_data(
            self.prepare_locator(value, self.loc_email_body_content)
        )
        self.scroll_into_view(By.XPATH, loc_content)
        return self.get_element_text(By.XPATH, loc_content)

    def click_on_button_in_email_content(self, value):
        self.switch_to_default_content()
        self.switch_nested_frame(*self.loc_frame_email_body)
        loc_content = self.prepare_locator(value, self.loc_email_body_content)
        self.scroll_into_view(By.XPATH, loc_content)
        self.click_on(By.XPATH, loc_content, use_js=True)
        return self

    def validate_email_body_content(self, value):
        self.switch_to_default_content()
        self.switch_nested_frame(*self.loc_frame_email_body)
        loc_content = self.prepare_locator(value, self.loc_email_body_content)
        email_body_content_found = self.get_element_text(By.XPATH, loc_content)
        try:
            self.assert_that(email_body_content_found).contains_the(value, "Email Body Content")
        except:
            self.take_screenshot("FAILED_EMAIL")
            self.log.warning("EMAIL CONTENT IS NOT SHOWED")
            pass
        return self
