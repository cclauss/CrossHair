import unittest
from typing import cast, Generic, Optional, List, TypeVar

from crosshair.condition_parser import *

class Foo:
    """A thingy.

    Examples::
        >>> 'blah'
        'blah'

    inv:: self.x >= 0

    inv:
        # a blank line with no indent is ok:

        self.y >= 0
    notasection:
        self.z >= 0
    """
    x: int
    def isready(self) -> bool:
        """
        Checks for readiness

        post[]::
            __return__ == (self.x == 0)
        """
        return self.x == 0

def single_line_condition(x: int) -> int:
    ''' post: return >= x '''
    return x

class ConditionParserTest(unittest.TestCase):

    def test_class_parse(self) -> None:
        class_conditions = get_class_conditions(Foo)
        self.assertEqual(set([c.expr_source for c in class_conditions.inv]),
                         set(['self.x >= 0', 'self.y >= 0']))
        self.assertEqual(set(class_conditions.methods.keys()), set(['isready']))
        method = class_conditions.methods['isready']
        self.assertEqual(set([c.expr_source for c in method.pre]),
                         set(['self.x >= 0', 'self.y >= 0']))
        self.assertEqual(set([c.expr_source for c in method.post]),
                         set(['__return__ == (self.x == 0)', 'self.x >= 0', 'self.y >= 0']))

    def test_single_line_condition(self) -> None:
        conditions = get_fn_conditions(single_line_condition)
        self.assertEqual(set([c.expr_source for c in conditions.post]),
                         set(['__return__ >= x']))
        
        
if __name__ == '__main__':
    unittest.main()

