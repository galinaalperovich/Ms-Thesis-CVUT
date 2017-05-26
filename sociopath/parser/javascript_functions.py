"""
JavaScript functions for PhantomJS webdriver
Example of use:

driver = webdriver.PhantomJS()
driver.get("google.com")
 driver.execute_script(get_xpath_by_xy, 100, 100)
"""


def get_all_css_properties():
    return """
    var style = window.getComputedStyle(arguments[0]);
      var styleMap = {};
      for (var i = 0; i < style.length; i++) {
        var prop = style[i]; //the numbered props
        var value = style.getPropertyValue(prop); //access the value;
        styleMap[prop] = value;
      }
      return styleMap;
    """


def get_xpath_by_xy():
    return """
    function getPathTo(element) {
        if (element.id!=='')
            return 'id("'+element.id+'")';
        if (element===document.body)
            return element.tagName;

        var ix= 0;
        var siblings= element.parentNode.childNodes;
        for (var i= 0; i<siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling===element)
                return getPathTo(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
            if (sibling.nodeType===1 && sibling.tagName===element.tagName)
                ix++;
        }
    }

    var element = document.elementFromPoint(arguments[0], arguments[1]);
    return getPathTo(element);
    """


def get_text_elements_xpaths():
    return """
    var iterator = document.evaluate("//*[not(contains(@style,'display:none')) and normalize-space(text())]",
                                    document, null, XPathResult.UNORDERED_NODE_ITERATOR_TYPE, null);
    var thisNode = iterator.iterateNext();
    var nodes = [];
    while (thisNode) {
        // var xpath = getPathTo(thisNode);
        nodes.push(thisNode);
        thisNode = iterator.iterateNext();
    }
    return nodes;
    """


def get_xpath_by_element():
    return """

        function getPathTo(element) {
        if (element.id!=='')
            return 'id("'+element.id+'")';
        if (element===document.body)
            return element.tagName;

        var ix= 0;
        var siblings= element.parentNode.childNodes;
        for (var i= 0; i<siblings.length; i++) {
            var sibling= siblings[i];
            if (sibling===element)
                return getPathTo(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
            if (sibling.nodeType===1 && sibling.tagName===element.tagName)
                ix++;
            }
        }

        return getPathTo(arguments[0])

    """
