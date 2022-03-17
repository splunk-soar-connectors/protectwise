[comment]: # "Auto-generated SOAR connector documentation"
# ProtectWise

Publisher: Splunk  
Connector Version: 2\.0\.4  
Product Vendor: ProtectWise  
Product Name: ProtectWise  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app integrates with the ProtectWise cloud platform to implement ingestion and investigative actions

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2016-2022 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
The ProtectWise app enables the collection of events and the corresponding related observations into
containers and artifacts in Phantom.

The first thing to do is create the ProtectWise asset in Phantom.  
It's good practice to set the Label of the objects from this source to a **NEW ENTRY** called
**Event** .  
Once the asset is saved, run Test Connectivity and make sure it passes.  
The Test connection action is successful only when the session is created and the REST API call is
made successfully.  

## Containers created

The app will create a single container for each Event that it ingests from ProtectWise.  

## Event Artifact

Every Event in ProtectWise is made up of Observations. Each Observation is ingested and added as an
Artifact into the created Container. [![](img/artifact.png)](img/artifact.png)  
  
The fields that are present in the artifact greatly depend upon the type of Observation that was
ingested. Different Observations will have different types of values in the artifacts.  
The app supports two modes of ingestion, let's discuss the differences between them.

## POLL NOW

POLL NOW should be used to get a sense of the containers and artifacts that are created by the app.
The POLL NOW dialog allows the user to set the "Maximum containers" that should be ingested at this
instance. Since a single container is created for each event, this value equates to the maximum
events that are ingested by the app. The app will fetch the events in the order they were created in
ProtectWise. The time interval can be configured in hours using the **poll_hours** asset config,
E.g. to ingest events that have been generated in the last 2 hours, configure this value to be 2.
However, the query to ingest this data can be quite time-consuming.

## Scheduled Polling

This mode is used to schedule a polling action on the asset at regular intervals, which is
configured via the INGEST SETTINGS tab of the asset. It makes use of the following asset
configuration parameters (among others):

-   Maximum events to poll the first time

      
    The app detects the first time it is polling an asset and will ingest this number of events (at
    the most). It will also use the **poll_hours** value.

-   Maximum Containers for scheduled polling

      
    For all scheduled polls after the first, the app will ingest this number of events.

