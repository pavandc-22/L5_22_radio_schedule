"""Programme schedule for a radio station: book, list and remove show slots."""
import ast
import operator
import os
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE slots (id INTEGER PRIMARY KEY, show TEXT, host TEXT, start_hour INTEGER, minutes INTEGER)")
STUDIO_PASSWORD = os.environ.get("STUDIO_PASSWORD")

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


def add_slot(show, host, start_hour, minutes):
    """Book a new show slot in the schedule."""
    conn.execute("INSERT INTO slots (show, host, start_hour, minutes) VALUES (?, ?, ?, ?)", (show, host, start_hour, minutes))


def slot_label(show, host):
    """Return a printable label for a show and its host."""
    return f"{show} hosted by {host}"


def _safe_eval(node):
    """Evaluate a parsed arithmetic/comparison expression without eval()."""
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


def overlap_free(formula):
    """Return True if the timing formula (e.g. '7 + 1 <= 13') holds."""
    try:
        return _safe_eval(ast.parse(formula, mode="eval"))
    except (SyntaxError, ValueError, ZeroDivisionError):
        return False


def morning_shows():
    """Return the names of all shows starting before noon."""
    query = "SELECT show FROM slots WHERE start_hour < 12"
    return [r[0] for r in conn.execute(query)]


def remove_slot(slot_id):
    """Remove the slot with the given id."""
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    """Run a short demonstration of the schedule."""
    add_slot("Sunrise Beats", "Vik", 7, 60)
    add_slot("Midday Talk", "Anu", 13, 45)
    print(slot_label("Sunrise Beats", "Vik"))
    print(overlap_free("7 + 1 <= 13"), morning_shows())
    remove_slot(2)


if __name__ == "__main__":
    main()