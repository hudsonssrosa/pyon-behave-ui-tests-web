from driver_wrappers.selenium.page_wrapper import BasePage
from selenium.webdriver.common.by import By


class CartSummaryPage(BasePage):
    loc_label_total_product = (By.ID, "total_product")
    loc_label_total_shipping = (By.ID, "total_shipping")
    loc_label_total_price = (By.ID, "total_price")

    def validate_label_total_product(self, value_expected):
        self.refresh_page()
        total_product_found = self.get_element_text(*self.loc_label_total_product)
        self.assert_that(total_product_found).is_equals_to(value_expected)
        return self

    def validate_label_total_shipping(self, value_expected):
        total_shipping_found = self.get_element_text(*self.loc_label_total_shipping)
        self.assert_that(total_shipping_found).is_equals_to(value_expected)
        return self

    def validate_label_total_price(self, value_expected):
        total_price_found = self.get_element_text(*self.loc_label_total_price)
        self.assert_that(total_price_found).is_equals_to(value_expected)
        return self
