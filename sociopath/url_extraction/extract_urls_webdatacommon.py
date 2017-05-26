import os

'''
This code process big 70 GB data with URL for Event microformat.
Output: file with URLs
'''

DATA = "/Users/jetbrains/Yandex.Disk.localized/Diploma/schema_Event"
urls_file = open('data_urls.txt', 'w')
errors = open('errors.txt', 'w')
fileSize = os.path.getsize(DATA)

progress = 0
all_urls = set()
i = 0
with open(DATA) as infile:
    prev_url = ''
    for line in infile:
        try:
            i += 1
            progress += len(line)
            progressPercent = (1.0 * progress) / fileSize
            if i % 50000 == 0:
                print(progressPercent)
            line_split = line.split(' ')
            schema = line_split[2]
            if 'schema' not in schema:
                continue
            schema_split = schema.split('/')
            if len(schema_split) < 3:
                continue
            prop_name = schema_split[3]
            if len(line_split) == 5 and 'Event' in prop_name:
                url = line_split[3]
                if prev_url is not url:
                    if url not in all_urls:
                        urls_file.write(prop_name[:-1] + '\t' + url[1:-1] + '\n')
                        prev_url = url
                        all_urls.add(url)
        except:
            errors.write(line)
