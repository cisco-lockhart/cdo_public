from dataclasses import dataclass, asdict


@dataclass
class ASAIOSModel:
    """Data model for adding an ASA to CDO"""
    name: str
    deviceType: str
    host: str
    ipv4: str
    larType: str
    larUid: str
    model: bool
    ignore_cert: bool = None

    def asdict(self):
        return asdict(self)


@dataclass
class FTDMetaData:
    """Data model for representing options for onboarding an FTD to CDO/cdFMC"""
    accessPolicyName: str
    accessPolicyUuid: str
    license_caps: str
    performanceTier: str

    def asdict(self):
        return asdict(self)


@dataclass
class FTDModel:
    """Data model for adding an FTD to CDO/cdFMC"""
    name: str
    associatedDeviceUid: str
    metadata: FTDMetaData
    deviceType: str = "FTDC"
    model: bool = False
    state: str = 'NEW'
    type: str = 'devices'

    def asdict(self):
        return asdict(self)
