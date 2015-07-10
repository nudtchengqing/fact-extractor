import click
import re
import os
import json
import sys


def iter_split(iterator, split):
    acc = []
    for item in iterator:
        acc.append(item)
        if split(item):
            yield acc
            acc = []


def process_article(content, tokens, output_dir, max_words):
    attrs = dict(re.findall(r'([^\s=]+)="([^"]+)"', content))

    all_sentences = re.split(r'\.\s+', content)
    i = 0
    for sentence in all_sentences:
        sentence += '.'
        snt_tokens = sentence.split()
        if len(snt_tokens) < max_words and \
                any(token in snt_tokens for token in tokens):

            fout = os.path.join(output_dir, '%s.%d' % (attrs['id'], i))
            with open(fout, 'w') as f:
                f.write(sentence.encode('utf8'))
            i += 1

    print >> sys.stderr, "%10s %30s %5d sentences%s" % (
                         attrs['id'], attrs['title'], i,
                         ' (skipped)' if i == 0 else '')


@click.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('token_list', type=click.File('r'))
@click.argument('output_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--max-words', default=25)
def main(input_file, token_list, output_dir, max_words):
    tokens = {row.strip().decode('utf8') for row in token_list}

    mapping = {}
    for i, rows in enumerate(iter_split(input_file, lambda row: '</doc>' in row)):
        article = '\n'.join(rows).decode('utf8')
        process_article(article, tokens, output_dir, max_words)

    print >> sys.stderr, 'Processed %d articles' % i

if __name__ == '__main__':
    main()
