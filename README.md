# luadns-ddnsupdater

I wanted a hands off(automated) way to update my luadns.com DNS records, but didn't want to install 3rd party libraries or use their git integration and they don't support updating via a specialy formatted URL like many DDNS providers (because they are not that type of provider). 

update the following values in the script to match your account, api_key, zone, hostname and trarget type. 

```
user_id = 'email@tld.com'
api_key = 'abc123xyz890'

target_zone_name = 'zone.tld'
target_record_name = 'hostname.zone.tld'
target_type = 'A'
```

Then run as cronjob or as needed to update the desired record. Should be fairly easy to extend functionality to do multiple records if needed/required. Would also need a little work to do MX records. 
