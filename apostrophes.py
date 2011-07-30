"""
MediaWiki-style markup; from py-wikimarkup

Copyright (C) 2008 David Cramer <dcramer@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
import re

_quotePat = re.compile(u"(''+)", re.UNICODE)

default_tags = {'bold': '<strong>',
                'bold_close': '</strong>',
                'italic': '<em>',
                'italic_close': '</em>'}


def _parseQuotes(text, tags=default_tags):
        arr = _quotePat.split(text)
        if len(arr) == 1:
            return text

        # First, do some preliminary work. This may shift some apostrophes from
        # being mark-up to being text. It also counts the number of occurrences
        # of bold and italics mark-ups.
        numBold = numItalics = 0
        for i, r in enumerate(arr):
            if i % 2:
                l = len(r)
                if l == 4:
                    arr[i-1] += u"'"
                    arr[i] = u"'''"
                elif l > 5:
                    arr[i-1] += u"'" * (len(arr[i]) - 5)
                    arr[i] = u"'''''"
                if l == 2:
                    numItalics += 1
                elif l == 3:
                    numBold += 1
                elif l == 5:
                    numItalics += 1
                    numBold += 1

        # If there is an odd number of both bold and italics, it is likely
        # that one of the bold ones was meant to be an apostrophe followed
        # by italics. Which one we cannot know for certain, but it is more
        # likely to be one that has a single-letter word before it.
        if numBold % 2 and numItalics % 2:
            firstSingleLetterWord = firstMultiLetterWord = firstSpace = -1
            for i, r in enumerate(arr):
                if i % 2 and len(r) == 3:
                    x1 = arr[i-1][-1:]
                    x2 = arr[i-1][-2:-1]
                    if x1 == u' ':
                        if firstSpace == -1:
                            firstSpace = i
                    elif x2 == u' ':
                        if firstSingleLetterWord == -1:
                            firstSingleLetterWord = i
                    elif firstMultiLetterWord == -1:
                        firstMultiLetterWord = i

            # If there is a single-letter word, use it!
            if firstSingleLetterWord > -1:
                arr[firstSingleLetterWord] = u"''"
                arr[firstSingleLetterWord - 1] += u"'"
            # If not, but there's a multi-letter word, use that one.
            elif firstMultiLetterWord > -1:
                arr[firstMultiLetterWord] = u"''"
                arr[firstMultiLetterWord - 1] += u"'"
            # ... otherwise use the first one that has neither.
            # (notice that it is possible for all three to be -1 if, for example,
            # there is only one pentuple-apostrophe in the line)
            elif firstSpace > -1:
                arr[firstSpace] = u"''"
                arr[firstSpace - 1] += u"'"

        # Now let's actually convert our apostrophic mush to HTML!
        output = []
        buffer = []
        state = ''
        for i, r in enumerate(arr):
            if not i % 2:
                if state == 'both':
                    buffer.append(r)
                else:
                    output.append(r)
            else:
                if len(r) == 2:
                    if state == 'i':
                        output.append(tags['italic_close'])
                        state = ''
                    elif state == 'bi':
                        output.append(tags['italic_close'])
                        state = 'b'
                    elif state == 'ib':
                        output.append(tags['bold_close']+tags['italic_close']+tags['bold'])
                        state = 'b'
                    elif state == 'both':
                        output.append(tags['bold']+tags['italic'])
                        output.append(u''.join(buffer))
                        output.append(tags['italic_close'])
                        state = 'b'
                    else: # ''
                        output.append(tags['italic'])
                        state += 'i'
                elif len(r) == 3:
                    if state == 'b':
                        output.append(tags['bold_close'])
                        state = ''
                    elif state == 'bi':
                        output.append(tags['italic_close']+tags['bold_close']+tags['italic'])
                        state = 'i'
                    elif state == 'ib':
                        output.append(tags['bold_close'])
                        state = 'i'
                    elif state == 'both':
                        output.append(tags['italic']+tags['bold'])
                        output.append(u''.join(buffer))
                        output.append(tags['bold_close'])
                        state = 'i'
                    else: # ''
                        output.append(tags['bold'])
                        state += 'b'
                elif len(r) == 5:
                    if state == 'b':
                        output.append(tags['bold_close']+tags['italic'])
                        state = 'i'
                    elif state == 'i':
                        output.append(tags['italic_close']+tags['bold'])
                        state = 'b'
                    elif state == 'bi':
                        output.append(tags['italic_close']+tags['bold_close'])
                        state = ''
                    elif state == 'ib':
                        output.append(tags['bold_close']+tags['italic_close'])
                        state = ''
                    elif state == 'both':
                        output.append(tags['italic']+tags['bold'])
                        output.append(u''.join(buffer))
                        output.append(tags['bold_close']+tags['italic_close'])
                        state = ''
                    else: # ''
                        buffer = []
                        state = 'both'

        if state == 'b' or state == 'ib':
            output.append(tags['bold_close'])
        if state == 'i' or state == 'bi' or state == 'ib':
            output.append(tags['italic_close'])
        if state == 'bi':
            output.append(tags['bold_close'])
        if state == 'both' and buffer is not []:
            output.append(tags['italic']+tags['bold'])
            output.append(u''.join(buffer))
            output.append(tags['bold_close']+tags['italic_close'])
        return u''.join(output)


def parseAllQuotes(text, tags=default_tags):
    sb = []
    lines = text.split(u'\n')
    first = True
    for line in lines:
        if not first:
            sb.append(u'\n')
        else:
            first = False
        sb.append(_parseQuotes(line, tags))
    return u''.join(sb)
