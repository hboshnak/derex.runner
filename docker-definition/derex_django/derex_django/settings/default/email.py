EMAIL_HOST = "smtp"
EMAIL_PORT = "25"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

CONTACT_EMAIL = "contact@example.com"
BUGS_EMAIL = CONTACT_EMAIL
CONTACT_MAILING_ADDRESS = CONTACT_EMAIL
DEFAULT_FEEDBACK_EMAIL = CONTACT_EMAIL
FEEDBACK_SUBMISSION_EMAIL = CONTACT_EMAIL
PRESS_EMAIL = CONTACT_EMAIL
TECH_SUPPORT_EMAIL = CONTACT_EMAIL
UNIVERSITY_EMAIL = CONTACT_EMAIL

DEFAULT_FROM_EMAIL = "no-reply@example.com"
EDXAPP_BULK_EMAIL_DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
EDXAPP_DEFAULT_SERVER_EMAIL = DEFAULT_FROM_EMAIL