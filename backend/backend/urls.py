"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from dotenv import load_dotenv
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

load_dotenv(settings.BASE_DIR / ".env")

admin.site.site_title = "PMP"
admin.site.index_title = "Admin Panel"
admin.site.site_header = "[ Project Management Portal ]"

urlpatterns = [
    path(
        f"{os.getenv('BASE_URL')}",
        include(
            [
                path("admin/", admin.site.urls),
                path(
                    "api/",
                    include(
                        [
                            path(
                                "user/",
                                include(
                                    ("authentication.api.urls", "user_management"),
                                    namespace="user-api",
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )
]
