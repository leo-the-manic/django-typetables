import re


def istypetable(cls):
    """Check if class ``cls`` looks like a type table.

    :return: bool -- ``True`` if a type table, ``False`` otherwise.

    This works by searching the docstring for ``"A type table."``
    """
    docstring = cls.__doc__
    return docstring and 'A type table.' in docstring


def extract_values_from_class(typetable_cls):
    docstring = typetable_cls.__doc__
    value_str = find_values_string(docstring)
    return extract_values_from_string(value_str)


def extract_values_from_string(docstring):
    """Get a list of values from the given docstring.

    :return: A list of string values.

    Assumes the source class is a typetable as per ``istypetable``.
    """

    values = []  # values detected will be stored in this list

    # find all words surrounded by single quotes
    for match in re.finditer(r"'(.*?)'", docstring):
        val = match.group(1)  # get the value, without single quotes

        # lists may be written like: 'foo,' 'bar,' 'baz.'
        val = val.rstrip(',.')  # remove trailing punctuation

        values.append(val)

    return values


def get_docstring_lines(docstring):
    """Return all docstring paragraphs as single lines.

    Leading and trailing whitespace is also removed.

    :param docstring: (str) a docstring

    :return: A list of strings, one string per docstring paragraph.
    """

    # split docstring into 'paragraphs' (chunks separated by a blank line)
    paragraphs = docstring.split('\n\n')

    # join paragraphs into whole lines
    lines = []
    for paragraph in paragraphs:
        inner_lines = [s.strip() for s in paragraph.splitlines()]
        inner_lines = [_f for _f in inner_lines if _f]  # remove blank entries
        whole_line = ' '.join(inner_lines)
        lines.append(whole_line)

    return lines


def find_values_string(docstring):
    """Get the string which contains values from the given class's docstring.

    :param typetable_cls: A type table class (makes ``istypetable`` return
                          ``True``)

    :return: The portion of the docstring which contains the typetable values.
    """

    # join docstring paragraphs into single lines so it's easy to work with
    docstring_lines = get_docstring_lines(docstring)

    # search for 'Example values are'
    for line in docstring_lines:
        if line.startswith('Example values are'):
            return line
