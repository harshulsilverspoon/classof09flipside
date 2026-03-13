import re

timing_dict = {}
current_key = None


with open('scene_list.txt') as fp:
    for line in fp:
        if re.match('^s.*s$', line):
            current_key = line.replace('\n', '')
            timing_dict[current_key] = []
        else:
            timing_dict[current_key].append(line.replace('\n', ''))

current_replacement = None

new_file = ""

with open('script.rpy') as fp:
    for line in fp:
        match = re.match('^label scene_(.*):$', line)
        if match:
            current_replacement = 's%ss' % match.group(1)
        else:
            match = re.match(r'(.*)(undefined),(undefined)\)$', line)
            if match:
                try:
                    first_time = timing_dict[current_replacement].pop(0)
                    second_time = timing_dict[current_replacement][0]
                    line = "%s%s,%s)\n" % (match.group(1), first_time, second_time)  # noqa: E501
                except (KeyError, IndexError):
                    pass
        new_file += line

with open('output.rpy', 'w') as fp:
    fp.write(new_file)
