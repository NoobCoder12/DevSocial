from .forms import PostForm


def post_form_processor(request):
    return {'post_form': PostForm()}
