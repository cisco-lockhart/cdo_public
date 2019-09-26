# Integration with VMware NSX: automatic update of ASAs object with ever-changing list of VMs in NSX

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