In case of Scheduled Polling, on every poll, the app remembers the time of the last event that it
has ingested and will pick up from the same time in the next polling cycle. For best results, keep
the poll interval and *Maximum Containers for scheduled polling* values close to the number of
events you would get within a time interval. This way, every poll will end up ingesting all the new
events.  
It is also very important that the *Maximum Container for scheduled polling* configured should be
greater than the maximum events that are generated **per second** . If the app detects it got the
maximum configured events and all occurred in the same second, it will start polling from the next
second in the next polling cycle.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a ProtectWise asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**auth\_token** |  required  | password | Authentication Token
**max\_containers** |  required  | numeric | Maximum events for scheduled polling
**first\_run\_max\_events** |  required  | numeric | Maximum events to poll the first time \(For scheduled polling\)
**poll\_hours** |  required  | numeric | Ingest events in last N hours \(Poll Now and First Run\)
**allow\_duplicate\_artifacts** |  optional  | boolean | Display duplicate artifacts from polling
**allow\_duplicate\_containers** |  optional  | boolean | Display duplicate containers from polling

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity  
[get pcap](#action-get-pcap) - Download pcap for an event or observation  
[hunt ip](#action-hunt-ip) - Hunt an IP in the network  
[hunt domain](#action-hunt-domain) - Hunt a domain in the network  
[hunt file](#action-hunt-file) - Hunt for a file in the network  
[on poll](#action-on-poll) - Query ProtectWise for Events and Observables and ingest into Phantom  

## action: 'test connectivity'
Validate the asset configuration for connectivity

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'get pcap'
Download pcap for an event or observation

Type: **investigate**  
Read only: **True**

A few things to note\:<ul><li>Valid values for the <b>type</b> parameter are\: <ul><li>Event</li><li>Observation</li></ul></li><li>The app adds the <i>Event ID</i> to every container as its <b>Source ID</b>\(source\_data\_identifier\)<a href="/app\_resource/protectwise\_e8f8d8dc\-916f\-4267\-be15\-e9b697dd58c5/img/sdi\.png"><img src="/app\_resource/protectwise\_e8f8d8dc\-916f\-4267\-be15\-e9b697dd58c5/img/sdi\.png"/></a><br>Unfortunately, this value can get clipped in the UI\. Instead, use the download button to download the container json and extract the source\_data\_identifier key value<a href="/app\_resource/protectwise\_e8f8d8dc\-916f\-4267\-be15\-e9b697dd58c5/img/sdi2\.png"><img src="/app\_resource/protectwise\_e8f8d8dc\-916f\-4267\-be15\-e9b697dd58c5/img/sdi2\.png"/></a><br></li><li>The app adds the <i>Observation ID</i> to every Artifact in a key named <b>observationId</b> of the cef dictionary<a href="/app\_resource/protectwise\_e8f8d8dc\-916f\-4267\-be15\-e9b697dd58c5/img/artifact\.png"><img src="/app\_resource/protectwise\_e8f8d8dc\-916f\-4267\-be15\-e9b697dd58c5/img/artifact\.png"/></a><br></li><li>The <b>sensorid</b> parameter is only required if the <b>type</b> is <b>Observation</b></li><li>The pcap file is added to the vault with a file name of &lt;<b>id</b>&gt;\.pcap</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**type** |  required  | The ID type | string | 
**id** |  required  | ID Value \(Event or Observation \) | string |  `protectwise event id`  `protectwise observation id` 
**sensorid** |  optional  | Sensor ID | string |  `protectwise sensor id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `protectwise event id`  `protectwise observation id` 
action\_result\.parameter\.sensorid | string |  `protectwise sensor id` 
action\_result\.parameter\.type | string | 
action\_result\.data\.\*\.estimatedSize | numeric | 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.netflows\.\*\.endTime | numeric | 
action\_result\.data\.\*\.netflows\.\*\.flowId | string | 
action\_result\.data\.\*\.netflows\.\*\.sensorId | numeric |  `protectwise sensor id` 
action\_result\.data\.\*\.netflows\.\*\.startTime | numeric | 
action\_result\.data\.\*\.vault\_info\.container | numeric | 
action\_result\.data\.\*\.vault\_info\.file\_name | string | 
action\_result\.data\.\*\.vault\_info\.hash | string | 
action\_result\.data\.\*\.vault\_info\.message | string | 
action\_result\.data\.\*\.vault\_info\.succeeded | boolean | 
action\_result\.data\.\*\.vault\_info\.vault\_id | string |  `vault id` 
action\_result\.summary\.vault\_id | string |  `vault id` 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'hunt ip'
Hunt an IP in the network

Type: **investigate**  
Read only: **True**

To get info within a time range specify the <b>start\_time</b> and <b>end\_time</b>\. These parameters take time in the Zulu format which can be expressed as %Y\-%m\-%dT%H\:%M\:%S\.%fZ e\.g\. 2016\-12\-30T13\:00\:00\.0000Z\.<br><ul><li>If <b>start\_time</b> and <b>end\_time</b> both are not specified, then the app defaults to last 5 days</li><li>If <b>start\_time</b> is specified and <b>end\_time</b> is not, then the app will default the <b>end\_time</b> to <i>current</i></li><li>If <b>start\_time</b> is not specified and <b>end\_time</b> is, the app will throw an error</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** |  required  | IP Address | string |  `ip`  `ipv6` 
**start\_time** |  optional  | Start time \(Zulu format\) | string | 
**end\_time** |  optional  | End time \(Zulu format\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.end\_time | string | 
action\_result\.parameter\.ip | string |  `ip`  `ipv6` 
action\_result\.parameter\.start\_time | string | 
action\_result\.data\.\*\.ip\.host | string | 
action\_result\.data\.\*\.ip\.organization | string | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.timeRange\.end | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.timeRange\.interval | string | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.timeRange\.intervalSize | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.timeRange\.start | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.values\.\*\.count | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.values\.\*\.timestamp | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.total | numeric | 
action\_result\.data\.\*\.threat\.events\.maxThreatLevel | string | 
action\_result\.data\.\*\.threat\.events\.maxThreatScore | numeric | 
action\_result\.data\.\*\.threat\.events\.threatCategory\.MaliciousHost | numeric | 
action\_result\.data\.\*\.threat\.events\.threatSubCategory\.MachineGeneratedDomain | numeric |  `domain` 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.agentId | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.category | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.cid | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.confidence | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.endedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.id | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.isUpdate | boolean | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.killChainStage | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.message | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.netflowCount | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.observationCount | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.observedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.observedStage | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.sensorIds | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.startedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.threatLevel | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.threatScore | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.threatSubCategory | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_original\.type | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.agentId | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.category | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.cid | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.confidence | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.endedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.id | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.isUpdate | boolean | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.killChainStage | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.message | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.netflowCount | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.observationCount | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.observedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.observedStage | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.sensorIds | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.startedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.threatLevel | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.threatScore | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.threatSubCategory | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.\_state\.type | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.agentId | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.category | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.cid | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.confidence | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.endedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.id | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.isUpdate | boolean | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.killChainStage | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.message | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.netflowCount | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.observationCount | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.observedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.observedStage | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.priority | boolean | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.sensorId | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.sensorIds | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.startedAt | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.threatLevel | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.threatScore | numeric | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.threatSubCategory | string | 
action\_result\.data\.\*\.threat\.events\.top\.\*\.type | string | 
action\_result\.data\.\*\.threat\.observations\.maxThreatLevel | string | 
action\_result\.data\.\*\.threat\.observations\.maxThreatScore | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.timeRange\.end | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.timeRange\.interval | string | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.timeRange\.intervalSize | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.timeRange\.start | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.values\.\*\.count | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.values\.\*\.timestamp | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.agentId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.direction | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.dstGeo\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.dstGeo\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.dstIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.dstMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.dstPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.layer3Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.layer4Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.srcIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.srcMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.ip\.srcPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.key | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.associatedId\.flowId\.startTime | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.category | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.cid | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.confidence | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.dstIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.dstMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.dstPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.layer3Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.layer4Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.srcIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.srcMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.connectionInfo\.srcPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.dnsReputation\.category | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.dnsReputation\.dns | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.dnsReputation\.partnerCategory | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.idsEvent\.classification | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.idsEvent\.description | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.idsEvent\.generatorId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.idsEvent\.priorityId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.idsEvent\.revision | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.idsEvent\.signatureId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.idsEvent\.timestampMicros | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.data\.idsEvent\.timestampSeconds | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.dstGeo\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.dstGeo\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.id | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.info\.coordinates\.\*\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.info\.coordinates\.\*\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.info\.ips | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.info\.ports | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.killChainStage | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.netflowId | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.observationDirection | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.observedAt | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.observedStage | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.occurredAt | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.severity | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.source | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.threatLevel | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.threatScore | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_original\.threatSubCategory | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.agentId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.direction | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.dstGeo\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.dstGeo\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.dstIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.dstMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.dstPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.layer3Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.layer4Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.srcIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.srcMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.ip\.srcPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.key | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.associatedId\.flowId\.startTime | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.category | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.cid | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.confidence | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.dstIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.dstMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.dstPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.layer3Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.layer4Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.srcIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.srcMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.connectionInfo\.srcPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.dnsReputation\.category | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.dnsReputation\.dns | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.dnsReputation\.partnerCategory | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.idsEvent\.classification | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.idsEvent\.description | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.idsEvent\.generatorId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.idsEvent\.priorityId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.idsEvent\.revision | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.idsEvent\.signatureId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.idsEvent\.timestampMicros | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.data\.idsEvent\.timestampSeconds | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.dstGeo\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.dstGeo\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.id | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.info\.coordinates\.\*\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.info\.coordinates\.\*\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.info\.ips | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.info\.ports | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.killChainStage | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.netflowId | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.observationDirection | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.observedAt | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.observedStage | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.occurredAt | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.severity | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.source | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.threatLevel | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.threatScore | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.\_state\.threatSubCategory | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.agentId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.direction | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.dstGeo\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.dstGeo\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.dstIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.dstMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.dstPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.layer3Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.layer4Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.srcIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.srcMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.ip\.srcPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.key | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.associatedId\.flowId\.startTime | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.category | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.cid | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.confidence | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.dstIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.dstMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.dstPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.layer3Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.layer4Proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.proto | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.srcIp | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.srcMac | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.connectionInfo\.srcPort | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.dnsReputation\.category | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.dnsReputation\.dns | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.dnsReputation\.partnerCategory | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.idsEvent\.classification | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.idsEvent\.description | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.idsEvent\.generatorId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.idsEvent\.priorityId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.idsEvent\.revision | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.idsEvent\.signatureId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.idsEvent\.timestampMicros | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.data\.idsEvent\.timestampSeconds | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.dstGeo\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.dstGeo\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.id | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.info\.coordinates\.\*\.lat | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.info\.coordinates\.\*\.lon | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.info\.ips | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.info\.ports | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.killChainStage | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.netflowId | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.observationDirection | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.observedAt | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.observedStage | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.occurredAt | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.sensorId | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.severity | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.source | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.threatLevel | string | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.threatScore | numeric | 
action\_result\.data\.\*\.threat\.observations\.top\.\*\.threatSubCategory | string | 
action\_result\.data\.\*\.threat\.observations\.types\.DnsReputation | numeric | 
action\_result\.data\.\*\.threat\.observations\.types\.Ids | numeric | 
action\_result\.summary\.event\_count | numeric | 
action\_result\.summary\.ip\_organization | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'hunt domain'
Hunt a domain in the network

Type: **investigate**  
Read only: **True**

To get info within a time range specify the <b>start\_time</b> and <b>end\_time</b>\. These parameters take time in the Zulu format which can be expressed as %Y\-%m\-%dT%H\:%M\:%S\.%fZ e\.g\. 2016\-12\-30T13\:00\:00\.0000Z\.<br><ul><li>If <b>start\_time</b> and <b>end\_time</b> both are not specified, then the app defaults to last 5 days</li><li>If <b>start\_time</b> is specified and <b>end\_time</b> is not, then the app will default the <b>end\_time</b> to <i>current</i></li><li>If <b>start\_time</b> is not specified and <b>end\_time</b> is, the app will throw an error</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain | string |  `domain` 
**start\_time** |  optional  | Start time \(Zulu format\) | string | 
**end\_time** |  optional  | End time \(Zulu format\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.domain | string |  `domain` 
action\_result\.parameter\.end\_time | string | 
action\_result\.parameter\.start\_time | string | 
action\_result\.data\.\*\.domain\.resolveData\.\*\.firstSeen | numeric | 
action\_result\.data\.\*\.domain\.resolveData\.\*\.lastSeen | numeric | 
action\_result\.data\.\*\.domain\.resolveData\.\*\.resolvesTo | string | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.timeRange\.end | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.timeRange\.interval | string | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.timeRange\.intervalSize | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.timeRange\.start | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.values\.\*\.count | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.timeSeries\.values\.\*\.timestamp | numeric | 
action\_result\.data\.\*\.threat\.events\.count\.total | numeric | 
action\_result\.data\.\*\.threat\.ipAddresses | string | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.timeRange\.end | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.timeRange\.interval | string | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.timeRange\.intervalSize | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.timeRange\.start | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.values\.\*\.count | numeric | 
action\_result\.data\.\*\.threat\.observations\.timeSeries\.values\.\*\.timestamp | numeric | 
action\_result\.summary\.domain\_organization | string | 
action\_result\.summary\.event\_count | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'hunt file'
Hunt for a file in the network

Type: **investigate**  
Read only: **True**

To get info within a time range specify the <b>start\_time</b> and <b>end\_time</b>\. These parameters take time in the Zulu format which can be expressed as %Y\-%m\-%dT%H\:%M\:%S\.%fZ e\.g\. 2016\-12\-30T13\:00\:00\.0000Z\.<br><ul><li>If <b>start\_time</b> and <b>end\_time</b> both are not specified, then the app defaults to last 5 days</li><li>If <b>start\_time</b> is specified and <b>end\_time</b> is not, then the app will default the <b>end\_time</b> to <i>current</i></li><li>If <b>start\_time</b> is not specified and <b>end\_time</b> is, the app will throw an error</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hash** |  required  | File Hash | string |  `sha256` 
**start\_time** |  optional  | Start time \(Zulu format\) | string | 
**end\_time** |  optional  | End time \(Zulu format\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.end\_time | string | 
action\_result\.parameter\.hash | string |  `sha256` 
action\_result\.parameter\.start\_time | string | 
action\_result\.data\.\*\.behavior\.network\.dns\.\*\.hostname | string |  `host name` 
action\_result\.data\.\*\.behavior\.network\.dns\.\*\.ip | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.behavior\.network\.hosts | string | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.body | string | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.data | string | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.host | string | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.method | string | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.path | string | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.port | numeric | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.uri | string | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.user\-agent | string | 
action\_result\.data\.\*\.behavior\.network\.http\.\*\.version | string | 
action\_result\.data\.\*\.behavior\.network\.tcp\.\*\.dport | numeric |  `port` 
action\_result\.data\.\*\.behavior\.network\.tcp\.\*\.dst | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.behavior\.network\.tcp\.\*\.sport | numeric |  `port` 
action\_result\.data\.\*\.behavior\.network\.tcp\.\*\.src | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.behavior\.network\.udp\.\*\.dport | numeric | 
action\_result\.data\.\*\.behavior\.network\.udp\.\*\.dst | string | 
action\_result\.data\.\*\.behavior\.network\.udp\.\*\.sport | numeric | 
action\_result\.data\.\*\.behavior\.network\.udp\.\*\.src | string | 
action\_result\.data\.\*\.info\.detectedFileSize | numeric | 
action\_result\.data\.\*\.info\.detectedType | string | 
action\_result\.data\.\*\.info\.hashes\.md5 | string |  `md5` 
action\_result\.data\.\*\.info\.hashes\.sha1 | string |  `sha1` 
action\_result\.data\.\*\.info\.hashes\.sha256 | string |  `sha256` 
action\_result\.data\.\*\.info\.hashes\.sha512 | string |  `sha512` 
action\_result\.data\.\*\.info\.id | string | 
action\_result\.data\.\*\.info\.isArchive | boolean | 
action\_result\.data\.\*\.info\.isEncrypted | boolean | 
action\_result\.data\.\*\.info\.type | string | 
action\_result\.data\.\*\.observations\.count | numeric | 
action\_result\.data\.\*\.observations\.facets\.fields\.fileExtractedName | string | 
action\_result\.data\.\*\.observations\.facets\.fields\.fileExtractedName\.23\.exe | numeric | 
action\_result\.data\.\*\.observations\.nextOffset | string | 
action\_result\.data\.\*\.observations\.results\.\*\.agentId | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.direction | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.dstGeo\.lat | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.dstGeo\.lon | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.dstIp | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.dstMac | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.dstPort | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.layer3Proto | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.layer4Proto | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.proto | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.srcIp | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.srcMac | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.ip\.srcPort | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.key | string | 
action\_result\.data\.\*\.observations\.results\.\*\.associatedId\.flowId\.startTime | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.category | string | 
action\_result\.data\.\*\.observations\.results\.\*\.cid | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.confidence | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.dstIp | string | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.dstMac | string | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.dstPort | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.layer3Proto | string | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.layer4Proto | string | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.proto | string | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.srcIp | string | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.srcMac | string | 
action\_result\.data\.\*\.observations\.results\.\*\.connectionInfo\.srcPort | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.advertisedType | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.category | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.detectedFileSize | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.detectedType | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.end | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.extractedName | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.extractedPath | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.finding\.score | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.hashes\.md5 | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.hashes\.sha1 | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.hashes\.sha256 | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.hashes\.sha512 | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.id | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.isArchive | boolean | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.isEncrypted | boolean | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.isTruncated | boolean | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.isTypeMismatched | boolean | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.serviceType | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.start | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.transportProtocol | string | 
action\_result\.data\.\*\.observations\.results\.\*\.data\.fileReputation\.type | string | 
action\_result\.data\.\*\.observations\.results\.\*\.dstGeo\.lat | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.dstGeo\.lon | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.id | string | 
action\_result\.data\.\*\.observations\.results\.\*\.info\.coordinates\.\*\.lat | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.info\.coordinates\.\*\.lon | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.info\.ips | string | 
action\_result\.data\.\*\.observations\.results\.\*\.info\.ports | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.killChainStage | string | 
action\_result\.data\.\*\.observations\.results\.\*\.netflowId | string | 
action\_result\.data\.\*\.observations\.results\.\*\.observationDirection | string | 
action\_result\.data\.\*\.observations\.results\.\*\.observedAt | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.observedStage | string | 
action\_result\.data\.\*\.observations\.results\.\*\.occurredAt | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.sensorId | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.severity | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.source | string | 
action\_result\.data\.\*\.observations\.results\.\*\.threatLevel | string | 
action\_result\.data\.\*\.observations\.results\.\*\.threatScore | numeric | 
action\_result\.data\.\*\.observations\.results\.\*\.threatSubCategory | string | 
action\_result\.summary\.detected\_type | string | 
action\_result\.summary\.file\_type | string | 
action\_result\.summary\.id | string | 
action\_result\.summary\.observation\_count | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'on poll'
Query ProtectWise for Events and Observables and ingest into Phantom

Type: **ingest**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container\_id** |  optional  | Container IDs to limit the ingestion to | string | 
**start\_time** |  optional  | Start of time range, in epoch time \(milliseconds\), if not specified, the default is past 10 days | numeric | 
**end\_time** |  optional  | End of time range, in epoch time \(milliseconds\), if not specified, the default is now | numeric | 
**container\_count** |  optional  | Maximum number of container records to query for | numeric | 
**artifact\_count** |  optional  | Maximum number of artifact records to query for | numeric | 

#### Action Output
No Output