from os.path import abspath

from factory.base_context import BaseContext as Bctx
from factory.handling.assertion import Assertion as Assert
from factory.handling.running_exception import RunningException as Rexc
from factory.singleton_web_driver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from factory.utils.StringsUtil import StringUtil as String
from factory.utils.DataEncryptedUtil import DataEncrypted as RandomData


ELEMENT_LOCATION = "/html/body"
driver = WebDriver.use()


class BasePage(WebDriver):
    @staticmethod
    def assert_that(comparative_value=""):
        return Assert(comparative_value)

    def is_loader_container_closed(self, locator=""):
        loc_loader = (By.CSS_SELECTOR, locator)
        self.get_page_to_load()
        is_loader_element_present = self.wait_for_element(*loc_loader, is_presented=True)
        try:
            while is_loader_element_present:
                self.wait_for_element(*loc_loader, is_visible=True)
                return False
        except:
            return True
        return self

    def is_the_element_presented(self, by_type, element_location, timeout=30):
        self.get_page_to_load()
        return self.wait_for_element(
            by_type, element_location, is_presented=True, handle_timeout=timeout
        )

    def scroll_into_view(self, by_type, element_location, go_to_bottom=False):
        self.wait_for_element(by_type, element_location, handle_timeout=5)
        element = BasePage.get_element_by(by_type, element_location)
        option = "false" if go_to_bottom else "true"
        self.execute_javascript(
            f"arguments[0].scrollIntoView({option});",
            element,
        )
        return self

    def press_key(self, by_type=None, element_location="", key_type="", number_of_times=1):
        if element_location == "" or element_location is None:
            self.perform_pure_send_keys(key_type)
        else:
            for i in range(0, number_of_times):
                self.get_element_by(by_type, element_location).send_keys(key_type)
            self.wait_for_element(by_type, element_location)
        return self

    def press_key_down(self, number_of_times=1):
        for i in range(0, number_of_times):
            self.get_element_by(By.XPATH, ELEMENT_LOCATION).send_keys(Keys.ARROW_DOWN)
        return self

    def press_key_up(self, number_of_times=1):
        for i in range(0, number_of_times):
            self.get_element_by(By.XPATH, ELEMENT_LOCATION).send_keys(Keys.ARROW_UP)
        return self

    def press_key_page_down(self, number_of_times=1):
        for i in range(0, number_of_times):
            self.perform_pure_send_keys(Keys.PAGE_DOWN)
        return self

    def press_key_page_up(self, number_of_times=1):
        for i in range(0, number_of_times):
            self.perform_pure_send_keys(Keys.PAGE_UP)
        return self

    def press_key_home(self):
        height = self.execute_javascript("return document.documentElement.scrollHeight")
        self.execute_javascript("window.scrollTo(" + str(height) + ", 0);")
        self.perform_pure_send_keys(Keys.HOME)
        return self

    def press_key_end(self):
        self.perform_pure_send_keys(Keys.END)
        self.execute_javascript("window.scrollTo(0, document.body.scrollHeight)")
        return self

    def press_key_tab(self, number_of_times=1):
        for i in range(0, number_of_times):
            self.wait_for_element(typing_secs=0.3)
            self.perform_pure_send_keys(Keys.TAB)
        return self

    def press_key_space(self):
        self.perform_pure_send_keys(Keys.SPACE)
        return self

    def press_key_enter(self):
        self.perform_pure_send_keys(Keys.ENTER)
        return self

    def accept_cookies(self, by_type, custom_xpath=""):
        self.interact_only_if_displayed(by_type, custom_xpath)
        return self

    def interact_only_if_displayed(self, by_type, element_location):
        try:
            self.switch_to_default_content()
            if self.is_the_element_presented(by_type, element_location, timeout=5) is False:
                pass
            else:
                self.perform_click_action(by_type, element_location, timeout=5)
        except:
            pass
        finally:
            return self

    def accept_alert(self):
        try:
            alert = WebDriver.use().switch_to.alert
            if alert is not None:
                alert.accept()
                print("   └> Alert accepted!")
        except:
            pass
        return self

    def cancel_alert(self):
        try:
            alert = WebDriver.use().switch_to.alert
            if alert is not None:
                alert.dismiss()
                print("   └> Alert canceled!")
        except:
            pass
        return self

    @staticmethod
    def is_on_mobile_mode():
        flag_mode = str(Bctx.flag_mode.get())
        if flag_mode == "mobile":
            return True

    @staticmethod
    def get_value_on_attr(attr_name, by_type, element_location, is_visible=False):
        if BasePage.is_not_empty_value(attr_name):
            try:
                BasePage.wait_for_element(by_type, element_location, is_visible=is_visible)
                element = BasePage.find_by(by_type, element_location)
                element_value = element.get_attribute(str(attr_name))
                return element_value
            except ValueError as ve:
                Rexc.raise_assertion_error(
                    f"The element '{element_location}' does not match the text value expected! ", ve
                )

    @staticmethod
    def get_element_text(by_type, element_location, is_visible=False):
        element_location = str(element_location)
        try:
            BasePage.wait_for_element(by_type, element_location, is_visible=is_visible)
            element = BasePage.get_element_by(by_type, element_location)
            try:
                BasePage.wait_for_element(by_type, element_location)
                text = WebDriver.execute_javascript("return arguments[0].textContent", element)
                return text
            except:
                text = str(element.text).strip()
                return text
        except ValueError as ve:
            Rexc.raise_assertion_error(
                f"The element '{element_location}' does not match the text value expected! ", ve
            )

    @staticmethod
    def paste_keys(by_type, element_location, text):
        element = BasePage.find_by(by_type, element_location)
        BasePage.execute_javascript(f"arguments[0].value='{text}';", element)

    @staticmethod
    def type_text(
        input_text,
        by_type,
        element_location,
        letter_by_letter=False,
        word_by_word=False,
        paste_string=False,
        clear_field=True,
        is_clickable=False,
    ):
        if BasePage.is_not_empty_value(input_text):
            try:
                if String.is_not_blank_or_null(input_text):
                    BasePage.wait_for_element(
                        by=by_type,
                        location=element_location,
                        is_clickable=is_clickable,
                    )
                    element = BasePage.get_element_by(by_type, element_location)
                    input_text_formatted = BasePage.generate_random_string_data(input_text)
                    if clear_field:
                        element.clear()
                        element.send_keys(Keys.HOME)
                        element.send_keys(Keys.SHIFT, Keys.END)
                        element.send_keys(Keys.DELETE)
                    if paste_string:
                        BasePage.paste_keys(by_type, element_location, input_text_formatted)
                    elif letter_by_letter:
                        forced_slow_typing = list(input_text_formatted)
                        for i in range(len(forced_slow_typing)):
                            BasePage.wait_for_element(typing_secs=0.009)
                            element.send_keys(str(forced_slow_typing[i]))
                    elif word_by_word:
                        forced_slow_typing = input_text_formatted.split()
                        for i in range(len(forced_slow_typing)):
                            input_with_replaced_space = (
                                forced_slow_typing[i] + " "
                                if i < len(forced_slow_typing) - 1
                                else forced_slow_typing[i]
                            )
                            BasePage.wait_for_element(typing_secs=0.05)
                            element.send_keys(str(input_with_replaced_space))
                    else:
                        element.send_keys(str(input_text_formatted))
            except ValueError as ve:
                Rexc.raise_assertion_error(
                    f"The element '{element_location}' is not iterable or value {input_text} not matches! ",
                    ve,
                )

    @staticmethod
    def parse_by_type_id_to_css_selector(by_type, element_location):
        return (
            (By.CSS_SELECTOR, f'[id="{element_location}"]')
            if by_type == By.ID
            else (by_type, element_location)
        )

    @staticmethod
    def click_on(by_type, element_location, use_js=False, is_visible=False, timeout=30):
        if use_js:
            BasePage.click_by_js(by_type, element_location, timeout, is_visible)
        else:
            BasePage.perform_click_action(by_type, element_location, timeout, is_visible)

    @staticmethod
    def click_by_js(by_type, element_location, timeout, is_visible=False):
        try:
            if by_type is None or by_type == "":
                BasePage.execute_javascript(f'$("{element_location}").click();')
            else:
                try:
                    BasePage.wait_for_element(
                        by_type,
                        element_location,
                        is_visible=is_visible,
                        is_clickable=True,
                        handle_timeout=timeout,
                    )
                    element = BasePage.get_element_by(by_type, element_location)
                    WebDriver.execute_javascript("arguments[0].click();", element)
                except:
                    BasePage.perform_click_action(by_type, element_location, timeout)
                BasePage.log_action(element_location, action_name="click by JS")
        except ValueError as ve:
            Rexc.raise_assertion_error(
                f"It was not possible to click using javascript on the element '{element_location}'. ",
                ve,
            )

    @staticmethod
    def click_with_coordinates_using_javascript(pos_x, pos_y):
        try:
            WebDriver.execute_javascript(
                f"driver.driver.execute_script('el=document.elementFromPoint({pos_x},{pos_y});el.click();')"
            )
        except ValueError as ve:
            Rexc.raise_assertion_error(
                f"It was not possible to click using javascript on this element.", ve
            )

    @staticmethod
    def click_on_list_of_elements(by_type, root_elements_location):
        element_list_ = BasePage.get_elements_by(by_type, root_elements_location)
        for item in range(len(element_list_)):
            element_list_[item].click()

    """
        All the common Selenium elements handled with Action Chains: Move to Element, Click, Double Click, Context Click, Drag and Drop.
    """

    @staticmethod
    def perform_click_action(by_type, element_location, timeout, is_visible=False):
        BasePage.wait_for_element(
            by=by_type,
            location=element_location,
            is_visible=is_visible,
            is_clickable=True,
            handle_timeout=timeout,
        )
        element_tuple = BasePage.parse_by_type_id_to_css_selector(by_type, element_location)
        element = BasePage.get_element_by(*element_tuple)
        if element.is_displayed():
            try:
                BasePage.perform_move_to_element(*element_tuple).click().perform()
            except:
                BasePage.click_by_js(*element_tuple, timeout, is_visible=is_visible)
        else:
            BasePage.click_by_js(*element_tuple, timeout, is_visible=is_visible)
        BasePage.log_action(element_tuple[1], action_name="click action")

    @staticmethod
    def perform_double_click_action(by_type, element_location):
        BasePage.wait_for_element(by=by_type, location=element_location, is_clickable=True)
        BasePage.perform_move_to_element(by_type, element_location).double_click().perform()

    @staticmethod
    def perform_context_click_action(by_type, element_location):
        BasePage.wait_for_element(by=by_type, location=element_location, is_clickable=True)
        BasePage.perform_move_to_element(by_type, element_location).context_click().perform()

    @staticmethod
    def perform_click_and_hold_action(by_type, element_location):
        BasePage.wait_for_element(by=by_type, location=element_location, is_clickable=True)
        BasePage.perform_move_to_element(by_type, element_location).click_and_hold().perform()

    @staticmethod
    def perform_click_action_with_offset(by_type, element_location, x, y):
        BasePage.wait_for_element(by=by_type, location=element_location, is_visible=True)
        BasePage.perform_move_to_element_with_offset(
            x, y, by_type, element_location
        ).click().perform()

    @staticmethod
    def perform_move_to_element(by_type, element_location):
        BasePage.wait_for_element(by=by_type, location=element_location)
        element = BasePage.get_element_by(by_type, element_location)
        return ActionChains(WebDriver.use()).move_to_element(element)

    @staticmethod
    def perform_move_to_element_with_offset(pos_x, pos_y, by_type, element_location):
        BasePage.wait_for_element(by=by_type, location=element_location)
        element = BasePage.get_element_by(by_type, element_location)
        return ActionChains(WebDriver.use()).move_to_element_with_offset(
            element, int(pos_x), int(pos_y)
        )

    @staticmethod
    def perform_move_to_element_releasing(by_type, element_location):
        BasePage.wait_for_element(by=by_type, location=element_location)
        element = BasePage.get_element_by(by_type, element_location)
        return ActionChains(WebDriver.use()).move_to_element(element).release(element).perform()

    @staticmethod
    def perform_pure_send_keys(input_value):
        actions = ActionChains(WebDriver.use())
        actions.send_keys(input_value)
        actions.perform()

    @staticmethod
    def perform_reset_action(by_type, element_location):
        BasePage.perform_move_to_element(by_type, element_location).reset_actions()

    @staticmethod
    def perform_drag_and_drop_action(by_type, element_location):
        BasePage.wait_for_element(by=by_type, location=element_location, is_clickable=True)
        BasePage.perform_move_to_element(by_type, element_location).drag_and_drop().perform()

    @staticmethod
    def perform_drag_and_drop_with_offset_action(by_type, element_location, x, y):
        element = BasePage.get_element_by(by_type, element_location)
        BasePage.wait_for_element(by=by_type, location=element_location, is_clickable=True)
        action_chains = ActionChains(WebDriver.use())
        return (
            action_chains.drag_and_drop_by_offset(element, x, y)
            .click_and_hold(element)
            .pause(3)
            .release(element)
            .perform()
        )

    @staticmethod
    def perform_move_by_offset_action(by_type, element_location, pos_x, pos_y):
        element = BasePage.get_element_by(by_type, element_location)
        BasePage.wait_for_element(
            by=by_type, location=element_location, is_visible=True, is_clickable=True
        )
        action_chains = ActionChains(WebDriver.use())
        action_chains.click_and_hold(element).move_by_offset(pos_x, pos_y).release(element).pause(
            1
        ).perform()
        BasePage.wait_for_element(by=by_type, location=element_location)

    """
        All advanced methods to get handle with complex components.
    """

    @staticmethod
    def choose_random_value(values_list):
        list_size = len(values_list) - 1
        random_option = int(
            RandomData.generate_random_data(
                length=3, start_threshold=0, end_threshold=list_size, step=1, only_numbers=True
            )
        )
        return values_list[random_option]

    @staticmethod
    def _choose_random_element(by_type, element_location):
        BasePage.wait_for_element(by_type, element_location)
        options_ = BasePage.list_element_strings(by_type, element_location)
        total_options = len(options_) - 1
        single_item_max = 1
        threshold = 0 if total_options < single_item_max else single_item_max
        random_value = (
            threshold
            if total_options <= single_item_max
            else RandomData.generate_random_data(
                length=4, start_threshold=1, end_threshold=total_options, only_numbers=True
            )
        )
        random_option = options_[int(random_value)]
        print(f"   └> Random option chosen: {random_option}")
        return random_option

    @staticmethod
    def find_a_limit_value_in_list(by_type, element_location, max_value=False):
        """Find Max or Min value in list of elements

        Args:
            by_type (By): Use By.XPATH, By.ID, By.CSS_SELECTOR or any other that defines the drop_locator
            element_location (str): Locator string from an element (can be an XPATH, ID, CSS_SELECTOR, etc.)
            max_value (bool, optional): Set it to True if you need only a max value into a list found. Defaults to False.

        Returns:
            [int]: Value found according parameter expected: if max or min number into the list
        """
        BasePage.wait_for_element(by_type, element_location)
        items_found = BasePage.find_elements_by(by_type, element_location)
        labels_found = [float(String.extract_decimal(item.text)[0]) for item in items_found]
        return max(labels_found) if max_value else min(labels_found)

    @staticmethod
    def list_element_strings(by_type, element_location, options_location=""):
        options_locator = (by_type, element_location + options_location)
        BasePage.wait_for_element(*options_locator)
        items_found = BasePage.find_elements_by(*options_locator)
        labels_found = [item.text for item in items_found]
        if BasePage.wait_for_element(*options_locator, is_presented=True):
            pass
        return labels_found[0].split("\n") if len(labels_found) == 1 else labels_found

    @staticmethod
    def format_prices_to_number(by_type, element_location):
        items_found = BasePage.get_elements_by(by_type, element_location)
        labels_found = []
        for item in items_found:
            price_fmt = String.convert_currency_to_number(value_to_format=item.text)
            labels_found.append(price_fmt)
        return labels_found

    @staticmethod
    def format_numbers_to_price(labels, by_type="", element_location="", symbol=""):
        items_found = (
            BasePage.get_elements_by(by_type, element_location)
            if element_location != ""
            else labels
        )
        BasePage.wait_for_element(by=by_type, location=element_location)
        for item in items_found:
            price = String.extract_number(item.text)
            price_fmt = String.convert_number_to_currency(value_to_format=price, currency=symbol)
            labels.append(price_fmt)
        return labels

    @staticmethod
    def select_dropdown_item(
        str_option,
        str_autocomplete="",
        root_by_type=By.XPATH,
        root_selector="",
        xpath_for_root_option="",
        xpath_with_an_option_set="",
        is_combobox=False,
        is_visible=False,
    ):
        """
        Select a dropdown item or find an option in an autocomplete input text filter.

        Args:
            str_option (str): The value used to be selected in the component
            str_autocomplete (str, optional): Text to be used in a search field with autocomplete function. Defaults to "".
            root_by_type (By.[TYPE], optional): A type for the "root_selector" argument. It can be a ID, XPATH or CSS_SELECTOR. Defaults to By.XPATH.
            root_selector (str, optional): A XPATH or CSS_SELECTOR to locate the root of a dropdown component. Defaults to "".
            xpath_for_root_option (str, optional): Generic selector to locate the root of elements presented in a visible dropdown list. Defaults to "".
            xpath_with_an_option_set (str, optional): Selector to a specific item presented in a visible dropdown list. Defaults to "".
            is_combobox (bool, optional): If you are considering the dropdown selection as a simple combobox. Defaults to False.
        """
        if BasePage.is_not_empty_value(str_option):
            if is_combobox:
                BasePage._combobox(str_option, root_by_type, root_selector)
            else:
                BasePage._dynamic_dropdown(
                    str_option,
                    str_autocomplete,
                    root_by_type,
                    root_selector,
                    xpath_for_root_option,
                    xpath_with_an_option_set,
                    is_component_visible=is_visible,
                )

    @staticmethod
    def _dynamic_dropdown(
        str_option,
        str_autocomplete,
        root_by_type,
        root_selector,
        xpath_for_root_option,
        xpath_with_an_option_set,
        is_component_visible,
    ):
        if BasePage.is_not_empty_value(str_option):
            BasePage.switch_to_default_content()
            if str_autocomplete != "":
                BasePage.type_text(
                    str_autocomplete,
                    root_by_type,
                    root_selector,
                    letter_by_letter=True,
                    is_clickable=True,
                )
            else:
                BasePage.perform_click_action(
                    root_by_type, root_selector, timeout=15, is_visible=is_component_visible
                )
            dropdown_item_value = (
                BasePage._choose_random_element(By.XPATH, xpath_for_root_option)
                if str_option == "" and xpath_with_an_option_set == ""
                else str_option
            )
            text_finder = BasePage.chain_dynamic_xpath_functions(
                searchable_text=dropdown_item_value
            )
            has_all_symbol = (
                "//*"
                if BasePage.wait_for_element(
                    By.XPATH,
                    f"{xpath_for_root_option}//*{text_finder}",
                    is_presented=True,
                )
                is True
                else ""
            )
            full_selector_item = (
                f"{xpath_for_root_option}{has_all_symbol}{text_finder}"
                if xpath_for_root_option != ""
                else xpath_with_an_option_set
            )
            print(f"   └> Dynamic option to selection:\n      {full_selector_item}")
            BasePage.wait_for_element(By.XPATH, full_selector_item)
            BasePage.perform_click_action(
                By.XPATH, full_selector_item, timeout=15, is_visible=is_component_visible
            )

    @staticmethod
    def _combobox(option, by_type, element_location):
        if BasePage.is_not_empty_value(option):
            BasePage.wait_for_element(by_type, element_location, is_clickable=True)
            select = Select(BasePage.get_element_by(by_type, element_location))
            try:
                select.select_by_value(option)
            except:
                if String.is_not_blank_or_null(option):
                    select.select_by_visible_text(option)
            print(f"   └> Option chosen: {option}")

    @staticmethod
    def upload_with_drag_and_drop(path_to_upload, by_type, element_location_to_drop):
        """
        The upload is performed automatically if provided the correct root locator from element that receives the file dropped.

        Args:
            path_to_upload (str): This argument needs the absolute path of file such as: "path/of/file/my_file_name.png"
            by_type (By): Use By.XPATH, By.ID, By.CSS_SELECTOR or any other that defines the drop_locator
            element_location_to_drop (str): Single Xpath, CssSelector or ID from the element where file should be dropped.
        """
        if BasePage.is_not_empty_value(path_to_upload):
            try:
                abs_file_path = abspath(path_to_upload)
                element_to_drop = BasePage.get_element_by(by_type, element_location_to_drop)
                WebDriver.execute_javascript(
                    'arguments[0].style = ""; arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";',
                    element_to_drop,
                )
                element_to_drop.send_keys(abs_file_path)
            except Exception as ex:
                Rexc.raise_assertion_error(
                    f"It was not possible to perform uploading on {element_location_to_drop}! ", ex
                )

    @staticmethod
    def pick_a_calendar_date(custom_date="first", by=By.XPATH, root_locator=""):
        """
        This method is able to select only the Day of current month presented on the Date Picker Component. It is possible to leave the custom_date arg as None.
        With this, the date will be chosen automatically, according the element with day defined as 'aria-disabled="false"'.

        Args:
            custom_date (str): When this parameter is not passed or is "", the next available day will be selected automatically considering
            the 'first' available date in the calendar, otherwise you can pass to arg the string 'last' day. A custom date is supported at moment'.
        """
        BasePage.switch_to_default_content()
        BasePage.wait_for_element(by, root_locator)
        root_date_picker_element = BasePage.get_element_by(by, root_locator)
        is_not_empty_date = custom_date is not None or custom_date != ""
        does_not_have_bars_in_date = "/" not in custom_date
        try:
            BasePage.wait_for_element(by, location=root_locator, is_clickable=True)
            root_date_picker_element.click()
            BasePage.switch_to_default_content()
            if is_not_empty_date and does_not_have_bars_in_date:
                loc_day = (
                    By.CSS_SELECTOR,
                    "<IMPLEMENT_SLECTOR_FOR_ACTIVE_DAY>",
                )
                BasePage.wait_for_element(*loc_day, is_clickable=True)
                list_of_day_elements = BasePage.get_elements_by(*loc_day)
                BasePage._click_on_available_custom_day(list_of_day_elements, custom_date)
        except Exception as ex:
            Rexc.raise_assertion_error(f"It was not possible to select any date! ", ex)

    @staticmethod
    def _click_on_available_custom_day(list_of_day_elements, custom_date):
        for day in range(0, len(list_of_day_elements)):
            first = 0
            last = 1
            day_chosen = last if custom_date == "last" else first
            if day == len(list_of_day_elements) - int(day_chosen):
                list_of_day_elements[day].click()

    @staticmethod
    def pick_offset_slider_and_drag_it(
        position_value_expected, step, is_start, is_end, by_type, root_element_location
    ):
        """
        This method is responsible to drag a Start or End slider handle element by offset. The calculation consider firstly the extraction
        of element values such as 'width' from root element slider, as well the 'start_value' and 'end_value' values from the slider handles. The STEP
        is a customized number that indicates a pace in each interval, for example: if you have a slider with a range from 1 to 50, but you are able
        to choose only ten by ten in the intervals 0, 10, 20, 30, 40 and 50, then the STEP is 10.
            With this, it is possible to determine the how many INTERVALS does this range have by 'END - START / STEP'.
        In this case, the result is 5.
            The OFFSET VALUE PER INTERVAL is obtained through the 'ROOT ELEMENT WIDTH / INTERVALS'. (i.e.: 244px / 5 = 48.8)
            Finally, it is possible to calculate the position in pixels based in the VALUE EXPECTED to be selected.

            For the start_value handler, it is necessary to consider this:
                CALC_START = 'OFFSET VALUE PER INTERVAL * ((VALUE EXPECTED - START) / STEP)'
                e.g: 48.8 * ((20 - 0) / 10) = 97.6 px

            For the end_value handler is almost the same, the difference is that the result should be always negative:
                CALC_END = ' - OFFSET VALUE PER INTERVAL * ((VALUE EXPECTED - END) / STEP)'

        Args:
            position_value_expected ([int]): Value to be set for start_value or end_value handle in the desired position
            step (int): Number that indicates the difference between each discretised position interval inside the range
            is_start (bool): Boolean to define if the start slider handle should be actived to drag. Set 'True' to do this.
            is_end (bool): Boolean to define if the end slider handle should be actived to drag. Set 'True' to do this.
            by_type (By): It expects always for By.ID, By.CSS_SELECTOR, By.XPATH or any other element type structure for a root_element_located
            root_element_location (str): Root locator string from slider element (can be an XPATH, ID, CSS_SELECTOR, etc.)
        """
        if BasePage.is_not_empty_value(position_value_expected):
            element_to_be_moved = ""
            total_abs_x = 0
            loc_root_to_rc_slider = root_element_location + '/..//div[@class="slider"]'
            BasePage.wait_for_element(by=By.XPATH, location=loc_root_to_rc_slider)
            elem_root_slider_width = BasePage.get_element_by(by_type, loc_root_to_rc_slider).size[
                "width"
            ]
            loc_slider_handle_start = loc_root_to_rc_slider + '//div[@role="slider"][1]'
            loc_slider_handle_end = loc_root_to_rc_slider + '//div[@role="slider"][2]'
            start_value = int(
                BasePage.get_element_by(by_type, loc_slider_handle_start).get_attribute(
                    str("aria-valuemin")
                )
            )
            end_value = int(
                BasePage.get_element_by(by_type, loc_slider_handle_end).get_attribute(
                    str("aria-valuemax")
                )
            )
            total_interval = abs(float((end_value - start_value) / step))
            drag_offset_per_interval = abs(float(elem_root_slider_width / total_interval))
            if is_start and is_end is None or is_end is False:
                calc_position_chosen = round(
                    drag_offset_per_interval * ((int(position_value_expected) - start_value) / step)
                )
                total_abs_x = abs(calc_position_chosen)
                element_to_be_moved = loc_slider_handle_start
            if is_end and is_start is None or is_start is False:
                calc_position_chosen = round(
                    drag_offset_per_interval * ((int(position_value_expected) - end_value) / step)
                )
                total_abs_x = -abs(calc_position_chosen)
                element_to_be_moved = loc_slider_handle_end
            BasePage.wait_for_element(by=by_type, location=element_to_be_moved, is_visible=True)
            BasePage.perform_move_by_offset_action(by_type, element_to_be_moved, total_abs_x, 0)
