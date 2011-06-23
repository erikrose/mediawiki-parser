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
_quotePat = re.compile(u"""(''+)""", re.UNICODE)
def parseQuotes(text):
        arr = _quotePat.split(text)
        if len(arr) == 1:
            return text
        # First, do some preliminary work. This may shift some apostrophes from
        # being mark-up to being text. It also counts the number of occurrences
        # of bold and italics mark-ups.
        numBold = 0
        numItalics = 0
        for i,r in zip(range(len(arr)), arr):
            if i%2 == 1:
                l = len(r)
                if l == 4:
                    arr[i-1] += u"'"
                    arr[i] = u"'''"
                elif l > 5:
                    arr[i-1] += u"'" * (len(arr[i]) - 5)
                    arr[i] = u"'''''"
                if l == 2:
                    numItalics += 1
                elif l >= 5:
                    numItalics += 1
                    numBold += 1
                else:
                    numBold += 1

        # If there is an odd number of both bold and italics, it is likely
        # that one of the bold ones was meant to be an apostrophe followed
        # by italics. Which one we cannot know for certain, but it is more
        # likely to be one that has a single-letter word before it.
        if numBold%2 == 1 and numItalics%2 == 1:
            firstSingleLetterWord = -1
            firstMultiLetterWord = -1
            firstSpace = -1
            for i,r in zip(range(len(arr)), arr):
                if i%2 == 1 and len(r) == 3:
                    x1 = arr[i-1][-1:]
                    x2 = arr[i-1][-2:-1]
                    if x1 == u' ':
                        if firstSpace == -1:
                            firstSpace = i
                    elif x2 == u' ':
                        if firstSingleLetterWord == -1:
                            firstSingleLetterWord = i
                    else:
                        if firstMultiLetterWord == -1:
                            firstMultiLetterWord = i

            # If there is a single-letter word, use it!
            if firstSingleLetterWord > -1:
                arr[firstSingleLetterWord] = u"''"
                arr[firstSingleLetterWord-1] += u"'"
            # If not, but there's a multi-letter word, use that one.
            elif firstMultiLetterWord > -1:
                arr[firstMultiLetterWord] = u"''"
                arr[firstMultiLetterWord-1] += u"'"
            # ... otherwise use the first one that has neither.
            # (notice that it is possible for all three to be -1 if, for example,
            # there is only one pentuple-apostrophe in the line)
            elif firstSpace > -1:
                arr[firstSpace] = u"''"
                arr[firstSpace-1] += u"'"

        # Now let's actually convert our apostrophic mush to HTML!
        output = []
        buffer = None
        state = ''
        for i,r in zip(range(len(arr)), arr):
            if i%2 == 0:
                if state == 'both':
                    buffer.append(r)
                else:
                    output.append(r)
            else:
                if len(r) == 2:
                    if state == 'i':
                        output.append(u"</em>")
                        state = ''
                    elif state == 'bi':
                        output.append(u"</em>")
                        state = 'b'
                    elif state == 'ib':
                        output.append(u"</strong></em><strong>")
                        state = 'b'
                    elif state == 'both':
                        output.append(u"<strong><em>")
                        output.append(u''.join(buffer))
                        buffer = None
                        output.append(u"</em>")
                        state = 'b'
                    elif state == 'b':
                        output.append(u"<em>")
                        state = 'bi'
                    else: # ''
                        output.append(u"<em>")
                        state = 'i'
                elif len(r) == 3:
                    if state == 'b':
                        output.append(u"</strong>")
                        state = ''
                    elif state == 'bi':
                        output.append(u"</em></strong><em>")
                        state = 'i'
                    elif state == 'ib':
                        output.append(u"</strong>")
                        state = 'i'
                    elif state == 'both':
                        output.append(u"<em><strong>")
                        output.append(u''.join(buffer))
                        buffer = None
                        output.append(u"</strong>")
                        state = 'i'
                    elif state == 'i':
                        output.append(u"<strong>")
                        state = 'ib'
                    else: # ''
                        output.append(u"<strong>")
                        state = 'b'
                elif len(r) == 5:
                    if state == 'b':
                        output.append(u"</strong><em>")
                        state = 'i'
                    elif state == 'i':
                        output.append(u"</em><strong>")
                        state = 'b'
                    elif state == 'bi':
                        output.append(u"</em></strong>")
                        state = ''
                    elif state == 'ib':
                        output.append(u"</strong></em>")
                        state = ''
                    elif state == 'both':
                        output.append(u"<em><strong>")
                        output.append(u''.join(buffer))
                        buffer = None
                        output.append(u"</strong></em>")
                        state = ''
                    else: # ''
                        buffer = []
                        state = 'both'

        if state == 'both':
            output.append(u"<em><strong>")
            output.append(u''.join(buffer))
            buffer = None
            output.append(u"</strong></em>")
        elif state != '':
            if state == 'b' or state == 'ib':
                output.append(u"</strong>")
            if state == 'i' or state == 'bi' or state == 'ib':
                output.append(u"</em>")
            if state == 'bi':
                output.append(u"</strong>")
        return u''.join(output)

def parseAllQuotes(text):
    sb = []
    lines = text.split(u'\n')
    for line in lines:
        sb.append(parseQuotes(line) + u'\n')
    return u''.join(sb)
