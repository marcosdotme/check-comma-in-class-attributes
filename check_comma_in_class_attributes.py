from __future__ import annotations

import argparse
import ast
from pathlib import Path
from typing import Sequence


TAB_LENGTH = 4

ERROR_MESSAGE_TEMPLATE = """\
File "{file}", line {line_number} in <class {class_name}>
    {code}
{pointer_location}
SyntaxError: Found comma in class attribute"""


class AttributeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.class_infos = []
        self.has_comma_in_class_attributes = False

    def visit_ClassDef(self, node):
        self.class_name = node.name
        self.generic_visit(node)

    def visit_Assign(self, node):
        if self.class_name is not None and isinstance(node.targets[0], ast.Attribute):
            attribute_name = node.targets[0].attr
            line_number = node.lineno

            if isinstance(node.value, ast.Tuple) and len(node.value.elts) == 1:
                self.has_comma_in_class_attributes = True
                self.class_infos.append((self.class_name, attribute_name, line_number))

        self.generic_visit(node)


def has_comma_in_class_attributes(file: str) -> bool:
    with open(file, mode='r') as f:
        code = f.read()
        code_lines = code.split('\n')
        code_lines = list(map(str.strip, code_lines))

    parsed_code = ast.parse(code)
    visitor = AttributeVisitor()
    visitor.visit(parsed_code)

    if not visitor.has_comma_in_class_attributes:
        return False

    for class_name, attribute_name, line_number in visitor.class_infos:
        code = code_lines[line_number-1]

        comma_position = code.find(',') + TAB_LENGTH
        pointer_location = ' '*comma_position + '^'

        print(
            ERROR_MESSAGE_TEMPLATE.format(
                file=Path(file).resolve(),
                class_name=class_name,
                line_number=line_number,
                code=code,
                attribute_name=attribute_name,
                pointer_location=pointer_location
            )
        )

    return True


def run(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest='files',
        nargs='*',
        help='Python files to check'
    )
    args = parser.parse_args(argv)

    return_value = 0

    for file in args.files:
        return_value |= int(has_comma_in_class_attributes(file=file))
    
    return return_value


if __name__ == '__main__':
    raise SystemExit(run())
