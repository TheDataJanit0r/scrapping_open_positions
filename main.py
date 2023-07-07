import importlib.util
import os
from os import listdir
from datetime import datetime
import locale
from exchangelib import OAuth2LegacyCredentials, Configuration, Account, DELEGATE, Message, Mailbox, FileAttachment
from exchangelib.version import Version, EXCHANGE_O365
import sys
from dotenv import load_dotenv
import pandas as pd
import shutil
from crawlers import old_crawler
from logger import Logger

SCRIPT_PATH = os.path.dirname(__file__)

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
sys.path.append(os.path.join(SCRIPT_PATH, "./crawlers"))

crawlers = []

LOGGER = Logger(name="Main")


def load_crawlers():
    imported_crawlers = []
    crawler_modules_path = [file.split(".")[0] for file in listdir(os.path.join(SCRIPT_PATH, "./crawlers")) if file not in ["__init__.py", "__pycache__"]]

    for module_path in crawler_modules_path:
        module = importlib.import_module(module_path)

        if hasattr(module, 'fetch'):
            imported_crawlers.append(module)
            LOGGER.info("Successfully imported %s @ version %s" % (module.name, module.version))
        else:
            LOGGER.info("Module %s has no required fetch function!" % module_path)

    return imported_crawlers


def send_mail(output_file_path):
    # At this point all crawled data was merged and written to disk (to output_file), so it can be sent now
    credentials = OAuth2LegacyCredentials(
        client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'),
        tenant_id=os.getenv('TENANT_ID'), username="crawler@cintellic.com", password=os.getenv('USER_PWD')
    )
    config = Configuration(credentials=credentials, server="outlook.office365.com",
                           auth_type="OAuth 2.0",
                           version=Version(build=EXCHANGE_O365), )
    account = Account(primary_smtp_address="crawler@cintellic.com", autodiscover=False, config=config,
                      access_type=DELEGATE)

    # Create email attachment base on previously created output file (e.g. xlsx)
    with open(output_file_path, "rb") as attachment_file:
        attachment = FileAttachment(name=os.path.basename(output_file_path), content=attachment_file.read())

    m = Message(
        account=account,
        subject="Neue Stellen - %s" % (datetime.now().strftime("%d.%m.%Y")),
        body=old_crawler.fetch_text(SCRIPT_PATH),
        to_recipients=[Mailbox(email_address='dienstleister@cintellic.com')]
    )
    
    m.attach(attachment)

    m.send_and_save()


if __name__ == '__main__':
    load_dotenv(os.path.join(SCRIPT_PATH, '.env'))
    crawlers = load_crawlers()
    

    # Determine the path of the new output file (e.g. xlsx file)
    output_file = os.path.join(SCRIPT_PATH, "%s-Stellen.xlsx" % datetime.now().strftime("%Y%m%d"))

    final_frame = pd.DataFrame(columns=['Name','Standort','Link','Aufgaben','Anforderungen'])

    for crawler in crawlers:
        final_frame = final_frame.append(crawler.fetch())
    
    
    final_frame.to_excel(output_file, index=False)

    send_mail(output_file)

    shutil.move(output_file, "%s/%s" % (os.path.join(SCRIPT_PATH, "./Archiv"), os.path.basename(output_file)))

    os.remove(os.path.join(SCRIPT_PATH, "./Stellen.txt"))