# hcpaste
Give this STDIN and it will send it to someone on your HipChat

Setup
---

There are two environment variables that need to be set in order for this script to work:

```Python
hc_api_url = os.environ['HCP_HC_API_URL']
hc_api_headers = os.environ['HCP_HC_API_HEADERS']
```

Make sure you export both of these!

Other than that, you can pipe to this script, provide it arguments, or really just send it any STDIN and have it output to someone on HipChat.
