from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from users.models import Profile


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/pages/profile.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get("pk")
        lookup = Profile.objects.filter(pk=profile_id)
        lookup = lookup.select_related("author")
        profile = get_object_or_404(lookup, pk=profile_id)
        return self.render_to_response({**context, "profile": profile})
