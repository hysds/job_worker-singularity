### broker_url = "amqp://hysdsops:Y2FkNTllND@100.67.33.56:5672//"
broker_url = "amqp://hysdsops:Y2FkNTllND@tpfe2.nas.nasa.gov:5672//"
### result_backend = "redis://:NDIyZWFmNWQ2MjZjMTg1OGYzMjBkMjVh@100.67.33.56"
result_backend = "redis://:NDIyZWFmNWQ2MjZjMTg1OGYzMjBkMjVh@tpfe2.nas.nasa.gov:6379"

task_serializer = "msgpack"
result_serializer = "msgpack"
accept_content = ["msgpack"]

task_acks_late = True
result_expires = 86400
worker_prefetch_multiplier = 1

event_serializer = "msgpack"
worker_send_task_events = True
task_send_sent_event = True
task_track_started = True

task_queue_max_priority = 10

task_reject_on_worker_lost = True

broker_heartbeat = 120
broker_heartbeat_checkrate = 2

broker_pool_limit = None
broker_transport_options = { "confirm_publish": True }

imports = [
    "hysds.task_worker",
    "hysds.job_worker",
    "hysds.orchestrator",
]

CELERY_SEND_TASK_ERROR_EMAILS = False
ADMINS = (
    ('', ''),
)
### SERVER_EMAIL = '100.67.32.182'
SERVER_EMAIL = 'tpfe2.nas.nasa.gov:10025'

HYSDS_HANDLE_SIGNALS = False
HYSDS_JOB_STATUS_EXPIRES = 86400

BACKOFF_MAX_VALUE = 64
BACKOFF_MAX_TRIES = 10

HARD_TIME_LIMIT_GAP = 300

PYMONITOREDRUNNER_CFG = {
    "rabbitmq": {
        ### "hostname": "100.67.33.56",
        "hostname": "tpfe2.nas.nasa.gov",
        "port": 5672,
        "queue": "stdouterr"
    },

    "StreamObserverFileWriter": {
        "stdout_filepath": "_stdout.txt",
        "stderr_filepath": "_stderr.txt"
    },

    "StreamObserverMessenger": {
        "send_interval": 1
    }
}

### MOZART_URL = "https://100.67.33.56/mozart/"
MOZART_URL = "https://tpfe2.nas.nasa.gov:8443/mozart/"
### MOZART_REST_URL = "https://100.67.33.56/mozart/api/v0.1"
MOZART_REST_URL = "https://tpfe2.nas.nasa.gov:8443/mozart/api/v0.1"
### JOBS_ES_URL = "http://100.67.33.56:9200"
JOBS_ES_URL = "http://tpfe2.nas.nasa.gov:9200"
JOBS_PROCESSED_QUEUE = "jobs_processed"
USER_RULES_JOB_QUEUE = "user_rules_job"
ON_DEMAND_JOB_QUEUE = "on_demand_job"
USER_RULES_JOB_INDEX = "user_rules"
STATUS_ALIAS = "job_status"

### TOSCA_URL = "https://100.67.35.28/search/"
TOSCA_URL = "https://tpfe2.nas.nasa.gov:28443/search/"
### GRQ_URL = "http://100.67.35.28:8878"
GRQ_URL = "http://tpfe2.nas.nasa.gov:28878"
### GRQ_REST_URL = "http://100.67.35.28:8878/api/v0.1"
GRQ_REST_URL = "http://tpfe2.nas.nasa.gov:28878/api/v0.1"
### GRQ_UPDATE_URL = "http://100.67.35.28:8878/api/v0.1/grq/dataset/index"
GRQ_UPDATE_URL = "http://tpfe2.nas.nasa.gov:28878/api/v0.1/grq/dataset/index"
### GRQ_ES_URL = "http://100.67.35.28:9200"
GRQ_ES_URL = "http://tpfe2.nas.nasa.gov:29200"
DATASET_PROCESSED_QUEUE = "dataset_processed"
USER_RULES_DATASET_QUEUE = "user_rules_dataset"
ON_DEMAND_DATASET_QUEUE = "on_demand_dataset"
USER_RULES_DATASET_INDEX = "user_rules"
DATASET_ALIAS = "grq"

USER_RULES_TRIGGER_QUEUE = "user_rules_trigger"

PROCESS_EVENTS_TASKS_QUEUE = "process_events_tasks"

### REDIS_JOB_STATUS_URL = "redis://:NDIyZWFmNWQ2MjZjMTg1OGYzMjBkMjVh@100.67.33.56"
REDIS_JOB_STATUS_URL = "redis://:NDIyZWFmNWQ2MjZjMTg1OGYzMjBkMjVh@tpfe2.nas.nasa.gov:6379"
REDIS_JOB_STATUS_KEY = "logstash"
### REDIS_JOB_INFO_URL = "redis://:OWNhYTVkNWNkYWQ1NjJmZTMxYTFlNGE5@100.67.32.43"
REDIS_JOB_INFO_URL = "redis://:OWNhYTVkNWNkYWQ1NjJmZTMxYTFlNGE5@tpfe2.nas.nasa.gov:36379"
REDIS_JOB_INFO_KEY = "logstash"
### REDIS_INSTANCE_METRICS_URL = "redis://:OWNhYTVkNWNkYWQ1NjJmZTMxYTFlNGE5@100.67.32.43"
REDIS_INSTANCE_METRICS_URL = "redis://:OWNhYTVkNWNkYWQ1NjJmZTMxYTFlNGE5@tpfe2.nas.nasa.gov:36379"
REDIS_INSTANCE_METRICS_KEY = "logstash"
REDIS_UNIX_DOMAIN_SOCKET = "unix://:NDIyZWFmNWQ2MjZjMTg1OGYzMjBkMjVh@/tmp/redis.sock"

WORKER_CONTIGUOUS_FAILURE_THRESHOLD = 10
WORKER_CONTIGUOUS_FAILURE_TIME = 5.

### ROOT_WORK_DIR = "/data/work"
ROOT_WORK_DIR = "/nobackupp12/lpan/worker/"
WEBDAV_URL = None
WEBDAV_PORT = 8085

WORKER_MOUNT_BLACKLIST = [
    "/dev",
    "/etc",
    "/lib",
    "/proc",
    "/usr",
    "/var",
]

CONTAINER_REGISTRY = "localhost:5050"
