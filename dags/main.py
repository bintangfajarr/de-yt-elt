from airflow import DAG
import pendulum
from datetime import timedelta,datetime
from api.video_data import get_playlist_id, get_video_ids,  extract_video_data, save_to_json

local_tz = pendulum.timezone("Asia/Jakarta")

default_args = {
    'owner': 'airflow',
    
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'email': ['data@engineers.com'],
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
    'dagrun_timeout': timedelta(hours=1),
    'start_date': datetime(2025, 12, 12, tzinfo=local_tz),
    'end_date': None,
    }
with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='dag to produce json file with raw data',
    schedule='0 14 * * *',
    catchup=False,
) as dag:

    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extracted_data = extract_video_data(video_ids)
    save_to_json_task=save_to_json(extracted_data)
    playlist_id >> video_ids >> extracted_data >> save_to_json_task