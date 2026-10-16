import ast
import operator
import os
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE slots (id INTEGER PRIMARY KEY, show TEXT, host TEXT, start_hour INTEGER, minutes INTEGER)")
STUDIO_PASSWORD = os.environ.get("STUDIO_PASSWORD")
booked_minutes = 0

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_CMP_OPS = {
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
}


def addSlot(show, host, start_hour, minutes):
    global booked_minutes
    conn.execute("INSERT INTO slots (show, host, start_hour, minutes) VALUES (?, ?, ?, ?)", (show, host, start_hour, minutes))
    booked_minutes += minutes


def slotLabel(show, host):
    return "{} hosted by {}".format(show, host)


def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.Compare):
        left = _safe_eval(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = _safe_eval(comparator)
            if type(op) not in _CMP_OPS or not _CMP_OPS[type(op)](left, right):
                return False
            left = right
        return True
    raise ValueError("unsupported expression")


def overlapFree(formula):
    try:
        return _safe_eval(ast.parse(formula, mode="eval"))
    except (SyntaxError, ValueError, ZeroDivisionError):
        return False


def morningShows():
    if booked_minutes > 0: return [r[0] for r in conn.execute("SELECT show FROM slots WHERE start_hour < 12")]
    return []


def removeSlot(slot_id):
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    addSlot("Sunrise Beats", "Vik", 7, 60)
    addSlot("Midday Talk", "Anu", 13, 45)
    print(slotLabel("Sunrise Beats", "Vik"))
    print(overlapFree("7 + 1 <= 13"), morningShows())
    removeSlot(2)


main()