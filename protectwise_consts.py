# --
# File: protectwise_consts.py
#
# Copyright (c) Phantom Cyber Corporation, 2016
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber Corporation.
#
# --

PW_JSON_AUTH_TOKEN = "auth_token"
PW_JSON_LAST_DATE_TIME = "last_date_time"
PW_JSON_POLL_HOURS = "poll_hours"
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
