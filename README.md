# email_filter

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Overview

``` mermaid
graph TD


    Start[Fetch New Emails] --&gt; CheckAddress[Check Address]
    Start[Fetch New Emails] --&gt; Update[Update trusted list based on new sent]


    CheckAddress[Check Address] --&gt;|&quot;trusted\n(previous interaction)&quot;| Inbox[Inbox]
    CheckAddress[Check Address] --&gt;|not trusted| CheckDomain[Check Domain]

    
    %% Domain Checks
    CheckDomain --&gt;|&quot;trusted \n(previous interaction,\nknown university,\nor whitelist)&quot;| IsNewsletter1[Check if Newsletter]
    CheckDomain --&gt;|untrusted| Occasionally[Read Occasionally]
    
    
    %% Second Newsletter Checks
    IsNewsletter1 --&gt;|&quot;newsletter\n(unsubscribe in email text,\nblacklist)&quot;| Occasionally[Read Occasionally]
    IsNewsletter1 --&gt;|not Newsletter| Inbox[Inbox]
    
    %% Labels for Inbox Moves
    style Inbox fill:#9f9,stroke:#333,stroke-width:2px

    
    %% Labels for Folder Moves
    style Occasionally fill:#ff9,stroke:#333,stroke-width:2px

```

## Install

``` sh
pip install email_filter
```
