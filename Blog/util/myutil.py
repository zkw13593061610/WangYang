from django.shortcuts import redirect, render, reverse


def authuser(fn):
    def newfn(request):
        email = request.session.get('email', None)
        if email:
            res = fn(request)
            print(res)
            return res
        else:
            return redirect(reverse("blogs:index"))
    return newfn
