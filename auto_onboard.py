import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linkedin.django_settings")
django.setup()

from linkedin.onboarding import OnboardConfig, apply, missing_keys

# If AUTO_ONBOARD is true, seed the database from Railway variables
if os.environ.get("AUTO_ONBOARD") == "true":
    # Check if onboarding is already complete
    if missing_keys():
        print("Auto-onboarding using environment variables...")
        config = OnboardConfig(
            linkedin_email=os.environ.get("LINKEDIN_EMAIL", ""),
            linkedin_password=os.environ.get("LINKEDIN_PASSWORD", ""),
            campaign_name=os.environ.get("CAMPAIGN_NAME", "Default Campaign"),
            product_description=os.environ.get("PRODUCT_DESCRIPTION", "We provide amazing B2B services."),
            campaign_objective=os.environ.get("CAMPAIGN_OBJECTIVE", "Book a meeting"),
            booking_link=os.environ.get("BOOKING_LINK", ""),
            seed_urls=os.environ.get("SEED_URLS", ""),
            llm_api_key=os.environ.get("LLM_API_KEY", ""),
            ai_model=os.environ.get("AI_MODEL", "gpt-4o"),
            llm_api_base=os.environ.get("LLM_API_BASE", ""),
            connect_daily_limit=int(os.environ.get("CONNECT_DAILY_LIMIT", 20)),
            connect_weekly_limit=int(os.environ.get("CONNECT_WEEKLY_LIMIT", 100)),
            follow_up_daily_limit=int(os.environ.get("FOLLOW_UP_DAILY_LIMIT", 40)),
            newsletter=(os.environ.get("NEWSLETTER", "true").lower() == "true"),
            legal_acceptance=True
        )
        if config.linkedin_email and config.linkedin_password and config.llm_api_key:
            apply(config)
            print("Auto-onboarding successfully applied.")
            
            # Inject cookies if provided
            cookie_json = os.environ.get("LINKEDIN_COOKIES_JSON", "")
            if cookie_json:
                import json
                try:
                    from linkedin.models import LinkedInProfile
                    profile = LinkedInProfile.objects.get(linkedin_username=config.linkedin_email)
                    cookies = json.loads(cookie_json)
                    if isinstance(cookies, list):
                        cookies = {"cookies": cookies, "origins": []}
                    profile.cookie_data = cookies
                    profile.save(update_fields=["cookie_data"])
                    print("Cookies successfully injected from environment variables.")
                except Exception as e:
                    print(f"Error injecting cookies: {e}")
        else:
            print("WARNING: LINKEDIN_EMAIL, LINKEDIN_PASSWORD, or LLM_API_KEY missing from environment variables.")
    else:
        print("Onboarding already complete, skipping auto-onboard.")

