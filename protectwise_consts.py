# File: protectwise_consts.py
#
# Copyright (c) 2016-2022 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
PW_JSON_AUTH_TOKEN = "auth_token"
PW_JSON_LAST_DATE_TIME = "last_date_time"
PW_JSON_POLL_HOURS = "poll_hours"
PW_JSON_ALLOW_ARTIFACT_DUPLICATES = "allow_duplicate_artifacts"
PW_JSON_ALLOW_CONTAINER_DUPLICATES = "allow_duplicate_containers"
PW_JSON_TYPE = "type"
PW_JSON_ID = "id"
PW_JSON_SENSOR_ID = "sensorid"
PW_JSON_MAX_CONTAINERS = "max_containers"
PW_JSON_START_TIME = "start_time"
PW_JSON_END_TIME = "end_time"
PW_JSON_IP = "ip"
PW_JSON_DOMAIN = "domain"
PW_JSON_HASH = "hash"

PW_ERR_SERVER_CONNECTION = "Error connecting to server"
PW_ERR_JSON_PARSE = "Unable to parse JSON"
PW_ERR_FROM_SERVER = "API failed, Status code: {status}, Detail: {detail}"
PW_BASE_URL = "https://api.protectwise.com/api/v1"
PW_ERR_API_UNSUPPORTED_METHOD = "Unsupported requests method: '{method}' specified"
PW_PROG_FINISHED_DOWNLOADING_STATUS = "Finished downloading {0:.0%}"

PW_CEF_CONTAINS = {
    "observationId": ["protectwise observation id"],
    "sensorId": ["protectwise sensor id"]}
VALID_PW_TYPES = ["event", "observation"]
PW_N_DAYS_HOURS = (5 * 24)

# actions that this app supports
ACTION_ID_GET_PACKETS = 'get_packets'
ACTION_ID_HUNT_IP = 'hunt_ip'
ACTION_ID_HUNT_DOMAIN = 'hunt_domain'
ACTION_ID_HUNT_FILE = 'hunt_file'
ACTION_ID_TEST_ASSET_CONNECTIVITY = 'test_asset_connectivity'
PROTECTWISE_DEFAULT_TIMEOUT = 30
