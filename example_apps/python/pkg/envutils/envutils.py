
US_BASE_URL = "https://www.defenseorchestrator.com"
STAGING_BASE_URL = "https://staging.dev.lockhart.io"
EU_BASE_URL = "https://www.defenseorchestrator.eu"
LOCALHOST_BASE_URL = "http://localhost:9000"

DEVICES_URL = "{0}/aegis/rest/v1/services/targets/devices"

ANALYSIS_RESULTS_URL = "{0}/aegis/rest/v1/services/analysis/results"
NOTES_URL = "{0}/aegis/rest/v1/services/common/notes"

def get_base_url(env):
    if env == 'us':
        return US_BASE_URL
    elif env == 'staging':
        return STAGING_BASE_URL
    elif env == 'eu':
        return EU_BASE_URL
    else:
        return LOCALHOST_BASE_URL


def get_devices_url(env):
    return DEVICES_URL.format(get_base_url(env))


def get_analysis_results_url(env):
    return ANALYSIS_RESULTS_URL.format(get_base_url(env))

def get_notes_url(env):
    return NOTES_URL.format(get_base_url(env))


def get_headers(api_token):
    return {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
    }

