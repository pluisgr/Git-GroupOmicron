# This is a script to create a network for it.
#
# You need to have Python 3 and the Requests module installed. You
#
# To run the script, enter:
#  python deployappliance.py -k <key> -o <org> -s <sn> -n <netw> -c <cfg_tmpl> [-t <tags>] [-a <addr>] [-m ignore_error]
#
# To make script chaining easier, all lines containing informational messages to the user
#  start with the character @

import sys, getopt, requests, json

def printusertext(p_message):
	#prints a line of text that is meant for the user to read
	#do not process these lines when chaining scripts
	print('@ %s' % p_message)

def printhelp():
	#prints help text

	printusertext('')
	printusertext('This is a script to claim a device into Dashboard, create a new network for it and bind')
	printusertext('the network to a pre-existing template.')
	printusertext('')
	printusertext('To run the script, enter:')
	printusertext('python deployappliance.py -k <key> -o <org> -s <sn> -n <netw> [-t <tags>] [-a <addr>] [-m ignore_error]')
	printusertext('')
	printusertext('<key>: Your Meraki Dashboard API key')
	printusertext('<org>: Name of the Meraki Dashboard Organization to modify')
	printusertext('<netw>: Name the new network will have')
	printusertext('<cfg_template>: Name of the config template the new network will bound to')
	printusertext('-t <tags>: Optional parameter. If defined, network will be tagged with the given tags')
	printusertext('-a <addr>: Optional parameter. If defined, device will be moved to given street address')
	printusertext('-m ignore_error: Optional parameter. If defined, the script will not stop if network exists')
	printusertext('')
	printusertext('Example:')
	printusertext('python a_dashboardMeraki.py -k 1234 -o MyCustomer -s XXXX-YYYY-ZZZZ -n NewBranch -c MyCfgTemplate')
	printusertext('')
	printusertext('Use double quotes ("") in Windows to pass arguments containing spaces. Names are case-sensitive.')
	
def getorgid(p_apikey, p_orgname):
	#looks up org id for a specific org name
	#on failure returns 'null'
	
	r = requests.get('https://dashboard.meraki.com/api/v0/organizations', headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
	
	if r.status_code != requests.codes.ok:
		return 'null'
	
	rjson = r.json()
	
	for record in rjson:
		if record['name'] == p_orgname:
			return record['id']
	return('null')
	
def getshardurl(p_apikey, p_orgid):
	#patch
	return("api.meraki.com")
	
def getnwid(p_apikey, p_shardurl, p_orgid, p_nwname):
	#looks up network id for a network name
	#on failure returns 'null'

	r = requests.get('https://%s/api/v0/organizations/%s/networks' % (p_shardurl, p_orgid), headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
	
	if r.status_code != requests.codes.ok:
		return 'null'
	
	rjson = r.json()
	
	for record in rjson:
		if record['name'] == p_nwname:
			return record['id']
	return('null') 
	
def createnw(p_apikey, p_shardurl, p_dstorg, p_nwdata):
	#creates network if one does not already exist with the same name
	
	#check if network exists
	getnwresult = getnwid(p_apikey, p_shardurl, p_dstorg, p_nwdata['name'])
	if getnwresult != 'null':
		printusertext('WARNING: Skipping network "%s" (Already exists)' % p_nwdata['name'])
		return('null')
	
	if p_nwdata['type'] == 'combined':
		#find actual device types
		nwtype = 'wireless switch appliance'
	else:
		nwtype = p_nwdata['type']
	if nwtype != 'systems manager':
		r = requests.post('https://%s/api/v0/organizations/%s/networks' % (p_shardurl, p_dstorg), data=json.dumps({'timeZone': p_nwdata['timeZone'], 'tags': p_nwdata['tags'], 'name': p_nwdata['name'], 'organizationId': p_dstorg, 'type': nwtype}), headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
	else:
		printusertext('WARNING: Skipping network "%s" (Cannot create SM networks)' % p_nwdata['name'])
		return('null')
		
	return('ok')

	
def bindnw(p_apikey, p_shardurl, p_nwid, p_templateid):
	#binds a network to a template
	
	r = requests.post('https://%s/api/v0/networks/%s/bind' % (p_shardurl, p_nwid), data=json.dumps({'configTemplateId': p_templateid}), headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
		
	if r.status_code != requests.codes.ok:
		return 'null'
		
	return('ok')
	
	
def main(argv):
	#set default values for command line arguments
	arg_apikey = 'null'
	arg_orgname = 'null'
	arg_nwname = 'null'
	arg_modexisting = 'null'
	arg_address = 'null'
	arg_nwtags = 'null'
		
	#get command line arguments
	#  python deployappliance.py -k <key> -o <org> -s <sn> -n <netw> -c <cfg_tmpl> [-t <tags>] [-a <addr>] [-m ignore_error]
	try:
		opts, args = getopt.getopt(argv, 'hk:o:s:n:c:m:a:t:')
	except getopt.GetoptError:
		printhelp()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			printhelp()
			sys.exit()
		elif opt == '-k':
			arg_apikey = arg
		elif opt == '-o':
			arg_orgname = arg
		elif opt == '-n':
			arg_nwname = arg
		elif opt == '-m':
			arg_modexisting = arg
		elif opt == '-a':
			arg_address = arg
		elif opt == '-t':
			arg_nwtags = arg
				
	#check if all parameters are required parameters have been given
	if arg_apikey == 'null' or arg_orgname == 'null' or	arg_nwname == 'null':
		printhelp()
		sys.exit(2)
	
	#set optional flag to ignore error if network already exists
	stoponerror = True
	if arg_modexisting == 'ignore_error':
		stoponerror = False
	
	#get organization id corresponding to org name provided by user
	orgid = getorgid(arg_apikey, arg_orgname)
	if orgid == 'null':
		printusertext('ERROR: Fetching organization failed')
		sys.exit(2)
	
	#get shard URL where Org is stored
	shardurl = getshardurl(arg_apikey, orgid)
	if shardurl == 'null':
		printusertext('ERROR: Fetching Meraki cloud shard URL failed')
		sys.exit(2)
		
	#make sure that a network does not already exist with the same name	
	nwid = getnwid(arg_apikey, shardurl, orgid, arg_nwname)
	if nwid != 'null' and stoponerror:
		printusertext('ERROR: Network with that name already exists')
		sys.exit(2)	
		
			
	#gather parameters to create network
	#valid values for parameter 'type': 'wireless', 'switch', 'appliance', 'combined', 'wireless switch', etc
	nwtags = ''
	if arg_nwtags != 'null':
		nwtags = arg_nwtags
	nwparams = {'name': arg_nwname, 'timeZone': 'Europe/Helsinki', 'tags': nwtags, 'organizationId': orgid, 'type': 'appliance'}
	
	#create network and get its ID
	if nwid == 'null':
		createstatus = createnw (arg_apikey, shardurl, orgid, nwparams)
		if createstatus == 'null':
			printusertext('ERROR: Unable to create network')
			sys.exit(2)
		nwid = getnwid(arg_apikey, shardurl, orgid, arg_nwname)
		if nwid == 'null':
			printusertext('ERROR: Unable to get ID for new network')
			sys.exit(2)	
		
	#bind network to template
	bindstatus = bindnw(arg_apikey, shardurl, nwid, templateid)
	if bindstatus == 'null' and stoponerror:
		printusertext('ERROR: Unable to bind network to template')
		sys.exit(2)

	printusertext('End of script.')
			
if __name__ == '__main__':
	main(sys.argv[1:])