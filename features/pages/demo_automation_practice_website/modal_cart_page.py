from driver_wrappers.selenium.page_wrapper import BasePage
from selenium.webdriver.common.by import By


class ModalCartPage(BasePage):
    loc_modal_cart_adding = (By.CSS_SELECTOR, "#layer_cart div.layer_cart_cart")
    loc_modal_proceed_to_checkout = (By.CSS_SELECTOR, "#layer_cart div div.layer_cart_cart")
    loc_button_proceed_to_checkout = (
        By.CSS_SELECTOR,
        '#layer_cart div a[title="Proceed to checkout"]',
    )

    def wait_until_modal_cart_is_visible(self):
        self.switch_to_default_content()
        self.wait_for_element(*self.loc_modal_cart_adding)
        self.perform_move_to_element(*self.loc_modal_cart_adding)
        return self

    def wait_until_proceed_to_checkout_is_visible(self):
        self.switch_to_default_content()
        self.wait_for_element(
            *self.loc_modal_proceed_to_checkout, is_presented=True, handle_timeout=10
        )
        return self

    def click_on_proceed_to_checkout(self):
        self.switch_to_default_content()
        try:
            self.click_on(*self.loc_button_proceed_to_checkout)
        except:
            self.click_on(*self.loc_button_proceed_to_checkout, use_js=True)
            self.refresh_page()
        return self
