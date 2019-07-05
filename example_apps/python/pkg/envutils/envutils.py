
US_BASE_URL = "https://www.defenseorchestrator.com"
STAGING_BASE_URL = "https://staging.dev.lockhart.io"
EU_BASE_URL = "https://www.defenseorchestrator.eu"
LOCALHOST_BASE_URL = "http://localhost:9000"

PROXIES_URL="{0}/aegis/rest/v1/services/targets/proxies"
SPECIFIC_DEVICE_URL="{0}/aegis/rest/v1/device/{1}/specific-device"
ASAS_URL="{0}/aegis/rest/v1/services/asa/configs"
ASA_URL=ASAS_URL + '/{1}'
JOBS_URL="{0}/aegis/rest/v1/services/state-machines/jobs"
DEVICES_URL = "{0}/aegis/rest/v1/services/targets/devices"
OBJECT_CSV_URL = "{0}/aegis/rest/v1/services/targets/objectcsvs"
OBJECTS_URL = "{0}/aegis/rest/v1/services/targets/objects"
OBJECT_URL = "{0}/aegis/rest/v1/services/targets/objects/{1}"
ANALYSIS_RESULTS_URL = "{0}/aegis/rest/v1/services/analysis/results"
NOTES_URL = "{0}/aegis/rest/v1/services/common/notes"
ACCESS_GROUPS_URL="{0}/aegis/rest/v1/services/targets/accessgroups"

def get_base_url(env):
    if env == 'us':
        return US_BASE_URL
    elif env == 'staging':
        return STAGING_BASE_URL
    elif env == 'eu':
        return EU_BASE_URL
    else:
        return LOCALHOST_BASE_URL

def get_proxies_url(env):
    return PROXIES_URL.format(get_base_url(env))

def get_specific_device_url(env, uid):
    return SPECIFIC_DEVICE_URL.format(get_base_url(env), uid)

def get_asa_url(env, asa_uid):
    return ASA_URL.format(get_base_url(env), asa_uid)

def get_jobs_url(env):
    return JOBS_URL.format(get_base_url(env))

def get_devices_url(env):
    return DEVICES_URL.format(get_base_url(env))

def get_access_groups_url(env):
    return ACCESS_GROUPS_URL.format(get_base_url(env))

def get_analysis_results_url(env):
    return ANALYSIS_RESULTS_URL.format(get_base_url(env))

def get_notes_url(env):
    return NOTES_URL.format(get_base_url(env))


def get_object_csv_url(env):
    return OBJECT_CSV_URL.format(get_base_url(env))

def get_objects_url(env):
    return OBJECTS_URL.format(get_base_url(env))


def get_object_url(env, obj_uid):
    return OBJECT_URL.format(get_base_url(env), obj_uid)

def get_headers(api_token):
    return {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
    }

