# Demoly handoff

Shared by `launch-video` and `product-demo-video`. Keep both copies identical.

## Create link

```text
https://demoly.ai/create?kind=<kind>&url=<encoded product URL>[&direction=<direction>]
```

- `kind`: `launch` for a launch video, `demo` for a product demo.
- `url`: the product URL, percent-encoded (`https://acme.io/pricing` becomes `https%3A%2F%2Facme.io%2Fpricing`).
- `direction`: demo only. One of `product_overview`, `feature_walkthrough`, `onboarding_flow`, `sales_demo`, `new_feature_launch`. Leave it out for a launch video.

These values only fill in the first step; the user can still change them. The brief cannot be passed in the link, so give it as a separate copyable block for the user to paste.

Example:

```text
https://demoly.ai/create?kind=demo&url=https%3A%2F%2Fapp.acme.io&direction=onboarding_flow
```

## Account and access

- Making a video needs a Demoly account. The user can sign up on the site with Google or email.
- There is a daily limit on new videos per account. If the site says the limit is reached, the user can try again the next day.
- Finished and in-progress videos are listed at https://demoly.ai/library.

## What not to promise

- Do not state prices, credits, free plans, or how long generation takes in minutes. Point the user to the site.
- Do not promise a specific length, aspect ratio, language, or resolution beyond what the Skill says.
- Do not say the video was created, or describe its contents, since you cannot see it.
- Do not ask for or handle Demoly passwords or the product's passwords. All sign-ins happen on the site.
- Do not submit forms on demoly.ai on the user's behalf through a browser tool unless the user explicitly asks; the handoff link is the default.

## Privacy

The product URL and the brief are sent to Demoly when the user submits them on the site. See https://demoly.ai/privacy and https://demoly.ai/terms.
