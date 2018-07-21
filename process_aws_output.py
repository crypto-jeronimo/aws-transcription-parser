import json

from collections import deque
from functools import partial
from operator import itemgetter


def load_json(fname):
    with open(fname, 'rt') as f:
        content = f.read()
        data = json.loads(content)
        content = None

    return data

def load_raw_transcription(fname):
    data = load_json(fname)
    status = data['status']

    if status != "COMPLETED":
        raise ValueError("AWS job [{}] status is {}".format(fname, status))

    return data['results'], data['jobName']

def get_end_times(speaker_label_items):
    items = sorted(speaker_label_items, key=lambda _: float(itemgetter('end_time')(_)))
    return deque([(i['end_time'], i['speaker_label']) for i in items])


def update_speaker(html, speaker_name, speaker_map=()):
    speaker = speaker_map[int(speaker_name[-1])]
    html = append(html, '<p><b>{}: </b></p><p>'.format(speaker))
    return html, speaker_name

def append_token(html, line, separator=' '):
    if len(line['alternatives']) == 1:
        token = line['alternatives'][0]['content']
    else:
        token = sorted(line['alternatives'],
                       key=lambda _: float(itemgetter('confidence')(_)),
                       reverse=True)[0]

    html = append(html, token, separator=separator)
    return html

def build_html(lines, end_times, job_name, speaker_map):
    _update_speaker = partial(update_speaker, speaker_map=speaker_map)
    html = '<html><head><title>{}</title></head><body>'.format(job_name)

    current_speaker = None
    speaker_changes = 0
    punctuation = ''
    i = -1
    num_lines = len(lines)

    while i < num_lines - 1:
        i += 1
        line = lines[i]

        if line['type'] == 'punctuation':
            try:
                punctuation = append(punctuation, line['alternatives'][0]['content'], separator='', postfix=' ')
            except (KeyError, IndexError):
                pass
            continue

        try:
            end_time, range_speaker = end_times[speaker_changes]
        except IndexError:
            break

        if punctuation:
            html = append(html, punctuation, separator='')
            punctuation = ''

            if float(line['end_time']) < float(end_time):
                if current_speaker is None:
                    html, current_speaker = _update_speaker(html, range_speaker)
            elif lines[i-1]['type'] == 'punctuation' and lines[i-1]['alternatives'][0]['content'] in '.!?':
                speaker_changes += 1
                html, current_speaker = _update_speaker(html, range_speaker)

        html = append_token(html, line)

    html = append(html, '</p></body></html>')
    return html

def write_to_file(html, fname):
    with open('{}.html'.format(fname), 'wt') as f:
        f.write(html)

def parse_raw_transcription(fname, speaker_names):
    data, job_name = load_raw_transcription(fname)
    end_times = get_end_times(data['speaker_labels']['segments'])
    lines = data['items']
    html = build_html(lines, end_times, job_name, speaker_names)
    write_to_file(html, job_name)

def append(html, text, separator='\n', postfix=''):
    return '{}{}{}{}'.format(html, separator, text, postfix)

def run(fname):
    with open(fname, 'rt') as f:
        for line in f:
            line = line.strip().split(';')

            fname = line.pop(0)
            speakers = line.pop().split(',')
            parse_raw_transcription(fname, speakers)

    print("SUCCESS!")

if __name__ == '__main__':
    run('input.txt')
