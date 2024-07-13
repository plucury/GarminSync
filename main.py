import os
import zipfile
from copy import deepcopy
from io import BytesIO, FileIO
import click
import garth
from garth.exc import GarthHTTPError
from dotenv import load_dotenv

load_dotenv()

CN_DOMAIN = "garmin.cn"
GLOBAL_DOMAIN = "garmin.com"


def get_activities(client, start=0, limit=20):
    activities = client.request(
        "GET",
        "connectapi",
        f"activitylist-service/activities/search/activities?limit={limit}&start={start}",
        api=True,
    )
    return activities.json()


def get_activity(client, activity_id):
    activity = client.request(
        "GET", "connectapi", f"activity-service/activity/{activity_id}", api=True
    )
    return activity.json()


def download_activity(client, activity_id):
    return client.download(f"/download-service/files/activity/{activity_id}")


def upload_activity(client, fp: FileIO):
    try:
        client.upload(fp)
        print(f"Uploaded file: {fp.name}")
    except GarthHTTPError as e:
        if e.error.response.status_code == 409:
            print(f"File already exists: {fp.name}")

@click.command()
@click.option('--size', default=10, help='每次同步回溯的活动数量')
def main(size):
    cn_username = os.getenv("CN_USERNAME")
    cn_password = os.getenv("CN_PASSWORD")
    global_username = os.getenv("GLOBAL_USERNAME")
    global_password = os.getenv("GLOBAL_PASSWORD")
    assert cn_username, "CN_USERNAME is required"
    assert cn_password, "CN_PASSWORD is required"
    assert global_username, "GLOBAL_USERNAME is required"
    assert global_password, "GLOBAL_PASSWORD is required"

    garth.configure(domain=CN_DOMAIN)
    garth.login(cn_username, cn_password)
    cn_client = deepcopy(garth.client)

    garth.configure(domain=GLOBAL_DOMAIN)
    garth.login(global_username, global_password)
    g_client = deepcopy(garth.client)
    start = 0
    activities = []
    while size:
        limit = min(20, size)
        activities.extend(get_activities(cn_client, start=start, limit=limit))
        size = size - limit
        start = start + limit

    for activity in activities:
        activity_id = activity["activityId"]

        activity_bytes = download_activity(cn_client, activity_id)
        with zipfile.ZipFile(BytesIO(activity_bytes), mode="r") as zip_file:
            for file_name in zip_file.namelist():
                with zip_file.open(file_name) as file:
                    upload_activity(g_client, file)


if __name__ == '__main__':
    main()
