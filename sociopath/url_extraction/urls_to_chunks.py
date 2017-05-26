input = open('/Users/jetbrains/PycharmProjects/SocioPath/data/all_urls.csv', 'r')

i = 0
id_file = 0
id_line = 0
for line in input:
    if i < 1114:
        i += 1
        continue
    output = open('/Users/jetbrains/PycharmProjects/SocioPath/data_output/data_output_{}.csv'.format(id_file), 'a')
    if id_line < 100:
        output.write(line)
        id_line += 1
    else:
        id_line = 0
        id_file += 1
