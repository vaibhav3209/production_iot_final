# import sib_api_v3_sdk
# from django.conf import settings
#
# def send_email(
#     to_email: str,
#     subject: str,
#     html_content: str,
# ):
#     configuration = sib_api_v3_sdk.Configuration()
#     configuration.api_key["api-key"] = settings.BREVO_API_KEY
#
#     api_client = sib_api_v3_sdk.ApiClient(configuration)
#     api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)
#
#     email = sib_api_v3_sdk.SendSmtpEmail(
#         to=[{"email": to_email}],
#         subject=subject,
#         html_content=html_content,
#         sender={
#             "name": settings.EMAIL_SENDER_NAME,
#             "email": settings.DEFAULT_FROM_EMAIL,
#         },
#     )
#
#     api_instance.send_transac_email(email)
