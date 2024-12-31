"""Functionality for bridging definition gaps between dialects."""


def check_for_unique_violation(e: Exception) -> bool:
    """Check if the provided exception is a unique constraint violation
    database exception type; indicating that the overarching operation
    should be updated if it were an insert.
    """
    orig_arg_code = e.orig.args[0]
    if str(orig_arg_code).startswith("UNIQUE") or \
        orig_arg_code == 1062 or orig_arg_code == 2627:
        return True
    return False