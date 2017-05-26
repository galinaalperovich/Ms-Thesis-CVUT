class MicroProperty:
    def __init__(self, name, value, selector, url, scope):
        self.name = name
        self.value = value
        self.xpath = self.__get_xpath()
        self.scope = scope
        self.url = url
        self.selector = selector

    def __get_xpath(self):
        return """set:difference(.//*[@itemscope]//*[@itemprop="{0}"],
        .//*[@itemscope]//*[@itemscope]//*[@itemprop="{0}"])""".format(
            self.name)
