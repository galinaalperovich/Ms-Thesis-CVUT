from PIL import Image

from parser.javascript_functions import get_all_css_properties


class EventFeature:
    def __init__(self, micro_property, driver):
        self.url = micro_property.url
        self.micro_property = micro_property
        self.xpath = self.__get_xpath()
        self.driver = driver
        self.driver.get(self.micro_property.url.strip())
        self.webelement = self.__get_web_element()
        self.meta_name = micro_property.name

        self.num_childs = self.__get_num_childs()
        self.depth_after_me = self.__get_depth_after_me()
        self.num_siblings = self.__get_num_siblings()

        self.tag = self.__get_tag()

        self.text_property = self.__get_text_property(micro_property.value)
        self.text_webelement = self.webelement.text if self.webelement else None
        self.text_density = self.__get_text_density()

        self.xy_coords = self.__get_xy_coords()
        self.block_size = self.__get_block_size()

        self.classes = self.__get_css_classes()
        self.css_prop = self.__get_css_properties()

    def __get_num_childs(self):

        try:
            self.driver.execute_script(
                "return arguments[0].children.length;", self.webelement)
        except Exception as e:
            return None

    def __get_depth_after_me(self):
        return None

    def __get_tag(self):
        return self.webelement.tag_name if self.webelement else None

    def __get_text_density(self):
        return None

    def __get_xy_coords(self):
        return self.webelement.location if self.webelement else None

    def __get_block_size(self):
        return self.webelement.size if self.webelement else None

    def __get_css_classes(self):
        try:
            return self.driver.execute_script("return arguments[0].className.split(' ')", self.webelement)
        except Exception as e:
            return None

    def __get_css_properties(self):
        try:
            node = self.driver.find_element_by_xpath(self.xpath)
            return self.driver.execute_script(
                get_all_css_properties(), node)
        except Exception as e:
            return None

    def __get_xpath(self):
        return ".//*[@itemprop='{}']".format(self.micro_property.name)

    def __get_web_element(self):
        driver = self.driver

        my_scope = self.micro_property.scope
        xpath_scope = "//*[@itemscope][@itemtype='{}']".format(my_scope)
        scope_element = driver.find_elements_by_xpath(xpath_scope)

        if not scope_element:
            return None

        xpath = self.__get_xpath()
        values_elements = set(
            scope_element.pop().find_elements_by_xpath(xpath))

        scopes = driver.find_elements_by_xpath("//*[@itemscope]")
        excepted_elements = set()
        for scope in scopes:
            type = scope.get_attribute('itemtype')

            if type == my_scope:
                continue
            excepted_element = scope.find_elements_by_xpath(xpath)
            for el in excepted_element:
                excepted_elements.add(el)

        one_element = values_elements.difference(excepted_elements)

        if one_element:
            return one_element.pop()

        return None

    def __get_num_siblings(self):
        try:
            return self.driver.execute_script(
                "var temp = arguments[0].parentNode; child = temp.children; return child.length;", self.webelement)
        except Exception as e:
            return None

    def __save_screenshot(self):
        element = self.webelement
        if element is None:
            return None
        location = element.location

        size = element.size

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        if left == 0 and top == 0 and right == 0 and bottom == 0:
            return

        shot_name = '/Users/jetbrains/PycharmProjects/SocioPath/screenshots/{}_{}.png'.format(self.meta_name, self.url)
        self.driver.save_screenshot(shot_name)

        im = Image.open(shot_name)
        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save(shot_name)

    def __get_text_property(self, text):
        return text.replace('\t', ' ').replace('\n', ' ')
