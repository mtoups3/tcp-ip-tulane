"""This is a basic profile with two hosts connected by a router.
Instructions:
Wait for the profile instance to start, then log in to each node by clicking on it in the topology and choosing the `shell` menu item, or go to `list view` and choose the ssh command to use your own terminal. 
"""

## 2025 update: remove VNC and routable_control_ip to make this start more easily on cloudlab
##        also: set 'Site 1' to try to get these all on one machine from our reservation
## (previously: make hardware_type selectable as parameter? nah)

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

## We don't definite parameters here after all --mt
#pc.defineParameter("hardware_type", "Optional physical node type (d710, d430, xl170, sm110p, etc)",
#                   portal.ParameterType.STRING, "")
# Retrieve the values the user specifies during instantiation.
#params = pc.bindParameters()

# Node romeo
node_romeo = request.XenVM('romeo')
node_romeo.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_romeo.Site('Site 1') # put this VM onto Site 1 (should help? --mt)
node_romeo.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ffund/tcp-ip-essentials/cloudlab/scripts/no-offload.sh | bash'))
iface0 = node_romeo.addInterface('interface-1', pg.IPv4Address('10.0.1.100','255.255.255.0'))
node_romeo.exclusive = True
# no VNC, thus no routable IP required
#node_romeo.routable_control_ip = True # required for VNC
#node_romeo.startVNC()

# Node juliet
node_juliet = request.XenVM('juliet')
node_juliet.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_juliet.Site('Site 1') # put this VM onto Site 1 (should help? --mt)
node_juliet.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ffund/tcp-ip-essentials/cloudlab/scripts/no-offload.sh | bash'))
iface1 = node_juliet.addInterface('interface-3', pg.IPv4Address('10.0.2.100','255.255.255.0'))
node_juliet.exclusive = True
#node_juliet.routable_control_ip = True # required for VNC
#node_juliet.startVNC()

# Node router
node_router = request.XenVM('router')
node_router.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_router.Site('Site 1') # put this VM onto Site 1 (should help? --mt)
node_router.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ffund/tcp-ip-essentials/cloudlab/scripts/no-offload.sh | bash'))
iface2 = node_router.addInterface('interface-0', pg.IPv4Address('10.0.1.10','255.255.255.0'))
iface3 = node_router.addInterface('interface-2', pg.IPv4Address('10.0.2.10','255.255.255.0'))
node_router.exclusive = True
#node_router.routable_control_ip = True # required for VNC
#node_router.startVNC()

# Link link-0
link_0 = request.Link('link-0')
link_0.addInterface(iface2)
link_0.addInterface(iface0)

# Link link-1
link_1 = request.Link('link-1')
link_1.addInterface(iface3)
link_1.addInterface(iface1)


# Print the generated rspec
pc.printRequestRSpec(request)

