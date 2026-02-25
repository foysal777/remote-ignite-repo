
from rest_framework.exceptions import PermissionDenied

PLAN_LIMIT = {"freebie": 20, "premium": 50}

def check_prompt_limit(user):
    user.reset_prompt_count_if_needed()

    if user.role == "admin":
        return

    base_limit = PLAN_LIMIT.get(user.plan_type, 20)
    carry = getattr(user, "carry_forward_prompts", 0) or 0
    topup = getattr(user, "extra_prompts", 0) or 0

    total_limit = base_limit + carry + topup

    if user.monthly_prompt_count >= total_limit:
        raise PermissionDenied(
            f"You have reached your monthly limit of {total_limit} prompts. "
            f"You buy a top-up."
        )

    user.increment_prompt_count()





