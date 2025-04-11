"""This is a basic profile with two hosts connected by a router.
Instructions:
Wait for the profile instance to start, then log in to each node by clicking on it in the topology and choosing the `shell` menu item, or go to `list view` and choose the ssh command to use your own terminal. 
"""

## 2025 update: remove VNC and routable_control_ip to make this start more easily on cloudlab
## also: make hardware_type selectable as parameter

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

pc.defineParameter("hardware_type",
                   "Optional physical node type (d710, d430, xl170, sm110p, etc)",
                   portal.ParameterType.STRING, "")

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()

if params.hardware_type != "":
    node.hardware_type = params.hardware_type

# Node romeo
#node_romeo = request.XenVM('romeo')
node_romeo = request.RawPC("node")
if params.hardware_type != "": # if students chose a hardware type (like d710 ?)
    node_romeo.hardware_type = params.hardware_type
node_romeo.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_romeo.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ffund/tcp-ip-essentials/cloudlab/scripts/no-offload.sh | bash'))
iface0 = node_romeo.addInterface('interface-1', pg.IPv4Address('10.0.1.100','255.255.255.0'))
#node_romeo.exclusive = False
# no VNC, thus no routable IP required
#node_romeo.routable_control_ip = True # required for VNC
#node_romeo.startVNC()

# Node juliet
#node_juliet = request.XenVM('juliet')
node_juliet = request.RawPC("node")
if params.hardware_type != "": # if students chose a hardware type (like d710 ?)
    node_juliet.hardware_type = params.hardware_type
node_juliet.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_juliet.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ffund/tcp-ip-essentials/cloudlab/scripts/no-offload.sh | bash'))
iface1 = node_juliet.addInterface('interface-3', pg.IPv4Address('10.0.2.100','255.255.255.0'))
#node_juliet.exclusive = False
#node_juliet.routable_control_ip = True # required for VNC
#node_juliet.startVNC()

# Node router
#node_router = request.XenVM('router')
node_router = request.RawPC("node")
if params.hardware_type != "": # if students chose a hardware type (like d710 ?)
    node_router.hardware_type = params.hardware_type
node_router.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_router.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ffund/tcp-ip-essentials/cloudlab/scripts/no-offload.sh | bash'))
iface2 = node_router.addInterface('interface-0', pg.IPv4Address('10.0.1.10','255.255.255.0'))
iface3 = node_router.addInterface('interface-2', pg.IPv4Address('10.0.2.10','255.255.255.0'))
node_router.exclusive = False
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

