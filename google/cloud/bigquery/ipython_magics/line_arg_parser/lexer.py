# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import namedtuple
from collections import OrderedDict
import itertools
import re

import enum


Token = namedtuple("Token", ("type_", "lexeme", "pos"))
StateTransition = namedtuple("StateTransition", ("new_state", "total_offset"))


# Token definition order is important, thus an OrderedDict is needed with tightly
# controlled member definitions (i.e. passed as a sequnce, and *not* via kwargs).
token_types = OrderedDict(
    [
        (
            "state_1",
            OrderedDict(
                [
                    (
                        "GOTO_STATE_2",
                        r"(?P<GOTO_STATE_2>(?=--))",  # double dash - starting the options list
                    ),
                    (
                        "DEST_VAR",
                        r"(?P<DEST_VAR>[^\d\W]\w*)",  # essentially a Python ID
                    ),
                ]
            ),
        ),
        (
            "state_2",
            OrderedDict(
                [
                    (
                        "GOTO_STATE_3",
                        r"(?P<GOTO_STATE_3>(?=--params(?:\s|=|$)))",  # the --params option
                    ),
                    ("OPTION_SPEC", r"(?P<OPTION_SPEC>--\w+)"),
                    ("OPTION_EQ", r"(?P<OPTION_EQ>=)"),
                    ("OPT_VAL", r"(?P<OPT_VAL>\S+?(?=\s|--|$))"),
                ]
            ),
        ),
        (
            "state_3",
            OrderedDict(
                [
                    (
                        "PY_STRING",
                        r"(?P<PY_STRING>(?:{})|(?:{}))".format(
                            r"'(?:[^'\\]|\.)*'",
                            r'"(?:[^"\\]|\.)*"',  # single and double quoted strings
                        ),
                    ),
                    ("PARAMS_OPT_SPEC", r"(?P<PARAMS_OPT_SPEC>--params)"),
                    ("PARAMS_OPT_EQ", r"(?P<PARAMS_OPT_EQ>=)"),
                    (
                        "GOTO_STATE_2",
                        r"(?P<GOTO_STATE_2>(?=--\w+))",  # found another option spec
                    ),
                    ("PY_BOOL", r"(?P<PY_BOOL>True|False)"),
                    ("DOLLAR_PY_ID", r"(?P<DOLLAR_PY_ID>\$[^\d\W]\w*)"),
                    (
                        "PY_NUMBER",
                        r"(?P<PY_NUMBER>-?[1-9]\d*(?:\.\d+)?(:?[e|E][+-]?\d+)?)",
                    ),
                    ("SQUOTE", r"(?P<SQUOTE>')"),
                    ("DQUOTE", r'(?P<DQUOTE>")'),
                    ("COLON", r"(?P<COLON>:)"),
                    ("COMMA", r"(?P<COMMA>,)"),
                    ("LCURL", r"(?P<LCURL>\{)"),
                    ("RCURL", r"(?P<RCURL>})"),
                    ("LSQUARE", r"(?P<LSQUARE>\[)"),
                    ("RSQUARE", r"(?P<RSQUARE>])"),
                    ("LPAREN", r"(?P<LPAREN>\()"),
                    ("RPAREN", r"(?P<RPAREN>\))"),
                ]
            ),
        ),
        (
            "common",
            OrderedDict(
                [
                    ("WS", r"(?P<WS>\s+)"),
                    ("EOL", r"(?P<EOL>$)"),
                    (
                        # anything not a whitespace or matched by something else
                        "UNKNOWN",
                        r"(?P<UNKNOWN>\S+)",
                    ),
                ]
            ),
        ),
    ]
)


