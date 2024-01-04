import os
import traceback

def mailify(tag, subject, body):
    MAIL_SUBJECT = f'[{tag}] {subject}'
    MAIL_BODY = body.replace("\\", "\\\\").replace("\"", "\\\"")
    CMD = f'mailifier_notify -s "{MAIL_SUBJECT}" -b "{MAIL_BODY}" > /dev/null'
    os.system(CMD)

def mailify_exception(tag, subject):
    body = traceback.format_exc()
    mailify(tag, subject, body)
