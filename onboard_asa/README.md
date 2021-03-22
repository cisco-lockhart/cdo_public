Script to automatically onboard an ASA device to CDO
===

Usage
---
You can provide the input parameters for this script via environmental variables or by editing the `.env` file.

To onboard an ASA device with this script, run the following command:
```shell
npm install
export CDO_TOKEN=<get the token from CDO dashboard>

ASA_HOST=192.168.0.1:443 node index.js
```
