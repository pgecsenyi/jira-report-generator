from domain.work_types import HELP, IMPLEMENTATION, OTHER, REVIEW


def categorize_work_log_item(work_log_item):
    help_tag = F'[{HELP}]'
    implementation_tag = F'[{IMPLEMENTATION}]'
    other_tag = F'[{OTHER}]'
    review_tag = F'[{REVIEW}]'

    if check_if_tag_matches(help_tag, work_log_item.comment):
        return HELP
    elif check_if_tag_matches(review_tag, work_log_item.comment):
        return REVIEW
    elif check_if_tag_matches(implementation_tag, work_log_item.comment):
        return IMPLEMENTATION

    return OTHER


def check_if_tag_matches(tag, content):
    length = len(tag)
    if (len(content) < length):
        return False

    contentStart = content[0:length]

    return contentStart.lower() == tag
