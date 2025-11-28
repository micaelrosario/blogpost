from django import template
from django.utils import timezone
import re

register = template.Library()


@register.filter(is_safe=True)
def pretty_date(value):
    """Return a cleaned, human date string.

    - If value is a datetime, convert to localtime and format as "DD de Month YYYY".
    - If value is a string (some inputs may already be formatted), remove any
      stray "UTC" tokens and nearby digits like "16UTC" and strip quotes.
    """
    if not value:
        return ""

    # If it's a datetime-like object, format it cleanly
    try:
        # Use timezone.localtime when possible to avoid showing UTC markers
        if hasattr(value, 'tzinfo'):
            try:
                value = timezone.localtime(value)
            except Exception:
                pass
        return value.strftime("%d de %B %Y")
    except Exception:
        s = str(value)
        # Remove patterns like "16UTC" or "16UTC'" and plain "UTC"
        s = re.sub(r"\b\d{1,2}UTC\b", "", s)
        s = s.replace("UTC", "")
        # Remove stray single quotes
        s = s.replace("'", "")
        # Collapse duplicated leading day numbers: "16 16 November" -> "16 November"
        s = re.sub(r"^(\d{1,2})\s+\1\b", r"\1", s)
        return s.strip()
