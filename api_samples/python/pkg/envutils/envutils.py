
US_BASE_URL = "https://www.defenseorchestrator.com"
STAGING_BASE_URL = "https://staging.dev.lockhart.io"
EU_BASE_URL = "https://www.defenseorchestrator.eu"
LOCALHOST_BASE_URL = "http://localhost:9000"


def get_base_url(env):
    if env == 'us':
        return US_BASE_URL
    elif env == 'staging':
        return STAGING_BASE_URL
    elif env == 'eu':
        return EU_BASE_URL
    else:
        return LOCALHOST_BASE_URL