# The _generate_next_value_() enum hook is only available in Python 3.6+, thus we
# need to do some acrobatics to implement an "auto str enum" base class. Implementation
# based on the recipe provided by the very author of the Enum library:
# https://stackoverflow.com/a/32313954/5040035
class StrEnumMeta(enum.EnumMeta):
    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        # Having deterministic enum members definition order is nice.
        return OrderedDict()

    def __new__(metacls, name, bases, oldclassdict):
        # Scan through the declared enum members and convert any value that is a plain
        # empty tuple into a `str` of the name instead.
        newclassdict = enum._EnumDict()
        for key, val in oldclassdict.items():
            if val == ():
                val = key
            newclassdict[key] = val
        return super(StrEnumMeta, metacls).__new__(metacls, name, bases, newclassdict)


# The @six.add_metaclass decorator does not work, Enum complains about _sunder_ names,
# and we cannot use class syntax directly, because the Python 3 version would cause
# a syntax error under Python 2.
AutoStrEnum = StrEnumMeta(
    "AutoStrEnum",
    (str, enum.Enum),
    {"__doc__": "Base enum class for for name=value str enums."},
)

TokenType = AutoStrEnum(
    "TokenType",
    [
        (name, name)
        for name in itertools.chain.from_iterable(token_types.values())
        if not name.startswith("GOTO_STATE")
    ],
)


class LexerState(AutoStrEnum):
    STATE_1 = ()  # parsing positional arguments
    STATE_2 = ()  # parsing options other than "--params"
    STATE_3 = ()  # parsing the "--params" option
    STATE_END = ()


class Lexer(object):
    """Lexical analyzer for tokenizing the cell magic input line."""

    _GRAND_PATTERNS = {
        LexerState.STATE_1: re.compile(
            "|".join(
                itertools.chain(
                    token_types["state_1"].values(), token_types["common"].values(),
                )
            )
        ),
        LexerState.STATE_2: re.compile(
            "|".join(
                itertools.chain(
                    token_types["state_2"].values(), token_types["common"].values(),
                )
            )
        ),
        LexerState.STATE_3: re.compile(
            "|".join(
                itertools.chain(
                    token_types["state_3"].values(), token_types["common"].values(),
                )
            )
        ),
    }

    def __init__(self, input_text):
        self._text = input_text

    def __iter__(self):
        # Since re.scanner does not seem to support manipulating inner scanner states,
        # we need to implement lexer state transitions manually using special
        # non-capturing lookahead token patterns to signal when a state transition
        # should be made.
        # Since we don't have "nested" states, we don't really need a stack and
        # this simple mechanism is sufficient.
        state = LexerState.STATE_1
        offset = 0  # the number of characters processed so far

        while state != LexerState.STATE_END:
            token_generator = self._get_state_token_generator(state, offset)

            for maybe_token in token_generator:  # pragma: NO COVER
                if isinstance(maybe_token, StateTransition):
                    state = maybe_token.new_state
                    offset = maybe_token.total_offset
                    break

                if maybe_token.type_ != TokenType.WS:
                    yield maybe_token

                if maybe_token.type_ == TokenType.EOL:
                    state = LexerState.STATE_END
                    break

    def _get_state_token_generator(self, state, current_offset):
        """Return token generator for the current state starting at ``current_offset``.

        Args:
            state (LexerState): The current lexer state.
            current_offset (int): The offset in the input text, i.e. the number
                of characters already scanned so far.

        Returns:
            A generator yielding ``Token`` and ``StateTransition`` instances.
        """
        pattern = self._GRAND_PATTERNS[state]
        scanner = pattern.scanner(self._text, current_offset)
        return self._scan_for_tokens(scanner)

    def _scan_for_tokens(self, scanner):
        """Yield tokens produced by the scanner or state transition objects.

        Args:
            scanner (SRE_Scanner): The text tokenizer.

        Yields:
            The next ``Token`` or ``StateTransition`` instance.
        """
        for match in iter(scanner.match, None):  # pragma: NO COVER
            token_type = match.lastgroup

            if token_type.startswith("GOTO_STATE"):
                yield StateTransition(
                    new_state=getattr(LexerState, token_type[5:]),  # w/o "GOTO_" prefix
                    total_offset=match.start(),
                )

            yield Token(token_type, match.group(), match.start())
