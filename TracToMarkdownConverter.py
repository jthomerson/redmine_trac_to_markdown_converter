import re

class TracToMarkdownConverter:

   def convert(self, text):
      if text is None or type(text) is not str:
         return text;

      def convertPreText(match):
         # add \r\n to ensure separation between pre body and text above it
         return '\r\n' + reduce(lambda x, y: x+'\t'+y+'\r\n', match.group(1).strip().splitlines(), '')

      def convertTable(match):
         lines = match.group(0).strip().split('\r\n')
         lines = [x for x in lines if x]
         for i, line in enumerate(lines):
            lines[i] = re.sub(r'\|\|', r'|', line.strip())
         if len(lines) > 1:
            lines.insert(1, '|---|---|---|')
         return '\r\n'.join(lines) + '\r\n\r\n'

      # Note: the order thsee are executed in matters!

      # {{{ }}}
      text = re.sub(r'\{\{\{([^\r\n]+?)\}\}\}', r'`\1`', text)
      # {{{ \r\n }}}
      text = re.sub(r'\{\{\{(.+?)\}\}\}', convertPreText, text, flags=re.S)
      # add space between text and list
      text = re.sub(r'([^\s]| )\r\n((\*|[0-9a-zA-Z]\.).*\r\n)+', r'\1\r\n\r\n\2', text, flags=re.S)
      # trac ignores \r\nline breaks
      text = re.sub(r'([a-zA-Z])[ ]?\r\n([a-zA-Z])', r'\1 \2', text)
      # [[Image(/path/to/image.png)]]
      text = re.sub(r'\[\[Image\((.+)\)\]\]', r'![](\1)', text)
      # [[br]]
      text = re.sub(r'\[\[[Bb][Rr]\]\]', '  \r\n', text)
      # table
      text = re.sub(r'(\|\|[^\r\n]*\|\|\s*)+', convertTable, text, flags=re.S)
      # ==== h4 ====
      text = re.sub(r'\=\=\=\=\s(.+?)\s\=\=\=\=', r'#### \1', text)
      # === h3 ====
      text = re.sub(r'\=\=\=\s(.+?)\s\=\=\=', r'### \1', text)
      # == h2 ==
      text = re.sub(r'\=\=\s(.+?)\s\=\=', r'## \1', text)
      # == h1 ==
      text = re.sub(r'\=\s(.+?)\s\=', r'# \1', text)
      #[wiki:docs Technical Documentation]
      text = re.sub(r'\[wiki:([^\s]+)[ ]*(.*)\]', r'[[\1|\2]]', text)
      #[docs Technical Documentation]
      text = re.sub(r'\[([a-zA-Z\_0-9]+) (.*)\]', r'[[\1|\2]]', text)
      # [http://www.example.org/en example.org description]
      text = re.sub(r'\[(http[^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](\1)', text)
      # [http://www.example.org/en]
      text = re.sub(r'\[(http[^\s\[\]]+)\]', r'[\1](\1)', text)
      # !escaped
      text = re.sub(r'\!(([A-Z][a-z0-9]+){2,})', r'\1', text)
      # '''bold'''
      text = re.sub(r"'''([^\']*)'''", r'**\1**', text)
      # ''italic''
      text = re.sub(r"''([^\']*)''", r'_\1_', text)
      # * list
      text = re.sub(r'^\s\*', '*', text)
      # 1. list
      text = re.sub(r'^\s\d\.', '1.', text)
      # line \\ breaks
      text = re.sub(r'\\\\\s', '  \r\n', text)

      return text

