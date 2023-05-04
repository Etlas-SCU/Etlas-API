from django.urls import path


from . import views

google = views.GoogleSocialAuthView.as_view({
    'post' : 'create',
})

facebook = views.FacebookSocialAuthView.as_view({
    'post' : 'create',
})

twitter = views.TwitterSocialAuthView.as_view({
    'post' : 'create',
})

urlpatterns = [
    path('google/', google, name="google"),
    path('facebook/', facebook, name="facebook"),
    path('twitter/', twitter, name="twitter"),
]
