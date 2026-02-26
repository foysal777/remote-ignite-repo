from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F

PLAN_LIMIT = {"freebie": 20, "premium": 50}


def check_prompt_limit(user):
    user.reset_prompt_count_if_needed()

    if getattr(user, "role", None) == "admin":
        return

    with transaction.atomic():
        # latest values lock-ish (row refreshed inside atomic)
        user.refresh_from_db(fields=[
            "plan_type",
            "carry_forward_prompts",
            "extra_prompts",
            "monthly_prompt_count",
        ])

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

        # DB-level safe increment
        UserModel = user.__class__
        UserModel.objects.filter(pk=user.pk).update(monthly_prompt_count=F("monthly_prompt_count") + 1)