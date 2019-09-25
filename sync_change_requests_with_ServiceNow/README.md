# Integration with ServiceNow, bring tickets to CDO ChangeRequest collection

Customer has ServiceNow in the cloud, wants CDO to automatically populate Change Requests available to choose from from ServiceNow

Copied everything to the customer's SDC VM, made some changes in cdo.update.loop to not really loop but run once, and created the scheduling with cron:
 */1 * * * * /usr/home/cdo/cdo.update.loop 2>&1 >> /usr/home/cdo/cdo.update.loop.log



