# IP address table:
#            private            public
#  mozart: 172.31.50.21      34.231.84.218
#     grq: 172.31.60.171     34.238.202.245
# metrics: 172.31.49.100     34.239.68.19
#
### BROKER_URL = "amqp://guest:guest@172.31.50.21:5672//"
### CELERY_RESULT_BACKEND = "redis://:@172.31.50.21"
### BROKER_URL = "amqp://guest:guest@34.231.84.218:5672//"
BROKER_URL = "amqp://guest:guest@3.84.50.148:5672//"
### CELERY_RESULT_BACKEND = "redis://:@34.231.84.218"
CELERY_RESULT_BACKEND = "redis://:@3.84.50.148"

CELERY_TASK_SERIALIZER = "msgpack"
CELERY_RESULT_SERIALIZER = "msgpack"
CELERY_ACCEPT_CONTENT = ["msgpack"]
CELERY_TIMEZONE = "US/Pacific-New"
CELERY_ENABLE_UTC = True

CELERY_ACKS_LATE = True
CELERY_TASK_RESULT_EXPIRES = 86400
CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_EVENT_SERIALIZER = "msgpack"
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TRACK_STARTED = True

CELERY_QUEUE_MAX_PRIORITY = 10

BROKER_HEARTBEAT = 300
BROKER_HEARTBEAT_CHECKRATE = 5

CELERY_IMPORTS = [
    "hysds.task_worker",
    "hysds.job_worker",
    "hysds.orchestrator",
]

CELERY_SEND_TASK_ERROR_EMAILS = False
ADMINS = (
    ('', ''),
)
SERVER_EMAIL = '172.31.48.126'

HYSDS_HANDLE_SIGNALS = False
HYSDS_JOB_STATUS_EXPIRES = 86400

BACKOFF_MAX_VALUE = 64
BACKOFF_MAX_TRIES = 10

HARD_TIME_LIMIT_GAP = 300

PYMONITOREDRUNNER_CFG = {
    "rabbitmq": {
        ### "hostname": "172.31.50.21",
        ### "hostname": "34.231.84.218",
        "hostname": "3.84.50.148",
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

### MOZART_URL = "https://172.31.50.21/mozart/"
### MOZART_REST_URL = "https://172.31.50.21/mozart/api/v0.1"
### JOBS_ES_URL = "http://172.31.50.21:9200"
### MOZART_URL = "https://34.231.84.218/mozart/"
MOZART_URL = "https://3.84.50.148/mozart/"
### MOZART_REST_URL = "https://34.231.84.218/mozart/api/v0.1"
MOZART_REST_URL = "https://3.84.50.148/mozart/api/v0.1"
### JOBS_ES_URL = "http://34.231.84.218:9200"
JOBS_ES_URL = "http://3.84.50.148:9200"
JOBS_PROCESSED_QUEUE = "jobs_processed"
USER_RULES_JOB_QUEUE = "user_rules_job"
ON_DEMAND_JOB_QUEUE = "on_demand_job"
USER_RULES_JOB_INDEX = "user_rules"
STATUS_ALIAS = "job_status"

### TOSCA_URL = "https://172.31.60.171/search/"
### GRQ_URL = "http://172.31.60.171:8878"
### GRQ_REST_URL = "http://172.31.60.171:8878/api/v0.1"
### GRQ_UPDATE_URL = "http://172.31.60.171:8878/api/v0.1/grq/dataset/index"
### GRQ_ES_URL = "http://172.31.60.171:9200"
### TOSCA_URL = "https://34.238.202.245/search/"
TOSCA_URL = "https://52.91.25.28/search/"
### GRQ_URL = "http://34.238.202.245:8878"
GRQ_URL = "http://52.91.25.28:8878"
### GRQ_REST_URL = "http://34.238.202.245:8878/api/v0.1"
GRQ_REST_URL = "http://52.91.25.28:8878/api/v0.1"
### GRQ_UPDATE_URL = "http://34.238.202.245:8878/api/v0.1/grq/dataset/index"
GRQ_UPDATE_URL = "http://52.91.25.28:8878/api/v0.1/grq/dataset/index"
### GRQ_ES_URL = "http://34.238.202.245:9200"
GRQ_ES_URL = "http://52.91.25.28:9200"
DATASET_PROCESSED_QUEUE = "dataset_processed"
USER_RULES_DATASET_QUEUE = "user_rules_dataset"
ON_DEMAND_DATASET_QUEUE = "on_demand_dataset"
USER_RULES_DATASET_INDEX = "user_rules"
DATASET_ALIAS = "grq"

USER_RULES_TRIGGER_QUEUE = "user_rules_trigger"

### REDIS_JOB_STATUS_URL = "redis://:@172.31.50.21"
### REDIS_JOB_STATUS_URL = "redis://:@34.231.84.218"
REDIS_JOB_STATUS_URL = "redis://:@3.84.50.148"
REDIS_JOB_STATUS_KEY = "logstash"
### REDIS_JOB_INFO_URL = "redis://:@172.31.49.100"
REDIS_JOB_INFO_URL = "redis://:@34.201.249.63"
REDIS_JOB_INFO_KEY = "logstash"
### REDIS_INSTANCE_METRICS_URL = "redis://:@172.31.49.100"
REDIS_INSTANCE_METRICS_URL = "redis://:@34.201.249.63"
REDIS_INSTANCE_METRICS_KEY = "logstash"
REDIS_UNIX_DOMAIN_SOCKET = "unix://:@/tmp/redis.sock"

WORKER_CONTIGUOUS_FAILURE_THRESHOLD = 10
WORKER_CONTIGUOUS_FAILURE_TIME = 5.

ROOT_WORK_DIR = "/nobackupp12/lpan/work"
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
