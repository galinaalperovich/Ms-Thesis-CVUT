# -*- coding: utf-8 -*-
import csv
import os
import time

from selenium import webdriver

# LOCAL IMPORTS
from parser.element_feature import ElementFeature
from parser.header import css_header
from parser.parser_utils import now

# METACENTRUM IMPORTS
# from parser_utils import now
# from element_feature import ElementFeature
# from header import css_header

GOOD_TAGS = ['span', 'time', 'div', 'p', 'h1', 'li', 'h3', 'td', 'h2', 'a',
             'strong', 'h5', 'item', 'dd', 'b', 'tr', 'h4', 'h5', 'dl', 'address',
             'pre', 'font', 'em', 'header', 'var', 'table', 'abbr']

CWD = os.getcwd()
PATH_PARSED_FILES = '/Users/jetbrains/Yandex.Disk.localized/Diploma/data_all_elements_parsed'  # LOCAL
# PATH_PARSED_FILES = CWD + '/data_all_elements_parsed'  # METACENTRUM

path_to_phantomjs = CWD + '/phantomjs'


def write_element_features(event_features, writer, output_file):
    print("{}   {}".format(now(), "Writing features"))
    for element_feature in event_features:
        row_1_part = [element_feature.url, 'not_event_element', element_feature.text_property,
                      element_feature.xy_coords['x'], element_feature.xy_coords['y'],
                      element_feature.block_size['height'], element_feature.block_size['width'],
                      element_feature.tag,
                      'NaN', element_feature.num_siblings
                      ]
        css_prop = element_feature.css_prop
        row_2_part = [css_prop.get(css_h, None) for css_h in css_header]
        row = row_1_part + row_2_part
        writer.writerow([str(s, "utf-8") for s in row])
        output_file.flush()


def get_element_features(url, driver):
    print('{}   Getting all element features for {}'.format(now(), url))
    driver.get(url)
    elements = driver.find_elements_by_xpath("//*[not(contains(@style,'display:none')) and normalize-space(text())]")
    element_features = []
    for element in elements:
        try:
            if element.tag_name in GOOD_TAGS and element.text != '':
                element_features.append(ElementFeature(element, url, driver))
        except Exception as e:
            print(e)

    return element_features


def process_url(driver, url, i):
    output_filename = "{}/{}_{}.csv".format(PATH_PARSED_FILES, 'all_elements', i)
    if os.path.exists(output_filename):
        print('{}   File already exists {}'.format(now(), output_filename))
        return

    try:
        driver.get(url)
    except:
        print('{}   The problem with url:   {}'.format(now(), url))
        return

    time.sleep(2)

    output_file = open(output_filename, 'a')
    writer = csv.writer(output_file, delimiter='\t')

    element_features = get_element_features(url, driver)
    write_element_features(element_features, writer, output_file)


def main():
    driver = webdriver.PhantomJS(executable_path=path_to_phantomjs)
    list_of_urls = open(CWD + '/event_urls.txt', 'r')
    for i, line in enumerate(list_of_urls):
        process_url(driver, line, i)


if __name__ == "__main__":
    main()
