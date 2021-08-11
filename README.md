# NextDNS-rewrite-tool
A tool that automatically updates the DNS Rewrite settings for your NextDNS account.

<br />

## About
Originally created as a utility to be run as a scheduled task, this program was created out of my inability to configure a static local IP for my computer on my only viable network - an Android wifi hotspot. This tool solves my requirement of being able to reliably reach my pc from other devices on the network for things like Remote Desktop, Kodi and whatnot.

The solution is made feasible by the wonderful [NextDNS](https://nextdns.io/) service, and in particular their DNS Rewrite functionality that allows for setting up custom domain name resolutions that may point to a local IP.

<br />

## Usage
Before running, it is required to configure the program by modifying the sections marked as `'change_this'` in the code. Configurations include stuff like your NextDNS Endpoint ID, your NextDNS account credentials, and your DNS Rewrite preferences.

<figure>
<img src = '/images/example-NextDNS-ID.png' />
  <figcaption align='right'><i>Your NextDNS Endpoint ID</i></figcaption>
  
  <br />
</figure> 
<br />
 
Additionally, this code is with quirks that meet my personal requirements - things like a check to run only if I'm connected to my home network, and a routine that returns local IP. It is recommended that you go through the code and remove functions that you don't require.

<figure>
<img src = '/images/example-configOptions.png' />
  <figcaption align='right'><i>Some of the configurable options in script</i></figcaption>
  
  <br />
</figure> 
<br />

This program creates a `nextDns_rewriteID.txt` in the folder where it is executed, to track the DNS Rewrites it has created by their ID. Please do not modify or delete this file to ensure the program always runs successfully.

<br />

## Credits and acknowledgements
A big thanks to the developers at NextDNS for creating the friendly API used in this program, and all the people at Stackoverflow who provide insights vital to the solutions of some of my problems.
