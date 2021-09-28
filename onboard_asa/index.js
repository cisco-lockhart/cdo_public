const {promisify} = require('util')
const request = require('request');
const requestAsync = promisify(request);
const forge = require('node-forge');
const _ = require('lodash');
const logger = require('log4js').getLogger('main');
require('dotenv').config();

const token = process.env.CDO_TOKEN;
const ignoreCertificate = process.env.IGNORE_CERT === 'true' || false;
const sdcName = process.env.SDC_NAME;

function encryptCredentials(publicKey, username, password, additionalCredentials, isApiToken = false) {
  const key = forge.util.decode64(publicKey.encodedKey);
  let credentials = {
    keyId: publicKey.keyId,
    username: isApiToken ? null : encryptCredentialInner(key, username || ''),
    password: encryptCredentialInner(key, password || '')
  };

  if (additionalCredentials) {
    Object.keys(additionalCredentials).forEach((property) => credentials[property] = encryptCredential(key, additionalCredentials[property] || ''));
  }
  return JSON.stringify(credentials);

  function encryptCredentialInner(publicKey, credential) {
    try {
      return encryptRSA(publicKey, credential);
    } catch (error) {
      logger.error(error);
      throw new Error('Failed to encrypt credentials.');
    }
  }
}

function encryptRSA(publicKeyPem, plaintext) {
  if(_.isString(publicKeyPem) && _.isString(plaintext)) {
    let buffer = forge.util.createBuffer(plaintext, 'utf8');
    let publicKey = forge.pki.publicKeyFromPem(publicKeyPem);
    let encryptedBytes = publicKey.encrypt(buffer.getBytes());
    return forge.util.encode64(encryptedBytes);
  } else {
    throw new Error('Input publicKeyPem and plaintext must be strings');
  }
}

function main() {
  logger.level = process.env.LOG_LEVEL;
  const device = {
    ipv4: process.env.ASA_HOST,
    port: process.env.ASA_PORT,
    model: false,
    name: process.env.ASA_NAME,
    deviceType: "ASA",
    ignoreCertificate
  };

  const username = process.env.ASA_USER;
  const password = process.env.ASA_PASSWORD
  return getProxy()
    .then(lar => {
      device['larUid'] = lar['uid']
      return device;
    })
    .then(updatedDevice => {
      return postDevice(updatedDevice);
    })
    .then(device => getDeviceConfigId(device))
    .then((config) => {
      logger.trace("Config", JSON.stringify(config));
      return getProxyPublicKey()
        .then((publicKey) => encryptCredentials(publicKey, username, password))
        .then(creds => {
          const payload = {
            "state": "CERT_VALIDATED",
            "credentials": creds
          }
          return putCredentials(config['uid'], payload)
        });
    })
    .catch(err => {
      logger.error("ERROR ", err);
    });
}

function filterByDefault(lar) {
  return lar.defaultLar;
}

function getProxy() {
  const index = 0;
  const url = getUrl("aegis/rest/v1/services/targets/proxies");
  return requestAsync({uri: url, headers: {'Authorization': `Bearer ${token}`}})
    .then((resp) => {
      const lars = JSON.parse(resp.body);
      return _.find(lars, filterByDefault);
    });
}

function getProxyPublicKey() {
  return getProxy()
    .then(lar => lar.larPublicKey);
}

function postDevice(devicePayload) {
  logger.trace("postDevice", devicePayload);
  const url = getUrl("aegis/rest/v1/services/targets/devices");
  return requestAsync({uri: url, method: 'POST', body: JSON.stringify(devicePayload), headers: {'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json'}})
    .then(resp => JSON.parse(resp.body));
}

function getDeviceConfigId(devicePayload) {
  logger.trace("getDeviceConfigId", JSON.stringify(devicePayload));
  const deviceUid = devicePayload['uid'];
  const specificDeviceUrl = getUrl(`aegis/rest/v1/device/${deviceUid}/specific-device`)
  return requestAsync({uri: specificDeviceUrl, method: 'GET', headers: {'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json'}})
    .then(specificDeviceResp => {
      const specificDevice = JSON.parse(specificDeviceResp.body);
      return specificDevice;
    })
    .then(specificDevice => {
      const sleepPromise = new Promise(resolve => setTimeout(resolve, 2000));
      logger.trace("getConfig", JSON.stringify(specificDevice));
      const configUrl = getUrl(`aegis/rest/v1/services/asa/configs/${specificDevice['uid']}`);
      return sleepPromise
        .then(() =>
      requestAsync({uri: configUrl, method: 'GET', headers: {'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json'}})
        .then(configResp => JSON.parse(configResp.body)));
    })
    .then(config => {
      logger.trace("Config", JSON.stringify(config));
      const currentState = config['state'];
      logger.debug("Current state: ", currentState);
      return config;
    });
}

function putCredentials(configUid, credentialsPayload) {
  logger.trace("putCredentials", configUid);
  const url = getUrl(`aegis/rest/v1/services/asa/configs/${configUid}`);
  return requestAsync({uri: url, method: 'PUT', body: JSON.stringify(credentialsPayload), headers: {'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json'}});
}

function getUrl(url) {
  const base_url = process.env.CDO_URL;
  if (!base_url.endsWith('/')) {
    throw Error("CDO_URL must end with '/'");
  }
  return base_url + url;
}

(async () => {
  await main();
  logger.info("Done");
})().catch(e => {
  // Deal with the fact the chain failed
  logger.error("Failed", e);
});
