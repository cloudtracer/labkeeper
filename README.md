LabKeeper.net
=============

Many networkers and other IT professionals build labs out of network equipment, servers, and other gear for the purposes of training and/or experimentation. These labs are often housed at a home or workplace and made accessible remotely. Unfortunately, scheduling lab access can be chaotic and authentication is generally done via static local means.

Inspired by the [PacketLife.net Community Lab](http://packetlife.net/lab/), LabKeeper.net provides a free scheduling and authentication service to enable lab owners to share their labs among friends, coworkers, or everyone in an organized and convenient manner. Lab members can reserve blocks of time on a lab using the site's scheduling interface. Upon login to a console server, the user is authenticated via RADIUS to the site's authentication backend, which validates their supplied credentials and reservation time.

## Lab Components

#### Lab

A lab is an autonomous collection of gear with a common owner or owners, typically all located in a single physical location. A lab can be publicly accessible or restricted to a set of approved members. A lab must have at least one owner and may have multiple administrators and/or members.

#### Console Server

A console server (also refered to as a _terminal server_) provides remote access to lab devices, typically via a physical console connection. A user connects to specific TCP port on the console server via Telnet or SSH, authenticates, and is patched into the associated device's console.

#### Pod

The devices within a lab can be grouped into logical pods. Devices in different pods belong to the same lab and can (but don't have to) share a common console server.

#### Device

A device is any piece of gear within a lab which a user is permitted to access. These can be routers, switches, firewalls, servers, access points -- anything with a CLI. Infrastrucutre gear that is not intended to be modified by end users are not considered lab devices.

## Scheduling

Labs may be scheduled in blocks of one-hour increments. The minimum and maximum duration of a reservation is configurable by the lab's owner(s), as are the maximum number of reservations per user, the time range during which the lab is available, and numerous other parameters.

## Lab Membership

Lab membership is divided into threee hierarchical tiers:

#### Owner

An owner has complete control over a lab. He or she can add, modify, and delete devices, console servers, and pods, as well as perform all administrative actions.

#### Administrator

An administrator cannot modify the lab or its components, but has full administrative control over reservations and the memberships of regular users.

#### Member

Lab membership is only significant when a lab is not public. Private labs are viewable publicly but can only reserved and accessed by designated members.

