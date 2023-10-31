import cloudinary
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail.message import EmailMessage
from selenium import webdriver

from app.api.gc_planify.models import GeneralContractor
from PIL import Image

logger = get_task_logger(__name__)


@shared_task(name="send_feedback_email_task")
def send_feedback_email_task(email, message):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
    # return send_feedback_email(email, message)


@shared_task(ignore_result=True)
def celery_send_email(user_name, last_name, contact_email, user_email, subject, body):
    email = EmailMessage(
        subject,
        body,
        from_email=f'{user_name} {last_name} <subs@intelconstruct.com>',
        to=[contact_email],
        reply_to=[user_email],
    )
    email.send()


@shared_task(ignore_result=True)
def celery_send_simple_email(from_email, send_to, reply_email, subject, body):
    email = EmailMessage(
        subject,
        body,
        from_email=from_email,
        to=[send_to],
        reply_to=[reply_email],
    )
    email.send()


# @shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries':3})
# def upload_to_cloudinary():
def get_screenshot(instance_id, urls):
    urls_with_value = {}
    for key, url in urls.items():
        print(f"key == {key} url = {url}")

        if url is None:
            # print(f"url.find('drive.google.com') == {url.find('drive.google.com')} url = {url}")

            continue

        try:
            options = webdriver.ChromeOptions()
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                         ' Chrome/60.0.3112.50 Safari/537.36'
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

            driver = webdriver.Chrome(options=options)
            driver.set_window_size(1280, 960)
            driver.get(url)

            height = driver.execute_script("return document.body.scrollHeight")
            driver.set_window_size(1280, height + 100)
            # sleep(10)
            driver.save_screenshot(f"screenshot.png")
            try:
                with open('screenshot.png', "rb") as imageFile:
                    img_src = imageFile.read()
                upload_data = cloudinary.uploader.upload(img_src)
                file_url = upload_data['secure_url']
                print(f"key {key} url{url} file_url {file_url}")
                logger.info(f"file_url {file_url}")
                urls_with_value[key] = file_url
                # logger.info(f"Uploaded url {urls}")
            except Exception as e:
                print(e)
                logger.error(e)


            # instance.file_url= file_url
            # instance.s
        except Exception as e:
            print(f"Exception {e}")
            logger.error("Sent feedback email")
    try:
        print(urls_with_value)
        gc = GeneralContractor.objects.filter(id=instance_id).update(**urls_with_value)
    except Exception as e:
        print(e)
        logger.error(f"Object {e}")

