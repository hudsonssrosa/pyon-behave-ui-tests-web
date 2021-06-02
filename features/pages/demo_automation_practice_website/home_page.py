from driver_wrappers.selenium.page_wrapper import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    loc_text_search = (By.ID, "search_query_top")
    loc_button_search = (By.CSS_SELECTOR, '#searchbox button[name="submit_search"]')
    loc_label_product_name = (
        '#center_column ul li h5[itemprop="name"] a.product-name[title="<PLACE_TEXT>"]'
    )
    loc_label_product_unit_price = (
        By.CSS_SELECTOR,
        '#center_column ul li div span.product-price[itemprop="price"]',
    )
    loc_hover_product = (By.CSS_SELECTOR, "#center_column > ul > li")
    loc_button_add_to_cart = (
        By.CSS_SELECTOR,
        "#center_column > ul > li > div > div.right-block > div.button-container > a.button.ajax_add_to_cart_button.btn.btn-default > span",
    )

    def set_product_name_label(self, product_name):
        return By.CSS_SELECTOR, self.prepare_locator(product_name, self.loc_label_product_name)

    def type_input_search(self, value_expected):
        self.type_text(value_expected, *self.loc_text_search)
        return self

    def click_on_search_button(self):
        self.click_on(*self.loc_button_search, is_visible=True)
        return self

    def wait_until_product_name_is_visible(self, product_name=""):
        loc_product_name = self.set_product_name_label(product_name)
        self.wait_for_element(*loc_product_name, is_visible=True)
        return self

    def move_over_to_product(self):
        self.perform_move_to_element_releasing(*self.loc_hover_product)
        return self

    def click_on_add_to_cart_button(self):
        self.click_on(*self.loc_button_add_to_cart, timeout=10)
        return self

    def validate_label_product_name(self, value_expected):
        loc_product_name = self.set_product_name_label(value_expected)
        self.scroll_into_view(*loc_product_name)
        product_name_found = self.get_element_text(*loc_product_name)
        self.assert_that(product_name_found).is_equals_to(value_expected)
        return self

    def validate_label_product_unit_price(self, value_expected):
        product_unit_price_found = self.get_element_text(*self.loc_label_product_unit_price)
        self.assert_that(product_unit_price_found).is_equals_to(value_expected)
        return self
