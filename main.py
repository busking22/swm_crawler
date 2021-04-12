import sys
import crawl
import asyncio
from getpass import getpass


async def get_infos():
    login_email = input("Type your SWM login E-mail : ")
    login_pw = getpass("Type your SWM login password : ")
    start_label = int(input("Type number to start crawling the label of first person (1~180) : "))
    end_label = int(input("Type number the label of last person (1~180) : "))
    return login_email, login_pw, start_label, end_label


async def main():
    task_get_info = asyncio.create_task(get_infos())
    await task_get_info
    login_email, login_pw, start_label, end_label = task_get_info.result()

    print("Running...")
    crawl.main(login_email, login_pw, start_label, end_label)


asyncio.run(main())