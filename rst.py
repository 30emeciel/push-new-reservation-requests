from babel.dates import format_date
from jinja2 import Environment, select_autoescape
from jinja2 import FileSystemLoader

settings_overrides = {

}


SLACK_DATE_FORMAT = "date"


def slack_date_format(dt):
    return f"<!date^{int(dt.timestamp())}^{{{SLACK_DATE_FORMAT}}}|{date_format(dt)}>"


def date_format(d, fmt="medium"):
    return format_date(d, locale='fr', format=fmt)


env = Environment(
    loader=FileSystemLoader("res"),
    autoescape=select_autoescape(
        enabled_extensions=('html', 'htm', 'xml'),
        default_for_string=False,
        default=False,
    )
)
env.filters["dateformat"] = date_format
env.filters["slackdateformat"] = slack_date_format

