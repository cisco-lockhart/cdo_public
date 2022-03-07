# Automated object (Network Group) update with IP addresses

## Allow access to Office 365
Fetch Office 365 IPs and update a Network Group with these IPs. 
To run the above script do:

1. Create a "network group" object called O365 and give it some default values.
2. Assign this object to at least 2 ASAs (so we create a shared object out of it)
3. Get a long-lived token for your tenant
4. On the command-line, run the following:
```
export OAUTH=<my_token_from_#3>
curl -s 'https://endpoints.office.com/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7' | jq -r ".[] | { ips: .ips[]? } | .[]" | grep -v : | sort -u > o365.ip
bash cdo.update.object O365 o365.ip [deploy]
```
Provide "deploy" as he thrid parameter there if you like the changed the script makes to be deployed to the device. If not provided, changes will be staged in CDO, to be reviewed and deployed by a user. 

## Integration with VMware NSX: automatic update of ASAs object with ever-changing list of VMs in NSX

Customer has an NSX env, servers are coming up and down all the time, need to udpate ASA policy to include/exclude these servers.
A deal was on the table, PAN can do it, CDO can't. 

So there's a loop running every second that:
1. Getting the current list of IPs from NSX
2. Getting the object from CDO
3. Figure the diff
4. PUT changes to object
5. Create a job to push to affected devices(!)

The flow we showed:
1.	You have 3 VMs running and happy, in cdo there’s a network object group called “application servers” with their 3 IP addresses, and it participates in the policy, giving and denying access to these VMs. This is a “shared object” in CDO, maintained across multiple firewalls. 
2.	You spin a new 4th VM in NSX.
3.	The IP of the 4th VM is automatically added to the “application servers” network object group, across all firewalls and the policy immediately deployed to all firewalls. 
4.	Victory. 

