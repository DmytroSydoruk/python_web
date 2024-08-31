from src.common.templates import templates


class LandingService:
    def get_home_page(self, request):
        return templates.TemplateResponse(request=request, name="index.html")
