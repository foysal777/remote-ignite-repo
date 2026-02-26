from rest_framework.exceptions import PermissionDenied
from django.db import transaction

PLAN_LIMIT = {"freebie": 20, "premium": 50}


def check_prompt_limit(user):
    user.reset_prompt_count_if_needed()

    # Admin unlimited
    if getattr(user, "role", None) == "admin":
        return

    base_limit = PLAN_LIMIT.get(getattr(user, "plan_type", "freebie"), 20)
    carry = getattr(user, "carry_forward_prompts", 0) or 0
    topup = getattr(user, "extra_prompts", 0) or 0
    used = getattr(user, "monthly_prompt_count", 0) or 0

    total_limit = max(base_limit + carry + topup, 0)

    if used >= total_limit:
        raise PermissionDenied(
            f"You have reached your monthly limit of {total_limit} prompts. "
            f"You can buy a top-up."
        )

    #  race-condition safe increment
    with transaction.atomic():
        user.refresh_from_db(fields=["monthly_prompt_count"])
        if user.monthly_prompt_count >= total_limit:
            raise PermissionDenied(
                f"You have reached your monthly limit of {total_limit} prompts. "
                f"You can buy a top-up."
            )

        user.increment_prompt_count()