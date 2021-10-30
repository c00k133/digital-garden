#!/usr/bin/env python3

import os, sys, json, yaml, itertools
import markdown
from datetime import datetime

if len(sys.argv) != 3:
    print(f'USAGE: {sys.argv[0]} <path_to_neuron_notes> <path_to_hugo_content>')
    sys.exit(1)

_, neuron_path, hugo_content = sys.argv
neuron_metadata = json.load(sys.stdin)

def convert_neuron_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    hugo_compatible_date = datetime.strftime(date_obj, '%Y-%m-%dT%H:%M:%S-00')
    return hugo_compatible_date

def sanitize_tags(tags):
    return list(filter(lambda tag: tag != 'digital-garden', tags))

def remove_title(lines, title):
    iterator = itertools.dropwhile(lambda line: title not in line, lines)
    next(iterator)
    return list(iterator)

md = markdown.Markdown(extensions=['full_yaml_metadata'])
for neuron_object in neuron_metadata:
    note_file = os.path.join(neuron_path, neuron_object['Path'])
    with open(note_file) as fd:
        md.convert(fd.read())

    new_metadata = {
        'title': neuron_object['Title'],
        'date': convert_neuron_date(neuron_object['Meta']['date']),
        'tags': sanitize_tags(neuron_object['Meta']['tags']),
    }
    post_file = os.path.join(hugo_content, neuron_object['Path'])
    with open(post_file, 'w+') as fd:
        fd.write('---\n')
        fd.write(yaml.dump(new_metadata))
        fd.write('---\n')
        fd.write('\n'.join(remove_title(md.lines, neuron_object['Title'])))

    md.reset()
